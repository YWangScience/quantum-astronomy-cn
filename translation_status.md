# Translation Status

This file tracks the bilingual restructuring and the English translation.

## Current Structure

- Chinese source: `frontmatter/zh/`, `chapters/zh/`, `appendices/zh/`
- English source: `frontmatter/en/`, `chapters/en/`, `appendices/en/`
- Shared assets and macros: `shared/`
- Shared figures and code: `figures/`, `code/`
- Shared bibliography: `references.bib`

## English Translation Progress

| Unit | Status | Notes |
|---|---|---|
| Preface | translated | Native English draft in `frontmatter/en/preface.tex`. |
| Chapter 1 | translated | Terminology aligned with `shared/terminology_zh_en.yml`. |
| Chapter 2 | translated | Added to `main_en.tex`; labels, ADS citation keys, and figure paths preserved. |
| Chapter 3 | translated | Added to `main_en.tex`; quantum-optics terminology aligned with Chapters 1--2. |
| Chapter 4 | translated | Added to `main_en.tex`; photon-statistics terminology aligned with Chapters 2--3. |
| Chapter 5 | translated | Added to `main_en.tex`; spatial-coherence and SII terminology aligned with earlier chapters. |
| Chapter 6 | translated | Added to `main_en.tex`; detector, clock, timing, and event-table terminology aligned with earlier chapters. |
| Chapter 7 | translated | Added to `main_en.tex`; likelihood, correlation-estimator, covariance, and posterior terminology aligned with Chapters 1--6. |
| Chapter 8 | translated | Added to `main_en.tex`; quantum-estimation, Rayleigh-limit, SPADE, and SII Fisher-information terminology aligned with earlier chapters. |
| Chapter 9 | translated | Added to `main_en.tex`; radiation-mechanism, brightness-temperature, coherence-function, and maser terminology aligned with earlier chapters. |
| Chapter 10 | translated | Added to `main_en.tex`; stellar SII, limb-darkening, angular-diameter, and binary-visibility terminology aligned with earlier chapters. |
| Chapter 11 | translated | Added to `main_en.tex`; compact-object, degeneracy-pressure, pulsar-timing, polarization, and hot-spot likelihood terminology aligned with earlier chapters. |
| Chapter 12 | translated | Added to `main_en.tex`; black-hole scale, accretion-disk, BLR, jet-polarization, photon-ring, and Hawking-temperature terminology aligned with earlier chapters. |
| Chapter 13 | translated | Added to `main_en.tex`; transient-trigger, expansion-parallax, kilonova, GRB-afterglow, TDE, and target-of-opportunity terminology aligned with earlier chapters. |
| Chapter 14 | translated | Added to `main_en.tex`; plasma-dispersion, Faraday-rotation, scattering, dust-extinction, lensing, wave-optics, and cosmic-Bell terminology aligned with earlier chapters. |
| Chapter 15 | translated | Added to `main_en.tex`; axion-photon, birefringence, PTA, FRB-Faraday, superradiance, and dark-matter-lensing terminology aligned with earlier chapters. |
| Chapter 16 | translated | Added to `main_en.tex`; CMB, inflationary-squeezing, non-Gaussianity, tensor-mode, birefringence, and map-likelihood terminology aligned with earlier chapters. |
| Chapter 17 | translated | Added to `main_en.tex`; quantum-network-telescope, Bell-pair, memory-assisted, time-bin, fidelity, CV-teleportation, and SII-complementarity terminology aligned with earlier chapters. |
| Chapter 18 | translated | Added to `main_en.tex`; observing-design, feasibility-ledger, baseline, photon-rate, coherence-dilution, SNR, calibration, and error-budget terminology aligned with earlier chapters. |
| Chapter 19 | translated | Added to `main_en.tex`; first-generation science-case, feasibility-ranking, rapid-rotator, binary, line-forming-region, transient, Crab-statistics, and astrophysical-laser terminology aligned. |
| Chapter 20 | translated | Added to `main_en.tex`; event-table, tabletop-HBT, correlator, uniform-disk, binary, SPADE, and Type-Ia toy-model terminology aligned. |
| Chapter 21 | translated | Added to `main_en.tex`; common-pitfall, g2-diagnostic, calibration, phase-retrieval, superresolution, maser-statistics, false-alarm, and new-physics-boundary terminology aligned. |
| Chapter 22 | translated | Added to `main_en.tex`; roadmap, readiness-vector, multichannel-event-table, network-pathfinder, milestone, risk-register, and research-plan terminology aligned. |
| Appendices A--G | translated | Added to `main_en.tex`; formula index, unit tables, glossary, route guide, code guide, course plan, and reading guide translated with labels preserved. |

## Translation Rules

- Keep ADS BibTeX keys unchanged.
- Keep equation labels, figure labels, and code filenames unchanged.
- Translate figure captions in the English chapter files; do not duplicate figure PDFs unless labels inside the figure itself must be translated.
- Use `shared/terminology_zh_en.yml` as the canonical terminology list.
- Prefer natural scientific English over literal sentence-by-sentence translation.
