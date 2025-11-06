-- Fix support_tickets table permissions
-- Run this as postgres user on server

-- Connect to database
\c quantum_nexus

-- Grant permissions to quantum user
GRANT ALL PRIVILEGES ON TABLE support_tickets TO quantum;
GRANT USAGE, SELECT ON SEQUENCE support_tickets_id_seq TO quantum;

-- If table doesn't exist, create it
CREATE TABLE IF NOT EXISTS support_tickets (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    topic VARCHAR(100),
    message TEXT,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    answered_at TIMESTAMP
);

-- Grant permissions again after creation
GRANT ALL PRIVILEGES ON TABLE support_tickets TO quantum;
GRANT USAGE, SELECT ON SEQUENCE support_tickets_id_seq TO quantum;











