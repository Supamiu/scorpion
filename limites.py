from metier import *


# Calcul du moment quadratique
def moment_quadratique(b, h):
    return b * math.pow(h, 3)


# Calcul de la force de traction
def traction(r, ld):
    return r * ld


# Calcul de la flèche maximum
def fleche_max(t, lb, poisson, moment_q):
    return (t * math.pow(lb, 3)) / (48 * poisson * moment_q)
