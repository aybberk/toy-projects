#ifndef FUNCTIONS_H_INCLUDED
#define FUNCTIONS_H_INCLUDED
#include <iostream>
#include "Classes.h"
#include <stdlib.h>
#include <stdio.h>
#include <vector>
#include <algorithm>
#include <math.h>
using namespace std;

Chromosome crossover(const Chromosome &chr1, const Chromosome &chr2)
{
    Chromosome child(0);
    cutPoint=rand()%chr1.size();
    if(rand()%2==1)
    {
        for(int n=0;n<cutPoint;n++)
        {
            child.addGene(chr1.getGene(n));
        }
        for(int n=cutPoint;n<chr1.size();n++)
        {
            child.addGene(chr2.getGene(n));
        }
    }
    else
        {
        for(int n=0;n<cutPoint;n++)
        {
            child.addGene(chr2.getGene(n));
        }
        for(int n=cutPoint;n<chr1.size();n++)
        {
            child.addGene(chr1.getGene(n));
        }
        }
    return child;
}


#endif // FUNCTIONS_H_INCLUDED
