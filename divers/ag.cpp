// **************************************************************************************************************************** //
// Cette source est un petit algorithme génétique très simple [AI genetic algorithm]
// La population va muter de génération en génération afin de se rapprocher du but : (ici) trouver la cible "Vive l'IA !"
// Le meilleur membre de la population est affiché ainsi que son fitness
// par neo_00110010101 [neo_00110010101@hotmail.com]

// Débuté le 28/06/04
// Terminé le 20/02/05 (longtemps resté inerte)
// Mise A Jour du **/**/**

// Comment fonctionne l'algorithme génétique :

// Selon l'algorithme génétique, de nombreuses solutions, plus ou moins bonnes, au problème donné sont créées au hasard, selon
// une forme définie à l'avance : itinéraire, emploi du temps, base de règles de décision, plan de production, réseau de neurones,
// etc. Ces «solutions», étant créées au hasard, ne sont au départ pas très bonnes : il manque des cours dans les emplois du temps
// ou bien les itinéraires ne passent pas par tous les points à desservir.
// La population de solutions est alors soumise à une imitation de l'évolution des espèces : mutations et reproduction
// par hybridation. En favorisant la survie des plus «aptes» (les solutions les plus correctes), on provoque l'apparition
// d'hybrides meilleurs que chacun de leurs parents.
// La population initiale donne ainsi naissance à des générations successives, mutés et hybridés à partir de leurs «parents».
// Le mécanisme d'encouragement des éléments les plus aptes («pression de l'évolution») a pour résultat que les générations
// successives sont de plus en plus adaptées à la résolution du problème.
//
// [extrait de http://www.pmsi.fr/gainit.htm]

// Ou bien encore :

// Considérons un environnement quelconque dans lequel vit une population primitive, i.e. peu adaptée à cet environnement.
// Bien sûr, quoique globalement inadaptée, cette population n'est pas uniforme : certains individus sont mieux armés que
// d'autres pour profiter des ressources offertes par environnement (nourritures, abris, etc.) et pour faire face aux dangers
// qui y rôdent (prédateurs, intempéries, etc.).
// Ces individus mieux équipés ont par conséquent une probabilité de survie plus grande que leurs congénères et auront de fait
// d'autant plus de chances de pouvoir se reproduire. 
// En se reproduisant entre individus bien adaptés, ils vont transmettre à leurs enfants ces caractéristiques qui faisaient 
// leur excellence. 
// La population qui résultera de cette reproduction sera donc globalement mieux adaptée à environnement que la précédente 
// puisque la plupart des individus auront hérité de plusieurs (puisque chacun hérite à la fois de sa mère et de son père) 
// des caractéristiques de l' "élite" de la génération précédente. 
// Et c'est ainsi, en recombinant à chaque génération les caractéristiques élémentaires de bonne adaptation et en saupoudrant 
// le tout d'un peu de hasard, que la population va évoluer vers une adéquation toujours meilleure avec l'environnement.

// [extrait de http://www.vieartificielle.com/index.php?action=article&id=44]
// **************************************************************************************************************************** //

#pragma warning (disable:4005) // empêche les erreurs warnings (futile)

#include <iostream>
#include <windows.h>
#include <math.h>
#include <string>
#include <vector>
#include <algorithm>
#include <time.h>

// TAILLE DE LA POPULATION

#define PRGM_TAILLEPOPULATION    2048 // logiquement, plus il y a de membres, plus il y a de chances d'en trouver un de bon

// MAXIMUM DE POSSIBILITES (OU D'ESSAIS)
// -> il se peut qu'aucune solution ne soit trouvée alors pas la peine d'attendre

#define PRGM_MAXESSAIS    10000

// TAUX DE MUTATION

#define PRGM_TAUXMUTATION    0.25 // plus c'est grand, plus il y aura de chance d'avoir de "bons" membres dans chaque génération
#define PRGM_MUTATION    RAND_MAX * PRGM_TAUXMUTATION

// TAUX D'ELITISME

#define PRGM_TAUXELITISME    0.10 // voir définition de "élitisme" -> le fait de ne s'occuper QUE des meilleurs : plus le chiffre
// est bas, et moins il y aura de "meilleurs" affichés (0.10 = un seul)

// LA CIBLE : la chaîne de caractère "Vive l'IA !" parmis la population (le nom d'un membre par exemple)

#define PRGM_CIBLE    string("nagajhsqhjhffhfhhbvbvnxhgghh")

using namespace std;

struct prgm_structure 
{
    string nom;
    unsigned int fitness;
    // -> A chaque génération, les individus dont le fitness est le plus élevé seront sélectionnés afin de transmettre
    // leur caractère génétique à leurs descendants (plus le fitness est élévé, plus les gènes correspondants sont pertinents)
};

typedef vector<prgm_structure> prgm_vecteur;

// INITIALISATION DE LA POPULATION

void initialisation_population(prgm_vecteur &population, prgm_vecteur &buffer) 
{
    int taillecible = PRGM_CIBLE.size();

    for (int i = 0; i < PRGM_TAILLEPOPULATION; i++)
    {
        prgm_structure individu;
        individu.fitness = 0;
        individu.nom.erase();

        for (int j = 0; j < taillecible; j++)
        {
            individu.nom += (rand() % 90) + 32;
        }

        population.push_back(individu);
    }

    buffer.resize(PRGM_TAILLEPOPULATION);
}

// FITNESS

void calcul_fitness(prgm_vecteur &population)
{
    string cible = PRGM_CIBLE;
    int taillecible = cible.size();
    unsigned int fitness;

    for (int i = 0; i < PRGM_TAILLEPOPULATION; i++)
    {
        fitness = 0;
        for (int j = 0; j < taillecible; j++)
        {
            fitness += abs(int(population[i].nom[j] - cible[j]));
        }
        
        population[i].fitness = fitness;
    }
}

// TRI

bool trier_fitness(prgm_structure x, prgm_structure y) 
{
    return (x.fitness < y.fitness);
}

void trier_par_fitness(prgm_vecteur &population)
{ 
    sort(population.begin(), population.end(), trier_fitness);
}

// ELITISME

void elitisme( prgm_vecteur &population, prgm_vecteur &buffer, int tailleelitisme )
{
    for (int i = 0; i < tailleelitisme; i++)
    {
        buffer[i].nom = population[i].nom;
        buffer[i].fitness = population[i].fitness;
    }
}

// MUTATION

void mutation(prgm_structure &membre)
{
    int taillecible = PRGM_CIBLE.size();
    int c = rand() % taillecible;
    int d = (rand() % 90) + 32; 

    membre.nom[c] = ((membre.nom[c] + d) % 122);
}

// JOINDRE

void joindre(prgm_vecteur &population, prgm_vecteur &buffer)
{
    int tailleelitisme = PRGM_TAILLEPOPULATION * PRGM_TAUXELITISME;
    int taillecible = PRGM_CIBLE.size(), e, iun, ideux;

    elitisme(population, buffer, tailleelitisme);

    for (int i = tailleelitisme; i < PRGM_TAILLEPOPULATION; i++)
    {
        iun = rand() % (PRGM_TAILLEPOPULATION / 2);
        ideux = rand() % (PRGM_TAILLEPOPULATION / 2);
        e = rand() % taillecible;

        buffer[i].nom = population[iun].nom.substr(0, e) + population[ideux].nom.substr(e, tailleelitisme - e);

        if (rand() < PRGM_MUTATION) mutation(buffer[i]);
    }
}

// AFFICHAGE DU MEILLEUR INDIVIDU : SON NOM ET SON FITNESS

void affiche_meilleur(prgm_vecteur &vecalgogenetique)
{ 
    CONSOLE_SCREEN_BUFFER_INFO csbiInfo;
    HANDLE HCmd = GetStdHandle(STD_OUTPUT_HANDLE);
    GetConsoleScreenBufferInfo(HCmd, &csbiInfo);
    SetConsoleTextAttribute(HCmd, FOREGROUND_BLUE|FOREGROUND_INTENSITY);
    cout << "Le meilleur : " << flush;
    SetConsoleTextAttribute(HCmd, FOREGROUND_GREEN);
    cout << vecalgogenetique[0].nom << flush;
    SetConsoleTextAttribute(HCmd, FOREGROUND_RED|FOREGROUND_INTENSITY);
    cout << " [" << vecalgogenetique[0].fitness << "]" << endl;
}

// CROSSOVER
// -> Echanger les gènes des individus deux à deux pour créer les enfants
// exemple :
// individu 5 : 1-1-0|-0-1-1-1-0
// individu 1 : 0-1-1|-1-0-0-1-1
//
// va donner :
//
// enfant 1 : 1-1-0|-1-0-0-1-1
// enfant 2 : 0-1-1|-0-1-1-1-0

void echange(prgm_vecteur *&population, prgm_vecteur *&buffer)
{
    prgm_vecteur *temp = population; population = buffer; buffer = temp;
}

int main()
{
    srand(unsigned(time(NULL)));

    prgm_vecteur population_a, population_b;
    prgm_vecteur *population, *buffer;

    initialisation_population(population_a, population_b);
    population = &population_a;
    buffer = &population_b;

    for (int i = 0; i < PRGM_MAXESSAIS; i++)// de 0 à 125 :
    {
        calcul_fitness(*population);
        trier_par_fitness(*population);
        affiche_meilleur(*population);
        
        if ((*population)[0].fitness == 0) break;// si le fitness d'un membre = 0, c'est qu'il n'y a pas de meilleur individu et
        // donc, que c'est la cible

        joindre(*population, *buffer);// joindre la population ensemble
        echange(population, buffer);
    }

    // PAS DE SOLUTION
    
    if ( i >= PRGM_MAXESSAIS)
    {
        HANDLE HCmd = GetStdHandle(STD_OUTPUT_HANDLE);
        SetConsoleTextAttribute(HCmd, FOREGROUND_RED|FOREGROUND_INTENSITY);
        cout << "Aucune solution trouv\202e, maximum d'essais d\202pass\202 ..." << endl;
        SetConsoleTextAttribute(HCmd, FOREGROUND_GREEN);
        system("pause");
        return 0;
    }

    // SOLUTION TROUVEE !
    
    HANDLE HCmd = GetStdHandle(STD_OUTPUT_HANDLE);
    SetConsoleTextAttribute(HCmd, FOREGROUND_GREEN|FOREGROUND_INTENSITY);
    cout << "Cible trouv\202e !" << endl;
    SetConsoleTextAttribute(HCmd, FOREGROUND_GREEN);
    system("pause");
    return 0;
}

// neo_00110010101
// 20/02/2005
// IA algorithme génétique
// www.cppfrance.com

// voir aussi : http://fr.wikipedia.org/wiki/Algorithme_g%C3%A9n%C3%A9tique
