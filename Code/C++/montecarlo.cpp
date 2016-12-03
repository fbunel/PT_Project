#include <math.h> 
#include "montecarlo.h"

using namespace std;

/*Constructeur de base*/
Montecarlo :: Montecarlo(
    int size,
    int equiSample,
    int meanSample,
    double temperature,
    bool startRandom,
    string outputFile) :
    lattice(size),
    size(size),
    equiSample(equiSample),
    meanSample(meanSample),
    temperature(temperature),
    compteur(0),
    accepted(0),
    dmax(0.01),
    gen(std::random_device()()),
    dis(0,1),
    outputFile(outputFile) {

    energies.resize(size*size*size*meanSample);    

    if (startRandom) {
        lattice.randomConfiguration();
        dmax = 1;
    } else {
        lattice.groundstateConfiguration();
        dmax = 0.01;
    }
}

void Montecarlo :: equilibrate() {

    double energieVariation;
    bool moveAccepted;

    accepted = 0;
    compteur = 0;

    for (int cycle = 0; cycle < equiSample; ++cycle) {
        
        cout << std::flush
             << "\rCycle d'équilibrage': " 
             << cycle + 1 
             << '/' 
             << meanSample;

        lattice.shuffleRandomSiteList();
        for (int site = 0; site < pow(size,3); ++site) {           
            moveAccepted = this->MCMove(site, energieVariation);
            this->updateStep(moveAccepted);
        }
    }
    cout << endl << "Ratio d'acceptance : "   << double(accepted)/compteur  << endl;
}

void Montecarlo :: calculate() {

    double energieVariation;
    bool moveAccepted;
    int i;

    accepted = 0;
    compteur = 0;

    for (int cycle = 0; cycle < meanSample; ++cycle) {

        cout << std::flush
             << "\rCycle de calcul: " 
             << cycle + 1 
             << '/' 
             << meanSample;

        lattice.shuffleRandomSiteList();
        for (int site = 0; site < pow(size,3); ++site) {
            energieVariation = 0;
            i = cycle * pow(size,3) + site;
            moveAccepted = this->MCMove(site, energieVariation);
            
            this->updateStep(moveAccepted);
            this->updateEnergie(i, energieVariation);

        }
    }
    cout << endl << "Ratio d'acceptance : "   << double(accepted)/compteur  << endl;
}

double Montecarlo :: meanEnergie() const {

    double meanEnergie = 0;
    meanEnergie = accumulate(energies.begin(), energies.end(), 0.0);
   
    return(meanEnergie/pow(size,6)/meanSample-lattice.minimalEnergie);

}

bool Montecarlo :: MCMove(
    const int site,
    double &energieVariation) {

    //La fonction moveEnergie tente le move et renvoie la variation d'énergie.
    energieVariation = lattice.moveEnergie(site,dmax);

    //On calcule la probabilité d'accepter ce move et on teste cette proba.
    if (dis(gen)<min(double(1),this->boltzmannFactor(energieVariation))) {
        return(true);
    } else {
        lattice.moveCancel();
        energieVariation = 0;
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

void Montecarlo :: updateEnergie(
    const int i,
    const double &energieVariation) {

    if (i==0) {
        energies[0] = lattice.latticeEnergie();
    } else {
        energies[i] = energies[i-1] + energieVariation;
    }
}

double Montecarlo :: boltzmannFactor(const double energie) const {

    return(exp(-energie/temperature));
}
