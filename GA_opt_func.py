# %%
import numpy as np
import random

def target_function(x):
    return np.exp(-(x-0.1) ** 2) * np.sin(6 * np.pi * x ** (3 / 4)) ** 2
get_scores = np.vectorize(target_function)

def encode(ind):
    '''
    parameter: ind <float>
    return: code <list> (n, theta)
    n: 0 - 5
    theta: 0 - 1/6
    '''
    n = ind * 6 // 1
    theta = ind - n / 6
    return np.array([n, theta])
def encode_all(population):
    ans = []
    for ind in population:
        ans.append(encode(ind))
    return np.array(ans)

def decode(code):
    n = code[0]
    theta = code[1]
    return n / 6 + theta
def decode_all(chromsomes):
    ans = []
    for c in chromsomes:
        ans.append(decode(c))
    return np.array(ans)

# best crossover
def isSelected(score):
    return score > random.random()
v_isSeleted = np.vectorize(isSelected)

def crossover(parents):
    '''
    parameter: parents <list>
    return: children <list>
    '''
    children = []
    N = len(parents)
    for i in range(N):
        for j in range(N):
            if i != j:
                children += [[parents[i][0], parents[j][1]]]
    return children



def select_and_crossover(population, crossover_rate = 0.3, drop_rate = 0.5):
    scores = get_scores(population)
    chromsomes = encode_all(population)
    
    index = list(reversed(np.argsort(scores)))
    retain_bound = int(crossover_rate * len(population))
    drop_bound = int(drop_rate * len(population))
    
    parents_index = index[ : retain_bound]
    retained_index = index[ :-drop_bound]
    
    parents_ready = []
    for i in parents_index:
        parents_ready += [chromsomes[i]]
    children_ready = crossover(parents_ready)
    children = list(decode_all(children_ready))
    
    retained = []
    for i in retained_index:
        retained += [population[i]]

    new_population = np.array(retained + children)
    return new_population

    # crossover(parent)
def mutate(chromsome, mutation_rate = 0.1):
    new_chromsome = chromsome
    if random.random() < mutation_rate:
        if random.random() < 0.5:
            new_chromsome[0] = random.randint(0,5)
        else:
            new_chromsome[1] = random.random()/6
    return new_chromsome

def mutatie_all(chromsomes, mutation_rate = 0.1):
    for i in range(len(chromsomes)):
        chromsomes[i] = mutate(chromsomes[i], mutation_rate=mutation_rate)
    return chromsomes

def get_best(population):
    best_ind = max(population, key=target_function)
    return best_ind, target_function(best_ind)

# %% 


# %%
