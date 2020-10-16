# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import math
from IPython.display import display, clear_output
import random
import matplotlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from time import time

origin = 1
Distance= []

# %%
''' 
Get Input
Return <Distance>
'''
def read_txt_input(path='./input/data.txt'):
    grid = []
    with open(path, 'r') as f:
        lines = f.readlines()
    for line in lines:
        line = line.split('\n')[0]
        line = line.split(',')
        try:
            grid.append([int(line[0]),int(line[1]),int(line[2])])
        except:
            print("输入文件格式误，请检查")
    arr = np.array(grid)

    m = len(lines)

    city_count = 0
    for i in range(m):
        if arr[i][0] >= city_count:
            city_count = arr[i][0]        
    for i in range(m):
        if arr[i][1] >= city_count:
            city_count = arr[i][1]
    print(f'city_count={city_count}')

    global Distance
    arr1 = [[float('inf')]*city_count]*city_count
    Distance = np.array(arr1)
    for i,item in enumerate(arr):
        Distance[arr[i,0]-1,arr[i,1]-1] = arr[i,2]
        Distance[arr[i,1]-1,arr[i,0]-1] = arr[i,2]
    print(f'Distance=\n{Distance}')
    return city_count, np.array(Distance)

# 计算距离
def get_total_distance(x):
    '''
    x: an individual
    distance: distance of the individua
    '''
    global origin, Distance
    distance = 0
    distance += Distance[origin][x[0]]
    for i in range(len(x)):
        if i==len(x)-1:
            distance += Distance[origin][x[i]]
        else:
            distance += Distance[x[i]][x[i+1]]
    return distance

#改良
def improve(x, improve_count=10000):
    i=0
    distance=get_total_distance(x)
    while i<improve_count:
        # randint [a,b]
        u = random.randint(0,len(x)-1)
        v = random.randint(0, len(x)-1)
        if u!=v:
            new_x=x.copy()
            t=new_x[u]
            new_x[u]=new_x[v]
            new_x[v]=t
            new_distance=get_total_distance(new_x)
            if new_distance<distance:
                distance=new_distance
                x=new_x.copy()
        else:
            continue
        i+=1
#自然选择
def selection(population, retain_rate=0.3, random_select_rate=0.5):
    """
    选择
    先对适应度从大到小排序，选出存活的染色体
    再进行随机选择，选出适应度虽然小，但是幸存下来的个体
    """
    # 对总距离从小到大进行排序
    graded = [[get_total_distance(x), x] for x in population]
    graded = [x[1] for x in sorted(graded)]
    # 选出适应性强的染色体
    retain_length = int(len(graded) * retain_rate)
    parents = graded[:retain_length]
    # 选出适应性不强，但是幸存的染色体
    for chromosome in graded[retain_length:]:
        if random.random() < random_select_rate:
            parents.append(chromosome)
    return parents

#交叉繁殖
def crossover(parents, count=300):
    #生成子代的个数,以此保证种群稳定
    target_count=count-len(parents)
    #孩子列表
    children=[]
    while len(children)<target_count:
        male_index = random.randint(0, len(parents) - 1)
        female_index = random.randint(0, len(parents) - 1)
        if male_index!=female_index:
            male=parents[male_index]
            female=parents[female_index]
            left=random.randint(0,len(male)-2)
            right=random.randint(left+1,len(male)-1)
            #交叉片段
            gene1=male[left:right]
            gene2=female[left:right]
            child1_c=male[right:]+male[:right]
            child2_c=female[right:]+female[:right]
            child1=child1_c.copy()
            child2= child2_c.copy()
            for o in gene2:
                child1_c.remove(o)
            for o in gene1:
                child2_c.remove(o)
            child1[left:right]=gene2
            child2[left:right]=gene1
            child1[right:]=child1_c[0:len(child1)-right]
            child1[:left] = child1_c[len(child1) - right:] 
            child2[right:] = child2_c[0:len(child1) - right]
            child2[:left] = child2_c[len(child1) - right:] 
            children.append(child1)
            children.append(child2) 
    return children

#变异
def mutation(children, mutation_rate=0.1):
    for i in range(len(children)):
        if random.random() < mutation_rate:
            child=children[i]
            u = random.randint(0,len(child)-3)
            v = random.randint(u+1, len(child)-2)
            w = random.randint(v+1, len(child)-1)
            child=children[i]
            child=child[0:u]+child[v:w]+child[u:v]+child[w:]
            
#得到最佳纯输出结果
def get_result(population):
    graded = [[get_total_distance(x), x] for x in population]
    graded = sorted(graded)
    return graded[0][0],graded[0][1]

def TSP_run(city_count,
            count=300,
            improve_count=10000 ,
            itter_time=300,
            retain_rate=0.3,
            random_select_rate=0.5,
            mutation_rate=0.1):
    start = time()
    print('TSP is running')
    origin=1  #设置起点
    index=[i for i in range(city_count)]
    index.remove(1)

    #使用改良圈算法初始化种群
    population=[]
    for i in range(count):
        #随机生成个体
        x=index.copy()
        random.shuffle(x)
        improve(x, improve_count=improve_count)
        population.append(x) 
    register=[]
    i=0

    distance, result_path = get_result(population)
    print('entering the iter loop')
    while i<itter_time:
        #选择繁殖个体群
        parents=selection(population, retain_rate=retain_rate, random_select_rate=random_select_rate)
        #交叉繁殖
        children=crossover(parents, count=count)
        #变异操作
        mutation(children, mutation_rate=mutation_rate)
        #更新种群
        population=parents+children
        distance,result_path=get_result(population)
        register.append(distance)
        i=i+1
        clear_output(wait=True)
        display(f'iteration:{i}') 
    end = time()
    # output
    print(f'运行时间：{end-start}s')
    print(f'距离为：{distance}')
    print(f'路径为：{[1]+result_path}')
    result_path=[origin]+result_path+[origin]
    plt.plot(list(range(len(register))),register)
    plt.xlabel('iteration number')
    plt.ylabel('distance of the best')
    plt.show()
    return distance, result_path

def set_distance(arr):
    global Distance
    Distance = arr

# %%
if __name__ == '__main__':
    pass



    '''
    m = int(input())
    grid = [[] for i in range(m)]
    for i in range(m):
        line = input().split(' ') # 以空格表示一个组之间的间隔，换行表示下一组
        for j in range(len(line)):
            grid[i].append(int(line[j]))
    arr  = np.array(grid)
    print(arr)
    '''


