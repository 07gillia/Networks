# networks assignment
# question three
# alex gillies

import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import random
import queue

####################################################################################################################################

def make_random_graph(num_nodes, prob):
    """Returns a dictionary to a random graph with the specified number of nodes
    and edge probability.  The nodes of the graph are numbered 0 to
    num_nodes - 1.  For every pair of nodes, i and j, the pair is considered
    twice: once to add an edge (i,j) with probability prob, and then to add an
    edge (j,i) with probability prob. 
    """
    #initialize empty graph
    random_graph = {}
    #consider each vertex
    for vertex in range(num_nodes):
        out_neighbours = []
        for neighbour in range(num_nodes):
            if vertex != neighbour:
                random_number = random.random()
                if random_number < prob:
                    out_neighbours += [neighbour]        
        #add vertex with list of out_ neighbours
        random_graph[vertex] = set(out_neighbours)
    return random_graph

####################################################################################################################################

def make_PA_Graph(total_nodes, out_degree):
    """creates a PA_Graph on total_nodes where each vertex is iteratively
    connected to a number of existing nodes equal to out_degree"""
    #initialize graph by creating complete graph and trial object
    PA_graph = make_complete_graph(out_degree)
    trial = PATrial(out_degree)
    for vertex in range(out_degree, total_nodes):
        PA_graph[vertex] = trial.run_trial(out_degree)
    return PA_graph

####################################################################################################################################

def make_group_graph(m, k, p, q):
    """
    create mk vertices
    split into m groups
    of size k
    for a pair of vertices in the same group they have an edge between them at probability p
    for a pair of vertices not in the same group they have an edge between them at probability q
    """

    graph = {}
    # this is a dictionary that stores the vertex as its key and the list of nodes it's connected to as its value

    for x in range(1, (m*k) + 1):
        graph[x] = []
    # iterate through the number of vertices in the graph and add to the dictionary its key and a list as the value

    for x in range(1,m+1):
        # iterate through the number of groups
        for y in range(((x-1) * k) + 1,(x * k) + 1):
            # iterate through the vertices in each group
            for z in range(y + 1, (x * k) + 1):
                # iterate through the edges it could be connected to
                test_random = random.random()
                # get a random number 

                if test_random < p:
                    # if there should be an edge between the two
                    graph[y].append(z)
                    graph[z].append(y)
                    # add the edges to each one
    
    # iterate through all the nodes in a given nodes group
    # get some random numnber, if it passes then add this vertex to the list of connected nodes, this needs to be done both ways

    for x in range(1,m*k+1):
        for y in range(x,m*k+1):
            test_random = random.random()

            if test_random < q and not y in graph[x] and not x in graph[y]:
                graph[x].append(y)
                graph[y].append(x)

    # iterate through all nodes not in a given nodes group

    # get some random number, if it passes then add this vertex to the list of connected nodes, this needs to be done both ways

    # print (str(m) + ", " + str(k) + ", " + str(p) + ", " + str(q))
    # print (graph)

    return graph

####################################################################################################################################
