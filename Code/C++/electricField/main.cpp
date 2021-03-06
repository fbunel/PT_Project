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
double electricField = 0.01;
int equiSample = 5000;
int meanSample = 1;
double tempStart = 1;
double tempEnd = 1.20;
double tempSample = 1;
bool startRandom = false;
string basename = "Results/electricTest0001";


Study study(size, electricField, equiSample, meanSample, tempStart, tempEnd, tempSample, startRandom, basename);
study.run();


cout << "Temps de calcul: " << (clock() - start) / (double)(CLOCKS_PER_SEC) 
     << " secondes" << endl;



return 0;
}
