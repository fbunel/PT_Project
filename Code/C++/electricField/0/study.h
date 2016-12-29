#ifndef STUDY
#define STUDY



#include "montecarlo.h"

#include <string>
#include <iostream>
#include <fstream>
#include <iomanip>
#include "color.h"
       
/* */
class Study
{
    public:
    /*Constructeur de la classe*/
    Study(
        int size,
        double electricField,
        int equiSample,
        int meanSample,
        double tempStart,
        double tempEnd,
        int tempSample,
        bool startRandom,
        std::string outputFile);

    /*Constructeur de la classe*/
    Study(std::string basename);

    /*L'objet Montecarlo qui comptient l'objet Lattice*/
    Montecarlo montecarlo;

    /*Réalise l'étude*/
    void run();

    private:

    void studySave() const;

    /*Compteur de l'avancée du programme*/
    int compteur;

    /*Nombre de température étudiée*/
    int tempSample;

    /*Tableau des températures*/
    std::vector<double> Temperatures;

    /*Tableau des énergies*/
    std::vector<std::array<double, 2>> Energies;

    /*Tableau des paramètres d'ordre*/
    std::vector<std::array<double, 2>> Orders;
 
    /*Nom de base des fichiers de sortie*/
    std::string outputFile;

};

#endif
