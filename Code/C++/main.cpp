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
int equiSample = 300;
int meanSample = 100;
double tempStart = 1;
double tempEnd = 1;
double tempSample = 1;
bool startRandom = false;
string basename = "equilibrage";
string outputfile;

// for (int stud = 0; stud < 20; ++stud) {
//     outputfile = basename + to_string(stud);
//     Study study(size, electricField, equiSample, meanSample, tempStart, tempEnd, tempSample, startRandom, outputfile);
//     study.run();
// }

Study study(size, electricField, equiSample, meanSample, tempStart, tempEnd, tempSample, startRandom, basename);
study.run();

cout << "Temps de calcul: " << (clock() - start) / (double)(CLOCKS_PER_SEC) 
     << " secondes" << endl;



return 0;
}
