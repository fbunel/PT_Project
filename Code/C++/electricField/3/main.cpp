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
double electricField = 0.2;
int equiSample = 1000;
int meanSample = 5000;
double tempStart = 1;
double tempEnd = 1.3;
double tempSample = 100;
bool startRandom = false;
string basename = "Results/electricTest02";
string outputfile;

Study study(size, electricField, equiSample, meanSample, tempStart, tempEnd, tempSample, startRandom, basename);

study.run();

cout << "Temps de calcul: " << (clock() - start) / (double)(CLOCKS_PER_SEC) 
     << " secondes" << endl;



return 0;
}
