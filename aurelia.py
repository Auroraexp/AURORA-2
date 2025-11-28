# Placeholder for Aurelia risk aggregator

def evaluate_aurelia(x_sem, context=None):
    # returns a scalar risk score (0..1)
    x = abs(x_sem)
    score = min(1.0, x / (abs(x) + 10.0))
    return score
