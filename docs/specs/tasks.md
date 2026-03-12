# Implementation Plan: Intelli-Credit Engine

## Overview

This implementation plan breaks down the Intelli-Credit Engine into discrete coding tasks following a bottom-up approach. We'll start with core data models and utilities, then build the three main components (Data Ingestor, Research Agent, Recommendation Engine), and finally wire everything together with the Workflow Orchestrator. The implementation uses Python with FastAPI for the web interface, PostgreSQL for structured data, and AWS S3 for document storage.

## Tasks

- [x] 1. Set up project structure and core infrastructure
  - Create Python project with virtual environment
  - Set up directory structure: `src/`, `tests/`, `config/`, `templates/`
  - Configure dependencies: FastAPI, SQLAlchemy, boto3, hypothesis, pytest, python-docx, reportlab
  - Set up database schema and migrations (Alembic)
  - Configure AWS S3 client for document storage
  - Create configuration management (environment variables, config files)
  - _Requirements: 10.1, 10.6_

- [ ] 2. Implement core data models and database layer
  - [x] 2.1 Create SQLAlchemy models for all entities
    - Implement models: LoanApplication, Promoter, Document, ExtractedData, FinancialMetric, ResearchFinding, QualitativeNotes, CreditScore, CAMDocument, AuditLog
    - Define relationships and foreign keys
    - Add validation constraints
    - _Requirements: 10.6_
  
  - [ ]* 2.2 Write property test for data model persistence
    - **Property 33: Intermediate Results Persistence**
    - **Validates: Requirements 10.6**
  
  - [~] 2.3 Implement database repository layer
    - Create repository classes for CRUD operations
    - Implement transaction management
    - Add query methods for common access patterns
    - _Requirements: 10.6_

- [ ] 3. Implement PDF Parser component
  - [~] 3.1 Create PDF text extraction module
    - Implement PDF text extraction using PyPDF2 or pdfplumber
    - Add table detection and extraction
    - Implement section identification (financial statements, risk factors)
    - _Requirements: 1.1_
  
  - [ ]* 3.2 Write property test for PDF extraction
    - **Property 1: Multi-Format Document Extraction (PDF portion)**
    - **Validates: Requirements 1.1**
  
  - [~] 3.3 Implement financial data extraction rules
    - Create regex patterns for financial metrics (revenue, profit, debt)
    - Implement named entity recognition for key terms
    - Add confidence scoring for extracted values
    - _Requirements: 1.1, 8.5_
  
  - [ ]* 3.4 Write property test for confidence scoring
    - **Property 25: Confidence-Based Quality Control**
    - **Validates: Requirements 8.1, 8.4, 8.5**

- [ ] 4. Implement OCR Engine component
  - [~] 4.1 Create image preprocessing module
    - Implement image enhancement: deskewing, noise reduction, contrast adjustment
    - Add quality detection (resolution, contrast metrics)
    - _Requirements: 8.2_
  
  - [ ]* 4.2 Write property test for image enhancement
    - **Property 26: Image Enhancement Application**
    - **Validates: Requirements 8.2**
  
  - [~] 4.3 Integrate AWS Textract for OCR
    - Implement Textract API client
    - Add async job handling for large documents
    - Implement result parsing and normalization
    - _Requirements: 1.2_
  
  - [ ]* 4.4 Write property test for OCR extraction
    - **Property 1: Multi-Format Document Extraction (OCR portion)**
    - **Validates: Requirements 1.2**

- [ ] 5. Implement Structured Data Parser component
  - [~] 5.1 Create GST return parser
    - Implement JSON/XML parser for GSTR-2A and GSTR-3B
    - Extract revenue, input tax credit, and other key fields
    - Normalize to common schema
    - _Requirements: 1.3, 7.1_
  
  - [~] 5.2 Create ITR parser
    - Implement JSON/XML parser for ITR forms
    - Extract income, deductions, tax paid
    - Normalize to common schema
    - _Requirements: 1.3_
  
  - [~] 5.3 Create bank statement parser
    - Implement CSV/Excel parser for bank statements
    - Extract transactions, balances, credits, debits
    - Calculate monthly revenue from credits
    - Normalize to common schema
    - _Requirements: 1.3_
  
  - [~] 5.4 Create CIBIL report parser
    - Implement parser for CIBIL Commercial reports
    - Extract credit score, payment history, outstanding loans
    - Normalize to common schema
    - _Requirements: 7.2_
  
  - [ ]* 5.5 Write property test for structured data parsing
    - **Property 1: Multi-Format Document Extraction (structured data portion)**
    - **Validates: Requirements 1.3**
  
  - [ ]* 5.6 Write property test for CIBIL extraction
    - **Property 22: CIBIL Report Extraction**
    - **Validates: Requirements 7.2**

- [ ] 6. Implement Cross-Verification Engine
  - [~] 6.1 Create data matching module
    - Implement fuzzy matching for company names and periods
    - Create alignment logic for data from different sources
    - _Requirements: 2.1_
  
  - [~] 6.2 Implement variance calculation
    - Create variance calculation function
    - Add threshold-based flagging logic
    - Implement discrepancy categorization (circular trading, revenue inflation)
    - _Requirements: 2.2, 2.4_
  
  - [ ]* 6.3 Write property test for variance calculation
    - **Property 6: Variance Calculation Accuracy**
    - **Validates: Requirements 2.4**
  
  - [~] 6.3 Implement GST cross-verification
    - Compare GSTR-2A vs GSTR-3B for input tax credit
    - Identify and categorize differences
    - _Requirements: 2.3, 7.1_
  
  - [ ]* 6.4 Write property test for GST comparison
    - **Property 5: GST Form Comparison**
    - **Validates: Requirements 2.3**
  
  - [~] 6.5 Implement verification report generator
    - Create report structure with all discrepancies
    - Add evidence and source references
    - _Requirements: 2.5_
  
  - [ ]* 6.6 Write property test for cross-verification detection
    - **Property 4: Cross-Verification Detection**
    - **Validates: Requirements 2.1, 2.2**
  
  - [ ]* 6.7 Write property test for discrepancy reporting
    - **Property 7: Discrepancy Report Completeness**
    - **Validates: Requirements 2.5**

- [ ] 7. Implement Data Ingestor orchestration
  - [~] 7.1 Create Data Ingestor main class
    - Implement document routing logic (PDF vs structured vs scanned)
    - Add batch processing capability
    - Implement error handling and logging
    - _Requirements: 1.4, 1.5_
  
  - [ ]* 7.2 Write property test for batch processing
    - **Property 2: Batch Processing Completeness**
    - **Validates: Requirements 1.4**
  
  - [ ]* 7.3 Write property test for error isolation
    - **Property 3: Error Isolation**
    - **Validates: Requirements 1.5**
  
  - [~] 7.4 Implement data validation module
    - Add range validation for numerical data
    - Implement format validation
    - Add flagging logic for out-of-range values
    - _Requirements: 8.3_
  
  - [ ]* 7.5 Write property test for data validation
    - **Property 27: Data Validation**
    - **Validates: Requirements 8.3**

- [~] 8. Checkpoint - Ensure Data Ingestor tests pass
  - Run all Data Ingestor unit and property tests
  - Verify document extraction accuracy with sample documents
  - Ask the user if questions arise

- [ ] 9. Implement Web Crawler component
  - [~] 9.1 Create search API integration
    - Implement Google Custom Search API client
    - Add query construction for company and promoter names
    - Implement result filtering and ranking
    - _Requirements: 3.1_
  
  - [~] 9.2 Create web scraping module
    - Implement HTTP client with retry logic
    - Add HTML parsing using BeautifulSoup
    - Extract article text, date, source
    - Implement deduplication logic
    - _Requirements: 3.1_
  
  - [~] 9.3 Implement sentiment analysis
    - Use pre-trained NLP model (VADER or TextBlob) for sentiment
    - Classify articles as positive, neutral, negative
    - Calculate relevance scores
    - _Requirements: 3.1_
  
  - [~] 9.4 Implement sector research module
    - Create queries for sector-specific regulations
    - Prioritize Indian regulatory sources (RBI, SEBI)
    - Extract and summarize regulatory changes
    - _Requirements: 3.2, 7.3_
  
  - [ ]* 9.5 Write property test for Indian source prioritization
    - **Property 23: Indian Source Prioritization**
    - **Validates: Requirements 7.3, 7.4**

- [ ] 10. Implement API Integrator component
  - [~] 10.1 Create e-Courts API client
    - Implement authentication and request handling
    - Add litigation search by company/promoter name
    - Parse and normalize case details
    - Implement retry logic with exponential backoff
    - _Requirements: 3.3_
  
  - [~] 10.2 Create MCA API client
    - Implement authentication and request handling
    - Add company filing retrieval by CIN
    - Parse and normalize filing data
    - Implement rate limiting
    - _Requirements: 3.4_
  
  - [ ]* 10.3 Write property test for research execution
    - **Property 8: Research Execution Completeness**
    - **Validates: Requirements 3.1, 3.3, 3.4**
  
  - [ ]* 10.4 Write property test for sector research
    - **Property 9: Sector Research Coverage**
    - **Validates: Requirements 3.2**

- [ ] 11. Implement Qualitative Input Handler
  - [~] 11.1 Create qualitative notes data model and API
    - Implement REST API endpoints for note submission
    - Add note categorization logic
    - Implement sentiment extraction from notes
    - _Requirements: 4.1, 4.2_
  
  - [ ]* 11.2 Write property test for qualitative data association
    - **Property 11: Qualitative Data Association**
    - **Validates: Requirements 4.2, 4.5**
  
  - [~] 11.3 Implement risk adjustment logic
    - Create mapping from sentiment to score adjustment
    - Implement adjustment calculation
    - Add adjustment tracking for audit trail
    - _Requirements: 4.3, 4.4_
  
  - [ ]* 11.4 Write property test for risk score adjustment
    - **Property 12: Risk Score Adjustment Bidirectionality**
    - **Validates: Requirements 4.3, 4.4**

- [ ] 12. Implement Research Agent orchestration
  - [~] 12.1 Create Research Agent main class
    - Implement parallel execution of research tasks
    - Add result consolidation logic
    - Implement error handling for API failures
    - _Requirements: 3.5_
  
  - [ ]* 12.2 Write property test for research report consolidation
    - **Property 10: Research Report Consolidation**
    - **Validates: Requirements 3.5**

- [~] 13. Checkpoint - Ensure Research Agent tests pass
  - Run all Research Agent unit and property tests
  - Verify API integrations with mock data
  - Ask the user if questions arise

- [ ] 14. Implement Score Calculator component
  - [~] 14.1 Create Five Cs scoring framework
    - Implement Character score calculation (promoter background, litigation, news sentiment)
    - Implement Capacity score calculation (revenue, profitability, DSCR)
    - Implement Capital score calculation (net worth, equity)
    - Implement Collateral score calculation (asset valuation, security coverage)
    - Implement Conditions score calculation (sector analysis, economic conditions)
    - _Requirements: 6.1, 6.2_
  
  - [~] 14.2 Implement weighted scoring model
    - Create configurable weight system for Five Cs
    - Implement overall score calculation
    - Add score breakdown generation
    - _Requirements: 6.1, 6.2_
  
  - [ ]* 14.3 Write property test for credit score determinism
    - **Property 16: Credit Score Determinism**
    - **Validates: Requirements 6.1**
  
  - [ ]* 14.4 Write property test for score breakdown consistency
    - **Property 17: Score Breakdown Consistency**
    - **Validates: Requirements 6.2**
  
  - [~] 14.5 Implement loan terms suggestion logic
    - Calculate maximum loan amount from capacity and collateral
    - Implement interest rate mapping from risk score
    - Add tenure and covenant suggestions
    - _Requirements: 6.3, 6.4_
  
  - [ ]* 14.6 Write property test for loan amount reasonableness
    - **Property 18: Loan Amount Reasonableness**
    - **Validates: Requirements 6.3**
  
  - [ ]* 14.7 Write property test for risk-rate correlation
    - **Property 19: Risk-Rate Correlation**
    - **Validates: Requirements 6.4**
  
  - [~] 14.8 Implement Indian regulatory compliance checks
    - Add RBI guideline validation (LTV ratios, exposure limits)
    - Implement sector-specific restrictions
    - _Requirements: 7.5_
  
  - [ ]* 14.9 Write property test for regulatory compliance
    - **Property 24: Regulatory Compliance**
    - **Validates: Requirements 7.5**

- [ ] 15. Implement Explainability Engine
  - [~] 15.1 Create explanation generator
    - Implement natural language generation for score factors
    - Add evidence linking for each factor
    - Create rejection reason generator
    - _Requirements: 6.5, 6.6, 9.1_
  
  - [ ]* 15.2 Write property test for explanation completeness
    - **Property 20: Explanation Completeness**
    - **Validates: Requirements 6.5, 6.6**
  
  - [ ]* 15.3 Write property test for source traceability
    - **Property 28: Source Traceability**
    - **Validates: Requirements 9.1**
  
  - [~] 15.4 Implement citation generator
    - Create citation formatter for different source types
    - Add citation validation (all required fields present)
    - _Requirements: 9.2, 9.3_
  
  - [ ]* 15.5 Write property test for citation format completeness
    - **Property 29: Citation Format Completeness**
    - **Validates: Requirements 9.2, 9.3**

- [ ] 16. Implement CAM Generator component
  - [~] 16.1 Create CAM document templates
    - Design Word template with all required sections
    - Add placeholders for dynamic content
    - Create PDF template as alternative
    - _Requirements: 5.1, 5.2_
  
  - [~] 16.2 Implement template population logic
    - Use python-docx for Word document generation
    - Implement section population (Five Cs, executive summary, analysis)
    - Add table and chart generation
    - Format financial statements
    - _Requirements: 5.1, 5.2, 5.3_
  
  - [ ]* 16.3 Write property test for CAM generation success
    - **Property 13: CAM Generation Success**
    - **Validates: Requirements 5.1**
  
  - [ ]* 16.4 Write property test for CAM structure completeness
    - **Property 14: CAM Structure Completeness**
    - **Validates: Requirements 5.2, 5.3**
  
  - [~] 16.5 Implement citation and reference section
    - Add inline citations throughout CAM
    - Generate references section with all sources
    - _Requirements: 5.4, 9.5_
  
  - [ ]* 16.6 Write property test for citation completeness
    - **Property 15: Citation Completeness**
    - **Validates: Requirements 5.4**

- [ ] 17. Implement Recommendation Engine orchestration
  - [~] 17.1 Create Recommendation Engine main class
    - Implement data retrieval from database
    - Orchestrate score calculation, explanation, and CAM generation
    - Add error handling and logging
    - _Requirements: 5.1, 6.1_
  
  - [~] 17.2 Implement audit trail generation
    - Log all data sources accessed
    - Log all calculations performed
    - Log all decisions made
    - _Requirements: 9.4_
  
  - [ ]* 17.3 Write property test for audit trail completeness
    - **Property 30: Audit Trail Completeness**
    - **Validates: Requirements 9.4, 9.5**

- [~] 18. Checkpoint - Ensure Recommendation Engine tests pass
  - Run all Recommendation Engine unit and property tests
  - Verify CAM generation with sample data
  - Ask the user if questions arise

- [ ] 19. Implement Workflow Orchestrator
  - [~] 19.1 Create job management system
    - Implement job creation and status tracking
    - Add progress percentage calculation
    - Create job queue using in-memory queue or Redis
    - _Requirements: 10.2, 10.3_
  
  - [~] 19.2 Implement pipeline orchestration
    - Create sequential execution: Data Ingestor → Research Agent → Recommendation Engine
    - Add stage completion detection
    - Implement error handling and job failure logic
    - _Requirements: 10.2_
  
  - [ ]* 19.3 Write property test for workflow orchestration sequence
    - **Property 31: Workflow Orchestration Sequence**
    - **Validates: Requirements 10.2**
  
  - [~] 19.4 Implement notification system
    - Create email notification service
    - Add in-app notification mechanism
    - Send notifications on job completion
    - _Requirements: 10.4_
  
  - [ ]* 19.5 Write property test for completion notification
    - **Property 32: Completion Notification**
    - **Validates: Requirements 10.4**

- [ ] 20. Implement Web Interface (FastAPI)
  - [~] 20.1 Create document upload API
    - Implement multipart file upload endpoint
    - Add file validation (size, format)
    - Store files to S3
    - Create document metadata records
    - _Requirements: 10.1_
  
  - [~] 20.2 Create job management API
    - Implement job initiation endpoint
    - Add job status query endpoint
    - Create job cancellation endpoint
    - _Requirements: 10.2, 10.3_
  
  - [~] 20.3 Create CAM retrieval API
    - Implement CAM download endpoint
    - Add CAM preview endpoint
    - Create CAM editing endpoint (allow manual edits)
    - _Requirements: 10.4, 10.5_
  
  - [~] 20.4 Create qualitative notes API
    - Implement note submission endpoint
    - Add note retrieval endpoint
    - _Requirements: 4.1_
  
  - [~] 20.5 Implement authentication and authorization
    - Add JWT-based authentication
    - Implement role-based access control (Credit Officer, Admin)
    - Add API key authentication for external integrations
    - _Requirements: 10.1_

- [ ] 21. Create frontend UI (optional for hackathon)
  - [~] 21.1 Create document upload page
    - Build file upload interface with drag-and-drop
    - Add upload progress indicators
    - Display uploaded document list
    - _Requirements: 10.1_
  
  - [~] 21.2 Create job monitoring dashboard
    - Display job status and progress
    - Show current processing stage
    - Add job cancellation button
    - _Requirements: 10.3_
  
  - [~] 21.3 Create CAM review page
    - Display generated CAM
    - Add inline editing capability
    - Implement download button
    - _Requirements: 10.4, 10.5_
  
  - [~] 21.4 Create qualitative notes form
    - Build note input form with categorization
    - Add note submission
    - Display submitted notes
    - _Requirements: 4.1_

- [ ] 22. Integration and end-to-end testing
  - [ ]* 22.1 Write end-to-end integration tests
    - Test complete pipeline with sample loan application
    - Verify data flow through all components
    - Test error scenarios (API failures, invalid documents)
    - _Requirements: 10.2, 10.4_
  
  - [~] 22.2 Perform accuracy validation
    - Test with real anonymized documents
    - Validate extraction accuracy against ground truth
    - Measure OCR accuracy on scanned documents
    - _Requirements: 8.1_
  
  - [~] 22.3 Performance testing
    - Test with large documents (50-100MB)
    - Measure end-to-end processing time
    - Test concurrent job processing
    - _Requirements: 10.2_

- [ ] 23. Documentation and deployment preparation
  - [~] 23.1 Create API documentation
    - Generate OpenAPI/Swagger documentation
    - Add usage examples for each endpoint
    - Document authentication requirements
    - _Requirements: 10.1_
  
  - [~] 23.2 Create deployment configuration
    - Write Dockerfile for containerization
    - Create docker-compose for local development
    - Write deployment scripts for AWS (ECS/Lambda)
    - Configure environment variables
    - _Requirements: 10.1_
  
  - [~] 23.3 Create user documentation
    - Write user guide for Credit Officers
    - Document supported document formats
    - Add troubleshooting guide
    - _Requirements: 10.1_

- [~] 24. Final checkpoint - Complete system validation
  - Run all tests (unit, property, integration)
  - Verify all requirements are met
  - Test complete workflow with sample data
  - Ask the user if questions arise

## Notes

- Tasks marked with `*` are optional property-based tests that can be skipped for faster MVP development
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation at major milestones
- Property tests validate universal correctness properties across all inputs
- Unit tests validate specific examples, edge cases, and integration points
- The implementation follows a bottom-up approach: data layer → components → orchestration → API → UI
- For hackathon purposes, focus on core functionality (tasks 1-20) and defer optional UI (task 21) if time is limited
