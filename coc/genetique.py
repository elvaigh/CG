import random

#---------VARIABLES----------
## Nombre d'individus dans la population par génération
nb_population = 200

## Nombre maximal de générations avant de trouver la solution
nbmax_generation = 10000

## Pourcentage d'individus sauvés parmi les meilleurs
saufs_bons_pourcent = 0.1

## Pourcentage d'individus sauvés parmi les mauvais
chance_quun_nuls_soit_sauve = 0.9


longueur_a_deviner=3

# Caractères autorisés : caractères ASCII et l'espace
actions_autorises = [0,1,2,3,4,5,6]


## Probabilité de mutation d'un individu (fonction pour attribuer une plus grande mutation aux plus nuls)
def chance_mutation(x): return 0.3/x

# Nombre d'individus sauvés parmi les meilleurs
saufs_bons_nb = int(nb_population * saufs_bons_pourcent)


#---------FONCTIONS----------

# Fonction qui fait pareil qu'une fonction de la librairie random mais en plus rapide :)
choix = lambda x: x[int(random.random() * len(x))]

#----Fonction qui retourne un caractère aléatoire tiré de la liste des caractères autorisés
def obtenir_caractere_alea(): random.randInt(0,23)

#----Fonction qui génère un individu (= chaine de caractère)
def obtenir_individu_alea(): return [obtenir_action_alea()%7,obtenir_action_alea(),obtenir_action_alea()%21]

#----Fonction qui génère une population
def obtenir_population_alea(): return [obtenir_individu_alea() for _ in range(nb_population)]


#----Fonction qui donne le score d'un individu
def obtenir_score(individu,game,playerIdx): 
    score = game.players[playerIdx].score()
    game.players[playerIdx].action=individu[0]
    game.players[playerIdx].target=Case(individu[1],individu[2])
    game.applyActions()
    score = game.players[playerIdx].score()-score
    return score
    


#----Fonction qui calcule le score moyen de la population
def obtenir_score_moyen(population,game,playerIdx): 
    score_total = 0
    for individu in population: #Pour chaque individu on récupère son score et on l'ajoute au score total de la population
        score_total += obtenir_score(individu,game,playerIdx)
    return score_total / nb_population #On calcule la moyenne en divisant le score total par le nombre d'individu dans la population


#----Fonction qui classe les individus en fonction de leur score
def classement_population(population,game,playerIdx): 
    liste_individu = [] #Liste contenant tous les individus associés à leur score dans le désordre
    for individu in population: #Pour chaque individu dans la population
        liste_individu.append((individu, obtenir_score(individu,game,playerIdx))) #on ajoute à la fin de cette liste le tuple (individu, score)
    return sorted(liste_individu, key=lambda x: x[1], reverse=True) #On trie la liste des individus selon la case "score" (donc 1 du tuple) et on l'inverse pour avoir un ordre décroissant et non pas croissant.

#----Fonction primordiale qui fait évoluer, muter, etc la population
def evolution_population(population,game,playerIdx): 
    
    # Classement des individus, obtention du score moyen et de la solution
    population_classee_brute = classement_population(population,game,playerIdx)
    score_moyen = 0
    population_classee = [] #Liste qui contiendra uniquement les individus classés, sans leur score
    for individu, score in population_classee_brute: #Pour chaque tuple (individu, score) dans le classement,
        score_moyen += score
        population_classee.append(individu) #On ajoute cet individu sans son score à la liste
    score_moyen /= nb_population    
    
    # Filtrage des meilleurs candidats
    parents = population_classee[:saufs_bons_nb] #Les parents (= ceux qui pourront se "reproduire") sont les meilleurs individus
    
    
    # Sauvetage de chanceux
    for individu in population_classee[saufs_bons_nb:]: #Pour chaque individu parmi les non-meilleurs
        if random.random() < saufs_bons_pourcent: #On jette un dé pour savoir s'il est sauvé
            parents.append(individu) #Si oui on l'ajoute à la liste des parents
    
    # Mutations
    for individu in parents: #Pour chaque individu parmi les parents
        if obtenir_score(individu) == 0:
            mutation = 1
        else:
            mutation = chance_mutation(1/obtenir_score(individu,game,playerIdx))
        if random.random() < mutation: #On jette un dé pour savoir s'il subit une mutation
            caractere_a_modifier = int(random.random() * 3) #Si oui, on tire au pif le caractère à muter
            crt=obtenir_caractere_alea() 
            if caractere_a_modifier==0:crt=crt%7
            elif caractere_a_modifier==2:crt=crt%21
            individu[caractere_a_modifier] = crt#et on le remplace par un autre au hasard
    
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
    
    return population, obtenir_score_moyen(population)

def randomize(game,playerIdx):
    i=0
    population = obtenir_population_alea()
    score_moyen = obtenir_score_moyen(population,game,playerIdx)
    g=1
    while i < nbmax_generation:
        population, score_moyen = evolution_population(population,game,playerIdx)
        i+=1