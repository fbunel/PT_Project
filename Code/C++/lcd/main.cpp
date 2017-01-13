#include <iostream> 
#include <string>
#include <stdlib.h> 
#include <array>
#include <ctime>

#include "montecarlo.h"
#include "lattice.h"
#include "color.h"

using namespace std;

int main()
{

clock_t start;
start = clock();

int size = 30;
double electricField = 0.5;
int equiSample = 20000;
double temp = 0.1;
string basename = "lcd";


Montecarlo montecarlo(size, equiSample, temp, electricField);
montecarlo.equilibrate();
montecarlo.lattice.saveLattice(basename);

cout << "Temps de calcul: " << (clock() - start) / (double)(CLOCKS_PER_SEC) 
     << " secondes" << endl;

return 0;
}
