# Makefile for Genetic Algorithms LaTeX Book

# Main file
MAIN = main
SOURCE = $(MAIN).tex

# Output directory
OUTPUT_DIR = output

# LaTeX compiler
LATEX = pdflatex
BIBTEX = bibtex

# Create output directory if it doesn't exist
$(shell mkdir -p $(OUTPUT_DIR))

# Default target
all: $(OUTPUT_DIR)/$(MAIN).pdf

# Main PDF compilation
$(OUTPUT_DIR)/$(MAIN).pdf: $(SOURCE) references.bib chapters/*.tex
	$(LATEX) -output-directory=$(OUTPUT_DIR) $(SOURCE)
	cp references.bib $(OUTPUT_DIR)/
	cd $(OUTPUT_DIR) && $(BIBTEX) $(MAIN) && cd ..
	$(LATEX) -output-directory=$(OUTPUT_DIR) $(SOURCE)
	$(LATEX) -output-directory=$(OUTPUT_DIR) $(SOURCE)

# Quick compilation (no bibliography)
quick: $(SOURCE) chapters/*.tex
	$(LATEX) -output-directory=$(OUTPUT_DIR) $(SOURCE)

# Clean auxiliary files
clean:
	rm -f $(OUTPUT_DIR)/*.aux $(OUTPUT_DIR)/*.log $(OUTPUT_DIR)/*.toc $(OUTPUT_DIR)/*.lot $(OUTPUT_DIR)/*.lof $(OUTPUT_DIR)/*.bbl $(OUTPUT_DIR)/*.blg $(OUTPUT_DIR)/*.out $(OUTPUT_DIR)/*.fdb_latexmk $(OUTPUT_DIR)/*.fls $(OUTPUT_DIR)/*.synctex.gz

# Clean everything including PDF
clean-all: clean
	rm -f $(OUTPUT_DIR)/*.pdf

# View PDF (Linux)
view: $(OUTPUT_DIR)/$(MAIN).pdf
	xdg-open $(OUTPUT_DIR)/$(MAIN).pdf

# View PDF (macOS)
view-mac: $(OUTPUT_DIR)/$(MAIN).pdf
	open $(OUTPUT_DIR)/$(MAIN).pdf

# DOCX conversion targets
docx: $(OUTPUT_DIR)/$(MAIN).pdf
	pandoc $(SOURCE) -o $(OUTPUT_DIR)/$(MAIN).docx --bibliography=references.bib --citeproc --toc --number-sections --standalone

docx-enhanced: $(OUTPUT_DIR)/$(MAIN).pdf
	pandoc $(SOURCE) -o $(OUTPUT_DIR)/$(MAIN)-enhanced.docx \
		--bibliography=references.bib \
		--citeproc \
		--toc \
		--number-sections \
		--standalone \
		--from=latex \
		--to=docx \
		--extract-media=$(OUTPUT_DIR)/media \
		--wrap=preserve \
		--columns=80

docx-from-pdf: $(OUTPUT_DIR)/$(MAIN).pdf
	pandoc $(OUTPUT_DIR)/$(MAIN).pdf -o $(OUTPUT_DIR)/$(MAIN)-from-pdf.docx

# Help
help:
	@echo "Available targets:"
	@echo "  all            - Build complete PDF with bibliography"
	@echo "  quick          - Quick build without bibliography"
	@echo "  docx           - Convert LaTeX to DOCX (basic)"
	@echo "  docx-enhanced  - Convert LaTeX to DOCX (enhanced formatting)"
	@echo "  docx-from-pdf  - Convert PDF to DOCX (alternative method)"
	@echo "  clean          - Remove auxiliary files"
	@echo "  clean-all      - Remove all generated files including PDF"
	@echo "  view           - Open PDF viewer (Linux)"
	@echo "  view-mac       - Open PDF viewer (macOS)"
	@echo "  help           - Show this help message"

.PHONY: all quick docx docx-enhanced docx-from-pdf clean clean-all view view-mac help