#!/usr/bin/env python3
"""
Setup script for CV Automation System - Phase 1
This script helps users get started quickly by setting up their personal CV data.
"""

import os
import shutil
import sys
from pathlib import Path

def main():
    """Setup script to initialize user's CV data."""
    print("CV Automation System - Phase 1 Setup")
    print("=" * 40)
    
    # Check if virtual environment exists
    if not os.path.exists("venv"):
        print("❌ Virtual environment not found!")
        print("Please run: python3 -m venv venv")
        sys.exit(1)
    
    # Check if requirements are installed
    try:
        import yaml
        from docx import Document
        print("✅ Dependencies are installed")
    except ImportError as e:
        print(f"❌ Missing dependencies: {e}")
        print("Please run: pip install -r requirements.txt")
        sys.exit(1)
    
    # Check if example file exists
    example_file = Path("data/example_cv.yaml")
    if not example_file.exists():
        print("❌ Example CV file not found!")
        print("Please ensure data/example_cv.yaml exists")
        sys.exit(1)
    
    # Check if user already has a master CV file
    master_file = Path("data/master_cv.yaml")
    if master_file.exists():
        print("✅ Master CV file already exists")
        response = input("Do you want to overwrite it? (y/N): ").lower().strip()
        if response != 'y':
            print("Setup cancelled. Your existing master_cv.yaml is preserved.")
            return
    
    # Copy example to master
    try:
        shutil.copy2(example_file, master_file)
        print("✅ Created data/master_cv.yaml from example template")
    except Exception as e:
        print(f"❌ Error copying example file: {e}")
        sys.exit(1)
    
    # Create output directory
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    print("✅ Created output directory")
    
    print("\n🎉 Setup complete!")
    print("\nNext steps:")
    print("1. Edit data/master_cv.yaml with your information")
    print("2. Run: python generate_cv.py")
    print("3. Check the output/ directory for your generated CV")
    print("\nFor help, see README.md")

if __name__ == "__main__":
    main()
