import time
import logging
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configuración del log
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler("monitor.log"),
        logging.StreamHandler()  # también muestra en consola
    ]
)

class ManejadorEventos(FileSystemEventHandler):

    def on_created(self, event):
        tipo = "DIRECTORIO" if event.is_directory else "ARCHIVO"
        logging.info(f"[CREADO]    {tipo}: {event.src_path}")

    def on_modified(self, event):
        tipo = "DIRECTORIO" if event.is_directory else "ARCHIVO"
        logging.info(f"[MODIFICADO] {tipo}: {event.src_path}")

    def on_deleted(self, event):
        tipo = "DIRECTORIO" if event.is_directory else "ARCHIVO"
        logging.info(f"[ELIMINADO] {tipo}: {event.src_path}")

    def on_moved(self, event):
        tipo = "DIRECTORIO" if event.is_directory else "ARCHIVO"
        logging.info(f"[MOVIDO]    {tipo}: {event.src_path} → {event.dest_path}")


def monitorear(directorio: str):
    manejador = ManejadorEventos()
    observer = Observer()
    observer.schedule(manejador, path=directorio, recursive=True)
    observer.start()

    logging.info(f"Monitoreando: '{directorio}' — Presioná Ctrl+C para detener.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        logging.info("Monitor detenido.")

    observer.join()


if __name__ == "__main__":
    monitorear(".")   # monitorea el directorio actual; cambiá por la ruta que quieras