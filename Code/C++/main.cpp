#include <iostream> 
#include <string>
#include <stdlib.h> 
#include <array>

#include "montecarlo.h"
#include "lattice.h"
#include "study.h"
#include "color.h"

using namespace std;

int main()
{

int size = 30;
int equiSample = 10;
int meanSample = 20;
double tempStart = 0.01;
double tempEnd = 2.2;
double tempSample = 20;
bool startRandom = false;
string outputfile = "save";

Study study(size, equiSample, meanSample, tempStart, tempEnd, tempSample, startRandom, outputfile);


study.run();

return 0;
}
