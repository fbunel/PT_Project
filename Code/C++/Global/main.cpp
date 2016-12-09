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
int meanSample = 5000;
double tempStart = 0.01;
double tempEnd = 2.01;
double tempSample = 200;
bool startRandom = false;
string outputfile = "global";

Study study(size, equiSample, meanSample, tempStart, tempEnd, tempSample, startRandom, outputfile);

study.run();

cout << "Temps de calcul: " << (clock() - start) / (double)(CLOCKS_PER_SEC) 
     << " secondes" << endl;

return 0;
}
