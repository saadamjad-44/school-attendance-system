#!/usr/bin/env bash
# Render.com build script

# Install dependencies
pip install -r requirements.txt

# Initialize database and seed data
python seed_data.py
