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
int equiSample = 1000;
int meanSample = 10000;
double tempStart = 1.12;
double tempEnd = 1.13;
double tempSample = 10;
bool startRandom = false;
string outputfile = "save";

Study study(size, equiSample, meanSample, tempStart, tempEnd, tempSample, startRandom, outputfile);

study.run();

cout << "Temps de calcul: " << (clock() - start) / (double)(CLOCKS_PER_SEC) 
     << " secondes" << endl;

return 0;
}
