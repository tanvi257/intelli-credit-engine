"""Setup script for Intelli-Credit Engine"""

from setuptools import setup, find_packages

setup(
    name="intelli-credit-engine",
    version="0.1.0",
    description="AI-powered Credit Decisioning Engine for Indian corporate lending",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "fastapi>=0.109.0",
        "uvicorn[standard]>=0.27.0",
        "sqlalchemy>=2.0.25",
        "alembic>=1.13.1",
        "psycopg2-binary>=2.9.9",
        "boto3>=1.34.34",
        "PyPDF2>=3.0.1",
        "pdfplumber>=0.10.3",
        "python-docx>=1.1.0",
        "reportlab>=4.0.9",
        "Pillow>=10.2.0",
        "nltk>=3.8.1",
        "textblob>=0.17.1",
        "beautifulsoup4>=4.12.3",
        "requests>=2.31.0",
        "pytest>=7.4.4",
        "hypothesis>=6.98.3",
        "python-dotenv>=1.0.0",
        "pydantic>=2.5.3",
        "pydantic-settings>=2.1.0",
    ],
    extras_require={
        "dev": [
            "pytest-asyncio>=0.23.3",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Financial and Insurance Industry",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
