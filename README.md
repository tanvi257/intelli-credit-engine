# Intelli-Credit Engine

AI-powered Credit Decisioning Engine that automates the preparation of Comprehensive Credit Appraisal Memos (CAM) for Indian corporate lending.

## Features

- **Multi-Format Document Ingestion**: Extracts data from PDFs, scanned documents, GST returns, ITRs, and bank statements
- **Automated Web Research**: Performs background checks on companies and promoters
- **Cross-Verification**: Validates financial data across multiple sources
- **Credit Scoring**: Calculates credit scores using the Five Cs framework
- **CAM Generation**: Produces professional credit appraisal memos with full traceability

## Project Structure

```
intelli-credit-engine/
├── src/
│   ├── config/          # Configuration and settings
│   ├── models/          # Database models (to be created)
│   ├── data_ingestor/   # Document processing components (to be created)
│   ├── research_agent/  # Web research components (to be created)
│   ├── recommendation/  # Credit scoring and CAM generation (to be created)
│   └── main.py          # Application entry point
├── tests/               # Test suite
├── alembic/             # Database migrations
├── config/              # Configuration files
├── templates/           # Document templates
├── requirements.txt     # Python dependencies
└── README.md
```

## Setup

### Prerequisites

- Python 3.10 or higher
- PostgreSQL 13 or higher
- AWS account (for S3 and Textract)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd intelli-credit-engine
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Set up the database:
```bash
# Create PostgreSQL database
createdb intellicredit

# Run migrations
alembic upgrade head
```

### Running the Application

Development mode:
```bash
python src/main.py
```

Or using uvicorn directly:
```bash
uvicorn src.main:app --reload
```

The API will be available at `http://localhost:8000`

API documentation: `http://localhost:8000/docs`

### Running Tests

Run all tests:
```bash
pytest
```

Run specific test types:
```bash
pytest -m unit          # Unit tests only
pytest -m property      # Property-based tests only
pytest -m integration   # Integration tests only
```

Run with coverage:
```bash
pytest --cov=src --cov-report=html
```

## Configuration

Key configuration options in `.env`:

- `DATABASE_URL`: PostgreSQL connection string
- `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`: AWS credentials
- `S3_BUCKET_NAME`: S3 bucket for document storage
- `TEXTRACT_ENABLED`: Enable/disable AWS Textract OCR
- `REVENUE_VARIANCE_THRESHOLD`: Threshold for flagging discrepancies (%)

## Development

### Database Migrations

Create a new migration:
```bash
alembic revision --autogenerate -m "description"
```

Apply migrations:
```bash
alembic upgrade head
```

Rollback:
```bash
alembic downgrade -1
```

### Code Style

This project follows PEP 8 guidelines. Format code before committing:
```bash
black src/ tests/
```

## Architecture

The system follows a three-stage pipeline:

1. **Data Ingestor**: Extracts and normalizes data from documents
2. **Research Agent**: Performs automated web research
3. **Recommendation Engine**: Generates credit scores and CAM documents

See `.kiro/specs/intelli-credit-engine/design.md` for detailed architecture documentation.

## Authors

**Project Team:** Team Optimizer  
**Lead Developer:** Tanvi Mandan (tanvimandan7@gmail.com)  
**Date:** 12 March 2026



