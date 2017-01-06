#ifndef LATTICE
#define LATTICE

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

#include <string>
#include <random>
#include <array>
#include <iostream>
#include <fstream>
#include <iomanip>
#include <math.h> 
#include <algorithm>
#include "color.h"
       
class Lattice
{
    public:
    /*Constructeur de la classe
    - size : la taille de la lattice*/
    Lattice(int size, double electricField);

    /*Constructeur de la classe
    - filename : Nom du fichier à partir duquel on extrait la lattice */
    Lattice(std::string basename);

    /*Initialise la lattice dans un état fondamental*/
    void groundstateConfiguration();

    /*Initialise la lattice dans un aléatoire, avec l'aide de randomOrientation*/
    void randomConfiguration();

    /*Shuffle la liste randomSiteList des sites*/
    void shuffleRandomSiteList();

    /*Réalise un move de MonteCarlo du site i, renvoie la variation d'énergie
    - i : site de la lattice (de randomSiteList)
    - dmax :  distance à l'angle précédant maximale*/
    double moveEnergie(
        const int i,
        const double dmax);

    /*Calcul et renvoie le paramètre d'ordre*/
    double orderParameter();

    /*Annule le move qu'on a tenté*/
    void moveCancel();

    /*Calcule l'énergie de la lattice*/
    double latticeEnergie();

    /*Fonction qui permet de reset la matrice du paramètre d'ordre*/
    void resetOrderParameterMatrix();

    /*Fonction qui display la diagonale de la lattice*/
    void display() const;

    /*Fonction qui sauvegarde toute la classe dans un fichier
    - filename : nom du fichier dans lequel on sauvegarde la lattice*/
    void saveLattice(std::string basename) const;

    /*Energie minimale de la lattice*/
    const double minimalEnergie;


    private:

    /*Renvoie une orientation aléatoire de la sphère unité
    - randomOrientation : array dans lequel on stocke le résultat
    (fonction uniquement appelée pour randomConfiguration)
        Les orientations tirées au hasard sont uniformément répartis sur la demi-sphère
        unité supérieure : http://mathworld.wolfram.com/SpherePointPicking.html
    */
    void randomOrientation(std::array<double, 2> &randomOrientation);

    /*Renvoie le site demandé de la liste ordonnée
    - i : site de la lattice (de randomSiteList)
    - randomLoc : array dans lequel on stocke le résultat*/
    void shuffledRandomSite(
        const int i,
        std::array<int, 3> &site) const;

    /* Change la valeur de l'angle du tableau d'une distance dmax
    utilise directement angleStocked et siteStocked*/
    void nearRandomOrientation(const double dmax);

    /*Calcule  l'énergie d'interaction avec ses voisins d'un site
    - site : site de la lattice*/ 
    double localEnergie(const std::array<int, 3> &site);

    /*Calcule l'énergie d'intéraction avec un champ électrique dirigée selon z*/
    double fieldEnergie(
        const std::array<int, 3> &site1) const;

    /*Calcule l'énergie d'intéraction entre deux sites*/
    double energie(
        const std::array<int, 3> &site1, 
        const std::array<int, 3> &site2) const;

    /*Remplie la liste des plus proches voisins nearestNeighboor
    - site : site de la lattice*/
    void nearestNeighboor(const std::array<int, 3> &site);

    /* Initialise la matrice du paramètre d'ordre*/
    void initialiseOrderMatrix();

    /* Met à jour la matrice du paramètre d'ordre*/
    void updateOrderMatrix();

    /*Réalise le changement de variable de sphérique vers cartesien*/
    void sphericalToCartesian(
        const std::array<double, 2> &spherical,
        std::array<double, 3> &cartesian) const;

    /*Calcule le cosinus de l'angle entre les deux directions données en argument*/
    double cosAngle(
        const std::array<double, 2> &oldAngle, 
        const std::array<double, 2> &newAngle) const;

    /*Renvoie les valeurs de latticeArray associées au site donné en argument*/
    void value(
        const std::array<int, 3> &site,
        std::array<double, 2> &angle) const;

    
    /*Taille de la lattice*/
    int size;

    /*Intensité du champ électrique*/
    double electricField;

    /*La lattice*/
    std::vector< std::vector<std::vector<std::array<double, 2>>>> latticeArray;

    /*Liste désordonnée des sites de la lattices*/
    std::vector<int> randomSiteList;

    /*Ancienne valeur de l'angle pour stockage*/
    std::array<double, 2> angleStocked;

    /*Site de la lattice associée pour stockage*/
    std::array<int, 3> siteStocked;

    /*Variable dans laquelle on stocke les plus proches voisins d'un site*/
    std::array<std::array<int, 3>, 6> nearestNeighboorStocked;

    /*Variable dans laquelle on stocke les plus proches voisins d'un site*/
    std::array<std::array<double, 3>, 3> orderMatrix;

    /*Variable qui sait si la matrice d'ordre a été initialisée ou non*/
    bool orderMatrixInitialised;

    /*Seed et générateur de nombre aléatoire*/
    std::mt19937 gen;
    std::uniform_real_distribution<double> dis;
};

#endif


