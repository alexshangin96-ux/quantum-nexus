#!/bin/bash
# Add answer column and grant permissions

sudo -u postgres psql quantum_nexus <<'EOF'
ALTER TABLE support_tickets ADD COLUMN IF NOT EXISTS answer TEXT;
GRANT ALL PRIVILEGES ON TABLE support_tickets TO quantum;
GRANT USAGE, SELECT ON SEQUENCE support_tickets_id_seq TO quantum;
\q
EOF

echo "✅ Column added and permissions granted!"



