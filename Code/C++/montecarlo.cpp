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
    size(size),
    lattice(size),
    equiSample(equiSample),
    meanSample(meanSample),
    temperature(temperature),
    compteur(0),
    accepted(0),
    dmax(0.01),
    gen(std::random_device()()),
    dis(0,1),
    outputFile(outputFile) {

    energies.resize(size*size*size);    

    if (startRandom) {
        lattice.randomConfiguration();
        dmax = 1;
    } else {
        lattice.groundstateConfiguration();
        dmax = 0.01;
    }
}

double Montecarlo :: latticeEnergie() const {

    std::array<int, 3> site;
    double latticeEnergie = 0;

    //Pour chaque site
    for (int i = 0; i < size; ++i) {
        site[0] = i;
        for (int j = 0; j < size ; ++j) {
            site[1] = j;
            for (int k = 0; k < size; ++k) {           
                site[2] = k;
                latticeEnergie += localEnergie(site);
            }
        }
    }

    latticeEnergie = latticeEnergie/2;

    return(latticeEnergie);
}

double Montecarlo :: localEnergie(const std::array<int, 3> &site) const {

    std::array<std::array<int, 3>, 6> nearestNeighboor;   
    double localEnergie = 0;

    //On récupère les voisins
    lattice.nearestNeighboor(site, nearestNeighboor);
    //Et on calcule l'énergie d'intéraction avec ces voisins
    for (int n = 0; n < 6; ++n) {
        localEnergie += lattice.energie(site, nearestNeighboor[n]);
    }

    return(localEnergie);
}

double Montecarlo :: boltzmannFactor(const double energie) const {

    return(exp(-energie/temperature));
}
