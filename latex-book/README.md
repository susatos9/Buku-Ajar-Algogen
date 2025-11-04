# Genetic Algorithms: Theory and Practice

A comprehensive LaTeX book covering genetic algorithms, based on course materials from UGM (Universitas Gadjah Mada).

## Table of Contents

1. **Introduction to Optimization and Evolutionary Computation**
   - Overview of optimization problems
   - Traditional vs. evolutionary methods
   - Applications of evolutionary computation

2. **What is a Genetic Algorithm?**
   - Biological inspiration
   - Basic structure and terminology
   - Simple examples and advantages/disadvantages

3. **GA Cycle and Holland Schema Theory**
   - Detailed genetic algorithm cycle
   - Schema theory and building block hypothesis
   - Implicit parallelism and deception

4. **Genetic Algorithm Encoding**
   - Binary, real-valued, integer encodings
   - Permutation and tree representations
   - Problem-specific encoding guidelines

5. **Selection Methods in Genetic Algorithms**
   - Proportional, rank-based, and tournament selection
   - Selection pressure and diversity preservation
   - Multi-objective selection methods

6. **Crossover (Recombination) in Genetic Algorithms**
   - Binary, real-valued, and permutation crossover
   - Schema disruption analysis
   - Advanced crossover techniques

## Appendices

- **Algorithm Implementations**: Complete Python implementations
- **Practical Examples and Case Studies**: Real-world applications

## Requirements

To compile this LaTeX book, you need:

- LaTeX distribution (TeX Live, MiKTeX, or MacTeX)
- Required packages (automatically installed with most distributions):
  - `amsmath`, `amsfonts`, `amssymb`
  - `graphicx`, `booktabs`, `array`
  - `listings`, `xcolor`, `hyperref`
  - `algorithm`, `algorithmic`
  - `tikz`, `pgfplots`

## Compilation

### Using Make (Recommended)

```bash
# Compile complete book with bibliography
make all

# Quick compilation without bibliography
make quick

# View PDF (Linux)
make view

# View PDF (macOS)
make view-mac

# Clean auxiliary files
make clean

# Clean everything including PDF
make clean-all

# Show help
make help
```

### Manual Compilation

```bash
# Create output directory
mkdir -p output

# Compile with bibliography
pdflatex -output-directory=output main.tex
cd output && bibtex main
cd .. && pdflatex -output-directory=output main.tex
pdflatex -output-directory=output main.tex
```

## File Structure

```
latex-book/
├── main.tex                    # Main LaTeX file
├── references.bib              # Bibliography database
├── Makefile                    # Build automation
├── README.md                   # This file
├── output/                     # Generated files (created during compilation)
├── figures/                    # Image files directory
└── chapters/                   # Chapter files
    ├── chapter01-introduction.tex
    ├── chapter02-what-is-ga.tex
    ├── chapter03-ga-cycle-schema.tex
    ├── chapter04-encoding.tex
    ├── chapter05-selection.tex
    ├── chapter06-crossover.tex
    ├── appendix-algorithms.tex
    └── appendix-examples.tex
```

## Customization

### Adding New Chapters

1. Create a new `.tex` file in the `chapters/` directory
2. Add the chapter to `main.tex` using `\include{chapters/your-chapter}`
3. Recompile the book

### Modifying Styling

The book uses the `book` document class with custom styling. Key style elements:

- **Page layout**: 2.5cm margins with fancy headers
- **Code highlighting**: Python syntax highlighting with `listings` package
- **Algorithms**: Formatted using `algorithm` and `algorithmic` packages
- **Mathematics**: Comprehensive math support with `amsmath`
- **Graphics**: TikZ and PGF for diagrams and plots

### Adding References

Add new bibliography entries to `references.bib` in BibTeX format. The book uses the `plain` bibliography style.

## Python Code Examples

The book includes complete Python implementations in the appendices:

- **Basic Genetic Algorithm**: Binary representation with standard operators
- **Real-Valued GA**: Continuous optimization with BLX-α crossover
- **TSP Genetic Algorithm**: Permutation-based GA for traveling salesman problem
- **NSGA-II**: Multi-objective optimization algorithm

All code examples are fully functional and can be extracted and run independently.

## Contributing

To contribute to this book:

1. Fork the repository
2. Create your feature branch
3. Make your changes
4. Test compilation
5. Submit a pull request

## Course Integration

This book is designed to complement genetic algorithm courses and includes:

- **Theoretical foundations**: Mathematical analysis and proofs
- **Practical implementations**: Working code examples
- **Exercise problems**: End-of-chapter questions
- **Case studies**: Real-world applications

## Troubleshooting

### Common Issues

1. **Missing packages**: Install required LaTeX packages through your distribution's package manager
2. **Compilation errors**: Check log files in the `output/` directory
3. **Bibliography issues**: Ensure BibTeX is run after the first LaTeX compilation
4. **Font issues**: Use PDF mode for better font handling

### Error Messages

- **"File not found"**: Check file paths and ensure all chapter files exist
- **"Undefined control sequence"**: Missing package or command
- **"Citation undefined"**: Run BibTeX and recompile

## License

This educational material is provided for academic use. Please cite appropriately when using in courses or research.

## Contact

For questions or suggestions regarding this LaTeX book, please refer to the course materials and documentation.

---

**Note**: This book is compiled from course materials and serves as a comprehensive reference for genetic algorithms in optimization and machine learning applications.