#include <math.h> 
#include <algorithm> 
#include "lattice.h"

using namespace std;

/*Constructeur de base*/
Lattice :: Lattice(int size) : size(size), gen(std::random_device()()), dis(0,1) {

    latticeArray.resize(size);
    for (int i = 0; i < size; ++i) {
        latticeArray[i].resize(size);
        for (int j = 0; j < size; ++j) {
            latticeArray[i][j].resize(size);
        }
    }

    randomSiteList.resize(size*size*size);

        //On initialise la liste des sites de la lattice
    for (int i = 0; i < size*size*size; ++i) {
        randomSiteList[i] = i;
    }
}

void Lattice :: groundstateConfiguration() {
    
    for (int i = 0; i < size; ++i) {
        for (int j = 0; j < size; ++j) {
            for (int k = 0; k < size; ++k) {
                latticeArray[i][j][k][0] = 0;
                latticeArray[i][j][k][1] = 0;
            }
        }
    }
}

void Lattice :: randomConfiguration() {
    
    for (int i = 0; i < size; ++i) {
        for (int j = 0; j < size; ++j) {
            for (int k = 0; k < size; ++k) {
                randomOrientation(latticeArray[i][j][k]);
            }
        }
    }
}

void Lattice :: randomOrientation(array<double, 2>  &randomOrientation) {
    
    randomOrientation[0] = 2*dis(gen)-1;
    randomOrientation[1] = 2*M_PI*dis(gen);
}

void Lattice :: nearRandomOrientation(
    const double dmax,
    const array<double, 2> &oldAngle,
    array<double, 2> &newAngle) {

    newAngle[0] = fmod(
        fmod(oldAngle[0] + (2*dis(gen)-1)*dmax - 1, 2) + 2,2) - 1;
    newAngle[1] = fmod(
        fmod(oldAngle[1] + (2*dis(gen)-1)*M_PI*dmax, 2*M_PI)+2*M_PI,2*M_PI);
}

void Lattice :: randomSite(std::array<int, 3> &randomLoc) const {

    randomLoc[0] = rand()%size;
    randomLoc[1] = rand()%size;
    randomLoc[2] = rand()%size;
}

void Lattice :: shuffleRandomSiteList() {

    shuffle(
        randomSiteList.begin(), randomSiteList.end(), gen);
}

void Lattice :: shuffledRandomSite(
    const int i,
    std::array<int, 3> randomLoc) const {

    int site = randomSiteList[i];

    randomLoc[2] = site%size;
    randomLoc[1] = (site/size)%size;
    randomLoc[0] = (site/size/size)%size;
}

void Lattice :: nearestNeighboor(
    const std::array<int, 3> &site,
    std::array<std::array<int, 3>, 6> &nearestNeighboor) const {

    for (int i = 0; i < 6; ++i) {
        nearestNeighboor[i] = site;
    }

    nearestNeighboor[0][0] += 1;
    nearestNeighboor[1][0] -= 1;
    nearestNeighboor[2][1] += 1;
    nearestNeighboor[3][1] -= 1;
    nearestNeighboor[4][2] += 1;
    nearestNeighboor[5][2] -= 1;

    for (int i = 0; i < 6; ++i) {
        for (int j = 0; j < 3; ++j) {
            nearestNeighboor[i][j] = (nearestNeighboor[i][j]%size + size)%size;
        }
    }
}

void Lattice :: value(
        const array<int, 3> &site,
        array<double, 2> &angle) const {

    angle = latticeArray[site[0]][site[1]][site[2]];
}

double Lattice :: cosAngle (
    const array<double, 2> &oldAngle,
    const array<double, 2> &newAngle) const {

    return(abs(
        sin(acos(oldAngle[0]))*sin(acos(newAngle[0]))*cos(newAngle[1]-oldAngle[1])
        + oldAngle[0]*newAngle[0]));
}

double Lattice :: energie (
    const std::array<int, 3> &site1, 
    const std::array<int, 3> &site2) const {

    return((1-3*pow(this->cosAngle(
        latticeArray[site1[0]][site1[1]][site1[2]],
        latticeArray[site2[0]][site2[1]][site2[2]]),2))/2);
}

void Lattice :: display () const {

    for (int i = 0; i < size; ++i) {
        cout << latticeArray[i][i][i][0]
             << ' '
             << latticeArray[i][i][i][1]
             << endl;
    }
}