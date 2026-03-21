from pathlib import Path
from pdfminer.high_level import extract_text


def parse_pdf_to_text(source_path: Path) -> str:
    text = extract_text(source_path)
    return text