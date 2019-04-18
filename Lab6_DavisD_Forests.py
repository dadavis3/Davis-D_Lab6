# DAVIS, DAVID A.

# In this lab assignment we are making a maze with disjoint set forest. A random
# maze was given to us. when we remove a wall, if the cell that were separated by 
# that wall belonged to different sets, you must unite these sets. The main goal f
# for this lab assignment is to learn to use disjoint set forests as a data structure.  

import matplotlib.pyplot as plt
import numpy as np
import random
from scipy import interpolate 


def DisjointSetForest(size):
    return np.zeros(size,dtype=np.int)-1
    

def find(S,i):
    # Returns root of tree that i belongs to
    if S[i]<0:
        return i
    return find(S,S[i])

def find_c(S,i): #Find with path compression 
    if S[i]<0: 
        return i
    r = find_c(S,S[i]) 
    S[i] = r 
    return r
    
def union(S,i,j):
    # Joins i's tree and j's tree, if they are different
    ri = find(S,i) 
    rj = find(S,j)
    if ri!=rj:
        S[rj] = ri

def union_c(S,i,j):
    # Joins i's tree and j's tree, if they are different
    # Uses path compression
    ri = find_c(S,i) 
    rj = find_c(S,j)
    if ri!=rj:
        S[rj] = ri
         
def union_by_size(S,i,j):
    # if i is a root, S[i] = -number of elements in tree (set)
    # Makes root of smaller tree point to root of larger tree 
    # Uses path compression
    ri = find_c(S,i) 
    rj = find_c(S,j)
    if ri!=rj:
        if S[ri]>S[rj]: # j's tree is larger
            S[rj] += S[ri]
            S[ri] = rj
        else:
            S[ri] += S[rj]
            S[rj] = ri

def NumSets(S):
    count =0
    for i in range(len(S)):
        if S[i]<0:
            count += 1
    return count

# -------------------     METHODS FOR THE LAB     ----------------------

def remove(S, maze_walls,numSets):
    while numSets > 1:
        w = random.choice(maze_walls)
        i = maze_walls.index(w)
        if find(S,w[0]) != find(S,w[1]):
            maze_walls.pop(i)
            union(S,w[0],w[1])
            numSets -= 1
    return w

def removeCompressed(S, maze_walls,numSets):
    while numSets > 1:
        w = random.choice(maze_walls)
        i = maze_walls.index(w)
        if find(S,w[0]) != find(S,w[1]):
            maze_walls.pop(i)
            union_by_size(S,w[0],w[1])
            numSets -= 1
    return w
    
def draw_maze(walls,maze_rows,maze_cols,cell_nums=False):
    fig, ax = plt.subplots()
    for w in walls:
        if w[1]-w[0] ==1: #vertical wall
            x0 = (w[1]%maze_cols)
            x1 = x0
            y0 = (w[1]//maze_cols)
            y1 = y0+1
        else:#horizontal wall
            x0 = (w[0]%maze_cols)
            x1 = x0+1
            y0 = (w[1]//maze_cols)
            y1 = y0  
        ax.plot([x0,x1],[y0,y1],linewidth=1,color='k')
    sx = maze_cols
    sy = maze_rows
    ax.plot([0,0,sx,sx,0],[0,sy,sy,0,0],linewidth=2,color='k')
    if cell_nums:
        for r in range(maze_rows):
            for c in range(maze_cols):
                cell = c + r*maze_cols   
                ax.text((c+.5),(r+.5), str(cell), size=10,
                        ha="center", va="center")
    ax.axis('off') 
    ax.set_aspect(1.0)

def wall_list(maze_rows, maze_cols):
    # Creates a list with all the walls in the maze
    w =[]
    for r in range(maze_rows):
        for c in range(maze_cols):
            cell = c + r*maze_cols
            if c!=maze_cols-1:
                w.append([cell,cell+1])
            if r!=maze_rows-1:
                w.append([cell,cell+maze_cols])
    return w

plt.close("all") 
maze_rows = 5
maze_cols = 10

#numSet = setAmount(S)
walls = wall_list(maze_rows,maze_cols)
#numSet = setAmount(S)


S = DisjointSetForest(maze_rows * maze_cols)
#numSet = setAmount(S)
remove(S,walls,NumSets(S))
#removeCompressed(S,walls,numSet)



draw_maze(walls,maze_rows,maze_cols,cell_nums=True) 

#for i in range(len(walls)//2): #Remove 1/2 of the walls 
#    d = random.randint(0,len(walls)-1)
#    print('removing wall ',walls[d])
#    walls.pop(d)

draw_maze(walls,maze_rows,maze_cols) 


