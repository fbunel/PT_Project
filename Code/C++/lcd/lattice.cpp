#include "lattice.h"

#include <iomanip>

using namespace std;

/*Constructeur de base*/
Lattice :: Lattice(int size, double electricField) : 
    size(size),
    electricField(electricField),
    gen(std::random_device()()),
    dis(0,1) {

    latticeArray.resize(size);
    for (int i = 0; i < size; ++i) {
        latticeArray[i].resize(size);
        for (int j = 0; j < size; ++j) {
            latticeArray[i][j].resize(size);
        }
    }

    //On initialise la liste des sites de la lattice
    randomSiteList.resize(pow(size,3));
    for (int i = 0; i < size*size*size; ++i) {
        randomSiteList[i] = i;
    }
}

void Lattice :: groundstateConfiguration() {
    
    for (int i = 0; i < size; ++i) {
        for (int j = 0; j < size; ++j) {

            for (int k = 0; k < size; ++k) {
                latticeArray[i][j][k][0] = 1;
                latticeArray[i][j][k][1] = 0;
            }
        }
    }
}

void Lattice :: shuffleRandomSiteList() {

    shuffle(
        randomSiteList.begin(), randomSiteList.end(), gen);
}

double Lattice :: moveEnergie(
    const int i,
    const double dmax) {

    double energieVariation = 0;

    //On sélectionne le bon site et on le stocke
    this->shuffledRandomSite(i, siteStocked);

    //On stocke la valeur de l'ancien angle
    this->value(siteStocked, angleStocked);

    //On calcule l'énergie
    energieVariation -= this->localEnergie(siteStocked);
    energieVariation -= this->fieldEnergie(siteStocked);

    //On change la valeur de l'angle de 
    this->nearRandomOrientation(dmax);

    //On recalcul l'énergie
    energieVariation += this->localEnergie(siteStocked);
    energieVariation += this->fieldEnergie(siteStocked);

    return energieVariation;
}

void Lattice :: moveCancel() {

    latticeArray[siteStocked[0]][siteStocked[1]][siteStocked[2]] = angleStocked;
}

void Lattice :: applyBC() {

    if (siteStocked[2]==0) {
        latticeArray[siteStocked[0]][siteStocked[1]][siteStocked[2]][0]=0;
        latticeArray[siteStocked[0]][siteStocked[1]][siteStocked[2]][1]=0;
    }
    else if (siteStocked[2]==size-1) {
        latticeArray[siteStocked[0]][siteStocked[1]][siteStocked[2]][0]=0;
        latticeArray[siteStocked[0]][siteStocked[1]][siteStocked[2]][1]=M_PI/2;
    }
    
}


void Lattice :: saveLattice(string basename) const{
    
    string filename = basename + "_lattice.dat";

    ofstream flux(filename.c_str(), ios::out | ios::trunc);

    if(flux) {
        for (int i = 0; i < size; ++i) {
            for (int j = 0; j < size; ++j) {
                for (int k = 0; k < size; ++k) {
                    flux << fixed << setprecision(10) 
                        << i << " " 
                        << j << " "
                        << k << " " 
                        << latticeArray[i][j][k][0] << " " 
                        << latticeArray[i][j][k][1]
                        << endl;
                }
            }
        }
        cout << GREEN
             << "     Lattice enregistrées dans : "  << filename.c_str() 
             << RESET << endl;  
    } else {
        cout << BOLDRED << "Impossible d'ouvrir le fichier " << filename 
             << RESET << endl;
    }

}

void Lattice :: shuffledRandomSite(
    const int i,
    std::array<int, 3> &site) const {

    int randomSite = randomSiteList[i];

    site[2] = randomSite%size;
    site[1] = (randomSite/size)%size;
    site[0] = (randomSite/size/size)%size;
}

void Lattice :: nearRandomOrientation(const double dmax) {

    latticeArray[siteStocked[0]][siteStocked[1]][siteStocked[2]][0] = fmod(
        fmod(angleStocked[0] + (2*dis(gen)-1)*dmax - 1, 2) + 2,2) - 1;
    latticeArray[siteStocked[0]][siteStocked[1]][siteStocked[2]][1] = fmod(
        fmod(angleStocked[1] + (2*dis(gen)-1)*M_PI*dmax, 2*M_PI)+2*M_PI,2*M_PI);
}

double Lattice :: localEnergie(const std::array<int, 3> &site) {
   
    double localEnergie = 0;

    //On récupère les voisins
    this->nearestNeighboor(site);
    //Et on calcule l'énergie d'intéraction avec ces voisins
    for (int n = 0; n < 6; ++n) {
        localEnergie += energie(site, nearestNeighboorStocked[n]);
    }

    return(localEnergie);
}

double Lattice :: fieldEnergie(
    const std::array<int, 3> &site1) const {

    return(
        electricField*(1-3*pow(latticeArray[site1[0]][site1[1]][site1[2]][0],2))/2);
}

double Lattice :: energie(
    const std::array<int, 3> &site1, 
    const std::array<int, 3> &site2) const {

    return((1-3*pow(this->cosAngle(
        latticeArray[site1[0]][site1[1]][site1[2]],
        latticeArray[site2[0]][site2[1]][site2[2]]),2))/2);
}

void Lattice :: nearestNeighboor(const std::array<int, 3> &site) {

    for (int i = 0; i < 6; ++i) {
        nearestNeighboorStocked[i] = site;
    }

    nearestNeighboorStocked[0][0] += 1;
    nearestNeighboorStocked[1][0] -= 1;
    nearestNeighboorStocked[2][1] += 1;
    nearestNeighboorStocked[3][1] -= 1;
    nearestNeighboorStocked[4][2] += 1;
    nearestNeighboorStocked[5][2] -= 1;

    for (int i = 0; i < 6; ++i) {
        for (int j = 0; j < 3; ++j) {
            nearestNeighboorStocked[i][j] =
                (nearestNeighboorStocked[i][j]%size + size)%size;
        }
    }
}

double Lattice :: cosAngle(
    const array<double, 2> &oldAngle,
    const array<double, 2> &newAngle) const {

    return(abs(
        sin(acos(oldAngle[0]))*sin(acos(newAngle[0]))*cos(newAngle[1]-oldAngle[1])
        + oldAngle[0]*newAngle[0]));
}

void Lattice :: value(
        const array<int, 3> &site,
        array<double, 2> &angle) const {

    angle = latticeArray[site[0]][site[1]][site[2]];
}
