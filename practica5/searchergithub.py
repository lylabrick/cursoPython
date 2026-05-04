import requests
import sys
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT


def get_repos(username: str, token: str = None) -> list:
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    repos = []
    page = 1
    while True:
        url = f"https://api.github.com/users/{username}/repos"
        params = {"per_page": 100, "page": page, "sort": "updated"}
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 404:
            print(f"Usuario '{username}' no encontrado.")
            sys.exit(1)
        elif response.status_code == 403:
            print("Rate limit alcanzado. Usá un token de GitHub.")
            sys.exit(1)
        elif response.status_code != 200:
            print(f"Error: {response.status_code} - {response.json().get('message')}")
            sys.exit(1)

        data = response.json()
        if not data:
            break
        repos.extend(data)
        page += 1

    return repos


def format_date(iso_date: str) -> str:
    if not iso_date:
        return "N/A"
    dt = datetime.strptime(iso_date, "%Y-%m-%dT%H:%M:%SZ")
    return dt.strftime("%d/%m/%Y %H:%M")


def generate_pdf(username: str, repos: list, output_file: str = "reporte_github.pdf"):
    doc = SimpleDocTemplate(
        output_file,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "Title",
        parent=styles["Title"],
        fontSize=20,
        textColor=colors.HexColor("#24292e"),
        spaceAfter=6,
        alignment=TA_CENTER,
    )
    subtitle_style = ParagraphStyle(
        "Subtitle",
        parent=styles["Normal"],
        fontSize=11,
        textColor=colors.HexColor("#586069"),
        spaceAfter=4,
        alignment=TA_CENTER,
    )
    repo_name_style = ParagraphStyle(
        "RepoName",
        parent=styles["Normal"],
        fontSize=13,
        textColor=colors.HexColor("#0366d6"),
        fontName="Helvetica-Bold",
        spaceAfter=2,
    )
    desc_style = ParagraphStyle(
        "Desc",
        parent=styles["Normal"],
        fontSize=9,
        textColor=colors.HexColor("#586069"),
        spaceAfter=4,
    )
    normal_small = ParagraphStyle(
        "NormalSmall",
        parent=styles["Normal"],
        fontSize=9,
        textColor=colors.HexColor("#24292e"),
    )

    elements = []

    # Encabezado
    elements.append(Paragraph(f"Reporte de Repositorios GitHub", title_style))
    elements.append(Paragraph(f"Usuario: @{username}", subtitle_style))
    elements.append(
        Paragraph(
            f"Generado el {datetime.now().strftime('%d/%m/%Y %H:%M')}  |  Total repos: {len(repos)}",
            subtitle_style,
        )
    )
    elements.append(Spacer(1, 0.4 * cm))
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e1e4e8")))
    elements.append(Spacer(1, 0.4 * cm))

    # Tabla resumen
    summary_data = [
        ["#", "Repositorio", "⭐ Stars", "🍴 Forks", "Último commit", "Lenguaje"],
    ]
    for i, repo in enumerate(repos, 1):
        summary_data.append([
            str(i),
            repo["name"],
            str(repo["stargazers_count"]),
            str(repo["forks_count"]),
            format_date(repo.get("pushed_at")),
            repo.get("language") or "—",
        ])

    table = Table(
        summary_data,
        colWidths=[1 * cm, 5.5 * cm, 1.8 * cm, 1.8 * cm, 4 * cm, 3 * cm],
        repeatRows=1,
    )
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#24292e")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 9),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("ALIGN", (1, 1), (1, -1), "LEFT"),
        ("FONTSIZE", (0, 1), (-1, -1), 8),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f6f8fa")]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e1e4e8")),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 0.6 * cm))
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e1e4e8")))
    elements.append(Spacer(1, 0.4 * cm))

    # Detalle por repositorio
    elements.append(Paragraph("Detalle por repositorio", styles["Heading2"]))
    elements.append(Spacer(1, 0.3 * cm))

    for i, repo in enumerate(repos, 1):
        elements.append(Paragraph(f"{i}. {repo['name']}", repo_name_style))

        desc = repo.get("description") or "Sin descripción."
        elements.append(Paragraph(desc, desc_style))

        detail_data = [
            ["⭐ Stars", str(repo["stargazers_count"]),
             "🍴 Forks", str(repo["forks_count"])],
            ["👁 Watchers", str(repo.get("watchers_count", 0)),
             "🐛 Issues abiertos", str(repo.get("open_issues_count", 0))],
            ["Lenguaje", repo.get("language") or "—",
             "Visibilidad", "Privado" if repo.get("private") else "Público"],
            ["Creado", format_date(repo.get("created_at")),
             "Último commit", format_date(repo.get("pushed_at"))],
            ["URL", repo.get("html_url", ""), "", ""],
        ]

        detail_table = Table(
            detail_data,
            colWidths=[3.5 * cm, 5 * cm, 3.5 * cm, 5 * cm],
        )
        detail_table.setStyle(TableStyle([
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("FONTNAME", (2, 0), (2, -1), "Helvetica-Bold"),
            ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#586069")),
            ("TEXTCOLOR", (2, 0), (2, -1), colors.HexColor("#586069")),
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f6f8fa")),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e1e4e8")),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("SPAN", (1, 4), (3, 4)),
        ]))

        elements.append(detail_table)
        elements.append(Spacer(1, 0.5 * cm))

    doc.build(elements)
    print(f"✅ Reporte generado: {output_file}")


if __name__ == "__main__":
    USERNAME = "lylabrick"       # <-- cambiá por el usuario que quieras
    TOKEN = None                 # <-- opcional: "ghp_tu_token_aqui" para más requests

    print(f"Obteniendo repositorios de @{USERNAME}...")
    repos = get_repos(USERNAME, TOKEN)
    print(f"Se encontraron {len(repos)} repositorios.")

    generate_pdf(USERNAME, repos, output_file=f"reporte_{USERNAME}.pdf")