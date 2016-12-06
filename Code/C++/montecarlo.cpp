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
    size(size),
    equiSample(equiSample),
    meanSample(meanSample),
    temperature(temperature),
    compteur(0),
    accepted(0),
    dmax(0.01),
    gen(std::random_device()()),
    dis(0,1) {

    energies.resize(size*size*size*meanSample);
    orders.resize(size*size*size*meanSample);

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
        flux >> size;
        flux >> equiSample;
        flux >> meanSample;
        flux >> dmax;

        cout << BOLDGREEN 
             << "Montecarlo chargée depuis : " 
             << RESET
             << GREEN 
             << filename 
             << RESET 
             << endl;   

        energies.resize(size*size*size*meanSample);
        orders.resize(size*size*size*meanSample); 
    } else {
        cout << BOLDRED
             << "Impossible d'ouvrir le fichier " 
             << filename 
             << RESET
             << endl;
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
        for (int site = 0; site < pow(size,3); ++site) {           
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
        for (int site = 0; site < pow(size,3); ++site) {
            energieVariation = 0;
            i = cycle * pow(size,3) + site;
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

double Montecarlo :: meanEnergie() const {

    double meanEnergie = 0;
    meanEnergie = accumulate(energies.begin(), energies.end(), 0.0);
   
    return(meanEnergie/pow(size,6)/meanSample-lattice.minimalEnergie);
}

double Montecarlo :: meanOrder() const {

    double meanOrder = 0;
    meanOrder = accumulate(orders.begin(), orders.end(), 0.0);
   
    return(meanOrder/pow(size,3)/meanSample);
}

void Montecarlo :: changeTemperature(const double temp) {

    temperature =  temp;    
}

void Montecarlo :: saveMontecarlo(string basename) const{
    
    string filename = basename + "_montecarlo.save";
    
    ofstream flux(filename.c_str(), ios::out | ios::trunc);

    if(flux) {
        flux << size << endl;
        flux << equiSample << endl;
        flux << meanSample << endl;
        flux << fixed << setprecision(10) << dmax << endl;
        cout << GREEN
             << "     MonteCarlo enregistrées dans : " 
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
