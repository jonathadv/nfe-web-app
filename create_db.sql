CREATE DATABASE nfeweb;
CREATE USER nfeweb WITH PASSWORD 'nfeweb';

ALTER ROLE nfeweb SET client_encoding TO 'utf8';
ALTER ROLE nfeweb SET default_transaction_isolation TO 'read committed';
ALTER ROLE nfeweb SET timezone TO 'UTC';

GRANT ALL PRIVILEGES ON DATABASE nfeweb TO nfeweb;