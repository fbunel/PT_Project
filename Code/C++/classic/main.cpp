#include <iostream> 
#include <string>
#include <stdlib.h> 
#include <array>
#include <ctime>

#include "montecarlo.h"
#include "lattice.h"
#include "study.h"
#include "color.h"

using namespace std;

int main()
{

clock_t start;
start = clock();

int size = 30;
double electricField = 0;
int equiSample = 800;
int meanSample = 5;
double tempStart = 1.5;
bool startRandom = false;
string basename = "Results/classic";

Montecarlo montecarlo(size, equiSample, meanSample, tempStart, electricField, startRandom);
montecarlo.equilibrate();
montecarlo.calculate();
montecarlo.lattice.saveLatticePart(basename);


cout << "Temps de calcul: " << (clock() - start) / (double)(CLOCKS_PER_SEC) 
     << " secondes" << endl;



return 0;
}
