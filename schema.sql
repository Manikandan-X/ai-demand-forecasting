USE forecast_db;
show tables;
ALTER TABLE users
ADD COLUMN role VARCHAR(50) DEFAULT 'user';
DESCRIBE users;
select * from forecast_history;
UPDATE users
SET role = 'admin'
WHERE email = 'mani@gmail.com';
SELECT * FROM users;
ALTER TABLE users
ADD INDEX idx_email (email);
ALTER TABLE datasets
ADD INDEX idx_uploaded_by (uploaded_by);
ALTER TABLE forecasts
ADD INDEX idx_dataset_id (dataset_id);
ALTER TABLE forecasts
ADD INDEX idx_model_used (model_used);
ALTER TABLE forecasts
ADD COLUMN model_used VARCHAR(100);
SHOW INDEX FROM users;
SHOW INDEX FROM datasets;
SHOW INDEX FROM forecasts;
EXPLAIN
SELECT * FROM forecasts
WHERE dataset_id = 1;
SELECT * FROM datasets;
SELECT * FROM forecasts;
SELECT id, name, role
FROM users;