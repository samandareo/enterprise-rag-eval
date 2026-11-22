import re
from dataclasses import dataclass


@dataclass
class Chunk:
    chunk_index: int
    section_header: str
    content: str
    token_count: int  # approximate word/subword count for monitoring

def _estimate_tokens(text: str) -> int:
    # Rough multilingual estimate (~1.3 tokens per whitespace-delimeted word)
    return max(1, int(len(text.split()) * 1.3))

def chunk_markdown(
    markdown_text: str,
    max_chars: int = 1200,
    overlap_chars: int = 200,
) -> list[Chunk]:
    """
    Splits Markdown structurally by headings, preserving tables and attaching the active section header to each chunk.
    """
    lines = markdown_text.splitlines()
    sections: list[tuple[str, list[str]]] = []
    current_header = "General"
    current_lines: list[str] = []
    
    header_pattern = re.compile(r"^(#{1,3})\s+(.*)$")

    for line in lines:
        match = header_pattern.match(line.strip())
        if match:
            if current_lines:
                sections.append((current_header, current_lines))
            current_header = match.group(2).strip()
            current_lines = []
        else:
            current_lines.append(line)

    if current_lines:
        sections.append((current_header, current_lines))

    chunks: list[Chunk] = []
    chunk_idx = 0

    for header, sec_lines in sections:
        body = "\n".join(sec_lines).strip()
        if not body:
            continue

        # So here, if entire section fits within max_chars (or is a table), keep it whole
        if len(body) <= max_chars or "|" in body and len(body) <= max_chars * 1.5:
            full_text = f"[{header}]\n{body}"
            chunks.append(
                Chunk(
                    chunk_index=chunk_idx,
                    section_header=header,
                    content=full_text,
                    token_count=_estimate_tokens(full_text),
                )
            )
            chunk_idx += 1
        else:
            # Split long sections by paragraphs with overlap
            paragraphs = [p.strip() for p in body.split("\n\n") if p.strip()]
            buffer = ""
            for para in paragraphs:
                if len(buffer) + len(para) + 2 <= max_chars:
                    buffer = f"{buffer}\n\n{para}".strip() if buffer else para
                else:
                    if buffer:
                        full_text = f"[{header}]\n{buffer}"
                        chunks.append(
                            Chunk(
                                chunk_index=chunk_idx,
                                section_header=header,
                                content=full_text,
                                token_count=_estimate_tokens(full_text),
                            )
                        )
                        chunk_idx += 1
                    overlap_tail = buffer[-overlap_chars:] if overlap_chars > 0 else ""
                    buffer = f"{overlap_tail}\n\n{para}".strip()

            if buffer:
                full_text = f"[{header}]\n{buffer}"
                chunks.append(
                    Chunk(
                        chunk_index=chunk_idx,
                        section_header=header,
                        content=full_text,
                        token_count=_estimate_tokens(full_text),
                    )
                )
                chunk_idx += 1

    return chunks

