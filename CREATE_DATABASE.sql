-- Create database and user for Quantum Nexus
-- Run this as postgres superuser

-- Create user (if not exists)
CREATE USER quantum WITH PASSWORD 'quantum123';

-- Create database (if not exists)
CREATE DATABASE quantum_nexus OWNER quantum;

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE quantum_nexus TO quantum;

-- Connect to the database
\c quantum_nexus

-- Grant schema privileges
GRANT ALL ON SCHEMA public TO quantum;


