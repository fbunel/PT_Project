#include "lattice.h"

#include <iomanip>

using namespace std;

/*Constructeur de base*/
Lattice :: Lattice(int size) : 
    minimalEnergie(-3),
    size(size),
    orderMatrixInitialised(false),
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

/*Constructeur de base*/
Lattice :: Lattice(std::string basename) : 
    minimalEnergie(-3),
    orderMatrixInitialised(false),
    gen(std::random_device()()),
    dis(0,1) {


    string filename = basename + "_lattice.save";
    ifstream flux(filename.c_str(), ios::in);

    if(flux) {
        flux >> size;
        latticeArray.resize(size);
        for (int i = 0; i < size; ++i) {
            latticeArray[i].resize(size);
            for (int j = 0; j < size; ++j) {
                latticeArray[i][j].resize(size);
                for (int k = 0; k < size; ++k) {
                    flux >> latticeArray[i][j][k][0];
                    flux >> latticeArray[i][j][k][1];
                }
            }
        }
        cout << BOLDGREEN << "Lattice chargée depuis : " << RESET
             << GREEN << filename << RESET 
             << endl;  
    } else {
        cout << BOLDRED << "Impossible d'ouvrir le fichier " << filename 
             << RESET << endl;
    }

    randomSiteList.resize(pow(size,3));

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

    //On change la valeur de l'angle de 
    this->nearRandomOrientation(dmax);

    //On recalcul l'énergie
    energieVariation += this->localEnergie(siteStocked);

    return energieVariation;
}

void Lattice :: moveCancel() {

    latticeArray[siteStocked[0]][siteStocked[1]][siteStocked[2]] = angleStocked;
}

double Lattice :: latticeEnergie() {

    std::array<int, 3> site;
    double latticeEnergie = 0;

    //Pour chaque site
    for (int i = 0; i < size; ++i) {
        site[0] = i;
        for (int j = 0; j < size ; ++j) {
            site[1] = j;
            for (int k = 0; k < size; ++k) {           
                site[2] = k;
                latticeEnergie += localEnergie(site);
            }
        }
    }

    latticeEnergie = latticeEnergie/2;

    return(latticeEnergie);
}

void Lattice :: resetOrderParameterMatrix() {

    for (int im = 0; im < 3; ++im) {
        for (int jm = 0; jm < 3; ++jm) {
            orderMatrix[im][jm] = 0;
        }
    }

    orderMatrixInitialised = false;   
}

void Lattice :: display() const {

    for (int i = 0; i < size; ++i) {
        cout << latticeArray[i][i][i][0]
             << ' '
             << latticeArray[i][i][i][1]
             << endl;
    }
}

void Lattice :: saveLattice(string basename) const{
    
    string filename = basename + "_lattice.save";

    ofstream flux(filename.c_str(), ios::out | ios::trunc);

    if(flux) {
        flux << size << endl;
        for (int i = 0; i < size; ++i) {
            for (int j = 0; j < size; ++j) {
                for (int k = 0; k < size; ++k) {
                    flux << fixed << setprecision(10) 
                         << latticeArray[i][j][k][0] << ' ' << latticeArray[i][j][k][1]
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

void Lattice :: randomOrientation(array<double, 2>  &randomOrientation) {
    
    randomOrientation[0] = 2*dis(gen)-1;
    randomOrientation[1] = 2*M_PI*dis(gen);
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

double Lattice :: energie(
    const std::array<int, 3> &site1, 
    const std::array<int, 3> &site2) const {

    return((1-3*pow(this->cosAngle(
        latticeArray[site1[0]][site1[1]][site1[2]],
        latticeArray[site2[0]][site2[1]][site2[2]]),2))/2);
}

void Lattice :: initialiseOrderMatrix() {

    array<double, 3> cartesian;

    for (int il = 0; il < size; ++il) {
        for (int jl = 0; jl < size; ++jl) {
            for (int kl = 0; kl < size; ++kl) {
                sphericalToCartesian(latticeArray[il][jl][kl], cartesian);
                for (int im = 0; im < 3; ++im) {
                    for (int jm = 0; jm < 3; ++jm) {
                        orderMatrix[im][jm] += cartesian[im]*cartesian[jm];
                    }
                }

            }
        }
    }

    for (int im = 0; im < 3; ++im) {
        orderMatrix[im][im] -= pow(size,3)/3;
    }

    orderMatrixInitialised = true;
}

void Lattice :: updateOrderMatrix() {

    array<double, 3> cartesian;

    //On enlève l'ancien angle
    sphericalToCartesian(angleStocked, cartesian);

    for (int im = 0; im < 3; ++im) {
        for (int jm = 0; jm < 3; ++jm) {
            orderMatrix[im][jm] -= cartesian[im]*cartesian[jm];
        }
    }

    //On ajoute le nouveau
    sphericalToCartesian(
        latticeArray[siteStocked[0]][siteStocked[1]][siteStocked[2]], cartesian);

    for (int im = 0; im < 3; ++im) {
        for (int jm = 0; jm < 3; ++jm) {
            orderMatrix[im][jm] += cartesian[im]*cartesian[jm];
        }
    }
}

double Lattice :: orderParameter() {

    double orderParameter = 0;

    if (orderMatrixInitialised) {
        updateOrderMatrix();
    } else {
        initialiseOrderMatrix();
    }

    //Calcul du determinant
    orderParameter = 
          orderMatrix[0][0]*orderMatrix[1][1]*orderMatrix[2][2]
        + orderMatrix[1][0]*orderMatrix[2][1]*orderMatrix[0][2]
        + orderMatrix[2][0]*orderMatrix[0][1]*orderMatrix[1][2]
        - orderMatrix[0][2]*orderMatrix[1][1]*orderMatrix[2][0]
        - orderMatrix[1][2]*orderMatrix[2][1]*orderMatrix[0][0]
        - orderMatrix[2][2]*orderMatrix[0][1]*orderMatrix[1][0];

    //Le determinant vaut 2*S^3*size^9/9
    orderParameter = pow(max(0.,orderParameter)*27/2/pow(size,9),1.0/3);

    return(orderParameter);
}

void Lattice :: sphericalToCartesian(
        const array<double, 2> &spherical,
        array<double, 3> &cartesian) const {
    
    double sinTheta = sin(acos(spherical[0]));
    cartesian[0] = sinTheta*cos(spherical[1]);
    cartesian[1] = sinTheta*sin(spherical[1]);
    cartesian[2] = spherical[0];
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
