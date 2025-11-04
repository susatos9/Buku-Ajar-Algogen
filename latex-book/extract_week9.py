#!/usr/bin/env python3
"""
Extract content from Week 9 PDF about Mutation and Update Generation
"""

import fitz  # PyMuPDF
from pathlib import Path

def extract_week9_content():
    pdf_path = Path(__file__).parent.parent / "Course Material Week 9 - GA - Mutation and Update Generation.pdf"
    
    if not pdf_path.exists():
        print(f"PDF not found: {pdf_path}")
        return None
    
    print(f"Processing: {pdf_path.name}")
    
    # Open PDF
    doc = fitz.open(pdf_path)
    
    full_text = []
    
    # Extract text from each page
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()
        
        full_text.append(f"\n{'='*60}\n")
        full_text.append(f"Page {page_num + 1}\n")
        full_text.append(f"{'='*60}\n")
        full_text.append(text)
    
    doc.close()
    
    # Save to file
    output_file = Path(__file__).parent / "week9_extracted.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(''.join(full_text))
    
    print(f"✓ Extracted to: {output_file}")
    print(f"Total pages: {len(doc)}")
    
    return ''.join(full_text)

if __name__ == "__main__":
    content = extract_week9_content()
    if content:
        print(f"\nContent preview (first 500 chars):")
        print(content[:500])
