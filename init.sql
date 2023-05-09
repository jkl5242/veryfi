CREATE TABLE documents (
    document_id SERIAL PRIMARY KEY,
    ml_response VARCHAR
);

CREATE TABLE parsed_total (
    id SERIAL PRIMARY KEY,
    document_id INT,
    business_id INT,
    value NUMERIC,
    score NUMERIC,
    ocr_score NUMERIC,
    bounding_box NUMERIC[]
)