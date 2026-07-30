#!/bin/bash
set -e

echo "Setting up rsvr-sdd for local development..."
echo ""

# Check dependencies
echo "Checking dependencies..."
if ! command -v uv &> /dev/null; then
    echo "uv not found. Install from https://github.com/astral-sh/uv"
    exit 1
fi

if ! command -v docker &> /dev/null; then
    echo "Docker not found. Install from https://docs.docker.com/get-docker/"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "Docker Compose not found. Install from https://docs.docker.com/compose/install/"
    exit 1
fi

echo "All dependencies found"
echo ""

# Setup environment
echo "Setting up .env file..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env (update with your SECRET_KEY and other values)"
else
    echo ".env already exists"
fi
echo ""

# Install Python dependencies
echo "Installing Python dependencies..."
cd backend
uv sync
cd ..
echo "Dependencies installed"
echo ""

# Start database
echo "Starting PostgreSQL..."
docker-compose up -d db
echo "PostgreSQL started (listening on localhost:5432)"
echo ""

# Wait for database
echo "Waiting for database to be ready..."
until docker-compose exec -T db pg_isready -U ${POSTGRES_USER:-rsvr} > /dev/null 2>&1; do
    sleep 1
done
echo "Database is ready"
echo ""

# Migrations
echo "Running migrations..."
cd backend && uv run manage.py migrate && cd ..
echo "Migrations complete"
echo ""

# Seed data
read -p "Seed demo data? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    cd backend && uv run manage.py seed_data && cd ..
    echo "Demo data seeded"
fi
echo ""

# Create superuser
read -p "Create admin account? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    cd backend && uv run manage.py createsuperuser && cd ..
    echo "Admin account created"
fi
echo ""

echo "Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Review .env file with any custom settings"
echo "  2. Run: make serve"
echo "  3. Open http://localhost:8000 in your browser"
echo ""
echo "Useful commands:"
echo "  make db-up          Start database"
echo "  make db-stop        Stop database"
echo "  make serve          Start Django dev server"
echo "  make migrate        Run migrations"
echo "  make test           Run test suite"
echo "  make lint           Check code style"
