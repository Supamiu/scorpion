import data
import limites
import metier


def parse_element(el):
    e = list(map(float, el.split('|')))
    e[7] = int(e[7])
    e[8] = int(e[8])
    return e


# Structure de données qui simplifie le traitement des individus au sein des calculs
class Individu:
    def __init__(self, data_string):
        self.raw_string = data_string
        parsed = parse_element(data_string)
        # alpha|Lb|b|h|Lc|Lf|Rf|Marc|Mflèche
        self.alpha = parsed[0]
        self.lb = parsed[1]
        self.b = parsed[2]
        self.h = parsed[3]
        self.lc = parsed[4]
        self.lf = parsed[5]
        self.rf = parsed[6]
        self.marc = data.MATERIALS[parsed[7]]
        self.mfleche = data.MATERIALS[parsed[7]]
        # Une fois nos propriétés de base préparées, on calcule le reste
        # Ressort
        self.ressort = metier.ressort(self.marc[2], self.marc[3])
        # Longueur à vide
        self.lv = metier.longueur_a_vide(self.lb, self.lc)
        # Longueur de déplacement
        self.ld = metier.longueur_deplacement(self.lf, self.lv)
        # Masse du projectile
        self.mp = metier.masse_projectile(self.rf, self.lf, self.mfleche[1])
        # Vélocité
        self.velocite = metier.velocite(self.ressort, self.ld, self.mp)
        # Portée
        self.portee = metier.portee(self.velocite, self.alpha)
        # Energie de l'impact
        self.nrj = metier.tnt(metier.energie_impact(self.mp, self.velocite))
        # Moment quadratique
        self.moment_quadratique = limites.moment_quadratique(self.b, self.h)
        # Force de traction
        self.traction = limites.traction(self.ressort, self.ld)
        # Flèche maximum
        self.fleche_max = limites.fleche_max(self.traction, self.lb, self.marc[3], self.moment_quadratique)

    # Défini si l'individu peut tirer
    def peut_tirer(self):
        canfire = (self.fleche_max <= self.ld) \
                  & (self.lv > 0) \
                  & (self.lv <= self.lf) \
                  & (self.lc <= self.lb) \
                  & (self.lc > 0)
        return canfire

    # Retourne le génome complet de l'individu sous forme de tableau
    def as_array(self):
        return parse_element(self.raw_string)
