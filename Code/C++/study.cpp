#include "study.h"

using namespace std;

/*Constructeur de base*/
Study :: Study(
    int size, 
    int equiSample,
    int meanSample,
    double tempStart,
    double tempEnd,
    double tempSample,
    bool startRandom,
    string outputFile) :
    montecarlo(size, equiSample, meanSample, tempStart, startRandom),
    compteur(0),
    tempSample(tempSample),
    outputFile(outputFile) {

    Temperatures.resize(tempSample);
    Energies.resize(tempSample);
    Orders.resize(tempSample);

    for (int t = 0; t < tempSample; ++t) {
        Temperatures[t] = tempStart + (tempEnd - tempStart)*t/tempSample;
    }
}

/*Constructeur de base*/
Study :: Study(string basename) :
    montecarlo(basename) {

    string filename = basename + "_study.save";
    ifstream flux(filename.c_str(), ios::in);

    if(flux) {
        flux >> outputFile;
        flux >> tempSample;
        flux >> compteur;

        Temperatures.resize(tempSample);
        Energies.resize(tempSample);
        Orders.resize(tempSample);
        for (int t = 0; t < tempSample; ++t) {
                    flux >> Temperatures[t];
                    flux >> Energies[t];
                    flux >> Orders[t];
        }
        cout << BOLDGREEN 
             << "Study chargée depuis : " 
             << RESET
             << GREEN 
             << filename 
             << RESET 
             << endl;   
    } else {
        cout << BOLDRED
             << "Impossible d'ouvrir le fichier " 
             << filename 
             << RESET
             << endl;
    }
}


void Study :: run() {

    if (compteur == 0) {
        cout << "Equilibrage initial à la température : " << Temperatures[0] << endl;
        montecarlo.equilibrate();
    }

    while(compteur < tempSample){
        cout << endl 
             << BOLDYELLOW 
             << "Temperature " 
             << compteur + 1 
             << '/' 
             << tempSample
             << " : " 
             << RESET 
             << YELLOW 
             << Temperatures[compteur] 
             << RESET
             << endl;

        montecarlo.changeTemperature(Temperatures[compteur]);
        montecarlo.equilibrate();
        montecarlo.calculate();
        Energies[compteur] = montecarlo.meanEnergie();
        Orders[compteur] = montecarlo.meanOrder();

        cout << CYAN
             << "     Paramètre d'ordre : "
             << Orders[compteur]
             << RESET
             << endl;

        cout << CYAN
             << "     Energies : "
             << Energies[compteur]
             << RESET
             << endl;

        studySave();
        compteur++;
    }
}

void Study :: studySave() const{

    //Sauvegarde de la lattice
    montecarlo.lattice.saveLattice(outputFile);
    montecarlo.saveMontecarlo(outputFile);

    //Sauvegarde de l'état de Study
    string filename = outputFile + "_study.save";
    ofstream flux(filename.c_str(), ios::out | ios::trunc);
    if(flux) {
        flux << outputFile << endl;
        flux << tempSample << endl;
        flux << compteur << endl;
        for (int t = 0; t < tempSample ; ++t) {
            flux << fixed
                 << setprecision(10)
                 << Temperatures[t]
                 << ' '
                 << Energies[t]
                 << ' '
                 << Orders[t]
                 << endl;
        }
        cout << GREEN
             << "     Study enregistrée dans : "
             << filename.c_str() 
             << RESET
             << endl;  
    } else {
        cout << BOLDRED
             << "Impossible d'ouvrir le fichier " 
             << filename 
             << RESET
             << endl;
    }
}
