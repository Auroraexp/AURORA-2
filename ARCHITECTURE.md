# AURORA-2 Architecture

## Overview
AURORA-2 is a State-Encoding Ethical Meta-Intelligence (SEEMI) combining:
- KRE: dynamic reasoning engine
- OmniSphere: identity & context module
- AURELIA: ethical evaluator (NIM + NOVEMBER)

## Data flow
1. Input: x0 (state), context (I,E,C,A,S,eps,...)
2. KRE generates X_cand
3. RESTART stabilizes -> X_raw
4. OmniSphere applies S_corr -> X_corr
5. AURELIA computes ethical correction A_val
6. Combine and project -> X_final

## Notes
- Replace KRE_module with your FKRE integrator for physics/dynamics
- OmniSphere can be expanded to include vector embeddings
- AURELIA includes NIM (info-analysis) and NOVEMBER (impact/risk)
