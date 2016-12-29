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
    Montecarlo(int size, int equiSample, int meanSample, double temperature, double electricField, bool startRandom);

    /*Constructeur de la classe*/
    Montecarlo(std::string basename);

    /*Equilibre le système en réalisant des MCMove*/
    void equilibrate();

    /*Fais évoluer le système en réalisant des MCMove, remplie les résultats*/
    void calculate();

    /*Calcule la moyenne et la std*/
    void meanEnergie(std::array<double, 2> &meanstdEnergie) const;

    /*Calcule la moyenne et la std*/
    void meanOrder(std::array<double, 2> &meanstdOrder) const;

    /*Calcule un histogramme des énergies et le sotcke dans un fichier*/
    void histoEnergie(
        const std::string basename, const int histoDots, const int compteur) const ;

    /*Change la température du système*/
    void changeTemperature(const double temp);

    /*Export*/
    void exportArray(const std::string basename, const int compteur) const;

    /*Sauvegarde MonteCarlo*/
    void saveMontecarlo(const std::string basename) const;

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

    /*Mets à jour la valeur du paramètre d'ordre*/
    void updateOrderParameter(
        const int i,
        const bool moveAccepted);

    /*Calcule le facteur de Boltzmann associé à l'energie*/
    double boltzmannFactor(const double energie) const;

    /*Nombre de cycles pour équilibrer*/
    int equiSample;

    /*Nombre de cycles pour calculer*/
    int meanSample;

    /*Nombre de step dans un cycle*/
    int cycleMove;

    /*Nombre de step de calcul*/
    int totalMove;

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
