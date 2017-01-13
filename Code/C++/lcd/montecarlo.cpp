#include "montecarlo.h"
#include <algorithm>

using namespace std;

/*Constructeur de base*/
Montecarlo :: Montecarlo(
    int size,
    int equiSample,
    double temperature,
    double electricField) :
    lattice(size, electricField),
    equiSample(equiSample),
    cycleMove(pow(size,3)),
    temperature(temperature),
    compteur(0),
    accepted(0),
    dmax(0.01),
    gen(std::random_device()()),
    dis(0,1) {

    lattice.groundstateConfiguration();
    dmax = 0.01;
}

void Montecarlo :: equilibrate() {

    double energieVariation;
    bool moveAccepted;

    accepted = 0;
    compteur = 0;

    for (int cycle = 0; cycle < equiSample; ++cycle) {
        
        cout << std::flush
             << BLUE 
             << "\r     Cycle d'équilibrage': " 
             << RESET << BOLDBLUE
             << cycle + 1 
             << '/' 
             << equiSample 
             << RESET;

        lattice.shuffleRandomSiteList();
        for (int site = 0; site < cycleMove; ++site) {           
            moveAccepted = this->MCMove(site, energieVariation);
            this->updateStep(moveAccepted);
        }
    }
    cout << endl 
         << MAGENTA 
         << "          Ratio d'acceptance : " 
         << double(accepted)/compteur  
         << RESET << endl;
}

bool Montecarlo :: MCMove(
    const int site,
    double &energieVariation) {

    //La fonction moveEnergie tente le move et renvoie la variation d'énergie.
    energieVariation = lattice.moveEnergie(site,dmax);

    //On calcule la probabilité d'accepter ce move et on teste cette proba.
    if (dis(gen)<min(double(1),this->boltzmannFactor(energieVariation))) {
        lattice.applyBC();
        return(true);
    } else {
        lattice.moveCancel();
        energieVariation = 0;
        lattice.applyBC();
        return(false);
    }
}

void Montecarlo :: updateStep(const bool moveAccepted) {

    compteur ++;
    dmax = max(0.01, min(1., dmax + (moveAccepted-1./2)/100000));

    if (moveAccepted) {
        accepted++;
    }
}

double Montecarlo :: boltzmannFactor(const double energie) const {

    return(exp(-energie/temperature));
}
