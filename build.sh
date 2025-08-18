#!/bin/bash
set -e

echo "Starting build process..."

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Install and build frontend
echo "Installing Node.js dependencies..."
cd frontend
npm ci

echo "Building frontend..."
npm run build

echo "Build completed successfully!"