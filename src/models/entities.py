"""SQLAlchemy models for all entities in Intelli-Credit Engine"""

from sqlalchemy import (
    Column, String, Integer, Float, DateTime, Text, Boolean, 
    ForeignKey, JSON, Enum as SQLEnum, CheckConstraint
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from typing import Optional
import enum
from src.models.database import Base


# Enums
class ApplicationStatus(str, enum.Enum):
    """Loan application status"""
    DRAFT = "draft"
    SUBMITTED = "submitted"
    INGESTING = "ingesting"
    RESEARCHING = "researching"
    GENERATING = "generating"
    COMPLETE = "complete"
    FAILED = "failed"
    CANCELLED = "cancelled"


class DocumentType(str, enum.Enum):
    """Document type classification"""
    ANNUAL_REPORT = "annual_report"
    GST_RETURN = "gst_return"
    ITR = "itr"
    BANK_STATEMENT = "bank_statement"
    CIBIL_REPORT = "cibil_report"
    SANCTION_LETTER = "sanction_letter"
    FINANCIAL_STATEMENT = "financial_statement"
    OTHER = "other"


class DocumentFormat(str, enum.Enum):
    """Document file format"""
    PDF = "pdf"
    SCANNED_PDF = "scanned_pdf"
    JSON = "json"
    XML = "xml"
    CSV = "csv"
    EXCEL = "excel"


class SeverityLevel(str, enum.Enum):
    """Severity level for discrepancies and issues"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class SentimentType(str, enum.Enum):
    """Sentiment classification"""
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"


class RiskLevel(str, enum.Enum):
    """Risk level classification"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class CreditGrade(str, enum.Enum):
    """Credit grade classification"""
    AAA = "AAA"
    AA = "AA"
    A = "A"
    BBB = "BBB"
    BB = "BB"
    B = "B"
    C = "C"
    D = "D"


class NoteCategory(str, enum.Enum):
    """Qualitative note category"""
    FACTORY_VISIT = "factory_visit"
    MANAGEMENT_INTERVIEW = "management_interview"
    MARKET_FEEDBACK = "market_feedback"
    SITE_INSPECTION = "site_inspection"
    OTHER = "other"


# Models
class LoanApplication(Base):
    """Core loan application entity"""
    __tablename__ = "loan_applications"
    
    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(String(50), unique=True, nullable=False, index=True)
    company_name = Column(String(255), nullable=False, index=True)
    cin = Column(String(21), nullable=True, index=True)  # Corporate Identification Number
    requested_amount = Column(Float, nullable=False)
    requested_tenure_months = Column(Integer, nullable=False)
    purpose = Column(Text, nullable=True)
    submission_date = Column(DateTime, nullable=False, default=func.now())
    status = Column(SQLEnum(ApplicationStatus), nullable=False, default=ApplicationStatus.DRAFT)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
    
    # Relationships
    promoters = relationship("Promoter", back_populates="application", cascade="all, delete-orphan")
    documents = relationship("Document", back_populates="application", cascade="all, delete-orphan")
    extracted_data = relationship("ExtractedData", back_populates="application", cascade="all, delete-orphan")
    research_findings = relationship("ResearchFinding", back_populates="application", cascade="all, delete-orphan")
    qualitative_notes = relationship("QualitativeNotes", back_populates="application", cascade="all, delete-orphan")
    credit_scores = relationship("CreditScore", back_populates="application", cascade="all, delete-orphan")
    cam_documents = relationship("CAMDocument", back_populates="application", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="application", cascade="all, delete-orphan")
    
    # Constraints
    __table_args__ = (
        CheckConstraint('requested_amount > 0', name='check_positive_amount'),
        CheckConstraint('requested_tenure_months > 0', name='check_positive_tenure'),
    )


class Promoter(Base):
    """Promoter/stakeholder information"""
    __tablename__ = "promoters"
    
    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("loan_applications.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    pan = Column(String(10), nullable=True)  # PAN card number
    role = Column(String(100), nullable=True)
    shareholding_percentage = Column(Float, nullable=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    
    # Relationships
    application = relationship("LoanApplication", back_populates="promoters")
    
    # Constraints
    __table_args__ = (
        CheckConstraint('shareholding_percentage >= 0 AND shareholding_percentage <= 100', 
                       name='check_shareholding_range'),
    )


class Document(Base):
    """Document metadata (content stored in S3)"""
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(String(50), unique=True, nullable=False, index=True)
    application_id = Column(Integer, ForeignKey("loan_applications.id", ondelete="CASCADE"), nullable=False)
    document_type = Column(SQLEnum(DocumentType), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_format = Column(SQLEnum(DocumentFormat), nullable=False)
    file_size_bytes = Column(Integer, nullable=True)
    s3_key = Column(String(500), nullable=False)  # S3 object key
    upload_timestamp = Column(DateTime, nullable=False, default=func.now())
    processing_status = Column(String(50), nullable=False, default="pending")
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    
    # Relationships
    application = relationship("LoanApplication", back_populates="documents")
    extracted_data = relationship("ExtractedData", back_populates="document", cascade="all, delete-orphan")


class ExtractedData(Base):
    """Structured data extracted from documents"""
    __tablename__ = "extracted_data"
    
    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("loan_applications.id", ondelete="CASCADE"), nullable=False)
    document_id = Column(Integer, ForeignKey("documents.id", ondelete="CASCADE"), nullable=False)
    extraction_timestamp = Column(DateTime, nullable=False, default=func.now())
    confidence_score = Column(Float, nullable=True)
    raw_text = Column(Text, nullable=True)
    structured_data = Column(JSON, nullable=True)  # Flexible JSON storage for various data formats
    created_at = Column(DateTime, nullable=False, default=func.now())
    
    # Relationships
    application = relationship("LoanApplication", back_populates="extracted_data")
    document = relationship("Document", back_populates="extracted_data")
    financial_metrics = relationship("FinancialMetric", back_populates="extracted_data", cascade="all, delete-orphan")
    
    # Constraints
    __table_args__ = (
        CheckConstraint('confidence_score >= 0 AND confidence_score <= 1', 
                       name='check_confidence_range'),
    )


class FinancialMetric(Base):
    """Individual financial metrics with confidence scores"""
    __tablename__ = "financial_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    extracted_data_id = Column(Integer, ForeignKey("extracted_data.id", ondelete="CASCADE"), nullable=False)
    metric_name = Column(String(100), nullable=False, index=True)
    value = Column(Float, nullable=False)
    unit = Column(String(50), nullable=True)  # e.g., "INR", "USD", "percentage"
    period = Column(String(50), nullable=True)  # e.g., "FY2023", "Q1-2024"
    confidence = Column(Float, nullable=True)
    source_page = Column(Integer, nullable=True)
    flagged_for_review = Column(Boolean, default=False)
    review_reason = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    
    # Relationships
    extracted_data = relationship("ExtractedData", back_populates="financial_metrics")
    
    # Constraints
    __table_args__ = (
        CheckConstraint('confidence >= 0 AND confidence <= 1', 
                       name='check_metric_confidence_range'),
    )


class ResearchFinding(Base):
    """Research findings from web crawling and API integrations"""
    __tablename__ = "research_findings"
    
    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("loan_applications.id", ondelete="CASCADE"), nullable=False)
    finding_type = Column(String(50), nullable=False)  # "news", "litigation", "mca_filing", "sector_analysis"
    entity_name = Column(String(255), nullable=True)  # Company or promoter name
    title = Column(String(500), nullable=True)
    source = Column(String(255), nullable=True)
    source_url = Column(String(1000), nullable=True)
    publication_date = Column(DateTime, nullable=True)
    content = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    sentiment = Column(SQLEnum(SentimentType), nullable=True)
    relevance_score = Column(Float, nullable=True)
    metadata = Column(JSON, nullable=True)  # Additional structured data
    research_timestamp = Column(DateTime, nullable=False, default=func.now())
    created_at = Column(DateTime, nullable=False, default=func.now())
    
    # Relationships
    application = relationship("LoanApplication", back_populates="research_findings")
    
    # Constraints
    __table_args__ = (
        CheckConstraint('relevance_score >= 0 AND relevance_score <= 1', 
                       name='check_relevance_range'),
    )


class QualitativeNotes(Base):
    """Qualitative notes from Credit Officers"""
    __tablename__ = "qualitative_notes"
    
    id = Column(Integer, primary_key=True, index=True)
    note_id = Column(String(50), unique=True, nullable=False, index=True)
    application_id = Column(Integer, ForeignKey("loan_applications.id", ondelete="CASCADE"), nullable=False)
    credit_officer = Column(String(255), nullable=False)
    category = Column(SQLEnum(NoteCategory), nullable=False)
    content = Column(Text, nullable=False)
    sentiment = Column(SQLEnum(SentimentType), nullable=True)
    risk_impact = Column(String(50), nullable=True)  # "positive", "neutral", "negative"
    score_adjustment = Column(Float, nullable=True)  # Numerical adjustment to risk score
    timestamp = Column(DateTime, nullable=False, default=func.now())
    created_at = Column(DateTime, nullable=False, default=func.now())
    
    # Relationships
    application = relationship("LoanApplication", back_populates="qualitative_notes")


class CreditScore(Base):
    """Calculated credit scores with breakdowns"""
    __tablename__ = "credit_scores"
    
    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("loan_applications.id", ondelete="CASCADE"), nullable=False)
    overall_score = Column(Float, nullable=False)
    grade = Column(SQLEnum(CreditGrade), nullable=False)
    risk_level = Column(SQLEnum(RiskLevel), nullable=False)
    confidence = Column(Float, nullable=True)
    
    # Five Cs breakdown
    character_score = Column(Float, nullable=True)
    capacity_score = Column(Float, nullable=True)
    capital_score = Column(Float, nullable=True)
    collateral_score = Column(Float, nullable=True)
    conditions_score = Column(Float, nullable=True)
    
    # Scoring factors and evidence (stored as JSON)
    scoring_breakdown = Column(JSON, nullable=True)
    
    # Loan terms
    recommended_amount = Column(Float, nullable=True)
    maximum_amount = Column(Float, nullable=True)
    interest_rate_min = Column(Float, nullable=True)
    interest_rate_max = Column(Float, nullable=True)
    tenure_months = Column(Integer, nullable=True)
    conditions = Column(JSON, nullable=True)  # List of conditions
    covenants = Column(JSON, nullable=True)  # List of covenants
    
    calculation_timestamp = Column(DateTime, nullable=False, default=func.now())
    created_at = Column(DateTime, nullable=False, default=func.now())
    
    # Relationships
    application = relationship("LoanApplication", back_populates="credit_scores")
    
    # Constraints
    __table_args__ = (
        CheckConstraint('overall_score >= 0 AND overall_score <= 100', 
                       name='check_score_range'),
        CheckConstraint('confidence >= 0 AND confidence <= 1', 
                       name='check_score_confidence_range'),
        CheckConstraint('character_score >= 0 AND character_score <= 100', 
                       name='check_character_score_range'),
        CheckConstraint('capacity_score >= 0 AND capacity_score <= 100', 
                       name='check_capacity_score_range'),
        CheckConstraint('capital_score >= 0 AND capital_score <= 100', 
                       name='check_capital_score_range'),
        CheckConstraint('collateral_score >= 0 AND collateral_score <= 100', 
                       name='check_collateral_score_range'),
        CheckConstraint('conditions_score >= 0 AND conditions_score <= 100', 
                       name='check_conditions_score_range'),
    )


class CAMDocument(Base):
    """Generated CAM documents metadata (content in S3)"""
    __tablename__ = "cam_documents"
    
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(String(50), unique=True, nullable=False, index=True)
    application_id = Column(Integer, ForeignKey("loan_applications.id", ondelete="CASCADE"), nullable=False)
    format = Column(String(10), nullable=False)  # "docx", "pdf"
    s3_key = Column(String(500), nullable=False)  # S3 object key
    file_size_bytes = Column(Integer, nullable=True)
    sections = Column(JSON, nullable=True)  # List of section metadata
    references = Column(JSON, nullable=True)  # List of references/citations
    generation_timestamp = Column(DateTime, nullable=False, default=func.now())
    version = Column(Integer, nullable=False, default=1)
    is_final = Column(Boolean, default=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    
    # Relationships
    application = relationship("LoanApplication", back_populates="cam_documents")


class AuditLog(Base):
    """Complete audit trail of all operations"""
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("loan_applications.id", ondelete="CASCADE"), nullable=True)
    timestamp = Column(DateTime, nullable=False, default=func.now(), index=True)
    component = Column(String(100), nullable=False)  # "data_ingestor", "research_agent", etc.
    operation = Column(String(100), nullable=False)  # "extract_data", "calculate_score", etc.
    user = Column(String(255), nullable=True)  # User who triggered the operation
    status = Column(String(50), nullable=False)  # "success", "failure", "warning"
    details = Column(JSON, nullable=True)  # Additional operation details
    error_message = Column(Text, nullable=True)
    execution_time_ms = Column(Integer, nullable=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    
    # Relationships
    application = relationship("LoanApplication", back_populates="audit_logs")
