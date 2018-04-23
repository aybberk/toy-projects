#include <iostream>
#include "Classes.h"
#include <stdlib.h>
#include <stdio.h>
#include <vector>
#include <algorithm>
#include <math.h>
#include <string.h>
#include <time.h>
using namespace std;

int main(int argc, char** argv)
{
    int problemSize = atoi(argv[1]);
    int populationSize = atoi(argv[2]);
    cout << "Problem Size: " << problemSize << endl;
    cout << "Population Size: " << populationSize << endl; 
    Population gen(populationSize);
    Population nextGen(populationSize);
    gen.addRandom(populationSize,problemSize);
    gen.sortPopulation();
    int generation=0;
    double maxFitness=0;
    double averageFitness=0;
    const double fitnessThreshold=1;
    const int elite=1;
    srand (time(NULL));
    while(maxFitness<fitnessThreshold)
    {

        generation++;
        nextGen.clear();
        for(int n=0; n<elite; n++)
        {
            nextGen.add(gen.getIndividual(n));

        }
        nextGen.addRandom(populationSize/20,problemSize);
        while(!nextGen.isFilled())
        {
            nextGen.add(gen.produceChild(problemSize, populationSize));
        }
        gen=nextGen.copy();
        gen.sortPopulation();
        maxFitness=gen.maxFitness();
        averageFitness=gen.avgFitness();
        cout<<"max fitness of generation "<<generation<<"= "<<maxFitness<<endl;
        cout<<"avg fitness of generation "<<generation<<"= "<<averageFitness<<endl;
        if(generation%100==0)
        {
            gen.printPopulation();

            cout << "Best individual: " << endl;
            gen.getIndividual(0).printChromosome();
            gen.getIndividual(0).drawChromosome();
        }

    }

    gen.getIndividual(0).printChromosome();
    gen.getIndividual(0).drawChromosome();

    return 0;
}
