from contextlib import contextmanager
import psycopg
from pgvector.psycopg import register_vector
from rag_engine.config import settings


@contextmanager
def get_db_conn():
    with psycopg.connect(settings.database_url) as conn:
        register_vector(conn)
        yield conn

def get_document_by_hash(conn: psycopg.Connection, file_hash: str) -> int | None:
    with conn.cursor() as cur:
        cur.execute("SELECT id FROM documents WHERE file_hash = %s", (file_hash,))
        row = cur.fetchone()
        return row[0] if row else None

def insert_document(
    conn: psycopg.Connection,
    filename: str,
    file_hash: str,
    department: str,
    language: str,
) -> int:
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO documents (filename, file_hash, department, language)
            VALUES (%s, %s, %s, %s)
            RETURNING id
            """,
            (filename, file_hash, department, language),
        )
        return cur.fetchone()[0]

def insert_chunk(
    conn: psycopg.Connection,
    document_id: int,
    chunk_index: int,
    department: str,
    section_header: str,
    content: str,
    token_count: int,
    embedding: list[float] | None = None,
) -> int:
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO document_chunks (document_id, chunk_index, department, section_header, content, token_count, embedding)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id
            """,
            (document_id, chunk_index, department, section_header, content, token_count, embedding),
        )
        return cur.fetchone()[0]

