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
    Montecarlo(int size, int equiSample, double temperature, double electricField);


    /*Equilibre le système en réalisant des MCMove*/
    void equilibrate();

    /*La lattice*/
    Lattice lattice;

    private:

    /*Essaie un move de MonteCarlo sur un site de la lattice et renvoie l'energie*/
    bool MCMove(const int site, double &energieVariation);

    /*Mets à jour la valeur de dmax et les deux compteurs*/
    void updateStep(const bool moveAccepted);

    /*Calcule le facteur de Boltzmann associé à l'energie*/
    double boltzmannFactor(const double energie) const;

    /*Nombre de cycles pour équilibrer*/
    int equiSample;

    /*Nombre de step dans un cycle*/
    int cycleMove;

    /*Température*/
    double temperature;

    /*Compteur de pas*/
    int compteur;

    /*Compteur de pas acceptés*/
    int accepted;

    /*Distance maximale aux pas précédent*/
    double dmax ;

    /*Seed et générateur de nombre aléatoire*/
    std::mt19937 gen;
    std::uniform_real_distribution<double> dis;
};

#endif
