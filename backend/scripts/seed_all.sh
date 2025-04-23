#!/bin/bash

# Change to the scripts directory
cd "$(dirname "$0")"

# Run the scripts in sequence
echo "Running seed_reset.py..."
python seed_reset.py

echo "Running seed_corresponsales.py..."
python seed_corresponsales.py

echo "Running seed_usuarios.py..."
python seed_usuarios.py

echo "All seeding scripts completed!" 