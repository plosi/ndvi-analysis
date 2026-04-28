# ndvi-analysis
Exploring satellite‑derived NDVI as indicative evidence of irrigation effects

# Satellite‑derived NDVI analysis for irrigation monitoring

This repository contains the Python code used to support the analysis described in  
**“Exploring satellite‑derived NDVI as indicative evidence of irrigation effects”**.  
The analysis explores whether Earth Observation (EO) data—specifically NDVI—show
indicative signals of improved dry‑season vegetation persistence following the
implementation of a small‑scale irrigation scheme.

The work is intended as a **learning and feasibility exercise**, not a formal impact
evaluation.

---

## Overview

The analysis uses:
- **Sentinel‑2 Surface Reflectance** imagery to compute NDVI time series and composites.
- **CHIRPS precipitation** data for contextual rainfall interpretation.
- A **historical baseline (2018–2023)** to express NDVI and rainfall anomalies as
  z‑scores.
- **Pre‑ vs post‑intervention comparison**, aligned to the irrigation scheme
  operational date (Q4 2024).

