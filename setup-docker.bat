@echo off
REM Docker Setup Script for Greek Parliament Analysis

echo ==================================================
echo Greek Parliament Analysis
echo ==================================================
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker is not installed. Please install Docker Desktop first.
    pause
    exit /b 1
)

REM Check if Docker Compose is installed
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker Compose is not installed. Please install Docker Desktop first.
    pause
    exit /b 1
)

REM Check if data file exists
if not exist "backend\data\Greek_Parliament_Proceedings_1989_2020.csv" (
    echo WARNING: CSV data file not found at backend\data\Greek_Parliament_Proceedings_1989_2020.csv
    echo The backend will fail to load data until this file exists.
    echo.
)

echo Starting Docker containers...
echo.

REM Build and start containers
docker-compose up --build

echo.
echo ==================================================
echo Setup Complete!
echo ==================================================
echo.
echo Frontend (UI):    http://localhost:5173
echo Backend (API):    http://localhost:8000
echo.
echo Press Ctrl+C to stop containers
echo.
pause
