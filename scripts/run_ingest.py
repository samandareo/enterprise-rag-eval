from pathlib import Path
from rag_engine.parser import parse_document, compute_file_hash
from rag_engine.chunker import chunk_markdown
from rag_engine.embedder import MultilingualEmbedder
from rag_engine.db import get_db_conn, get_document_by_hash, insert_document, insert_chunk


DOC_METADATA = {
    "hr_policy_ru.pdf": {"department": "hr", "language": "ru"},
    "it_support_uz_lat.docx": {"department": "it", "language": "uz_lat"},
    "finance_faq_uz_cyr.pdf": {"department": "finance", "language": "uz_cyr"},
}

def run_ingestion() -> None:
    raw_dir = Path("data/raw_docs")
    embedder = MultilingualEmbedder()

    with get_db_conn() as conn:
        for file_path in sorted(raw_dir.iterdir()):
            if file_path.name not in DOC_METADATA:
                continue

            meta = DOC_METADATA[file_path.name]
            file_hash = compute_file_hash(file_path)

            # deduplication check part
            existing_id = get_document_by_hash(conn, file_hash)
            if existing_id is not None:
                print(f"[SKIP] {file_path.name} already ingested (doc_id={existing_id}).")
                continue

            # parse and chunk part
            print(f"[INGEST] Parsing {file_path.name} ({meta['department']} / {meta['language']})...")
            md_text = parse_document(file_path)
            chunks = chunk_markdown(md_text)

            # embed all chunks in one batch
            vectors = embedder.embed_texts([c.content for c in chunks])

            # save document and chunks inside one transaction
            doc_id = insert_document(
                conn,
                filename=file_path.name,
                file_hash=file_hash,
                department=meta["department"],
                language=meta["language"],
            )
            for chunk, vec in zip(chunks, vectors):
                insert_chunk(
                    conn,
                    document_id=doc_id,
                    chunk_index=chunk.chunk_index,
                    department=meta["department"],
                    section_header=chunk.section_header,
                    content=chunk.content,
                    token_count=chunk.token_count,
                    embedding=vec,
                )
            conn.commit()
            print(f"[DONE] Saved {len(chunks)} chunks for {file_path.name} (doc_id={doc_id}).")


if __name__ == "__main__":
    run_ingestion()
