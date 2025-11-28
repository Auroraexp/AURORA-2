# kre.py
import math

def KRE_module(x, w_K=0.28278):
    """Опрощена версия на KRE: генерира предложение от текущото състояние x.
    В реалния проект замени тази функция с твоя FKRE динамика/интеграл.
    """
    base = float(x)
    proposal = base + w_K * (0.5 * base + math.sin(base) * 0.1)
    return proposal
