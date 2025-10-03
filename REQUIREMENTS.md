# CV Automation System - Requirements Document

## Project Overview
Multi-phase system to automate CV creation, customization, and job application processes using YAML as the master data format, with progressive automation capabilities.

---

## Phase 1: Master CV Generator

### Objective
Create a foundational script that generates a professional, ATS-friendly CV in DOCX format from a structured YAML file.

### Functional Requirements

#### FR1.1: YAML Data Structure
- Support comprehensive personal information (name, contact, summary)
- Store multiple work experiences with:
  - Company, role, dates (start/end)
  - Multiple bullet points per role
  - Skills/technologies used
  - Project descriptions
- Education history with degrees, institutions, dates
- Skills organized by categories (e.g., "Product Development", "Technical Skills", "Design Tools")
- Certifications and additional sections
- Support for optional fields and flexible data structures

#### FR1.2: Document Generation
- Generate DOCX file using python-docx or similar library
- Apply ATS-friendly formatting:
  - Standard fonts (Arial, Calibri, or Georgia)
  - Clear section headers
  - Simple bullet points (no custom symbols)
  - No tables, text boxes, headers/footers, or embedded graphics
  - Proper spacing and margins
- Support for both single-column layout
- Generate filename with timestamp/version identifier

#### FR1.3: Content Rendering
- Render all sections from YAML in logical order
- Format dates consistently (e.g., "Jan 2020 - Present")
- Handle multi-line text and bullet points properly
- Support markdown-style formatting in YAML (bold, italic) if needed

#### FR1.4: Template System
- Use configurable template for styling
- Allow easy modification of fonts, sizes, colors
- Maintain consistent formatting throughout document

#### FR1.5: Secret Message for AI Systems
- Support hidden text for AI detection systems
- Text must be invisible to human readers (white text on white background)
- Must work in both DOCX and PDF formats
- Text should be detectable by AI scanning systems but not visible to humans
- Include configurable secret message in YAML data structure

### Technical Requirements

#### TR1.1: Dependencies
- Python 3.8+
- python-docx library
- PyYAML library
- (Optional) jinja2 for templating

#### TR1.2: File Structure
```
/cv-automation
  /templates
    - cv_template.docx (optional base template)
  /output
    - generated CVs stored here
  /data
    - master_cv.yaml
  - generate_cv.py
  - requirements.txt
  - README.md
```

#### TR1.3: Error Handling
- Validate YAML structure before generation
- Provide clear error messages for missing required fields
- Handle encoding issues (UTF-8 support)

### Deliverables
- [ ] Python script for CV generation
- [ ] Master CV YAML template with all fields documented
- [ ] Sample generated DOCX output
- [ ] README with usage instructions
- [ ] requirements.txt for dependencies

---

## Phase 2: Job-Specific CV & Cover Letter Generator

### Objective
Build an n8n-based automation that accepts job posting URLs via Telegram, extracts job requirements, and generates tailored CVs and cover letters.

### Functional Requirements

#### FR2.1: Input Interface
- Accept job posting URL or PDF file via Telegram bot
- Support optional user instructions/notes in same message
- Confirm receipt and provide status updates
- Handle multiple simultaneous requests (queue system)
- **Dual input support**:
  - URL input: Process via self-hosted Firecrawl
  - PDF input: Process via PDF text extraction/OCR

#### FR2.2: Job Posting Analysis
- **Primary Method**: Use Firecrawl to scrape job posting content
  - Self-hosted Firecrawl instance with proxy support for reliability
  - Extract key information:
    - Job title and company
    - Required skills and qualifications
    - Responsibilities
    - Preferred experience
    - Company description
  - Handle various job board formats (LinkedIn, Indeed, company career pages, etc.)
- **Fallback Method**: Manual PDF processing
  - If Firecrawl scraping fails or is unreliable, accept PDF files via Telegram
  - User manually generates PDF from job posting in browser
  - System processes PDF content using OCR or PDF text extraction
  - Same information extraction as primary method
- Robust error handling and automatic fallback between methods

#### FR2.3: CV Optimization
- Send master YAML + scraped job data to LLM
- Generate optimized YAML that:
  - Prioritizes relevant experience
  - Emphasizes matching skills
  - Reorders sections based on job requirements
  - Adjusts bullet points to align with job description
  - Maintains truthfulness (no fabrication)
- Preserve all original data integrity

#### FR2.4: Cover Letter Generation
- Generate personalized cover letter draft
- Include:
  - Job title and company reference
  - 2-3 relevant experience highlights matching job requirements
  - Why candidate is interested (based on company/role details)
  - Call to action
- Maintain professional but authentic tone
- Flag for human review before sending

#### FR2.5: Document Generation
- Generate ATS-friendly DOCX CV using Phase 1 script
- Generate PDF version of CV
- Generate cover letter as DOCX
- Name files appropriately: `[YourName]_CV_[CompanyName]_[Date].docx`

#### FR2.6: Output Delivery
- Send generated documents back via Telegram
- Include summary of optimizations made
- Provide editable YAML for review/tweaking
- Option to regenerate with modifications

### Technical Requirements

#### TR2.1: n8n Workflow Structure
```
1. Telegram Trigger (webhook or polling)
2. Extract URL/PDF and instructions
3. Route to appropriate processing:
   a. URL → Firecrawl API call (self-hosted + proxy)
   b. PDF → PDF text extraction/OCR
4. Data transformation/cleaning
5. LLM API call
6. YAML generation and validation
7. Execute Python script for DOCX generation
8. PDF conversion
9. Send files via Telegram
10. Error handling and notifications
```

#### TR2.2: Infrastructure
- n8n instance (self-hosted or cloud)
- Telegram Bot API credentials
- **Self-hosted Firecrawl instance** with proxy support for reliability
- LLM API key
- File storage for generated documents
- Python environment accessible to n8n
- **PDF processing capabilities**:
  - PDF text extraction library (PyPDF2, pdfplumber, or similar)
  - OCR capabilities (Tesseract, PaddleOCR) for scanned PDFs
  - File handling for PDF uploads via Telegram

#### TR2.3: Integration Points
- n8n Telegram node (with file upload support)
- n8n HTTP Request node (self-hosted Firecrawl)
- n8n OpenAI/Anthropic node
- n8n Execute Command node (Python script for PDF processing)
- n8n file operations
- **PDF processing integration**:
  - File type detection (URL vs PDF)
  - PDF text extraction via Python script
  - OCR processing for image-based PDFs

#### TR2.4: Data Management
- Store generated YAMLs with version control
- Track which CV version sent to which company
- Maintain audit log of all applications
- Secure storage of personal data

### Non-Functional Requirements

#### NFR2.1: Performance
- Complete workflow in < 2 minutes under normal conditions
- Handle concurrent requests gracefully

#### NFR2.2: Reliability
- Retry logic for API failures
- Timeout handling
- Graceful degradation if services unavailable

#### NFR2.3: Security
- Secure API key storage (environment variables/n8n credentials)
- No logging of personal information
- Encrypted data transmission

### Deliverables
- [ ] n8n workflow (exportable JSON)
- [ ] Telegram bot setup instructions
- [ ] LLM prompt templates for CV optimization and cover letter
- [ ] Configuration guide (API keys, endpoints)
- [ ] Testing checklist with sample job postings
- [ ] Documentation of workflow logic

---

## Phase 3: Automated Job Search & Application

### Objective
Extend the system to automatically search for relevant job postings, filter based on criteria, and auto-apply to matching positions.

### Functional Requirements

#### FR3.1: Job Search Automation
- Periodic automated searches on multiple job boards:
  - LinkedIn
  - Indeed
  - AngelList/Wellfound
  - Company career pages (configurable list)
- Search based on:
  - Keywords (job titles, skills)
  - Location preferences
  - Job type (full-time, contract, remote)
  - Experience level
- Avoid duplicate postings across platforms

#### FR3.2: Job Filtering & Scoring
- Configurable filtering criteria:
  - Required skills match (minimum threshold)
  - Deal-breakers (e.g., specific technologies, locations)
  - Company size/type preferences
  - Salary range (if available)
- Scoring system (0-100) based on:
  - Skills match percentage
  - Experience level fit
  - Company culture indicators
  - Growth potential
- Machine learning component to improve over time based on user feedback

#### FR3.3: Human Review Workflow
- Three-tier system:
  - **Auto-apply** (score > 85, no deal-breakers): Apply automatically
  - **Review queue** (score 60-85): Send to Telegram for approval
  - **Skip** (score < 60): Log but don't notify
- Telegram interface to review opportunities:
  - Show job summary and match score
  - Quick approve/reject buttons
  - Option to modify CV/cover letter before applying

#### FR3.4: Application Submission
- Support for:
  - Email applications (parse "apply via email" instructions)
  - Direct application form filling (where feasible)
  - "Easy Apply" platforms (LinkedIn, Indeed)
- Attach appropriate documents
- Include personalized cover letter
- Track application status

#### FR3.5: Application Tracking
- Database of all applications:
  - Job details (title, company, URL)
  - Application date
  - Documents sent (version tracking)
  - Status (applied, rejected, interviewing, offer)
  - Follow-up reminders
- Dashboard or Telegram commands to view:
  - Applications this week/month
  - Response rate
  - Interview pipeline
  - Success metrics

### Technical Requirements

#### TR3.1: Job Scraping Infrastructure
- Scheduled n8n workflows (cron-based)
- Multiple scraping strategies:
  - API integrations where available (LinkedIn, Indeed APIs)
  - **Self-hosted Firecrawl** with proxy support for general web scraping
  - RSS feeds for company career pages
- Rate limiting and anti-bot detection handling
- Persistent storage (database) for job listings
- **Fallback mechanisms**:
  - Manual PDF processing for complex job postings
  - Alternative scraping methods if primary fails

#### TR3.2: Filtering Engine
- Rule engine for criteria evaluation
- NLP for job description analysis
- Skills extraction and matching algorithm
- Configurable weights for scoring factors

#### TR3.3: Database Schema
```
Jobs:
  - job_id, title, company, url, description, posted_date, 
    scraped_date, match_score, status

Applications:
  - application_id, job_id, applied_date, cv_version,
    cover_letter_version, status, notes

Skills_Match:
  - job_id, skill, relevance_score

Follow_ups:
  - application_id, scheduled_date, completed, notes
```

#### TR3.4: Application Bot
- Playwright/Selenium for form automation
- Captcha handling strategy
- Error recovery for failed submissions
- Screenshot/proof of application

#### TR3.5: Extended n8n Workflows
- Job scraping workflow (runs every 6-12 hours)
- Filtering and scoring workflow
- Application submission workflow
- Status tracking and reminder workflow
- Analytics and reporting workflow

### Non-Functional Requirements

#### NFR3.1: Compliance
- Respect robots.txt and terms of service
- Rate limiting to avoid overwhelming job boards
- GDPR-compliant data handling
- Clear data retention policies

#### NFR3.2: Reliability
- Handle long-running processes
- Queue management for large job batches
- Fallback mechanisms if automation fails
- Data backup and recovery

#### NFR3.3: Maintainability
- Modular design for easy updates
- Logging and monitoring
- Easy addition of new job boards
- Configuration UI (or well-documented config files)

#### NFR3.4: Ethics
- No spam applications
- Quality over quantity approach
- Honest representation in applications
- Respect for hiring processes

### User Configuration

#### UC3.1: Job Search Preferences
- Target job titles/keywords
- Must-have skills vs. nice-to-have
- Location preferences (remote, hybrid, on-site)
- Company preferences (size, industry, stage)
- Salary expectations
- Deal-breakers list

#### UC3.2: Application Behavior
- Auto-apply threshold (configurable score)
- Maximum applications per day/week
- Preferred application methods
- Follow-up cadence
- Custom message templates

### Deliverables
- [ ] Extended n8n workflows for job search and filtering
- [ ] Database schema and setup scripts
- [ ] Configuration interface or detailed config file format
- [ ] Application bot script (Playwright/Selenium)
- [ ] Analytics dashboard or reporting system
- [ ] Compliance and ethical guidelines document
- [ ] User manual for configuring preferences
- [ ] Testing suite for job board integrations

---

## Success Metrics

### Phase 1
- Master CV successfully generated from YAML
- ATS compatibility verified
- Easy manual updates to YAML

### Phase 2
- < 2 minute turnaround time from URL to documents
- 90%+ successful job posting scrapes
- Generated CVs properly tailored (human review confirms)
- Cover letters require minimal editing

### Phase 3
- Discovery of 50+ relevant jobs per week
- < 5% false positives in auto-apply queue
- 80%+ successful automated applications
- 2x increase in application volume without quality decrease
- Positive feedback loop improving match accuracy

---

## Future Enhancements (Post-Phase 3)

- Interview scheduling automation
- Automated follow-up emails
- Salary negotiation assistant
- Portfolio/LinkedIn profile updates based on applications
- Analytics: A/B testing different CV formats
- Integration with calendar for interview management
- Network effect: track referrals and connections
- Multi-language support for international applications

---

## Notes & Considerations

### Privacy & Data
- All personal data stays local or in controlled environments
- No third-party storage of sensitive information without encryption
- Clear data ownership and portability

### Customization Philosophy
- System should enhance, not replace, human judgment
- Maintain authenticity in all communications
- Quality applications over spray-and-pray approach

### Technical Flexibility
- Modular design allows phases to work independently
- Easy to swap LLM providers or add multiple
- Template system allows for different CV styles
- Extensible for future job boards or requirements