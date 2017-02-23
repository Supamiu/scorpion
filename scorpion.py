from random import randrange, randint

import matplotlib.pyplot as plot

import data
from individu import Individu

# Distance de ma cible
TARGET = 350
# Taille de ma population
N = 500
# Nombre de générations
GENERATIONS = 200
# Chances de mutation en /1000
MUTATION = 1
# Chances d'hybridation en %
HYBRIDATION = 80


# C'est ici qu'on lance tout :D
def main():
    plot_data_score = []
    plot_data_nrj = []
    plot_data_range = []
    plot_data_variance = []
    population = generate_population(N)
    generation = [Individu(element_str) for element_str in population]
    for g in range(GENERATIONS):
        # On monitor notre génération avant de la renouveller
        totalscore = 0
        generation = [Individu(element_str) for element_str in population]
        max_nrj = maxnrj(generation)
        for element in generation:
            totalscore += evaluate(element, max_nrj)
        plot_data_score.append(totalscore / len(generation))
        plot_data_nrj.append(avgnrj(generation))
        plot_data_range.append(avgrange(generation))
        plot_data_variance.append(variance(generation, max_nrj))
        # Puis on renouvelle une generation
        population = new_generation(generation)
        print(str(int(g / GENERATIONS * 100)), "% done")

    max_nrj = maxnrj(generation)
    major = best(generation)
    # Debug
    print("BEST ELEMENT : ")
    print_element(major, max_nrj)
    # End debug
    plot.figure(1)
    plot.subplot(221)
    plot.plot(plot_data_score)
    plot.xlabel("Generation")
    plot.ylabel("Fitness Score /100")
    plot.subplot(222)
    plot.plot(plot_data_nrj)
    plot.xlabel("Generation")
    plot.ylabel("Energy: TNT")
    plot.subplot(223)
    plot.plot(plot_data_range)
    plot.xlabel("Generation")
    plot.ylabel("Range: m")
    plot.subplot(224)
    plot.plot(plot_data_variance)
    plot.xlabel("Generation")
    plot.ylabel("Fitness variance")

    plot.subplots_adjust(top=0.97, bottom=0.12,
                         left=0.14, right=0.92, hspace=0.25,
                         wspace=0.61)
    plot.show()
    return 0


# Récupère la variance du score de fitness d'une génération
def variance(generation, max_nrj):
    scores = [evaluate(e, max_nrj) for e in generation]
    m = avg(scores)
    v = avg([(x - m) ** 2 for x in scores])
    return v


# Fait la moyenne d'un tableau donné
def avg(array):
    total = 0
    for v in array:
        total += v
    return total / len(array)


# Récupère l'énergie moyenne d'une population
def avgnrj(generation):
    totalnrj = 0
    for element in generation:
        totalnrj += element.nrj
    return totalnrj / len(generation)


# Récupère la portée moyenne d'une génération
def avgrange(generation):
    totalrange = 0
    for element in generation:
        totalrange += element.portee
    return totalrange / len(generation)


# Fonction de debug, sert à afficher un élément en détails
def print_element(element, max_nrj):
    print("Score: " + str(evaluate(element, max_nrj)))
    print("Precision : " + str(abs(TARGET - element.portee)) + "m")
    print("Energie : " + str(element.nrj) + " TNT")
    print("Angle : " + str(element.alpha) + "°")
    print("Longueur du bras : " + str(element.lb) + "m")
    print("Base de section du bras : " + str(element.b) + "m")
    print("Hauteur de section du bras : " + str(element.h) + "m")
    print("Longueur de corde : " + str(element.lc) + "m")
    print("Longueur de flèche : " + str(element.lf) + "m")
    print("Rayon de la flèche : " + str(element.rf) + "m")
    print("Matière de l'arc : " + element.marc[0])
    print("Matière de la flèche : " + element.mfleche[0])


# Récupère l'élément avec le meilleur score de fitness d'une génération
def best(generation):
    top = generation[0]
    max_nrj = maxnrj(generation)
    for element in generation:
        if (evaluate(element, max_nrj) > evaluate(top, max_nrj)) & element.peut_tirer():
            top = element
    return top


# Créé une génération à partir d'une autre, renouvellement de la population via reproduction
def new_generation(actual_generation):
    next_gen = []
    for x in range(N):
        parents = select_parents(actual_generation)
        next_gen.extend(reproduce(parents))
    return next_gen


# Créé deux enfants à partir de deux parents
def reproduce(parents):
    p1 = parents[0].as_array()
    p2 = parents[1].as_array()
    hybrid = randint(1, 100)
    if hybrid <= HYBRIDATION:
        child1 = str(p1[0]) + "|" + str(p1[1]) + "|" + str(p1[2]) + "|" + str(p1[3]) + "|" + str(p1[4]) + "|" \
                 + str(p1[5]) + "|" + str(p1[6]) + "|" + str(p2[7]) + "|" + str(p2[8])
    else:
        base_child = map(str, p1)
        child1 = "|".join(base_child)
    if hybrid > 100 - HYBRIDATION:
        child2 = str(p2[0]) + "|" + str(p2[1]) + "|" + str(p2[2]) + "|" + str(p2[3]) + "|" + str(p1[4]) + "|" \
                 + str(p1[5]) + "|" + str(p1[6]) + "|" + str(p1[7]) + "|" + str(p1[8])
    else:
        base_child = map(str, p2)
        child2 = "|".join(base_child)
    mutation1 = randint(1, 1000)
    mutation2 = randint(1, 1000)
    if mutation1 <= MUTATION:
        child1 = mutate(child1)
    elif mutation2 <= MUTATION:
        child2 = mutate(child2)
    return [child1, child2]


# Récupère l'énergie maximum déployée par un seul individu au sein d'une population
def maxnrj(gen):
    topnrj = 0
    for element in gen:
        if element.nrj > topnrj:
            topnrj = element.nrj
    return topnrj


# Implémentation de l'agorithme de tournoi pour note reproduction
def select_parents(generation):
    max_nrj = maxnrj(generation)
    t1 = generation[randrange(len(generation) - 1)]
    t2 = generation[randrange(len(generation) - 1)]
    parent1 = winner(t1, t2, max_nrj)
    t1 = generation[randrange(len(generation) - 1)]
    t2 = generation[randrange(len(generation) - 1)]
    parent2 = winner(t1, t2, max_nrj)
    return [parent1, parent2]


# Système de tournoi classique qui compare le score de fitness.
def winner(t1, t2, max_nrj):
    t1score = evaluate(t1, max_nrj)
    t2score = evaluate(t2, max_nrj)
    t1chances = (t1score / (t1score + t2score)) * 100
    if randint(1, 100) <= t1chances:
        return t1
    else:
        return t2


# On évalue l'élément donné, en lui donnant une note de 0 s'il ne peut pas tirer
def evaluate(element, max_nrj):
    note = (element.portee / TARGET * 70 + element.nrj / max_nrj * 30) if element.peut_tirer() else 1
    return note


# Génère la population de la génération 0, aléatoire
def generate_population(size):
    return [generate_element() for _ in range(size)]


# Génère un élément sous forme de string
def generate_element():
    # Un élément est représenté sous la forme d'une string
    # La structure étant décrite ci-dessous:
    # alpha|Lb|b|h|Lc|Lf|Rf|Marc|Mflèche
    # Voir l'énoncé du TP page 3 pour la signification des variables.
    return str(genom(0)) + "|" + \
           str(genom(1)) + "|" + \
           str(genom(2)) + "|" + \
           str(genom(3)) + "|" + \
           str(genom(4)) + "|" + \
           str(genom(5)) + "|" + \
           str(genom(6)) + "|" + \
           str(genom(7)) + "|" + \
           str(genom(8))


# Créé une mutation sur l'élément donné sous forme de string
def mutate(element):
    base = element.split('|')
    index = randrange(0, len(base) - 1)
    base[index] = genom(index)
    mutated = map(str, base)
    return "|".join(mutated)


# Roll un génome à l'index donné, permet d'unifier la création avec la mutation
def genom(index):
    # alpha,Lb,b,h,Lc,Lf,Rf,Marc,Mflèche
    return [
        randint(0, 9000) / 100,
        randint(1, 500) / 100,
        randint(1, 500) / 100,
        randint(1, 500) / 100,
        randint(1, 500) / 100,
        randint(1, 500) / 100,
        randint(1, 500) / 100,
        str(randint(0, len(data.MATERIALS) - 1)),
        str(randint(0, len(data.MATERIALS) - 1))
    ][index]


if __name__ == '__main__':
    main()
