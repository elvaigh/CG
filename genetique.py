from random import random as randomizer

#---------VARIABLES----------
## Nombre d'individus dans la population par génération
nb_population = 200

## Nombre maximal de générations avant de trouver la solution
nbmax_generation = 10000

## Pourcentage d'individus sauvés parmi les meilleurs
saufs_bons_pourcent = 0.1

## Pourcentage d'individus sauvés parmi les mauvais
chance_quun_nuls_soit_sauve = 0.9


# Caractères autorisés : caractères ASCII et l'espace
actions_autorises = [0,1,2,3,4,5]


## Probabilité de mutation d'un individu (fonction pour attribuer une plus grande mutation aux plus nuls)
def chance_mutation(x): return 0.3/x

# Nombre d'individus sauvés parmi les meilleurs
saufs_bons_nb = int(nb_population * saufs_bons_pourcent)


#---------FONCTIONS----------

# Fonction qui fait pareil qu'une fonction de la librairie random mais en plus rapide :)
choix = lambda x: x[int(randomizer() * len(x))]

#----Fonction qui retourne un caractère aléatoire tiré de la liste des caractères autorisés
def obtenir_action_alea(): return choix(actions_autorises)


#----Fonction qui génère un individu (= chaine de caractère)
def obtenir_individu_alea(): 
	action=obtenir_action_alea()
	if 


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
https://github.com/Ansolix/genetics/blob/master/sentence_finder_FRENCH.py