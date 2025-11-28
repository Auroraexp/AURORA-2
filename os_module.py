# os_module.py
import math

def OS_module(context_vector, w_OS=0.17866):
    """OmniSphere корекция: приема контекст (словар/вектор) и връща корекционен скалар.
    Тук контекст_vector е словар с полета Au,Ag,mineral,FeCu,ID (или числов индикатор).
    """
    Au = float(context_vector.get('Au', 1.0))
    Ag = float(context_vector.get('Ag', 1.0))
    mineral = float(context_vector.get('mineral', 1.0))
    fe_cu = float(context_vector.get('fe_cu', 1.0))
    uid = float(context_vector.get('uid', 1.0))

    raw = Au + Ag + mineral + fe_cu + uid
    corr = w_OS * (raw / 5.0)
    return corr
