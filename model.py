# model.py
from .kre import KRE_module
from .os_module import OS_module
from .aurelia import AURELIA_module

WEIGHTS = {
    'w_K': 0.28278,
    'w_OS': 0.17866,
    'w_A': 0.26789,
    'w_G': 0.27067
}

def aurora_step(x0, context, params=None):
    if params is None:
        params = {}

    x_cand = KRE_module(x0, w_K=WEIGHTS['w_K'])

    mu = params.get('mu', 0.1)
    grad_est = 0.05 * x_cand
    x_raw = x_cand - mu * grad_est

    s_corr = OS_module(context, w_OS=WEIGHTS['w_OS'])
    x_corr = x_raw + s_corr

    a_val = AURELIA_module(context, w_A=WEIGHTS['w_A'])

    grad_Leth = params.get('grad_Leth', 0.5)

    v = x_corr + a_val - params.get('eta', 0.27) * grad_Leth
    x_final = v

    return {
        'X_final': x_final,
        'trace': {
            'x_cand': x_cand,
            'x_raw': x_raw,
            's_corr': s_corr,
            'a_val': a_val,
            'v': v
        }
    }
