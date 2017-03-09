#lecture7.py
#network analysis
#matthew johnson
#9 february 2015, last updated 11 February 2017

"""the task was to plot alpha vs search time for kleinberg graphs; see lecture7.pdf for a more detailed explaination

the plot on duo was created with the final function below;  for more information see Chapter 20 of Kleinberg and Easley"""

import random

def dist(v, w, num_nodes):
    """finds distance around a circle on num_nodes between v and w used in construction of kleinberg graphs"""
    distance = abs(w - v % num_nodes)   #distance between w and v but might be long way round the circle
    if distance > num_nodes / 2:        #if distance found is the long way round
        distance = num_nodes - distance     #find the shortest distance around the circle between v and w
    return distance
 
def make_kleinberg_graph(num_nodes, clockwise_neighbours, rewiring_prob, alpha):
    """Returns a dictionary to a undirected graph with num_nodes nodes; keys are nodes, values are list of neighbours.
    The nodes of the graph are numbered 0 to num_nodes - 1.
    Node i initially joined to i+1, i+2, ... , i+d mod N and i-1, i-2, ... , i-d mod N
    where d is the no. of clockwise neighbours.
    Each edge from i to j replaced with probability given with edge from i to k where k is randomly chosen
    with probability proportional to 1/d^alpha where d is the distante from i to k
    """
    #initialize empty graph
    kb_graph = {}
    for vertex in range(num_nodes): kb_graph[vertex] = []

    #add each vertex to clockwise neighbours
    for vertex in range(num_nodes):                                             #consider each vertex
        for neighbour in range(vertex + 1, vertex + clockwise_neighbours + 1):  #consider each clockwise neighbour
            neighbour = neighbour % num_nodes                                   #correct node label if value too high
            kb_graph[vertex] += [neighbour]                                     #add edge to dictionary
            kb_graph[neighbour] += [vertex]                                     #and again (each edge corresponds to two adjancencies)


    probs = []
    for d in range(1, num_nodes):
        #add to probs the proportional probability of rewiring to vertex at clockwise distance d
        distance = min(d, num_nodes - d)
        probs += [1.0*distance**(-1*alpha)]
    S = sum(probs) 

    #picking a destination vertex for rewiring
    def rewire_distance(vertex):
        """given vertex, choose a distance d with probability proportional
        to 1/d^alpha"""
        random_number = S * random.random()
        total = 0
        idx = 0
        while total < random_number:
            total += probs[idx]
            if total > random_number:
                return idx
            idx += 1
            
    #rewiring
    for vertex in range(num_nodes):                                             #consider each vertex
        for neighbour in range(vertex + 1, vertex + clockwise_neighbours + 1):  #consider each clockwise neighbour
            random_number = random.random()                                     #generate random number between 0 and 1
            if random_number < rewiring_prob:                                   #decide whether to rewire
                random_node = (vertex + rewire_distance(vertex)) % num_nodes    #choose random node
                if random_node != vertex and random_node not in kb_graph[vertex]:   #make sure no loops or duplicates edges
                    kb_graph[vertex].remove(neighbour % num_nodes)                          #delete edge from dictionary          
                    kb_graph[neighbour % num_nodes].remove(vertex)                          #in two places
                    kb_graph[vertex] += [random_node]                           #add new edge to dictionary
                    kb_graph[random_node] += [vertex]                           #in two places
    return kb_graph

"""function to see how long it takes to find one vertex from another"""

def search(graph, v, w, verbose=False):
    """number of steps to find w from v in a Kleinberg graph when each step is taken to minimise distance around circle to w"""
    num_nodes = (len(graph))
    current = v
    steps = 0
    while current != w and steps < 20:
        if verbose: print (current, graph[current])
        best_neighbour = graph[current][0]
        shortest_distance = dist(w, best_neighbour, num_nodes)
        for neighbour in graph[current][1:]:
            distance = dist(w, neighbour, num_nodes)
            if distance < shortest_distance:
                best_neighbour = neighbour
                shortest_distance = distance
        current = best_neighbour
        steps += 1
    return steps

"""function to find the search time of a graph"""

def search_time(graph):
    """finds the average number of steps required to find one vertex from another"""
    total = 0
    for start_vertex in graph:
        for target_vertex in graph:
            total += search(graph, start_vertex, target_vertex)
    return total / len(graph) / len(graph)

"""the above function is rather slow, so the next function finds the average search time by looking only at 2000 pairs of vertices;
is this latter function a reasonable proxy for the former? how could you investigate this?"""

def approx_search_time(graph):
    """finds the average number of steps required to find one vertex from another by sampling 2000 pairs"""
    num_nodes = len(graph)
    total = 0
    for i in range(2000):
        random_node1 = random.randint(0, num_nodes-1)
        random_node2 = random.randint(0, num_nodes-1)
        total += search(graph, random_node1, random_node2)
    return total / 2000

"""create data to plot; vary alpha and record search times"""
        
def alpha_vs_search_time_k(num_nodes, clockwise_neighbours, rewiring_prob):
    """create data to plot alpha against search time for Kleinberg graphs.

    xdata records alpha
    ydata records search time

    each data point is average of 1 trial (could be changed of course)"""
    xdata = []
    ydata = []
    alpha = 0
    while alpha <= 3:
        print (alpha)
        xdata += [alpha]
        g = make_kleinberg_graph(num_nodes, clockwise_neighbours, rewiring_prob, alpha)
        ydata += [approx_search_time(g)]
        alpha += 0.1
    return xdata, ydata

import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import textwrap

"""create a plot of alpha vs search time"""

def make_plot():
    xdata, ydata = alpha_vs_search_time_k(1500, 8, 0.33)    #plot on duo made with num_nodes=5000
    plt.clf() #clears plot
    plt.xlabel('alpha')
    plt.ylabel('search time')
    title = 'search time in Kleinberg graphs'
    plt.plot(xdata, ydata, marker='.', linestyle='-', color='b')
    plt.savefig('kleinberg2.png')
    plt.show()
