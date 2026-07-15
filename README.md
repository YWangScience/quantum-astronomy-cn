# Quantum Astronomy

[中文说明](README.zh.md)

## Preface

I am writing this book because I want to learn quantum astronomy.

At first I looked for a textbook that began with observations: real astronomical data first, then coherence functions, photon statistics, quantum estimation, and instrumental limits introduced as the data demanded them. I did not find that book. The relevant material certainly exists, and many papers and monographs are excellent, but the subject is scattered across statistical optics, quantum optics, interferometry, high-energy astrophysics, cosmology, and quantum information.

So I decided to write the book myself, and to treat the writing as part of the learning. The book is still being revised because I am still learning.

<p align="right">Yu Wang<br>July 2026</p>

## Downloads

- Online reading: <https://book.quantum-astronomy.ywang.science>
- English PDF: <https://github.com/YWangScience/quantum-astronomy/releases/latest/download/quantum-astronomy-en.pdf>
- Chinese PDF: <https://github.com/YWangScience/quantum-astronomy/releases/latest/download/quantum-astronomy-cn.pdf>
- Latest release: <https://github.com/YWangScience/quantum-astronomy/releases/latest>

## Local Build

The Chinese manuscript is built from `main.tex`. Build artifacts are written to
`build/`:

```bash
latexmk -xelatex -interaction=nonstopmode -halt-on-error -file-line-error -outdir=build main.tex
```

The generated PDF is `build/main.pdf`.

The current Chinese layout uses `qa-modern-clear.sty`, which reserves a right
margin for formula notes. Keep newly generated build artifacts in `build/`
rather than placing PDFs in the repository root.

## Table of Contents

- Preface

### Quickstart

- Essay 1. What is intensity interferometry?

### Part I: Foundations, Definitions, and Observables

- Chapter 1. The Most Basic Concepts
- Chapter 2. Why quantum astronomy is needed
- Chapter 3. Foundations of quantum optics
- Chapter 4. Photon statistics and coherence functions

### Part II: Instruments, Intensity Interferometry, and Information Limits

- Chapter 5. Spatial coherence and intensity interferometry
- Chapter 6. Detectors, clocks, and event tables
- Chapter 7. Data analysis for event tables
- Chapter 8. Quantum estimation and sub-resolution information

### Part III: The Quantum Language of Astrophysical Light

- Chapter 9. Astrophysical radiation mechanisms
- Chapter 10. Stars as quantum light sources
- Chapter 11. Compact stars and strong fields
- Chapter 12. Black holes and photon rings
- Chapter 13. Transients and multi-messenger astronomy

### Part IV: Propagation, Cosmology, New Physics, and Quantum Networks

- Chapter 14. Propagation effects
- Chapter 15. Dark matter and polarization channels
- Chapter 16. Quantum questions in cosmology
- Chapter 17. Quantum network telescopes

### Part V: Observing Design, Case Studies, Teaching, and Roadmap

- Chapter 18. Observing design and error budgets
- Chapter 19. First-generation science cases
- Chapter 20. Teaching and computational experiments
- Chapter 21. Common pitfalls
- Chapter 22. From white paper to research plan

### Appendices

- Appendix A. Index of Frequently Used Formulas
- Appendix B. Common Units and Numerical Scales
- Appendix C. Glossary
- Appendix D. Reading Routes and Validity Boundaries for Core Relations
- Appendix E. Guide to the Example Computational Code
- Appendix F. Suggested 14-Week Course Plan
- Appendix G. Reading Guide
