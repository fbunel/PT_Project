#ifndef LATTICE
#define LATTICE

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

#include <iostream>
#include <string>
#include <random>
#include <array>
       
class Lattice
{
    public:
    /*Constructeur de la classe*/
    Lattice(int size);

    /*Initialise la lattice dans un état fondamental*/
    void groundstateConfiguration();

    /*Initialise la lattice dans un aléatoire, avec l'aide de randomOrientation*/
    void randomConfiguration();

    /*Renvoie une orientation aléatoire de la sphère unité
        Les orientations tirées au hasard sont uniformément répartis sur la demi-sphère
        unité supérieure : http://mathworld.wolfram.com/SpherePointPicking.html
    */
    void randomOrientation(std::array<double, 2> &randomOrientation);

    /*Tire une orientation aléatoire de la sphère unité à une distance au maximum dmax
        de l'angle fourni en argument.*/
    void nearRandomOrientation(
        const double dmax,
        const std::array<double, 2> &oldAngle, 
        std::array<double, 2> &newAngle); 

    /*Renvoie un site aléatoire de la lattice*/
    void randomSite(std::array<int, 3> &randomLoc) const;

    /*Shuffle la liste randomSiteList*/
    void shuffleRandomSiteList();

    /*Renvoie le site demandé de la liste ordonnée*/
    void shuffledRandomSite(
        const int i,
        std::array<int, 3> randomLoc) const;

    /*Renvoie une liste des 6 plus proches voisins*/
    void nearestNeighboor(
        const std::array<int, 3> &site,
        std::array<std::array<int, 3>, 6> &nearestNeighboor) const;

    /*Renvoie les valeurs de latticeArray associées au site donné en argument*/
    void value(
        const std::array<int, 3> &site,
        std::array<double, 2> &angle) const;

    /*Calcule le cosinus de l'angle entre les deux directions données en argument*/
    double cosAngle(
        const std::array<double, 2> &oldAngle, 
        const std::array<double, 2> &newAngle) const;

    /*Calcule l'énergie d'intéraction entre deux sites*/
    double energie(
        const std::array<int, 3> &site1, 
        const std::array<int, 3> &site2) const; 

    /*Fonction qui display la diagonale de la lattice*/
    void display() const;


    private:

    /*Taille de la lattice*/
    const int size ;

    /*La lattice*/
    std::vector< std::vector<std::vector<std::array<double, 2>>>> latticeArray;

    /*Liste désordonnée des sites de la lattices*/
    std::vector<int> randomSiteList;

    /*Seed et générateur de nombre aléatoire*/
    std::mt19937 gen;
    std::uniform_real_distribution<double> dis;
};

#endif


