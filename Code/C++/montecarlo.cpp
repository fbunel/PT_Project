#include "montecarlo.h"

using namespace std;

/*Constructeur de base*/
Montecarlo :: Montecarlo(
    int size,
    int equiSample,
    int meanSample,
    double temperature,
    bool startRandom) :
    lattice(size),
    equiSample(equiSample),
    meanSample(meanSample),
    cycleMove(pow(size,3)),
    totalMove(cycleMove*meanSample),
    temperature(temperature),
    compteur(0),
    accepted(0),
    dmax(0.01),
    gen(std::random_device()()),
    dis(0,1) {

    energies.resize(totalMove);
    orders.resize(totalMove);

    if (startRandom) {
        lattice.randomConfiguration();
        dmax = 1;
    } else {
        lattice.groundstateConfiguration();
        dmax = 0.01;
    }
}

/*Constructeur de base*/
Montecarlo :: Montecarlo(string basename) :
    lattice(basename),
    compteur(0),
    accepted(0),
    gen(std::random_device()()),
    dis(0,1) {

    string filename = basename + "_montecarlo.save";

    ifstream flux(filename.c_str(), ios::in);

    if(flux) {
        flux >> equiSample;
        flux >> meanSample;
        flux >> cycleMove;
        flux >> totalMove;
        flux >> dmax;

        cout << BOLDGREEN << "Montecarlo chargée depuis : " << RESET
             << GREEN << filename 
             << RESET << endl;   

        energies.resize(totalMove);
        orders.resize(totalMove); 
    } else {
        cout << BOLDRED << "Impossible d'ouvrir le fichier " << filename 
             << RESET << endl;
    }

}

void Montecarlo :: equilibrate() {

    double energieVariation;
    bool moveAccepted;

    accepted = 0;
    compteur = 0;

    for (int cycle = 0; cycle < equiSample; ++cycle) {
        
        cout << std::flush
             << BLUE 
             << "\r     Cycle d'équilibrage': " 
             << RESET << BOLDBLUE
             << cycle + 1 
             << '/' 
             << equiSample 
             << RESET;

        lattice.shuffleRandomSiteList();
        for (int site = 0; site < cycleMove; ++site) {           
            moveAccepted = this->MCMove(site, energieVariation);
            this->updateStep(moveAccepted);
        }
    }
    cout << endl 
         << MAGENTA 
         << "          Ratio d'acceptance : " 
         << double(accepted)/compteur  
         << RESET << endl;
}

void Montecarlo :: calculate() {

    double energieVariation;
    bool moveAccepted;
    int i;

    accepted = 0;
    compteur = 0;

    lattice.resetOrderParameterMatrix();

    for (int cycle = 0; cycle < meanSample; ++cycle) {

        cout << std::flush
             << BLUE 
             << "\r     Cycle de calcul: " 
             << RESET << BOLDBLUE
             << cycle + 1 
             << '/' 
             << meanSample 
             << RESET;

        lattice.shuffleRandomSiteList();
        for (int site = 0; site < cycleMove; ++site) {
            energieVariation = 0;
            i = cycle * cycleMove + site;
            moveAccepted = this->MCMove(site, energieVariation);
            
            this->updateStep(moveAccepted);
            this->updateEnergie(i, energieVariation);
            this->updateOrderParameter(i, moveAccepted);
        }
    }
    cout << endl 
         << MAGENTA 
         << "          Ratio d'acceptance : " 
         << double(accepted)/compteur  
         << RESET << endl;
}

void Montecarlo :: meanEnergie(array<double, 2> &meanstdEnergie) const {

    meanstdEnergie[0] = 0;
    meanstdEnergie[1] = 0;

    for (int i = 0; i < totalMove; ++i) {
        meanstdEnergie[0] += energies[i];
    }

    meanstdEnergie[0] = meanstdEnergie[0]/totalMove;

    for (int i = 0; i < totalMove; ++i) {
        meanstdEnergie[1] += pow(energies[i]-meanstdEnergie[0],2);
    }

    meanstdEnergie[1] = sqrt(meanstdEnergie[1]/totalMove);

    meanstdEnergie[0] = meanstdEnergie[0]/cycleMove - lattice.minimalEnergie;
    meanstdEnergie[1] = meanstdEnergie[1]/cycleMove;
}

void Montecarlo :: meanOrder(array<double, 2> &meanstdOrder) const {

    meanstdOrder[0] = 0;
    meanstdOrder[1] = 0;

    for (int i = 0; i < totalMove; ++i) {
        meanstdOrder[0] += orders[i];
    }

    meanstdOrder[0] = meanstdOrder[0]/totalMove;

    for (int i = 0; i < totalMove; ++i) {
        meanstdOrder[1] += pow(orders[i]-meanstdOrder[0],2);
    }

    meanstdOrder[1] = sqrt(meanstdOrder[1]/totalMove);
}

void Montecarlo :: changeTemperature(const double temp) {

    temperature =  temp;    
}

void Montecarlo :: saveMontecarlo(string basename) const{
    
    string filename = basename + "_montecarlo.save";
    
    ofstream flux(filename.c_str(), ios::out | ios::trunc);

    if(flux) {
        flux << equiSample << endl;
        flux << meanSample << endl;
        flux << cycleMove << endl;
        flux << totalMove << endl;
        flux << fixed << setprecision(10) << dmax 
             << endl;
        cout << GREEN << "     MonteCarlo enregistrées dans : " << filename.c_str()
             << RESET << endl;  
    } else {
        cout << BOLDRED << "Impossible d'ouvrir le fichier " << filename 
             << RESET << endl;
    }
}

bool Montecarlo :: MCMove(
    const int site,
    double &energieVariation) {

    //La fonction moveEnergie tente le move et renvoie la variation d'énergie.
    energieVariation = lattice.moveEnergie(site,dmax);

    //On calcule la probabilité d'accepter ce move et on teste cette proba.
    if (dis(gen)<min(double(1),this->boltzmannFactor(energieVariation))) {
        return(true);
    } else {
        lattice.moveCancel();
        energieVariation = 0;
        return(false);
    }
}

void Montecarlo :: updateStep(const bool moveAccepted) {

    compteur ++;
    dmax = max(0.01, min(1., dmax + (moveAccepted-1./2)/100000));

    if (moveAccepted) {
        accepted++;
    }
}

void Montecarlo :: updateEnergie(
    const int i,
    const double &energieVariation) {

    if (i==0) {
        energies[0] = lattice.latticeEnergie();
    } else {
        energies[i] = energies[i-1] + energieVariation;
    }
}

void Montecarlo ::  updateOrderParameter(
    const int i,
    const bool moveAccepted) {

    if (moveAccepted || i==0) {
        orders[i] = lattice.orderParameter();
    } else {
        orders[i] = orders[i-1];
    }
}

double Montecarlo :: boltzmannFactor(const double energie) const {

    return(exp(-energie/temperature));
}
