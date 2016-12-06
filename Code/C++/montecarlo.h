#ifndef MONTECARLO
#define MONTECARLO

#include "lattice.h"

#include <string>
#include <random>
#include <math.h> 
#include <iostream>
#include <fstream>
#include <iomanip>
#include "color.h"

       
/* */
class Montecarlo
{
    public:
    /*Constructeur de la classe*/
    Montecarlo(int size, int equiSample, int meanSample, double temperature, bool startRandom);

    /*Constructeur de la classe*/
    Montecarlo(std::string basename);

    /*Equilibre le système en réalisant des MCMove*/
    void equilibrate();

    /*Fais évoluer le système en réalisant des MCMove, remplie les résultats*/
    void calculate();

    /*Equilibre le système en réalisant des MCMove*/
    double meanEnergie() const;

    /*Equilibre le système en réalisant des MCMove*/
    double meanOrder() const;

    /*Change la température du système*/
    void changeTemperature(const double temp);

    /*Sauvegarde MonteCarlo*/
    void saveMontecarlo(std::string basename) const;

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

    /*Mets à jour la valeur de dmax et les deux compteurs*/
    void updateOrderParameter(
        const int i,
        const bool moveAccepted);

    /*Calcule le facteur de Boltzmann associé à l'energie*/
    double boltzmannFactor(const double energie) const;

    /*Taille de la lattice*/
    int size = 30;

    /*Nombre de cycles pour équilibrer*/
    int equiSample;

    /*Nombre de cycles pour calculer*/
    int meanSample ;

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
};

#endif
