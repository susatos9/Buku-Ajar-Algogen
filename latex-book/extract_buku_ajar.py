#!/usr/bin/env python3
"""
Extract content from Buku-Ajar-docs.pdf including text and images
"""

import PyPDF2
import pdfplumber
from PIL import Image
import io
import os
import sys

def extract_pdf_content(pdf_path, output_dir="buku_ajar_extracted"):
    """Extract text and images from PDF"""
    
    # Create output directories
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(os.path.join(output_dir, "images"), exist_ok=True)
    
    text_output = []
    image_count = 0
    
    print(f"Extracting content from: {pdf_path}")
    
    # Extract text using pdfplumber
    with pdfplumber.open(pdf_path) as pdf:
        print(f"Total pages: {len(pdf.pages)}")
        
        for page_num, page in enumerate(pdf.pages, 1):
            print(f"Processing page {page_num}...")
            
            # Extract text
            text = page.extract_text()
            if text:
                text_output.append(f"\n{'='*80}\n")
                text_output.append(f"PAGE {page_num}\n")
                text_output.append(f"{'='*80}\n\n")
                text_output.append(text)
                text_output.append("\n")
            
            # Extract images
            if hasattr(page, 'images'):
                for img_idx, img in enumerate(page.images):
                    try:
                        image_count += 1
                        # Note: This is a simplified approach
                        # Some PDFs may require different extraction methods
                        print(f"  Found image on page {page_num}")
                    except Exception as e:
                        print(f"  Error extracting image: {e}")
    
    # Also try PyPDF2 for images
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                
                if '/XObject' in page['/Resources']:
                    xObject = page['/Resources']['/XObject'].get_object()
                    
                    for obj in xObject:
                        if xObject[obj]['/Subtype'] == '/Image':
                            try:
                                image_count += 1
                                size = (xObject[obj]['/Width'], xObject[obj]['/Height'])
                                data = xObject[obj].get_data()
                                
                                if xObject[obj]['/ColorSpace'] == '/DeviceRGB':
                                    mode = "RGB"
                                else:
                                    mode = "P"
                                
                                img_filename = f"page_{page_num + 1}_img_{obj[1:]}.png"
                                img_path = os.path.join(output_dir, "images", img_filename)
                                
                                img = Image.frombytes(mode, size, data)
                                img.save(img_path)
                                print(f"  Saved image: {img_filename}")
                                
                            except Exception as e:
                                print(f"  Error saving image: {e}")
    except Exception as e:
        print(f"Error with PyPDF2 extraction: {e}")
    
    # Save text content
    text_file = os.path.join(output_dir, "buku_ajar_content.txt")
    with open(text_file, 'w', encoding='utf-8') as f:
        f.write(''.join(text_output))
    
    print(f"\nExtraction complete!")
    print(f"Text saved to: {text_file}")
    print(f"Images extracted: {image_count}")
    print(f"Images directory: {os.path.join(output_dir, 'images')}")
    
    return text_file, image_count

if __name__ == "__main__":
    pdf_path = "../Buku-Ajar-docs.pdf"
    
    if not os.path.exists(pdf_path):
        print(f"Error: PDF file not found at {pdf_path}")
        sys.exit(1)
    
    extract_pdf_content(pdf_path)
