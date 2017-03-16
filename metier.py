import math

# Constantes
GRAVITY = 9.81


def ressort(E, v):
    return (E / (1 - (2 * v))) / 3


def longueur_a_vide(lb, lc):
    try:
        result = math.sqrt(
            math.pow(lb, 2) -
            (math.pow(lc, 2) / 4))
    except ValueError:
        result = -1
    return result


def longueur_deplacement(lf, lv):
    ld = lf - lv if not lv == -1 else 0.01
    return ld


def masse_projectile(rf, lf, mvp):
    return mvp * math.pi * math.pow(rf, 2) * lf


def velocite(r, ld, mp):
    return math.sqrt((r * math.pow(ld, 2)) / mp)


def portee(velocity, alpha):
    return (math.pow(velocity, 2) / GRAVITY) \
           * math.sin(2 * math.radians(alpha))


def energie_impact(mp, velocity):
    return 1 / 2 * mp * math.pow(velocity, 2)


def tnt(nrj_joule):
    return nrj_joule / 4184
