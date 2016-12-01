#include <iostream> 
#include <string>
#include <stdlib.h> 
#include <array>

#include "montecarlo.h"

using namespace std;

int main()
{

int size = 30;
int equiSample = 500;
int meanSample = 500;
double temperature = 0.1;
bool startRandom = false;
string outputfile = "save";


Montecarlo montecarlo(
    size, equiSample, meanSample, temperature, startRandom, outputfile);

double energie;
energie = montecarlo.latticeEnergie();



cout << energie << endl;
return 0;
}
