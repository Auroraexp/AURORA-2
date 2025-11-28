# aurelia.py

def NIM(I=1.0, E=1.0, C=1.0, A=1.0, S=1.0, eps=0.1):
    return (I + E + C + A + S) / 5.0

def NOVEMBER(deltaC=1.0, Hs=0.5, El=0.3, Psir=0.8, Tn=1.0, Lam=1.0):
    return deltaC * (Hs + El) * Psir * (Tn ** 1.0) * Lam

def AURELIA_module(context, w_A=0.26789, eta=0.27, alpha=0.574, beta=0.426):
    nim = NIM(
        I=context.get('I',1.0), E=context.get('E',1.0), C=context.get('C',1.0),
        A=context.get('A',1.0), S=context.get('S',1.0), eps=context.get('eps',0.1)
    )
    november = NOVEMBER(
        deltaC=context.get('deltaC',1.0), Hs=context.get('Hs',0.5), El=context.get('El',0.3),
        Psir=context.get('Psir',0.8), Tn=context.get('Tn',1.0), Lam=context.get('Lam',1.0)
    )
    val = eta * (alpha * nim + beta * november)
    return w_A * val
