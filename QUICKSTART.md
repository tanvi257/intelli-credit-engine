# Quick Start Guide

This guide will help you get the Intelli-Credit Engine up and running quickly.

## Prerequisites

- Python 3.10 or higher
- PostgreSQL 13 or higher (or use Docker)
- AWS account with S3 and Textract access (optional for full functionality)

## Option 1: Quick Setup with Docker (Recommended)

1. **Start the services**:
```bash
docker-compose up -d
```

2. **Access the application**:
- API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

That's it! The database and application are now running.

## Option 2: Manual Setup

### Step 1: Install Dependencies

**On Windows**:
```bash
scripts\setup.bat
```

**On Linux/Mac**:
```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

Or manually:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2: Configure Environment

1. Copy the environment template:
```bash
cp .env.example .env
```

2. Edit `.env` with your configuration:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/intellicredit
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
S3_BUCKET_NAME=your-bucket
```

### Step 3: Set Up Database

1. Create the database:
```bash
createdb intellicredit
```

2. Run migrations:
```bash
alembic upgrade head
```

### Step 4: Run the Application

```bash
python src/main.py
```

Or with uvicorn:
```bash
uvicorn src.main:app --reload
```

## Verify Installation

Run the validation script:
```bash
python scripts/validate_setup.py
```

Run tests (after installing dependencies):
```bash
pytest tests/test_infrastructure.py -v
```

## Next Steps

1. **Review the architecture**: See `.kiro/specs/intelli-credit-engine/design.md`
2. **Check the requirements**: See `.kiro/specs/intelli-credit-engine/requirements.md`
3. **Follow the implementation plan**: See `.kiro/specs/intelli-credit-engine/tasks.md`
4. **Start implementing Task 2**: Database models and repository layer

## Troubleshooting

### Database Connection Issues

If you get database connection errors:
1. Ensure PostgreSQL is running
2. Verify DATABASE_URL in `.env`
3. Check database exists: `psql -l`

### Import Errors

If you get import errors:
1. Ensure virtual environment is activated
2. Install dependencies: `pip install -r requirements.txt`
3. Verify you're in the project root directory

### AWS Configuration

For local development without AWS:
1. Set `TEXTRACT_ENABLED=False` in `.env`
2. OCR functionality will be disabled but other features will work

## Development Workflow

1. Create a feature branch
2. Implement the feature following the task list
3. Write tests (unit and property-based)
4. Run tests: `pytest`
5. Commit and push changes

## Useful Commands

```bash
# Run all tests
pytest

# Run specific test types
pytest -m unit
pytest -m property
pytest -m integration

# Run with coverage
pytest --cov=src --cov-report=html

# Create a new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1

# Format code
black src/ tests/

# Start development server
uvicorn src.main:app --reload
```
