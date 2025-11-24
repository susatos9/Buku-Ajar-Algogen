#!/usr/bin/env python3
"""
Analyze extracted Buku-Ajar content and organize by chapters
"""

import re
import os

def analyze_content():
    """Parse the extracted content and organize by chapters"""
    
    content_file = "buku_ajar_extracted/buku_ajar_content.txt"
    
    with open(content_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by page markers
    pages = re.split(r'={80}\nPAGE (\d+)\n={80}', content)
    
    # Organize content by chapters
    chapters = {
        'ch01': {'title': 'Pengantar Algoritma Genetika', 'pages': [], 'images': []},
        'ch02': {'title': 'Holland Schema', 'pages': [], 'images': []},
        'ch03': {'title': 'Encoding', 'pages': [], 'images': []},
        'ch04': {'title': 'Selection', 'pages': [], 'images': []},
        'ch05': {'title': 'Crossover', 'pages': [], 'images': []},
        'ch08': {'title': 'Mutation and Update', 'pages': [], 'images': []},
    }
    
    current_chapter = None
    
    # Process pages
    i = 1
    while i < len(pages):
        page_num = int(pages[i])
        page_content = pages[i+1] if i+1 < len(pages) else ""
        
        # Detect chapter transitions
        if '1) Pengantar Algoritma Genetika' in page_content:
            current_chapter = 'ch01'
        elif '2) Holland Schema' in page_content:
            current_chapter = 'ch02'
        elif '3) Encoding' in page_content:
            current_chapter = 'ch03'
        elif '4) Selection' in page_content:
            current_chapter = 'ch04'
        elif '5) Crossover' in page_content or '6) Crossover' in page_content or '7) Crossover' in page_content or '8) Crossover' in page_content:
            current_chapter = 'ch05'
        elif '11) Operator Mutasi' in page_content or '12) Perbaikan Generasi' in page_content or '13) Parameter' in page_content:
            current_chapter = 'ch08'
        
        if current_chapter:
            chapters[current_chapter]['pages'].append({
                'num': page_num,
                'content': page_content
            })
        
        i += 2
    
    # Print summary
    print("Chapter Analysis:")
    print("=" * 80)
    for ch_key, ch_data in chapters.items():
        if ch_data['pages']:
            page_nums = [p['num'] for p in ch_data['pages']]
            print(f"\n{ch_key.upper()}: {ch_data['title']}")
            print(f"  Pages: {min(page_nums)} - {max(page_nums)}")
            print(f"  Total pages: {len(page_nums)}")
            print(f"  Page numbers: {page_nums}")
    
    # List images
    print("\n\nImages Extracted:")
    print("=" * 80)
    images_dir = "buku_ajar_extracted/images"
    if os.path.exists(images_dir):
        images = sorted(os.listdir(images_dir))
        for img in images:
            if img.endswith('.png'):
                # Extract page number from filename
                match = re.search(r'page_(\d+)', img)
                if match:
                    page_num = int(match.group(1))
                    # Assign to chapter
                    for ch_key, ch_data in chapters.items():
                        page_nums = [p['num'] for p in ch_data['pages']]
                        if page_nums and min(page_nums) <= page_num <= max(page_nums):
                            chapters[ch_key]['images'].append(img)
                            print(f"  {img} -> {ch_key} ({ch_data['title']})")
                            break
    
    return chapters

if __name__ == "__main__":
    chapters = analyze_content()
    
    # Save chapter mapping
    with open("buku_ajar_extracted/chapter_mapping.txt", 'w', encoding='utf-8') as f:
        f.write("Chapter Mapping Summary\n")
        f.write("=" * 80 + "\n\n")
        
        for ch_key, ch_data in chapters.items():
            if ch_data['pages']:
                f.write(f"{ch_key.upper()}: {ch_data['title']}\n")
                f.write(f"  Pages: {[p['num'] for p in ch_data['pages']]}\n")
                f.write(f"  Images: {ch_data['images']}\n")
                f.write("\n")
