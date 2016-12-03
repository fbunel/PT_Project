#ifndef MONTECARLO
#define MONTECARLO

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

#include <iostream>
#include <string>
#include <random>
#include <array>

#include "lattice.h"
       
/* */
class Montecarlo
{
    public:
    /*Constructeur de la classe*/
    Montecarlo(int size, int equiSample, int meanSample, double temperature, bool startRandom, std::string outputFile);

    /*Equilibre le système en réalisant des MCMove*/
    void equilibrate();

    /*Fais évoluer le système en réalisant des MCMove, remplie les résultats*/
    void calculate();

    /*Equilibre le système en réalisant des MCMove*/
    double meanEnergie() const;


    /*La lattice*/
    Lattice lattice;

    private:

    /*Essaie un move de MonteCarlo sur un site de la lattice et renvoie l'energie*/
    bool MCMove(const int site, double &energieVariation);

    /*Mets à jour la valeur de dmax et les deux compteurs*/
    void updateStep(const bool moveAccepted);

    /*Mets à jour la valeur de l'énergie*/
    void updateEnergie(
        const int i,
        const double &energieVariation);

    /*Calcule le facteur de Boltzmann associé à l'energie*/
    double boltzmannFactor(const double energie) const;

    /*Taille de la lattice*/
    const int size = 30;

    /*Nombre de cycles pour équilibrer*/
    const int equiSample;

    /*Nombre de cycles pour calculer*/
    const int meanSample ;

    /*Température*/
    double temperature;

    /*Compteur de pas*/
    int compteur;

    /*Compteur de pas acceptés*/
    int accepted;

    /*Distance maximale aux pas précédent*/
    double dmax ;

    /*Tableau des énergies*/
    std::vector<double> energies;

    /*Tableau des paramètres d'ordre*/
    std::vector<double> orders;
 
    /*Seed et générateur de nombre aléatoire*/
    std::mt19937 gen;
    std::uniform_real_distribution<double> dis;

    /*Nom de base des fichiers de sortie*/
    const std::string outputFile;

};

#endif
