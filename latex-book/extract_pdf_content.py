#!/usr/bin/env python3
"""
PDF Content Extractor for Genetic Algorithm Course Materials
Extracts text content from course PDFs to enhance LaTeX chapters
"""

import os
import sys
from pathlib import Path

# Try different PDF libraries
pdf_library = None
try:
    import pikepdf
    pdf_library = "pikepdf"
    print("Using pikepdf library")
except ImportError:
    try:
        import PyPDF2
        pdf_library = "PyPDF2"
        print("Using PyPDF2 library")
    except ImportError:
        try:
            import fitz  # PyMuPDF
            pdf_library = "fitz"
            print("Using PyMuPDF library")
        except ImportError:
            print("No PDF library found. Please install: pip install pikepdf")
            sys.exit(1)

def extract_text_pikepdf(pdf_path):
    """Extract text using pikepdf"""
    try:
        with pikepdf.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                if '/Contents' in page:
                    # Basic text extraction - pikepdf doesn't have direct text extraction
                    # This is a limitation, we'd need additional tools
                    text += f"Page content from {pdf_path.name}\n"
            return text
    except Exception as e:
        return f"Error extracting from {pdf_path}: {e}"

def extract_text_with_subprocess(pdf_path):
    """Try using system tools like pdftotext"""
    import subprocess
    try:
        # Try pdftotext first
        result = subprocess.run(['pdftotext', str(pdf_path), '-'], 
                              capture_output=True, text=True, check=True)
        return result.stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        try:
            # Try pdfgrep or other tools
            result = subprocess.run(['strings', str(pdf_path)], 
                                  capture_output=True, text=True, check=True)
            return result.stdout
        except:
            return None

def main():
    # Find all PDF files in the parent directory
    base_dir = Path(__file__).parent.parent
    pdf_files = []
    
    for pdf_file in base_dir.glob("*.pdf"):
        if "Course Material" in pdf_file.name:
            pdf_files.append(pdf_file)
    
    print(f"Found {len(pdf_files)} course material PDFs:")
    for pdf in pdf_files:
        print(f"  - {pdf.name}")
    
    # Create output directory
    output_dir = Path(__file__).parent / "extracted_content"
    output_dir.mkdir(exist_ok=True)
    
    # Extract content from each PDF
    for pdf_path in pdf_files:
        print(f"\nProcessing: {pdf_path.name}")
        
        # Try subprocess method first (more reliable)
        text_content = extract_text_with_subprocess(pdf_path)
        
        if not text_content:
            print(f"  Subprocess extraction failed, trying {pdf_library}")
            if pdf_library == "pikepdf":
                text_content = extract_text_pikepdf(pdf_path)
        
        if text_content:
            # Save extracted content
            output_file = output_dir / f"{pdf_path.stem}_extracted.txt"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"Extracted from: {pdf_path.name}\n")
                f.write("=" * 50 + "\n\n")
                f.write(text_content)
            
            print(f"  ✓ Extracted to: {output_file.name}")
            print(f"  Content length: {len(text_content)} characters")
        else:
            print(f"  ✗ Failed to extract content")

if __name__ == "__main__":
    main()