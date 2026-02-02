#!/bin/bash
# Docker Setup Script for Greek Parliament Analysis System

set -e  # Exit on error

echo "=================================================="
echo "Greek Parliament Analysis"
echo "=================================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

if [ ! -f "backend/data/Greek_Parliament_Proceedings_1989_2020.csv" ]; then
    echo " Warning: CSV data file not found at backend/data/Greek_Parliament_Proceedings_1989_2020.csv"
    echo " The backend will fail to load data until this file exists."
    echo ""
fi

echo "Starting Docker containers..."
echo ""

docker-compose up --build

echo ""
echo "=================================================="
echo "Setup Complete!"
echo "=================================================="
echo ""
echo "Frontend (UI):    http://localhost:5173"
echo "Backend (API):    http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop containers"
