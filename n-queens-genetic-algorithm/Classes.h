#ifndef CLASSES_H_INCLUDED
#define CLASSES_H_INCLUDED
#include <iostream>
#include <stdlib.h>
#include <stdio.h>
#include <vector>
#include <algorithm>
#include <math.h>
#include <time.h>
using namespace std;


class Chromosome

{
private:
    vector<int> genes;
    int length;
public:

    Chromosome(int n=100)
    {
        length=n;
        for(int i=0; i<length; i++)
        {
            genes.push_back(i+1);
        }
        random_shuffle(genes.begin(),genes.end());
    }

    bool operator < (const Chromosome &chr2) const
    {
        double ffit=this->getFitness();
        double sfit=chr2.getFitness();

        return (ffit < sfit);
    }

    bool operator!=(const Chromosome &chr2) const
    {
        return genes!=chr2.genes;
    }
    void addGene(int n)
    {
        genes.push_back(n);
        length++;
    }

    void addGeneFirst(int n)
    {
        std::vector<int>::iterator it;
        it = genes.begin();
        genes.insert(it, n);
    }

    int popGene()
    {
        int lastGene = genes.back();
        genes.pop_back();
        return lastGene;
    }

    int getGene(int n) const
    {
        return genes[n];
    }

    void circularShift(int n)
    {
        for (int i = 0; i < n; i++)
        {
            this->addGeneFirst(this->popGene());
        }
    }


    void printChromosome() const
    {
        for (int i=0;i<length;i++)
        {
            cout<<genes[i]<<" ";
        }
        cout<<endl<<"fitness="<<getFitness()<<endl;
    }

    void drawChromosome() const
    {
        cout << endl << "Board:" << endl;
        for (int i = 0; i < genes.size(); i++)
        {
            cout << "\n";
            for (int n = 1; n < genes[i]; n++)
                {
                    cout << "- ";
                }
            cout << "/\\";
            for (int n = genes[i]; n < genes.size(); n++)
                {
                    cout << "- ";
                }
        }
        cout << endl;
    }


    Chromosome copy() const
    {
        Chromosome copied(0);
        copied.genes=this->genes;
        copied.length=this->length;
        return copied;
    }

    Chromosome crossover(const Chromosome &chr2)
    {
        Chromosome child(0);
        Chromosome parent1(0);
        Chromosome parent2(0);
        if(rand()%2==1)
        {
            parent1=this->copy();
            parent2=chr2.copy();

        }

        else
        {
            parent2=this->copy();
            parent1=chr2.copy();

        }
        int cutPoint=rand()%(parent1.length);
            for(int n=0;n<cutPoint;n++)
            {
                child.addGene(parent1.getGene(n));
            }
            vector<int> kalanlar (parent1.genes.begin()+cutPoint,parent1.genes.end());
            vector<int> copied=parent2.genes;
            for(int n=0; n<copied.size(); n++)
            {
                if(find(kalanlar.begin(), kalanlar.end(), copied[n]) != kalanlar.end())
                {
                    child.addGene(copied[n]);
                }
            }


        return child;
    }

    void mutate(double probability)
    {
        probability=probability*RAND_MAX;
        if(rand()<probability)
        {
            if(rand() % 2 == 1)
            {   
                iter_swap(genes.begin() + rand()% genes.size(), genes.begin() + rand()% genes.size());
            }
            else
            {
                this -> circularShift(rand() % genes.size());
            }
        }

    }


    double getFitness() const
    {
        int fault=0;

        for (int i=0; i<genes.size(); i++)
        {
            for(int j=i+1; j<genes.size(); j++)
            {
                if((genes[i] == genes[j]) || (j-i == genes[i]-genes[j]) || (i-j == genes[i]-genes[j]))
                {
                    fault++;
                }
            }
        }
        return 1.0/(fault+1);
    }


};


///*///////////////////////////////////////////////////////////////////////////*///

class Population
{
private:
    int popSize;
    vector<Chromosome> individuals;

public:
    Population(int n=200)
    {
        popSize=n;
    }
    Population copy()
    {
        Population pop2(popSize);
        pop2.individuals=this->individuals;
        return pop2;
    }
    void clear()
    {
        individuals.clear();
    }

    void sortPopulation()
    {
        sort(individuals.begin(),individuals.end());
        reverse(individuals.begin(),individuals.end());
    }
    Chromosome getIndividual(int n) const
    {
        return individuals[n];
    }
    Chromosome produceChild(int problemSize, int populationSize) const
    {

        double mutationProbability=1.0/50;
        mutationProbability=mutationProbability*0.99999;

        Chromosome parent1;
        Chromosome parent2;
        int tournamentSize=populationSize/30+1;
        vector<Chromosome> tournament;
        for(int n=0;n<tournamentSize;n++)
        {
            tournament.push_back(individuals[rand()%individuals.size()].copy());
        }
        sort(tournament.begin(),tournament.end());
        reverse(tournament.begin(),tournament.end());
        parent1=tournament[0].copy();
        parent2=tournament[1].copy();



        Chromosome child=parent1.crossover(parent2);
        child.mutate(mutationProbability);
        return child;
    }


    double maxFitness() const
    {
        return individuals[0].getFitness();
    }


    double avgFitness() const
    {
        double fitness=0;
        for(int n=0;n<individuals.size();n++)
        {
            fitness=fitness+individuals[n].getFitness();
        }
        return fitness/individuals.size();

    }
    bool isFilled() const
    {
        return individuals.size() >= popSize;
    }

    void addRandom(int nTane, int jLength)
    {
        for(int i=0;i<nTane;i++)
        {
            Chromosome chr(jLength);
            individuals.push_back(chr.copy());
        }
    }

    void add(const Chromosome& chr1)
    {
        if (individuals.size() >= popSize)
        {
            cout<<"population full";
        }
        else
        {
            individuals.push_back(chr1.copy());
        }

    }

    void printPopulation() const
    {
        for(int n=0;n<individuals.size();n++)
        {
            cout<<n<<". chromosome is:"<<endl;
            individuals[n].printChromosome();

        }
        cout<<"population="<<individuals.size()<<" people"<<endl;
        cout<<"avg fitness="<<avgFitness()<<endl;

    }


};

#endif // CLASSES_H_INCLUDED







