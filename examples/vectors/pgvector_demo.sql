-- Educational example, not executed as part of preparing these notes.
-- Run only in a disposable database with pgvector installed on the server.
-- All changes below are rolled back. No model is called.
\set ON_ERROR_STOP on
BEGIN;
CREATE EXTENSION IF NOT EXISTS vector;
CREATE TEMP TABLE notes_vectors_demo (
    id integer PRIMARY KEY,
    language text NOT NULL,
    embedding vector(3) NOT NULL
) ON COMMIT DROP;
INSERT INTO notes_vectors_demo VALUES
    (1, 'fa', '[1,0,0]'),
    (2, 'fa', '[0.8,0.6,0]'),
    (3, 'en', '[0,1,0]');
SELECT id,
       embedding <=> '[1,0,0]'::vector AS cosine_distance
FROM notes_vectors_demo
WHERE language = 'fa'
ORDER BY embedding <=> '[1,0,0]'::vector
LIMIT 2;
-- Expected mathematical distances: id 1 -> 0, id 2 -> approximately 0.2.
-- Optional index syntax for a larger teaching dataset:
-- CREATE INDEX ON notes_vectors_demo USING hnsw (embedding vector_cosine_ops);
ROLLBACK;
