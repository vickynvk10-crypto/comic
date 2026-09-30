from pathlib import Path
from datetime import datetime
from fpdf import FPDF
from app.config import BASE_DIR

def save_pdf(layout: list[dict]) -> str:
    export_dir = BASE_DIR / "static" / "exports"
    export_dir.mkdir(parents=True, exist_ok=True)
    filename = f"comiccraft_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    path = export_dir / filename

    pdf = FPDF("P", "mm", "A4")
    pdf.set_auto_page_break(auto=True, margin=14)

    for panel in layout:
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 18)
        pdf.cell(0, 12, f"Panel {panel['panel_number']}: {panel['title']}", ln=True)
        image_file = BASE_DIR / panel["image_path"].replace("/static/", "static/")
        if image_file.exists():
            pdf.image(str(image_file), x=15, y=28, w=180)
        pdf.ln(132)
        pdf.set_font("Helvetica", "I", 10)
        pdf.multi_cell(0, 6, panel["scene_description"])
        pdf.ln(2)
        pdf.set_font("Helvetica", "B", 11)
        if panel["caption"]:
            pdf.multi_cell(0, 6, f"Caption: {panel['caption']}")
        pdf.set_font("Helvetica", "", 11)
        if panel["narration"]:
            pdf.multi_cell(0, 6, f"Narration: {panel['narration']}")
        for line in panel["dialogue"]:
            pdf.multi_cell(0, 6, str(line))

    pdf.output(str(path))
    return f"/static/exports/{filename}"
