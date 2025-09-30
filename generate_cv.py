#!/usr/bin/env python3
"""
CV Generation Script - Phase 1
Generates ATS-friendly CV documents from YAML data using python-docx.

This script reads personal and professional information from a YAML file
and generates a professional CV in DOCX format optimized for ATS systems.
"""

import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

import yaml
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.shared import OxmlElement, qn

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('cv_generation.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class CVGenerator:
    """
    Generates professional CV documents from YAML data.
    Optimized for ATS (Applicant Tracking System) compatibility.
    """
    
    def __init__(self, yaml_file: str = "data/master_cv.yaml"):
        """
        Initialize CV generator with YAML data file.
        
        Args:
            yaml_file: Path to YAML file containing CV data
        """
        self.yaml_file = yaml_file
        self.data = None
        self.doc = None
        self.config = {}
        
        logger.info(f"Initializing CV generator with file: {yaml_file}")
    
    def validate_yaml_structure(self) -> bool:
        """
        Validate the structure of the loaded YAML data.
        
        Returns:
            bool: True if structure is valid, False otherwise
        """
        errors = []
        
        # Check required sections
        required_sections = ['personal_info']
        for section in required_sections:
            if section not in self.data:
                errors.append(f"Missing required section: '{section}'")
        
        # Validate personal_info structure
        if 'personal_info' in self.data:
            personal = self.data['personal_info']
            if not isinstance(personal, dict):
                errors.append("'personal_info' must be a dictionary")
            else:
                required_fields = ['name', 'email']
                for field in required_fields:
                    if field not in personal or not personal[field]:
                        errors.append(f"Missing required field in personal_info: '{field}'")
        
        # Validate list sections (experience, education, projects, languages, certifications)
        list_sections = ['experience', 'education', 'projects', 'languages', 'certifications']
        for section in list_sections:
            if section in self.data:
                if self.data[section] is None:
                    # Empty section with just comments - this is OK
                    continue
                elif not isinstance(self.data[section], list):
                    errors.append(f"'{section}' must be a list, got {type(self.data[section]).__name__}")
                else:
                    # Check each entry is a dictionary
                    for i, item in enumerate(self.data[section]):
                        if not isinstance(item, dict):
                            errors.append(f"'{section}' entry {i+1} must be a dictionary, got {type(item).__name__}: {item}")
        
        # Validate skills structure
        if 'skills' in self.data:
            skills = self.data['skills']
            if not isinstance(skills, dict):
                errors.append("'skills' must be a dictionary with skill categories")
            else:
                for category, skill_list in skills.items():
                    if not isinstance(skill_list, list):
                        errors.append(f"Skills category '{category}' must be a list, got {type(skill_list).__name__}")
                    else:
                        for i, skill in enumerate(skill_list):
                            if not isinstance(skill, str):
                                errors.append(f"Skill {i+1} in category '{category}' must be a string, got {type(skill).__name__}: {skill}")
        
        # Validate additional_sections structure
        if 'additional_sections' in self.data:
            additional = self.data['additional_sections']
            if not isinstance(additional, dict):
                errors.append("'additional_sections' must be a dictionary")
            else:
                for section_name, section_data in additional.items():
                    if section_name in ['volunteer', 'publications']:
                        if not isinstance(section_data, list):
                            errors.append(f"'{section_name}' in additional_sections must be a list, got {type(section_data).__name__}")
                            if isinstance(section_data, str) and section_data.lower() == 'pass':
                                errors.append(f"'{section_name}' contains 'pass' - use empty list [] instead")
                        else:
                            for i, item in enumerate(section_data):
                                if not isinstance(item, dict):
                                    errors.append(f"'{section_name}' entry {i+1} must be a dictionary, got {type(item).__name__}: {item}")
        
        # Report errors
        if errors:
            logger.error("YAML structure validation failed:")
            for error in errors:
                logger.error(f"  - {error}")
            logger.error("\\nPlease fix these issues in your YAML file and try again.")
            logger.error("\\nFor help with YAML structure, see data/example_cv.yaml")
            return False
        
        return True
    
    def load_data(self) -> bool:
        """
        Load and validate YAML data.
        
        Returns:
            bool: True if data loaded successfully, False otherwise
        """
        try:
            if not os.path.exists(self.yaml_file):
                logger.error(f"YAML file not found: {self.yaml_file}")
                logger.info("Please copy data/example_cv.yaml to data/master_cv.yaml and update with your information")
                return False
            
            with open(self.yaml_file, 'r', encoding='utf-8') as file:
                self.data = yaml.safe_load(file)
            
            if not self.data:
                logger.error("YAML file is empty or invalid")
                return False
            
            # Extract configuration
            self.config = self.data.get('cv_config', {})
            
            # Validate YAML structure
            if not self.validate_yaml_structure():
                return False
            
            logger.info("YAML data loaded successfully")
            return True
            
        except yaml.YAMLError as e:
            logger.error(f"Error parsing YAML file: {e}")
            logger.error("Please check your YAML syntax. Common issues:")
            logger.error("  - Incorrect indentation (use spaces, not tabs)")
            logger.error("  - Missing colons after keys")
            logger.error("  - Unquoted strings with special characters")
            logger.error("  - Using 'pass' instead of empty lists []")
            return False
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            return False
    
    def create_document(self):
        """Create a new Word document with ATS-friendly formatting."""
        self.doc = Document()
        
        # Set document margins (1 inch on all sides for ATS compatibility)
        sections = self.doc.sections
        for section in sections:
            section.top_margin = Inches(1)
            section.bottom_margin = Inches(1)
            section.left_margin = Inches(1)
            section.right_margin = Inches(1)
        
        logger.debug("Created new document with ATS-friendly margins")
    
    def add_personal_info(self):
        """Add personal information section to the document."""
        if 'personal_info' not in self.data:
            logger.warning("No personal information found in YAML data")
            return
        
        personal = self.data['personal_info']
        
        # Add name as main heading
        name_para = self.doc.add_heading(personal.get('name', ''), level=1)
        name_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # Add contact information - each on separate line for better ATS parsing
        if personal.get('email'):
            email_para = self.doc.add_paragraph(personal['email'])
            email_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        if personal.get('phone'):
            phone_para = self.doc.add_paragraph(personal['phone'])
            phone_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        if personal.get('location'):
            location_para = self.doc.add_paragraph(personal['location'])
            location_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        if personal.get('linkedin'):
            linkedin_para = self.doc.add_paragraph(f"LinkedIn: {personal['linkedin']}")
            linkedin_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        if personal.get('website'):
            website_para = self.doc.add_paragraph(f"Website: {personal['website']}")
            website_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        if personal.get('github'):
            github_para = self.doc.add_paragraph(f"GitHub: {personal['github']}")
            github_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        logger.info(f"Added personal information for: {personal.get('name', 'Unknown')}")
    
    def add_summary(self):
        """Add professional summary section."""
        if 'summary' not in self.data:
            logger.debug("No summary found in YAML data")
            return
        
        summary_text = self.data['summary'].strip()
        if not summary_text:
            return
        
        self.doc.add_heading('Professional Summary', level=2)
        summary_para = self.doc.add_paragraph(summary_text)
        # Add small spacing after summary
        self.doc.add_paragraph()
        
        logger.info("Added professional summary section")
    
    def add_experience(self):
        """Add work experience section."""
        if 'experience' not in self.data:
            logger.debug("No experience found in YAML data")
            return
        
        experiences = self.data['experience']
        if not experiences:
            return
        
        self.doc.add_heading('Professional Experience', level=2)
        
        try:
            for i, exp in enumerate(experiences):
                # Check if exp is a dictionary
                if not isinstance(exp, dict):
                    logger.error(f"Experience entry {i+1} must be a dictionary, got {type(exp).__name__}: {exp}")
                    logger.error("Expected format: - company: 'Company Name'\\n  role: 'Job Title'\\n  start_date: 'YYYY-MM'\\n  end_date: 'YYYY-MM' or 'Present'")
                    continue
                
                # Job title and company
                title_company = f"{exp.get('role', '')} - {exp.get('company', '')}"
                if exp.get('location'):
                    title_company += f" ({exp['location']})"
                
                self.doc.add_heading(title_company, level=3)
                
                # Date range
                start_date = exp.get('start_date', '')
                end_date = exp.get('end_date', 'Present')
                date_range = f"{start_date} - {end_date}"
                
                date_para = self.doc.add_paragraph(date_range)
                date_para.paragraph_format.italic = True
                
                # Description
                if exp.get('description'):
                    desc_para = self.doc.add_paragraph(exp['description'])
                
                # Achievements
                if exp.get('achievements'):
                    if not isinstance(exp['achievements'], list):
                        logger.error(f"Experience {i+1}: 'achievements' must be a list, got {type(exp['achievements']).__name__}")
                        logger.error("Expected format: achievements: ['Achievement 1', 'Achievement 2']")
                    else:
                        for achievement in exp['achievements']:
                            if not isinstance(achievement, str):
                                logger.error(f"Experience {i+1}: Each achievement must be a string, got {type(achievement).__name__}: {achievement}")
                                continue
                            achievement_para = self.doc.add_paragraph(achievement, style='List Bullet')
                
                # Technologies
                if exp.get('technologies'):
                    if not isinstance(exp['technologies'], list):
                        logger.error(f"Experience {i+1}: 'technologies' must be a list, got {type(exp['technologies']).__name__}")
                        logger.error("Expected format: technologies: ['Technology 1', 'Technology 2']")
                    else:
                        tech_text = f"Technologies: {', '.join(exp['technologies'])}"
                        tech_para = self.doc.add_paragraph(tech_text)
                        tech_para.paragraph_format.italic = True
                
                # Add spacing between jobs
                self.doc.add_paragraph()
        except Exception as e:
            logger.error(f"Error processing experience section: {e}")
            logger.error("Make sure experience entries are properly formatted as dictionaries")
            return
        
        logger.info(f"Added {len(experiences)} work experience entries")
    
    def add_education(self):
        """Add education section."""
        if 'education' not in self.data:
            logger.debug("No education found in YAML data")
            return
        
        education_list = self.data['education']
        if not education_list:
            return
        
        self.doc.add_heading('Education', level=2)
        
        try:
            for i, edu in enumerate(education_list):
                # Check if edu is a dictionary
                if not isinstance(edu, dict):
                    logger.error(f"Education entry {i+1} must be a dictionary, got {type(edu).__name__}: {edu}")
                    logger.error("Expected format: - degree: 'Degree Name'\\n  institution: 'Institution Name'\\n  graduation_date: 'YYYY-MM'")
                    continue
                
                # Degree and institution
                degree_inst = f"{edu.get('degree', '')} - {edu.get('institution', '')}"
                if edu.get('location'):
                    degree_inst += f" ({edu['location']})"
                
                self.doc.add_heading(degree_inst, level=3)
                
                # Graduation date
                grad_date = edu.get('graduation_date', '')
                if grad_date:
                    date_para = self.doc.add_paragraph(f"Graduated: {grad_date}")
                    date_para.paragraph_format.italic = True
                
                # GPA (if provided)
                if edu.get('gpa'):
                    gpa_para = self.doc.add_paragraph(f"GPA: {edu['gpa']}")
                
                # Honors (if provided)
                if edu.get('honors'):
                    honors_para = self.doc.add_paragraph(f"Honors: {edu['honors']}")
                
                # Relevant coursework
                if edu.get('relevant_coursework'):
                    if not isinstance(edu['relevant_coursework'], list):
                        logger.error(f"Education {i+1}: 'relevant_coursework' must be a list, got {type(edu['relevant_coursework']).__name__}")
                        logger.error("Expected format: relevant_coursework: ['Course 1', 'Course 2']")
                    else:
                        coursework_text = f"Relevant Coursework: {', '.join(edu['relevant_coursework'])}"
                        coursework_para = self.doc.add_paragraph(coursework_text)
                
                self.doc.add_paragraph()
        except Exception as e:
            logger.error(f"Error processing education section: {e}")
            logger.error("Make sure education entries are properly formatted as dictionaries")
            return
        
        logger.info(f"Added {len(education_list)} education entries")
    
    def add_skills(self):
        """Add skills section."""
        if 'skills' not in self.data:
            logger.debug("No skills found in YAML data")
            return
        
        skills = self.data['skills']
        if not skills:
            return
        
        self.doc.add_heading('Skills', level=2)
        
        for category, skill_list in skills.items():
            if skill_list:
                # Format category name (replace underscores with spaces, title case)
                category_name = category.replace('_', ' ').title()
                self.doc.add_heading(category_name, level=3)
                
                # Add skills as comma-separated list
                skills_text = ', '.join(skill_list)
                skills_para = self.doc.add_paragraph(skills_text)
        
        logger.info("Added skills section")
    
    def add_certifications(self):
        """Add certifications section."""
        if 'certifications' not in self.data:
            logger.debug("No certifications found in YAML data")
            return
        
        certs = self.data['certifications']
        if not certs or certs is None:
            return
        
        self.doc.add_heading('Certifications', level=2)
        
        try:
            for i, cert in enumerate(certs):
                # Check if cert is a dictionary
                if not isinstance(cert, dict):
                    logger.error(f"Certification entry {i+1} must be a dictionary, got {type(cert).__name__}: {cert}")
                    logger.error("Expected format: - name: 'Certification Name'\\n  issuer: 'Issuing Organization'\\n  date: 'YYYY-MM'")
                    continue
                
                cert_text = f"{cert.get('name', '')} - {cert.get('issuer', '')}"
                if cert.get('date'):
                    cert_text += f" ({cert['date']})"
                
                cert_para = self.doc.add_paragraph(cert_text)
                
                if cert.get('credential_id'):
                    id_para = self.doc.add_paragraph(f"Credential ID: {cert['credential_id']}")
                    id_para.paragraph_format.italic = True
        except Exception as e:
            logger.error(f"Error processing certifications section: {e}")
            logger.error("Make sure certification entries are properly formatted as dictionaries")
            return
        
        logger.info(f"Added {len(certs)} certifications")
    
    def add_projects(self):
        """Add projects section."""
        if 'projects' not in self.data:
            logger.debug("No projects found in YAML data")
            return
        
        projects = self.data['projects']
        if not projects:
            return
        
        self.doc.add_heading('Projects', level=2)
        
        try:
            for i, project in enumerate(projects):
                # Check if project is a dictionary
                if not isinstance(project, dict):
                    logger.error(f"Project entry {i+1} must be a dictionary, got {type(project).__name__}: {project}")
                    logger.error("Expected format: - name: 'Project Name'\\n  description: 'Description'\\n  technologies: ['Tech 1', 'Tech 2']")
                    continue
                
                # Project name
                self.doc.add_heading(project.get('name', ''), level=3)
                
                # Description
                if project.get('description'):
                    desc_para = self.doc.add_paragraph(project['description'])
                
                # Technologies
                if project.get('technologies'):
                    if not isinstance(project['technologies'], list):
                        logger.error(f"Project {i+1}: 'technologies' must be a list, got {type(project['technologies']).__name__}")
                        logger.error("Expected format: technologies: ['Technology 1', 'Technology 2']")
                    else:
                        tech_text = f"Technologies: {', '.join(project['technologies'])}"
                        tech_para = self.doc.add_paragraph(tech_text)
                        tech_para.paragraph_format.italic = True
                
                # URL (if provided)
                if project.get('url'):
                    url_para = self.doc.add_paragraph(f"URL: {project['url']}")
                
                # Date (if provided)
                if project.get('date'):
                    date_para = self.doc.add_paragraph(f"Date: {project['date']}")
                
                self.doc.add_paragraph()
        except Exception as e:
            logger.error(f"Error processing projects section: {e}")
            logger.error("Make sure project entries are properly formatted as dictionaries")
            return
        
        logger.info(f"Added {len(projects)} projects")
    
    def add_languages(self):
        """Add languages section."""
        if 'languages' not in self.data:
            logger.debug("No languages found in YAML data")
            return
        
        languages = self.data['languages']
        if not languages:
            return
        
        self.doc.add_heading('Languages', level=2)
        
        try:
            for lang in languages:
                # Check if lang is a dictionary
                if not isinstance(lang, dict):
                    logger.error(f"Language entry must be a dictionary, got {type(lang).__name__}: {lang}")
                    logger.error("Expected format: - language: 'Language Name'\\n  proficiency: 'Proficiency Level'")
                    continue
                
                lang_text = f"{lang.get('language', '')} - {lang.get('proficiency', '')}"
                lang_para = self.doc.add_paragraph(lang_text)
        except Exception as e:
            logger.error(f"Error processing languages section: {e}")
            logger.error("Make sure language entries are properly formatted as dictionaries")
            return
        
        logger.info(f"Added {len(languages)} languages")
    
    def add_additional_sections(self):
        """Add additional sections like volunteer work, publications, etc."""
        if 'additional_sections' not in self.data:
            logger.debug("No additional sections found in YAML data")
            return
        
        additional = self.data['additional_sections']
        
        # Volunteer work
        if 'volunteer' in additional and additional['volunteer']:
            self.doc.add_heading('Volunteer Experience', level=2)
            try:
                for vol in additional['volunteer']:
                    # Check if vol is a dictionary
                    if not isinstance(vol, dict):
                        logger.error(f"Volunteer entry must be a dictionary, got {type(vol).__name__}: {vol}")
                        logger.error("Expected format: - role: 'Role Name'\\n  organization: 'Organization'\\n  duration: 'Duration'")
                        continue
                    
                    vol_text = f"{vol.get('role', '')} - {vol.get('organization', '')}"
                    if vol.get('duration'):
                        vol_text += f" ({vol['duration']})"
                    
                    self.doc.add_heading(vol_text, level=3)
                    if vol.get('description'):
                        desc_para = self.doc.add_paragraph(vol['description'])
                    self.doc.add_paragraph()
            except Exception as e:
                logger.error(f"Error processing volunteer section: {e}")
                logger.error("Make sure volunteer entries are properly formatted as dictionaries")
        
        # Publications
        if 'publications' in additional and additional['publications']:
            self.doc.add_heading('Publications', level=2)
            try:
                for pub in additional['publications']:
                    # Check if pub is a dictionary
                    if not isinstance(pub, dict):
                        logger.error(f"Publication entry must be a dictionary, got {type(pub).__name__}: {pub}")
                        logger.error("Expected format: - title: 'Title'\\n  publication: 'Publication Name'\\n  date: 'Date'")
                        continue
                    
                    pub_text = f"{pub.get('title', '')} - {pub.get('publication', '')}"
                    if pub.get('date'):
                        pub_text += f" ({pub['date']})"
                    
                    self.doc.add_heading(pub_text, level=3)
                    if pub.get('url'):
                        url_para = self.doc.add_paragraph(f"URL: {pub['url']}")
                    self.doc.add_paragraph()
            except Exception as e:
                logger.error(f"Error processing publications section: {e}")
                logger.error("Make sure publication entries are properly formatted as dictionaries")
        
        logger.info("Added additional sections")
    
    def apply_formatting(self):
        """Apply ATS-friendly formatting to the document."""
        if not self.doc:
            return
        
        # Get font settings from config
        font_family = self.config.get('font_family', 'Arial')
        font_size = self.config.get('font_size', 11)
        
        # Apply formatting to all paragraphs
        for paragraph in self.doc.paragraphs:
            for run in paragraph.runs:
                run.font.name = font_family
                run.font.size = Pt(font_size)
            
            # Add proper spacing after headings
            if paragraph.style.name.startswith('Heading'):
                paragraph.paragraph_format.space_after = Pt(6)
            else:
                paragraph.paragraph_format.space_after = Pt(3)
        
        logger.debug(f"Applied formatting: {font_family}, {font_size}pt")
    
    def generate_filename(self) -> str:
        """Generate filename for the CV document."""
        personal = self.data.get('personal_info', {})
        name = personal.get('name', 'CV').replace(' ', '_')
        
        # Get filename prefix from config
        prefix = self.config.get('filename_prefix', name)
        
        # Add timestamp if configured
        if self.config.get('include_timestamp', True):
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{prefix}_{timestamp}.docx"
        else:
            filename = f"{prefix}.docx"
        
        return filename
    
    def save_document(self) -> str:
        """Save the document to the output folder."""
        if not self.doc:
            logger.error("No document to save")
            return ""
        
        # Create output directory if it doesn't exist
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        
        # Generate filename
        filename = self.generate_filename()
        filepath = output_dir / filename
        
        try:
            self.doc.save(str(filepath))
            logger.info(f"CV saved successfully: {filepath}")
            return str(filepath)
        except Exception as e:
            logger.error(f"Error saving document: {e}")
            return ""
    
    def generate_cv(self) -> bool:
        """
        Generate the complete CV document.
        
        Returns:
            bool: True if generation was successful, False otherwise
        """
        try:
            logger.info("Starting CV generation process")
            
            # Load data
            if not self.load_data():
                return False
            
            # Create document
            self.create_document()
            
            # Add sections in order
            section_order = self.config.get('section_order', [
                'personal_info', 'summary', 'experience', 'education', 
                'skills', 'certifications', 'projects', 'languages', 'additional_sections'
            ])
            
            # Map section names to methods
            section_methods = {
                'personal_info': self.add_personal_info,
                'summary': self.add_summary,
                'experience': self.add_experience,
                'education': self.add_education,
                'skills': self.add_skills,
                'certifications': self.add_certifications,
                'projects': self.add_projects,
                'languages': self.add_languages,
                'additional_sections': self.add_additional_sections
            }
            
            # Add sections in configured order
            for section in section_order:
                if section in section_methods and section not in self.config.get('hidden_sections', []):
                    section_methods[section]()
            
            # Apply formatting
            self.apply_formatting()
            
            # Save document
            filepath = self.save_document()
            if not filepath:
                return False
            
            logger.info("CV generation completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error during CV generation: {e}")
            return False


def main():
    """Main function to run the CV generator."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate CV from YAML data')
    parser.add_argument('--yaml-file', default='data/master_cv.yaml',
                       help='Path to YAML file containing CV data')
    parser.add_argument('--output-dir', default='output',
                       help='Output directory for generated CV')
    
    args = parser.parse_args()
    
    # Initialize generator
    generator = CVGenerator(args.yaml_file)
    
    # Generate CV
    success = generator.generate_cv()
    
    if success:
        logger.info("CV generation completed successfully!")
        sys.exit(0)
    else:
        logger.error("CV generation failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
