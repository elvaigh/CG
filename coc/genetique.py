""" Le but de ce programme est de montrer l'efficacité d'un algorithme évolutif en essayant de retrouver 
une phrase prédéfinie contenant des lettres ainsi que des espaces, ce qui signifie pour une phrases de 
N caractères composée uniquement de minuscules et d'espaces qu'il y a 27^N combinaisons possibles, 
c'est-à-dire pour une phrase de 20 caractères environ 4*10^28 combinaisons à tester en bruteforce. """


## = modifiable
#  = ne PAS toucher


# Importation de 2 fonctions externes : une pour obtenir un nombre random entre 0 et 1, l'autre contenant les ASCII
from random import random as randomizer
from string import ascii_letters
import numpy as np



#---------VARIABLES----------
## Nombre d'individus dans la population par génération
nb_population = 200

## Nombre maximal de générations avant de trouver la solution
nbmax_generation = 10000

## Pourcentage d'individus sauvés parmi les meilleurs
saufs_bons_pourcent = 0.1

## Pourcentage d'individus sauvés parmi les mauvais
chance_quun_nuls_soit_sauve = 0.9

## Probabilité de mutation d'un individu (fonction pour attribuer une plus grande mutation aux plus nuls)
def chance_mutation(x): return 0.3/x

## Phrase à trouver
a_deviner = "Le but de ce programme est de montrer l'efficacité d'un algorithme évolutif en essayant de retrouver une phrase prédéfinie contenant des lettres ainsi que des espaces, ce qui signifie pour une phrases de N caractères composée uniquement de minuscules et d'espaces qu'il y a 27^N combinaisons possibles, c'est-à-dire pour une phrase de 20 caractères environ 4*10^28 combinaisons à tester en bruteforce."


longueur_a_deviner = len(a_deviner)
milieu_a_deviner = longueur_a_deviner // 2

# Nombre d'individus sauvés parmi les meilleurs
saufs_bons_nb = int(nb_population * saufs_bons_pourcent)

# Caractères autorisés : caractères ASCII et l'espace
caracteres_autorises = ascii_letters + ' '

# La correspondance maximale avec la phrase à deviner(donc le score maximal) est sa longueur
score_max = len(a_deviner)

# Fonction qui fait pareil qu'une fonction de la librairie random mais en plus rapide :)
choix = lambda x: x[int(randomizer() * len(x))]



#---------FONCTIONS----------


#----Fonction qui retourne un caractère aléatoire tiré de la liste des caractères autorisés
def obtenir_caractere_alea(): return choix(caracteres_autorises)


#----Fonction qui génère un individu (= chaine de caractère)
def obtenir_individu_alea(): return [obtenir_caractere_alea() for _ in range(longueur_a_deviner)]


#----Fonction qui génère une population
def obtenir_population_alea(): return [obtenir_individu_alea() for _ in range(nb_population)]


#----Fonction qui donne le score d'un individu
def obtenir_score(individu): 
    score = 0
    for caractere_individu, caractere_attendu in zip(individu, a_deviner): #On utilise des couples de caractères
        if caractere_individu == caractere_attendu: #On compare 1 à 1 les caractères constituant l'individu à ceux de la phrase
            score += 1 #On incrémente le score de l'individu si les caractères correspondent
    return score


#----Fonction qui calcule le score moyen de la population
def obtenir_score_moyen(population): 
    score_total = 0
    for individu in population: #Pour chaque individu on récupère son score et on l'ajoute au score total de la population
        score_total += obtenir_score(individu)
    return score_total / nb_population #On calcule la moyenne en divisant le score total par le nombre d'individu dans la population


#----Fonction qui classe les individus en fonction de leur score
def classement_population(population): 
    liste_individu = [] #Liste contenant tous les individus associés à leur score dans le désordre
    for individu in population: #Pour chaque individu dans la population
        liste_individu.append((individu, obtenir_score(individu))) #on ajoute à la fin de cette liste le tuple (individu, score)
    return sorted(liste_individu, key=lambda x: x[1], reverse=True) #On trie la liste des individus selon la case "score" (donc 1 du tuple) et on l'inverse pour avoir un ordre décroissant et non pas croissant.

#----Fonction qui transforme une liste en chaîne de caractères
def version_str(liste):
    chaine = ""
    for i in range(len(liste)):
        chaine += str(liste[i])
    return chaine


#----Fonction primordiale qui fait évoluer, muter, etc la population
def evolution_population(population): 
    
    # Classement des individus, obtention du score moyen et de la solution
    population_classee_brute = classement_population(population)
    score_moyen = 0
    solution = [] #Liste qui contient les individus ayant trouvé la phrase à deviner
    population_classee = [] #Liste qui contiendra uniquement les individus classés, sans leur score
    for individu, score in population_classee_brute: #Pour chaque tuple (individu, score) dans le classement,
        score_moyen += score
        population_classee.append(individu) #On ajoute cet individu sans son score à la liste
        if score == score_max: #Si un idividu a atteint le score maximal
            solution.append(individu) #alors on l'ajoute à la liste des solutions car il a trouvé la réponse
    score_moyen /= nb_population    
    
    # Terminer le script si la solution a été trouvée
    if solution != []: #Si la liste n'est pas vide c'est-à-dire qu'on a au moins une solution
        return population, obtenir_score_moyen(population), solution #on renvoie tout ça

    
    # Filtrage des meilleurs candidats
    parents = population_classee[:saufs_bons_nb] #Les parents (= ceux qui pourront se "reproduire") sont les meilleurs individus
    
    
    # Sauvetage de chanceux
    for individu in population_classee[saufs_bons_nb:]: #Pour chaque individu parmi les non-meilleurs
        if randomizer() < saufs_bons_pourcent: #On jette un dé pour savoir s'il est sauvé
            parents.append(individu) #Si oui on l'ajoute à la liste des parents
    
    
    # Mutations
    for individu in parents: #Pour chaque individu parmi les parents
        if obtenir_score(individu) == 0:
            mutation = 1
        else:
            mutation = chance_mutation(1/obtenir_score(individu))
        if randomizer() < mutation: #On jette un dé pour savoir s'il subit une mutation
            caractere_a_modifier = int(randomizer() * longueur_a_deviner) #Si oui, on tire au pif le caractère à muter
            individu[caractere_a_modifier] = obtenir_caractere_alea() #et on le remplace par un autre au hasard
    
    # Reproduction
    nb_parents = len(parents)                   #On enregistre le nombre de parents
    nb_enfants = nb_population - nb_parents     #Le nombre de nouveaux individus est égal au nombre d'individus maximum dans la population moins le nombre de parents, qui font partie de cette nouvelle population
    enfants = []
    while len(enfants) < nb_enfants:            #Tant que le nombre d'enfants est inférieur au nombre d'enfants attendus
        papa = choix(parents)                   #On choisit un papa
        maman = choix(parents)                  #et une maman
        if papa != maman:                       #On vérifie qu'on a bien 2 individus différents, sinon on obtient un nouvel individu identique
            enfant = papa[:milieu_a_deviner] + maman[milieu_a_deviner:] #Un enfant est composé de la première moitié du père et de la seconde moitié de la mère
            enfants.append(enfant)              #On ajoute le nouvel individu à la liste des enfants
    
    population = parents
    population.extend(enfants)        #La nouvelle population est constituée des parents ainsi que des enfants
    
    return population, obtenir_score_moyen(population), solution

def ecriture_log(nom_fichier, donnees_log):
    fichierlog = open(nom_fichier, "w")
    fichierlog.write("score_max="+str(longueur_a_deviner)+"\n")
    fichierlog.write("nb_population="+str(nb_population)+"\n")
    fichierlog.write("nb_solution="+str(len(solution))+"\n")
    fichierlog.write("nbfinal_generation="+str(g)+"\n")
    fichierlog.write("saufs_bons_pourcent="+str(saufs_bons_pourcent)+"\n")
    fichierlog.write("chance_quun_nuls_soit_sauve="+str(chance_quun_nuls_soit_sauve)+"\n")
    fichierlog.write("chance_mutation="+str(chance_mutation))
    for k in range(len(donnees_log)):
        fichierlog.write("\n" + str(donnees_log[k]))
    fichierlog.close()
    
    
    
#----Fonction principale

#On crée une population de départ
population = obtenir_population_alea()
score_moyen = obtenir_score_moyen(population)

#On la fait évoluer
g = 1   #Numéro de la génération (on commence à la 2 car la première est générée hors de la boucle)
solution = []

log_score_moy = []
log_score_max = []
log_score_min = []

while solution == [] and g< nbmax_generation: #Tant qu'on a pas de solution et qu'on a pas dépassé la limite de générations
    p = classement_population(population)
    if g % 20 == 0:
        top = version_str(p[0][0])
        flop = version_str(p[-1][0])
        print(g,"-", " moy=", score_moyen, "     - best :", top, "     - worse :", flop)
    g += 1
    
    log_score_moy.append(score_moyen)
    log_score_max.append(obtenir_score(p[0][0]))
    log_score_min.append(obtenir_score(p[-1][0]))
    population, score_moyen, solution = evolution_population(population) #On fait évoluer la population

if g >= nbmax_generation:
    print("Nombre maximum de générations dépassé...")

print("\n", len(solution), "solution(s) trouvée(s) au bout de ", g-1,"générations")
p = classement_population(population)
top = version_str(p[0][0])
print(g-1,"-", " moy=", score_moyen, "- Meilleur mot :", top)

"""
ecriture_log("export_donnees_moy.txt",log_score_moy)
ecriture_log("export_donnees_max.txt",log_score_max)
ecriture_log("export_donnees_min.txt",log_score_min)

x = np.arange(1,g)
courbe_moy = np.loadtxt("export_donnees_moy.txt", skiprows = 7)
courbe_max = np.loadtxt("export_donnees_max.txt", skiprows = 7)
courbe_min = np.loadtxt("export_donnees_min.txt", skiprows = 7)
plt.plot(x, courbe_moy)
plt.plot(x, courbe_max)
plt.plot(x, courbe_min)

lim_max = np.ones(g-1)*longueur_a_deviner
plt.plot(x, lim_max)"""
