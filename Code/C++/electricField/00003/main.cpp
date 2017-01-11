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
double electricField = 0.0003;
int equiSample = 2000;
int meanSample = 5000;
double tempStart = 1;
double tempEnd = 1.20;
double tempSample = 200;
bool startRandom = false;
string basename = "Results/electricTest00003";
string outputfile;

for (int i = 0; i < 20; ++i)
{
    outputfile = basename + '_' + to_string(i);
    Study study(size, electricField, equiSample, meanSample, tempStart, tempEnd, tempSample, startRandom, outputfile);
    study.run();
}

cout << "Temps de calcul: " << (clock() - start) / (double)(CLOCKS_PER_SEC) 
     << " secondes" << endl;



return 0;
}
