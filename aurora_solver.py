import numpy as np

# Simplified, numerically stable MVP core

def aurora2_solve(kre, os, aurelia, modifiers=None):
    """
    AURORA-2 MVP core implementation.
    Inputs: numeric scalars or small vectors (for MVP we use scalars).
    Returns numeric output.
    """
    if modifiers is None:
        modifiers = {}

    alpha = float(modifiers.get("alpha", 1.12))
    beta = float(modifiers.get("beta", 0.87))
    eta = float(modifiers.get("eta", 1.03))

    # safe numeric coercion
    kre = float(kre)
    os = float(os)
    aurelia = float(aurelia)

    # Core transform (smooth, avoids overflow)
    a = np.power(abs(kre) + 1e-9, 0.38) * np.sign(kre)
    b = np.power(abs(os) + 1e-9, 0.42) * np.sign(os)
    c = np.power(abs(aurelia) + 1e-9, 0.56) * np.sign(aurelia)

    # Combine and apply modifiers
    value = (a * 0.9 + b * 0.95 + c * 1.05) * alpha * beta * eta

    # Clip to reasonable range for demo
    value = float(np.clip(value, -1e12, 1e12))

    return round(value, 6)
