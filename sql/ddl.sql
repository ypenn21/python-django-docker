-- setup alloy db follow these steps on codelabs https://codelabs.developers.google.com/codelabs/alloydb-ai-embedding#4

CREATE TYPE scope_type AS ENUM ('public', 'private');

-- 1. Authors Table
create TABLE authors (
    author_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    bio TEXT,
    embedding public.vector GENERATED ALWAYS AS (public.embedding('textembedding-gecko@003'::text, bio)) STORED
);

-- 2. Books Table
create TABLE document (
    document_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author_id INT NOT NULL,
    publication_year date,
    scope scope_type NOT NULL DEFAULT 'public',
    CONSTRAINT fk_author
        FOREIGN KEY(author_id)
        REFERENCES Authors(author_id)
);

-- 4. Pages Table
create TABLE pages (
    page_id SERIAL PRIMARY KEY,
    document_id INT NOT NULL,
    page_number INT NOT NULL,
    content TEXT,
    embedding public.vector GENERATED ALWAYS AS (public.embedding('textembedding-gecko@003'::text, content)) STORED,
    CONSTRAINT fk_pages
        FOREIGN KEY(document_id)
        REFERENCES document(document_id)
);


CREATE INDEX idx_pages_document_id ON pages (document_id);
CREATE INDEX idx_document_author_id ON document (author_id);
CREATE INDEX idx_document_document_id ON document (document_id);
CREATE INDEX idx_pages_author_id ON authors (author_id);