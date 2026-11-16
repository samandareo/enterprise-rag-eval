CREATE EXTENSION IF NOT EXISTS vector;

-- Documents table (tracks source files, versions, and dedUplications)
CREATE TABLE IF NOT EXISTS documents (
  id SERIAL PRIMARY KEY,
  filename TEXT NOT NULL,
  file_hash TEXT UNIQUE NOT NULL,
  department TEXT NOT NULL,
  language TEXT NOT NULL,
  version INT DEFAULT 1,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Chunks table (stores text, metadata, dense vector, and keyword search vector)
CREATE TABLE IF NOT EXISTS document_chunks (
  id SERIAL PRIMARY KEY,
  document_id INT NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
  chunk_index INT NOT NULL,
  department TEXT NOT NULL,
  page_number INT DEFAULT 1,
  section_header TEXT,
  content TEXT NOT NULL,
  token_count INT NOT NULL,
  embedding vector(1024),
  tsv tsvector GENERATED ALWAYS AS (to_tsvector('simple', content)) STORED,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Audit logs table (tracks every search, chunk accessed, and write action)
CREATE TABLE IF NOT EXISTS audit_logs (
  id SERIAL PRIMARY KEY,
  user_id TEXT NOT NULL,
  department TEXT NOT NULL,
  query TEXT NOT NULL,
  retrieved_chunk_ids INT[],
  action_type TEXT NOT NULL,  -- 'search', 'tool_call', 'write_pending_approval'
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_chunks_embedding_hnsw ON document_chunks USING hnsw (embedding vector_cosine_ops);

CREATE INDEX IF NOT EXISTS idx_chunks_tsv_gin ON document_chunks USING gin (tsv);

CREATE INDEX IF NOT EXISTS idx_chunks_department ON document_chunks (department);




