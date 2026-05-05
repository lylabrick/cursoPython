"""
Backup incremental automático → S3 / MinIO
==========================================
Comprime solo los archivos modificados desde el último backup,
nombra el .zip con timestamp y lo sube al bucket configurado.

Dependencias:
    pip install boto3 python-dotenv

Para MinIO local con Docker:
    docker run -p 9000:9000 -p 9001:9001 \
        -e MINIO_ROOT_USER=minioadmin \
        -e MINIO_ROOT_PASSWORD=minioadmin \
        minio/minio server /data --console-address ":9001"
"""

import os
import json
import zipfile
import hashlib
import logging
from datetime import datetime
from pathlib import Path

import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

load_dotenv()

# ──────────────────────────────────────────────
# Configuración
# ──────────────────────────────────────────────

# Carpeta a respaldar
SOURCE_DIR = Path(os.getenv("BACKUP_SOURCE_DIR", "./data_to_backup"))

# Carpeta local donde se guardan los .zip antes de subirlos
STAGING_DIR = Path(os.getenv("BACKUP_STAGING_DIR", "./backup_staging"))

# Archivo que registra el estado del último backup (hash por archivo)
STATE_FILE = Path(os.getenv("BACKUP_STATE_FILE", "./backup_state.json"))

# Nombre del bucket destino
BUCKET_NAME = os.getenv("BACKUP_BUCKET", "backups")

# ── S3 real ──────────────────────────────────
# AWS_ACCESS_KEY_ID y AWS_SECRET_ACCESS_KEY se toman de env / ~/.aws/credentials
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

# ── MinIO (Docker local) ─────────────────────
USE_MINIO = os.getenv("USE_MINIO", "true").lower() == "true"
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "http://localhost:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minioadmin")

# ──────────────────────────────────────────────
# Logging
# ──────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("incremental_backup")


# ──────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────

def file_hash(path: Path) -> str:
    """SHA-256 del contenido del archivo (detecta cambios reales, no solo mtime)."""
    sha = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            sha.update(chunk)
    return sha.hexdigest()


def load_state() -> dict:
    """Carga el estado del último backup: {ruta_relativa: sha256}."""
    if STATE_FILE.exists():
        with open(STATE_FILE) as f:
            return json.load(f)
    return {}


def save_state(state: dict) -> None:
    """Persiste el estado actual en disco."""
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)
    log.info("Estado guardado en %s", STATE_FILE)


def find_changed_files(source: Path, previous_state: dict) -> list[Path]:
    """
    Recorre source_dir y devuelve los archivos:
      - nuevos (no estaban en el estado anterior)
      - modificados (hash distinto al guardado)
    """
    changed = []
    for path in source.rglob("*"):
        if not path.is_file():
            continue
        rel = str(path.relative_to(source))
        current_hash = file_hash(path)
        if previous_state.get(rel) != current_hash:
            changed.append(path)
    return changed


def create_zip(files: list[Path], source: Path, zip_path: Path) -> None:
    """Comprime los archivos modificados preservando la estructura relativa."""
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in files:
            arcname = f.relative_to(source)
            zf.write(f, arcname)
            log.debug("  + %s", arcname)
    log.info("ZIP creado: %s (%.1f KB)", zip_path.name, zip_path.stat().st_size / 1024)


def build_s3_client():
    """Devuelve un cliente boto3 apuntando a MinIO o a S3 según configuración."""
    if USE_MINIO:
        return boto3.client(
            "s3",
            endpoint_url=MINIO_ENDPOINT,
            aws_access_key_id=MINIO_ACCESS_KEY,
            aws_secret_access_key=MINIO_SECRET_KEY,
            region_name="us-east-1",      # MinIO no usa región real
        )
    return boto3.client("s3", region_name=AWS_REGION)


def ensure_bucket(client, bucket: str) -> None:
    """Crea el bucket si no existe (útil en MinIO o cuentas nuevas)."""
    try:
        client.head_bucket(Bucket=bucket)
        log.info("Bucket '%s' ya existe.", bucket)
    except ClientError as e:
        code = e.response["Error"]["Code"]
        if code in ("404", "NoSuchBucket"):
            client.create_bucket(Bucket=bucket)
            log.info("Bucket '%s' creado.", bucket)
        else:
            raise


def upload_to_storage(client, zip_path: Path, bucket: str, s3_key: str) -> str:
    """Sube el ZIP al bucket y devuelve la URL/key resultante."""
    client.upload_file(str(zip_path), bucket, s3_key)
    dest = f"{'MinIO' if USE_MINIO else 'S3'}://{bucket}/{s3_key}"
    log.info("Subido → %s", dest)
    return dest


# ──────────────────────────────────────────────
# Pipeline principal
# ──────────────────────────────────────────────

def run_backup() -> None:
    log.info("═" * 55)
    log.info("Iniciando backup incremental")
    log.info("Fuente : %s", SOURCE_DIR.resolve())
    log.info("Destino: %s bucket '%s'", "MinIO" if USE_MINIO else "S3", BUCKET_NAME)
    log.info("═" * 55)

    # 1. Validar que existe la carpeta fuente
    if not SOURCE_DIR.exists():
        SOURCE_DIR.mkdir(parents=True)
        log.warning("Carpeta fuente no existía, creada vacía: %s", SOURCE_DIR)

    STAGING_DIR.mkdir(parents=True, exist_ok=True)

    # 2. Cargar estado anterior y detectar cambios
    previous_state = load_state()
    changed_files = find_changed_files(SOURCE_DIR, previous_state)

    if not changed_files:
        log.info("Sin cambios desde el último backup. Nada que hacer.")
        return

    log.info("%d archivo(s) modificado(s):", len(changed_files))
    for f in changed_files:
        log.info("  • %s", f.relative_to(SOURCE_DIR))

    # 3. Crear ZIP con timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_name = f"backup_incremental_{timestamp}.zip"
    zip_path = STAGING_DIR / zip_name

    create_zip(changed_files, SOURCE_DIR, zip_path)

    # 4. Subir a S3 / MinIO
    s3_key = f"incrementales/{zip_name}"
    client = build_s3_client()
    ensure_bucket(client, BUCKET_NAME)
    upload_to_storage(client, zip_path, BUCKET_NAME, s3_key)

    # 5. Actualizar estado (solo archivos subidos con éxito)
    new_state = dict(previous_state)   # conservar archivos no modificados
    for f in changed_files:
        rel = str(f.relative_to(SOURCE_DIR))
        new_state[rel] = file_hash(f)
    save_state(new_state)

    # 6. Limpiar staging local
    zip_path.unlink()
    log.info("ZIP local eliminado.")
    log.info("Backup completado exitosamente ✓")


# ──────────────────────────────────────────────
# Entry point
# ──────────────────────────────────────────────

if __name__ == "__main__":
    run_backup()