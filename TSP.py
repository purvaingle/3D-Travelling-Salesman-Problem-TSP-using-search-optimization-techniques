import numpy as np 
import pandas as pd
import random
import operator
import math


class On_campus_place:
    def __init__(self, x, y, z):
        self.x=x
        self.y=y
        self.z=z
    
    def calc_dist(self, ocplace):
        dist1 = np.sqrt(((abs(self.x - ocplace.x))** 2) + ((abs(self.y - ocplace.y)) ** 2) + ((abs(self.z - ocplace.z)) ** 2))
        return dist1
    

def writetofile(bp):
        f=open("output.txt","w")
        temp=bp[0]
        for itr in bp:
            f.write(str(itr.x) + " " + str(itr.y) + " " + str(itr.z) + "\n")
            
        f.write(str(temp.x) + " " + str(temp.y) + " " + str(temp.z))
        f.close()
    
   
class fitn:
    def __init__(self, path):
        self.path = path
        self.dist = 0
        self.fitness= 0.0
    
    def path_dist(self):
        if self.dist==0:
            dist_path=0  
            for i in range(0, len(self.path)):
                start_pl = self.path[i]
                dest_pl = None
                if i + 1 < len(self.path):
                    dest_pl = self.path[i + 1]
                else:
                    dest_pl = self.path[0]
                dist_path=dist_path+start_pl.calc_dist(dest_pl)
            self.dist=dist_path
        return self.dist
    
    def path_fitness(self):
        if self.fitness== 0:
            self.fitness=1/float(self.path_dist())
        return self.fitness

def create_path(places):
    path = random.sample(places, len(places))
    return path

def initialPopulation(pop_size, places):
    population = []
    for i in range(0, pop_size):
        population.append(create_path(places))
        #print(population)
    return population

def rank_fitness_of_paths(population):
    fitness_scores = {}
    for i in range(0,len(population)):
        fitness_scores[i] = fitn(population[i]).path_fitness()
    return sorted(fitness_scores.items(), key = operator.itemgetter(1), reverse = True)

def selec(ranked_population, top_ranked_size):
    selectionResults = []
    df = pd.DataFrame(np.array(ranked_population), columns=["Index","Fitness"])
    df['cum_sum'] = df.Fitness.cumsum()
    df['cum_perc'] = df.cum_sum/df.Fitness.sum()*100
    
    for i in range(0, top_ranked_size):
        selectionResults.append(ranked_population[i][0])
    for i in range(0, len(ranked_population) - top_ranked_size):
        pick = 100*random.random()
        for i in range(0, len(ranked_population)):
            if pick <= df.iat[i,3]:
                selectionResults.append(ranked_population[i][0])
                break
    return selectionResults


def create_matingpool(population, selectionResults):
    matingpool = []
    for i in range(0, len(selectionResults)):
        index = selectionResults[i]
        matingpool.append(population[index])
    return matingpool


def crossover(P1, P2):
    child = []
    C1 = []
    C2 = []
    
    geneA = int(random.random() * len(P1))
    geneB = int(random.random() * len(P2))
    
    starti = min(geneA, geneB)
    endi = max(geneA, geneB)

    for i in range(starti, endi):
        C1.append(P1[i])
        
    C2 = [item for item in P2 if item not in C1]

    child = C1 + C2
    return child

def breed(matingpool, top_ranked_size):
    children = []
    size = len(matingpool) - top_ranked_size
    pool = random.sample(matingpool, len(matingpool))

    for i in range(0,top_ranked_size):
        children.append(matingpool[i])
    
    for i in range(0, size):
        child = crossover(pool[i], pool[len(matingpool)-i-1])
        children.append(child)
    return children

def mut(ind, mut_rate):
    for temp1 in range(len(ind)):
        if(random.random() < mut_rate):
            temp2 = int(random.random() * len(ind))
            
            place1 = ind[temp1]
            place2 = ind[temp2]
            
            ind[temp1] = place2
            ind[temp2] = place1
    return ind


def mut_pop(population, mut_rate):
    population_mut = []
    
    for ind in range(0, len(population)):
        mut_ind = mut(population[ind], mut_rate)
        population_mut.append(mut_ind)
    return population_mut


def new_generation(curr_gen, top_ranked_size, mut_rate):
    ranked_population = rank_fitness_of_paths(curr_gen)
    #print(ranked_population)
    selectionResults = selec(ranked_population, top_ranked_size)
    matingpool = create_matingpool(curr_gen, selectionResults)
    children = breed(matingpool, top_ranked_size)
    next_gen = mut_pop(children, mut_rate)
    return next_gen

def GA(population, pop_size, top_ranked_size, mut_rate, gens):
    pop = initialPopulation(pop_size, population)
    print("Initial distance: " + str(1 / rank_fitness_of_paths(pop)[0][1]))
    
    for i in range(0, gens):
        pop = new_generation(pop, top_ranked_size, mut_rate)
    
    print("Final distance: " + str(1 / rank_fitness_of_paths(pop)[0][1]))
    best_path_index = rank_fitness_of_paths(pop)[0][0]
    best_path = pop[best_path_index]
    #print(best_path)
    return best_path




def main():
    global num_of_places
    places_list=[]
    population=[]
    Xc=[]
    Yc=[]
    Zc=[]
    top_ranked_size=20
    mut_rate=0.2
    gens=500
    global pop_size
    pop_size= 200
    
    f = open('input.txt', 'r')
    global routesize
    content=f.readline()[0]
    for i in content:
        if i.isdigit()==True:
            num_of_places=int(i)
    f.close()
    routesize=num_of_places+1

    f = open('input.txt', 'r')
    for line in f.readlines()[1:]:
        fields = line.split(' ')
        Xc.append(int(fields[0]))
        Yc.append(int(fields[1]))
        Zc.append(int(fields[2]))
    f.close()    
    
    places = []
    for i in range(0,num_of_places):
        places.append(On_campus_place(x=Xc[i], y=Yc[i],z=Zc[i]))
    
    bp=GA(population=places, pop_size=100, top_ranked_size=60, mut_rate=0.01, gens=500)    
    writetofile(bp)
    
    
if __name__ == "__main__":
    main()
