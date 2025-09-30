# CV Automation System - Phase 1

A Python-based system for generating professional, ATS-friendly CV documents from structured YAML data.

## Features

- **ATS-Optimized**: Generates CVs compatible with Applicant Tracking Systems
- **YAML-Based**: Store all your professional information in a structured YAML file
- **Professional Formatting**: Clean, readable layout with optimal spacing and standard fonts
- **Comprehensive Sections**: Support for experience, education, skills, certifications, projects, and more
- **Customizable**: Easy to modify templates and section ordering
- **Logging**: Detailed logging for debugging and monitoring
- **Contact Layout**: Each contact detail on separate lines for better ATS parsing

## Project Structure

```
JobSearchAutomation/
├── data/
│   └── example_cv.yaml          # Example template (included in git)
├── output/                      # Generated CVs (gitignored)
├── templates/                   # Optional template files
├── venv/                       # Virtual environment (gitignored)
├── generate_cv.py              # Main CV generation script
├── requirements.txt            # Python dependencies
├── .gitignore                 # Git ignore rules
└── README.md                  # This file
```

## Quick Start

### 1. Quick Setup (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd JobSearchAutomation

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run automated setup
python setup.py
```

### 2. Manual Setup (Alternative)

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy the example template
cp data/example_cv.yaml data/master_cv.yaml

# Edit with your information
nano data/master_cv.yaml  # or use your preferred editor
```

### 3. Generate Your CV

```bash
# Generate CV from your data
python generate_cv.py

# Or specify a different YAML file
python generate_cv.py --yaml-file data/my_cv.yaml
```

### 4. Test Your Setup

```bash
# Test the system with example data
python test_cv.py
```

The generated CV will be saved in the `output/` directory with a timestamp.

## YAML Data Structure

The YAML file should contain the following sections:

### Personal Information
```yaml
personal_info:
  name: "Your Name"
  email: "your.email@example.com"
  phone: "+1 (555) 123-4567"
  location: "City, State"
  linkedin: "linkedin.com/in/yourprofile"
  website: "yourwebsite.com"  # Optional
  github: "github.com/yourusername"  # Optional
```

### Professional Summary
```yaml
summary: |
  Your professional summary here. This should be a brief paragraph
  highlighting your key qualifications and career focus.
```

### Work Experience
```yaml
experience:
  - company: "Company Name"
    role: "Job Title"
    location: "City, State"
    start_date: "2022-01"
    end_date: "Present"
    description: |
      Brief description of your role and responsibilities.
    achievements:
      - "Achievement 1"
      - "Achievement 2"
    technologies: ["Python", "JavaScript", "React"]
```

### Education
```yaml
education:
  - degree: "Bachelor of Science in Computer Science"
    institution: "University Name"
    location: "City, State"
    graduation_date: "2020-05"
    gpa: "3.7"  # Optional
    relevant_coursework: ["Data Structures", "Algorithms"]
```

### Skills
```yaml
skills:
  programming_languages:
    - "Python"
    - "JavaScript"
    - "Java"
  frameworks_libraries:
    - "Django"
    - "React"
    - "Node.js"
```

### Certifications
```yaml
certifications:
  - name: "AWS Certified Solutions Architect"
    issuer: "Amazon Web Services"
    date: "2023-03"
    credential_id: "AWS-SAA-123456"  # Optional
```

### Projects (Optional)
```yaml
projects:
  - name: "Project Name"
    description: "Brief project description"
    technologies: ["Python", "Django", "PostgreSQL"]
    url: "github.com/username/project"  # Optional
    date: "2023"
```

### Configuration
```yaml
cv_config:
  font_family: "Arial"  # ATS-friendly fonts: Arial, Calibri, Georgia
  font_size: 11
  section_order:
    - "personal_info"
    - "summary"
    - "experience"
    - "education"
    - "skills"
    - "certifications"
  filename_prefix: "Your_Name_CV"
  include_timestamp: true
```

## Command Line Options

```bash
python generate_cv.py [options]

Options:
  --yaml-file PATH    Path to YAML file (default: data/master_cv.yaml)
  --output-dir PATH   Output directory (default: output)
  -h, --help         Show help message
```

## ATS Compatibility Features

- **Standard Fonts**: Uses Arial, Calibri, or Georgia fonts
- **Simple Formatting**: No tables, text boxes, or complex layouts
- **Clear Headers**: Standard section headers with proper spacing
- **Bullet Points**: Simple bullet points without custom symbols
- **Proper Margins**: 1-inch margins on all sides
- **No Graphics**: No embedded images or complex formatting
- **Contact Parsing**: Each contact detail on separate lines for ATS compatibility

## Customization

### Section Ordering
Modify the `section_order` in your YAML file to change the order of sections:

```yaml
cv_config:
  section_order:
    - "personal_info"
    - "summary"
    - "experience"
    - "skills"  # Move skills before education
    - "education"
    - "certifications"
```

### Hidden Sections
Hide sections you don't want to include:

```yaml
cv_config:
  hidden_sections:
    - "projects"
    - "languages"
```

### Font Customization
```yaml
cv_config:
  font_family: "Calibri"  # or "Georgia"
  font_size: 12
```

## Logging

The script generates detailed logs in `cv_generation.log` and console output:

- **INFO**: General progress information
- **DEBUG**: Detailed processing steps
- **WARNING**: Non-critical issues
- **ERROR**: Critical errors that prevent generation

## Troubleshooting

### Common Issues

1. **YAML file not found**
   ```
   Error: YAML file not found: data/master_cv.yaml
   ```
   **Solution**: Copy `data/example_cv.yaml` to `data/master_cv.yaml` and update with your information.

2. **Invalid YAML syntax**
   ```
   Error parsing YAML file: while parsing...
   ```
   **Solution**: Check your YAML syntax. Use a YAML validator online.

3. **Missing required fields**
   ```
   Warning: No personal information found in YAML data
   ```
   **Solution**: Ensure your YAML file has the required sections.

### Debug Mode

Enable debug logging by modifying the script:

```python
logging.basicConfig(level=logging.DEBUG, ...)
```

## Development

### Adding New Sections

To add a new section to the CV:

1. Add the section to your YAML file
2. Create a method in the `CVGenerator` class:
   ```python
   def add_new_section(self):
       """Add your new section."""
       if 'new_section' not in self.data:
           return
       # Implementation here
   ```
3. Add the section to the `section_methods` dictionary
4. Update the default `section_order` in the config

### Testing

```bash
# Test with example data
python generate_cv.py --yaml-file data/example_cv.yaml

# Run automated tests to verify CV structure
python test_cv.py

# Check the generated CV in output/ directory
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source. See the LICENSE file for details.

## Future Phases

This is Phase 1 of a larger automation system:

- **Phase 2**: Job-specific CV generation with n8n automation
- **Phase 3**: Automated job search and application

See `REQUIREMENTS.md` for the complete project roadmap.

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Review the logs in `cv_generation.log`
3. Open an issue on GitHub with your YAML file (remove personal information)
4. Include the error message and log output