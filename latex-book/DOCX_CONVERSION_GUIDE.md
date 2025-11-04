# DOCX Conversion Guide for LaTeX Project

This guide explains how to accurately convert your LaTeX document to Microsoft Word (DOCX) format.

## Prerequisites

- **Pandoc** (version 3.1.3 or later) - Universal document converter
- **LaTeX distribution** - For compiling the source document
- **Python** (optional) - For advanced preprocessing

## Conversion Methods (Ranked by Accuracy)

### Method 1: Enhanced Pandoc Conversion (Recommended)

This method provides the best balance of accuracy and formatting preservation:

```bash
# Build the project first
make all

# Convert with enhanced formatting
make docx-enhanced
```

**Manual command:**
```bash
pandoc main.tex -o output/main-enhanced.docx \
    --bibliography=references.bib \
    --citeproc \
    --toc \
    --number-sections \
    --standalone \
    --from=latex \
    --to=docx \
    --extract-media=output/media \
    --wrap=preserve \
    --columns=80
```

**Features preserved:**
- ✅ Table of contents
- ✅ Section numbering
- ✅ Bibliography and citations
- ✅ Basic formatting (bold, italic, etc.)
- ✅ Equations (converted to Word equations)
- ✅ Images and figures
- ✅ Tables
- ✅ Code blocks (basic formatting)

### Method 2: Basic Pandoc Conversion

Simpler conversion with fewer formatting options:

```bash
make docx
```

**Manual command:**
```bash
pandoc main.tex -o output/main.docx \
    --bibliography=references.bib \
    --citeproc \
    --toc \
    --number-sections \
    --standalone
```

### Method 3: PDF-to-DOCX Conversion (Alternative)

If LaTeX-to-DOCX conversion has issues:

```bash
make docx-from-pdf
```

**Manual command:**
```bash
pandoc output/main.pdf -o output/main-from-pdf.docx
```

**Note:** This method may lose some formatting but can handle complex LaTeX elements better.

## Improving Conversion Accuracy

### 1. LaTeX Code Optimization

Before conversion, ensure your LaTeX code is Pandoc-friendly:

**Good practices:**
```latex
% Use standard LaTeX environments
\begin{itemize}
\item First item
\item Second item
\end{itemize}

% Standard figure references
\begin{figure}[h]
\centering
\includegraphics[width=0.8\textwidth]{figure.png}
\caption{Figure caption}
\label{fig:example}
\end{figure}

% Standard table format
\begin{table}[h]
\centering
\begin{tabular}{lcc}
\toprule
Header 1 & Header 2 & Header 3 \\
\midrule
Data 1   & Data 2   & Data 3   \\
\bottomrule
\end{tabular}
\caption{Table caption}
\end{table}
```

**Avoid or minimize:**
```latex
% Complex TikZ diagrams (convert to images first)
% Custom commands with complex definitions
% Heavy use of \vspace, \hspace
% Complex page layouts
```

### 2. Preprocessing for Better Results

Create a preprocessing script to handle complex elements:

```python
# preprocess_latex.py
import re

def preprocess_latex(content):
    # Convert TikZ to image placeholders
    content = re.sub(
        r'\\begin{tikzpicture}.*?\\end{tikzpicture}',
        r'\\includegraphics{tikz_diagram.png}',
        content,
        flags=re.DOTALL
    )
    
    # Simplify complex math
    content = re.sub(
        r'\\begin{align\*?}(.*?)\\end{align\*?}',
        r'\\begin{equation}\1\\end{equation}',
        content,
        flags=re.DOTALL
    )
    
    return content
```

### 3. Post-Processing in Word

After conversion, manually adjust in Microsoft Word:

1. **Formatting Issues:**
   - Check heading styles
   - Verify table formatting
   - Adjust figure positioning

2. **Mathematical Equations:**
   - Convert to Word's equation editor if needed
   - Check equation numbering

3. **References:**
   - Verify bibliography formatting
   - Check cross-references

## Troubleshooting Common Issues

### Problem: Images Not Displaying
**Solution:**
```bash
# Copy images to output directory
cp -r figures/ output/
cp -r chapters/figures/ output/

# Use --extract-media option
pandoc main.tex -o output/main.docx --extract-media=output/media
```

### Problem: Bibliography Issues
**Solution:**
```bash
# Ensure bibliography file is accessible
cp references.bib output/
cd output && pandoc ../main.tex -o main.docx --bibliography=references.bib --citeproc
```

### Problem: Complex Tables Not Converting
**Solution:**
1. Simplify table structure in LaTeX
2. Use basic `tabular` environments
3. Convert complex tables to images if necessary

### Problem: TikZ Diagrams Missing
**Solution:**
1. Compile TikZ to standalone images first:
```bash
# Create standalone TikZ files and compile to PNG
pdflatex tikz_diagram.tex
convert tikz_diagram.pdf tikz_diagram.png
```

## Quality Checklist

Before finalizing your DOCX:

- [ ] Table of contents is properly formatted
- [ ] All figures are present and positioned correctly
- [ ] Tables maintain their structure
- [ ] Mathematical equations are readable
- [ ] Bibliography is complete and formatted
- [ ] Cross-references work correctly
- [ ] Code blocks are properly formatted
- [ ] Heading styles are consistent
- [ ] Page breaks are appropriate

## Advanced Options

### Custom Reference Document

Create a custom Word template for better styling:

```bash
# Extract default reference document
pandoc --print-default-data-file reference.docx > custom-reference.docx

# Use custom template
pandoc main.tex -o output/main.docx --reference-doc=custom-reference.docx
```

### Batch Processing

For multiple documents:

```bash
#!/bin/bash
for tex_file in *.tex; do
    basename=$(basename "$tex_file" .tex)
    pandoc "$tex_file" -o "output/${basename}.docx" \
        --bibliography=references.bib \
        --citeproc \
        --toc \
        --number-sections \
        --standalone
done
```

## Summary

The most accurate DOCX conversion from your LaTeX project is achieved using:

```bash
make docx-enhanced
```

This preserves most formatting elements while ensuring compatibility with Microsoft Word. For best results, review and manually adjust the converted document in Word to handle any complex elements that didn't convert perfectly.