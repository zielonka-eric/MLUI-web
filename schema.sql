CREATE TABLE Models (
    model_id CHAR(10) PRIMARY KEY,
    model BLOB,
    is_finished INTEGER NOT NULL
);

CREATE TABLE Results (
    result_id CHAR(10) PRIMARY KEY,
    results TEXT,
    model_id CHAR(10) NOT NULL,
    is_finished INTEGER NOT NULL,
    FOREIGN KEY (model_id) REFERENCES Models (model_id)
);

CREATE TABLE Data (
    data_id CHAR(10) PRIMARY KEY,
    data BLOB NOT NULL,
    filename TEXT NOT NULL
);