#include <iostream> 
#include <string>
#include <stdlib.h> 
#include <array>

#include "montecarlo.h"
#include "lattice.h"

using namespace std;

int main()
{

int size = 30;
int equiSample = 100;
int meanSample = 100;
double temperature = 0.01;
bool startRandom = false;
string outputfile = "save";


Montecarlo montecarlo(
    size, equiSample, meanSample, temperature, startRandom, outputfile);
montecarlo.equilibrate();
montecarlo.calculate();
double meanEnergie;
meanEnergie = montecarlo.meanEnergie();
cout << meanEnergie << endl;

// double energieVariation;

// Lattice lattice(3);
// lattice.shuffleRandomSiteList();
// energieVariation = lattice.moveEnergie(0,0.1);

// cout << energieVariation << endl;
return 0;
}
