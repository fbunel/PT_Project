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
int equiSample = 5000;
int meanSample = 25000;
double tempStart = 1.10;
double tempEnd = 1.14;
double tempSample = 100;
bool startRandom = false;
string basename = "Results/histo";
string outputfile;

Study study(size, electricField, equiSample, meanSample, tempStart, tempEnd, tempSample, startRandom, basename);
study.run();

cout << "Temps de calcul: " << (clock() - start) / (double)(CLOCKS_PER_SEC) 
     << " secondes" << endl;



return 0;
}
