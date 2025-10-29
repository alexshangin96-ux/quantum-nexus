#!/bin/bash

# Run database migration for shop levels
echo "Running database migration..."

# Connect to PostgreSQL and run the migration
sudo -u postgres psql -d quantum_nexus -f add_shop_levels.sql

if [ $? -eq 0 ]; then
    echo "✅ Migration completed successfully!"
    echo "Added columns: tap_boost_levels, energy_buy_levels, energy_expand_levels"
else
    echo "❌ Migration failed!"
    exit 1
fi
