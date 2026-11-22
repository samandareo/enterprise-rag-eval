import hashlib
from pathlib import Path
import pymupdf4llm
from docx import Document
from docx.document import Document as _Document
from docx.oxml.text.paragraph import CT_P
from docx.oxml.table import CT_Tbl
from docx.table import Table
from docx.text.paragraph import Paragraph


def compute_file_hash(file_path: Path) -> str:
    """Compute SHA-256 hash of a file for deduplication."""
    sha256 = hashlib.sha256()
    with file_path.open("rb") as f:
        for block in iter(lambda: f.read(65536), b""):
            sha256.update(block)
    return sha256.hexdigest()

def _iter_docx_blocks(parent: _Document):
    """Yield paragraphs and tables in the exact order they appear in a DOCX file."""
    for child in parent.element.body.iterchildren():
        if isinstance(child, CT_P):
            yield Paragraph(child, parent)
        elif isinstance(child, CT_Tbl):
            yield Table(child, parent)

def _table_to_markdown(table: Table) -> str:
    """Convert a python-docx Table into a clean Markdown table."""
    rows = []
    for row in table.rows:
        cells = [cell.text.strip().replace("\n", " ") for cell in row.cells]
        rows.append("| " + " | ".join(cells) + " |")
    if len(rows) >= 1:
        col_count = len(table.rows[0].cells)
        separator = "| " + " | ".join(["---" * col_count]) + " |"
        rows.insert(1, separator)
    return "\n".join(rows)

def parse_docx_to_markdown(file_path: Path) -> str:
    doc = Document(file_path)
    md_parts: list[str] = []

    for block in _iter_docx_blocks(doc):
        if isinstance(block, Paragraph):
            text = block.text.strip()
            if not text:
                continue
            style_name = block.style.name if block.style else ""
            if style_name.startswith("Heading 1"):
                md_parts.append(f"# {text}")
            elif style_name.startswith("Heading 2"):
                md_parts.append(f"## {text}")
            elif style_name.startswith("Heading 3"):
                md_parts.append(f"### {text}")
            else:
                md_parts.append(text)
        elif isinstance(block, Table):
            md_parts.append(_table_to_markdown(block))

    return "\n\n".join(md_parts)


def parse_document(file_path: Path) -> str:
    """Route PDF or DOCX files to the appropriate Markdown extractor."""
    suffix = file_path.suffix.lower()
    if suffix == ".pdf":
        return pymupdf4llm.to_markdown(str(file_path))
    elif suffix == ".docx":
        return parse_docx_to_markdown(file_path)
    else:
        raise ValueError(f"Unsupported file format: {suffix}")

