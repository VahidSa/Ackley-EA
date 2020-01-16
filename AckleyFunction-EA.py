import random, math

def xover_single(male, female):
    child1 = male
    child2 = female
    random_gen = random.randint(0,19)
    # xover x
    child1[random_gen] = (male[random_gen] + female[random_gen])/2
    child2[random_gen] = (male[random_gen] + female[random_gen])/2
    # xover sima
    child1[random_gen+DIMENSIONS] = (male[random_gen+DIMENSIONS] + female[random_gen+DIMENSIONS])/2
    child2[random_gen+DIMENSIONS] = (male[random_gen+DIMENSIONS] + female[random_gen+DIMENSIONS])/2
    return child1, child2

def xover_simple(male, female):
    child1 = male
    child2 = female
    random_point = random.randint(0,19)
    for gene in range(random_point):
        # xover x
        child1[gene] = (male[gene] + female[gene])/2
        child2[gene] = (male[gene] + female[gene])/2
        # xover sima
        child1[gene+DIMENSIONS] = (male[gene+DIMENSIONS] + female[gene+DIMENSIONS])/2
        child2[gene+DIMENSIONS] = (male[gene+DIMENSIONS] + female[gene+DIMENSIONS])/2
    return child1, child2

def xover_whole(male, female):
    child1 = male
    child2 = female
    for gene in range(DIMENSIONS):
        # xover x
        child1[gene] = (male[gene] + female[gene])/2
        child2[gene] = (male[gene] + female[gene])/2
        # xover sima
        child1[gene+DIMENSIONS] = (male[gene+DIMENSIONS] + female[gene+DIMENSIONS])/2
        child2[gene+DIMENSIONS] = (male[gene+DIMENSIONS] + female[gene+DIMENSIONS])/2
    return child1, child2

def xover(male, female):

    if XOVER_TYPE == 'Single' :
        return xover_single(male, female)
    elif XOVER_TYPE == 'Simple':
        return xover_simple(male, female)
    elif XOVER_TYPE == 'Whole':
        return xover_whole(male, female)
    else:
        print("xover_type is incorrect!")

def mutate(chromosome):
    # sigma'
    global counter_mutate_sigma, counter_mutate_sigma_not_in_range, counter_mutate_x, counter_mutate_x_not_in_range
    for i in range(DIMENSIONS,2*DIMENSIONS):
        counter_mutate_sigma +=1
        tn = chromosome[i] * math.exp(TAVP * random.gauss(0,1) + TAV * random.gauss(0,1))
        if tn< T and tn> -T:
            if tn > 0 and tn < 0.003 :
                tn = 0.003
            elif tn < 0 and tn > -0.003:
                tn = -0.003
            #tn = round(tn, 8)
            chromosome[i] = tn
        else:
            counter_mutate_sigma_not_in_range += 1
            #print('tn-6 is bigger than range:\n',tn)
        #tn = chromosome[i] + random.gauss(0,DELTA)
        #if tn<10 and tn>-10:
        #    chromosome[i] = tn
    # x'
    for i in range(DIMENSIONS):
        counter_mutate_x += 1
        tn = chromosome[i] + chromosome[i+DIMENSIONS] * random.gauss(0,1)
        if tn<T and tn>-T:
            tn = round(tn, 12)
            chromosome[i] = tn
            #if tn > 0 and tn < 0.003 :
            #    tn = 0
            #elif tn < 0 and tn > -0.003:
            #    tn = -0
        else:
            counter_mutate_x_not_in_range += 1
            #print('tn-x is bigger than range:\n',tn)
        #tn = chromosome[i] + random.gauss(0,chromosome[i+DIMENSIONS])
        #if tn<10 and tn>-10:
        #   chromosome[i] = tn
    return chromosome

def mating_pool(parents, children_quantity):
    children = []
    while len(children) < children_quantity:
        # select mates
        male = parents[random.randint(0,len(parents)-1)]
        female = parents[random.randint(0,len(parents)-1)]

        # xover parents
        if XOVER_CHANCE > random.random():
            child1, child2 = xover(male, female)
        else:
            child1 = female
            child2 = male
        # mutate child
        if MUTATION_CHANCE > random.random():
            child1 = mutate(child1)
        if MUTATION_CHANCE > random.random():
            child2 = mutate(child2)
            
        children.append(child1)
        children.append(child2)

    return children

def select_Ranking(population, size):
    population = sort_population(population)
    return population[:size]

def first_population():
    # number of population: 700
    return [ [random.uniform(-T,T) for i in range(20)] + [random.uniform(-1,1) for i in range(20)]  for i in range(POPULATION_SIZE)]

def cost(chromosome):
    firstSum = 0.0
    secondSum = 0.0
    for c in chromosome[:20]:
        firstSum += c**2
        secondSum += math.cos(2.0*math.pi*c)
    n = DIMENSIONS
    return -20.0*math.exp(-0.2*math.sqrt(firstSum/n)) - math.exp(secondSum/n) + 20 + math.exp(1)
    

def sort_population(population):
    return sorted(population, key=lambda x: cost(x), reverse = False)


# CONFIGS
POPULATION_SIZE = 1000
GEN_MAX = 100
XOVER_CHANCE = 0.8
MUTATION_CHANCE = 0.2
XOVER_TYPE = 'Whole'   # All-types: 'Single', 'Simple', 'Whole'
SELECT_SORVIVORS_TYPE = 'Ranking'

DIMENSIONS = 20  # dimensions number

children_selection_percentage = 7
DELTA = 1
T = 5
TAVP = 1/math.sqrt((2 * DIMENSIONS))
TAV = 1/math.sqrt(2 * math.sqrt(DIMENSIONS))


def main():
    global counter_mutate_x
    global counter_mutate_sigma
    
    global counter_mutate_x_not_in_range
    
    global counter_mutate_sigma_not_in_range
    global best_cost, best_chromosome
    best_cost = 100
    best_chromosome = []
    # creating first population randomly
    population = first_population()
    #print('cost_first_population:', cost(population[0]))
    for generation in range(1,GEN_MAX+1):
        counter_mutate_x = 0
        counter_mutate_sigma = 0
        counter_mutate_x_not_in_range = 0
        counter_mutate_sigma_not_in_range = 0
        # children_quantity must be integer and even, even because of parents in crossover
        children_quantity  = int (children_selection_percentage * POPULATION_SIZE)
        # making children - in EA population is parents
        children = mating_pool(population, children_quantity) 
        # (μ,λ)
        pop = children
        #select sorvivors  
        if SELECT_SORVIVORS_TYPE == 'Ranking':
            population = select_Ranking(pop, POPULATION_SIZE)
        else:
            print('SELECT_SORVIVORS_TYPE ERROR')
            return
        if cost(population[0]) < best_cost:
            #print('=========================\nHUUUUUUHUUUUUU==================')
            best_cost = cost(population[0])
            best_chromosome = population[0]
        # logging every generation results
        print("Generation %s :\n Best_Answer: %s  with cost: %s" % (generation, population[0], cost(population[0]) ) )
        print('counter_mutate_x, counter_mutate_x_not_in_range :', counter_mutate_x, counter_mutate_x_not_in_range)
        print('counter_mutate_sigma, counter_mutate_sigma_not_in_range :', counter_mutate_sigma, counter_mutate_sigma_not_in_range)
        generation += 1
        #if cost(population[0])>cost(population[1]):
            #print('WOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOW!!!!!!!!!!!!!!!!!!!!!!')
            #return

if __name__ == "__main__":
    main()
    print('===============================')
    print('===============================')
    print('best_cost:',best_cost)
    print('best_chromosome:',best_chromosome)
    
