# networks assignment
# question two
# alex gillies

import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import random
import queue
import PA # VERY IMPORTANT TO HAVE AS WELL

####################################################################################################################################

def q2_plot():
    plt.clf() #clears plot
    ydata = [1 for i in range(10)] + [2 for i in range(10)] + [3 for i in range(10)]+ [4 for i in range(10)]+ [5 for i in range(10)]
    random = [1, 10, 100, 20000, 10000, 100000, 500000, 700000, 1000000, 5000000]
    pa = [1, 3000, 100, 1000, 2000, 100000, 500000, 700000, 1000000, 5000000]
    group = [10, 10000, 100, 1000, 30000, 100000, 500000, 10000000, 1000000, 5000000]
    ws = [1000, 10000, 100, 1000, 10000, 100000, 500000, 200000, 1000000, 5000000]
    coauthorship = [5, 10, 100, 1000, 50000, 100000, 500000, 700000, 1000000, 5000000]
    xdata = random + pa + group + ws + coauthorship
    plt.ylim(0,6)
    plt.yticks((1, 2, 3, 4, 5), ('Random', 'PA', 'Group', 'WS', 'Coauthorship'))
    plt.semilogx(xdata, ydata, marker='.', linestyle = 'None', color='b')
    plt.savefig("example.png")

####################################################################################################################################

def four_cycles(graph, vertex):
    """counts the number of 4-cycles containing vertex in graph"""

    M = get_adjacency_matrix(graph)

    count = 0
    for idx1 in range(len(graph[vertex])):
        for idx2 in range(idx1 + 1, (len(graph[vertex]))):  #find all distinct pairs of neighbours of vertex
            neighbour1 = graph[vertex][idx1]
            neighbour2 = graph[vertex][idx2]
            for dist2_neighbour in graph[neighbour1]:                                   #look at neighbours of neighbour1
                if dist2_neighbour != vertex and M[dist2_neighbour][neighbour2] == 1:   #see if they are also neighbours of neighbour2
                    count += 1                                                          #if so a 4-cycle has been found
    return count

####################################################################################################################################

def five_cycles(graph, vertex):
    """counts the number of 5-cycles containing vertex in graph"""
    count = 0
    for idx1 in range(len(graph[vertex])):
        neighbour1 = graph[vertex][idx1]
        #print(neighbour1)
        for idx2 in range(idx1 + 1, (len(graph[vertex]))):                              #find all distinct pairs of neighbours of vertex
            neighbour2 = graph[vertex][idx2]
            for dist2_neighbour1 in graph[neighbour1]:                                      #look at neighbours of neighbour1
                if vertex != dist2_neighbour1:
                    for dist2_neighbour2 in graph[neighbour2]:                                  #and neighbours of neighbour2
                        if M[dist2_neighbour1][dist2_neighbour2] == 1 and vertex != dist2_neighbour2:      #see if they are adjacent
                            count += 1                                                          #if so a 5-cycle has been found
    return count

####################################################################################################################################

def load_graph(graph_txt):
    """
    Loads a graph from a text file.
    Then returns the graph as a dictionary.
    """
    graph_file = open(graph_txt)
    graph_text = graph_file.read()
    graph_lines = graph_text.split('\n')
    graph_lines = graph_lines[ : -1]    #ignore final blank line
    
    graph = {}
    for line in graph_lines:                    #read each edge
        link = line.split()                     #split into node and the neighbour it links to
        node = int(link[0])
        neighbour = int(link[1])
        if node != neighbour:                                   #check that node is not joined to itself
            if node in graph and neighbour not in graph[node]:  #if node already found and edge not already found 
                graph[node] += [neighbour]                      #add to its list of neighbours
            elif node not in graph:
                graph[node] = [neighbour]                       #if node seen for first time add to graph            
            if neighbour in graph and node not in graph[neighbour]:              
                graph[neighbour] += [node]                      #if neighbour already found add node to its list of neighbours unless already there
            elif neighbour not in graph:
                graph[neighbour] = [node]                       #if neighbour seen for first time add to graph
    #print ("Loaded graph with", len(graph), "vertices and", sum([len(graph[vertex]) for vertex in graph])//2 ,"edges")
    return graph

####################################################################################################################################

def get_adjacency_matrix(coauthorship_graph):
	vertices = range(1560)
	M = []
	#consider each vertex
	for v in vertices:
	    row = []
	    #check whether or not each vertex is a neighbour
	    for w in vertices:
	        if v in coauthorship_graph and w in coauthorship_graph and w in coauthorship_graph[v]:
	            row += [1]
	        else:
	            row += [0]
	    M += [row]

	return M

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

results_four_cycle = {}
results_five_cycle = {}

results_random_four_cycle = {}
results_random_five_cycle = {}

results_PA_four_cycle = {}
results_PA_five_cycle = {}

results_group_graph_four_cycle = {}
results_group_graph_five_cycle = {}



print("Start")

coauthorship_graph = load_graph("coauthorship.txt")

for key, value in coauthorship_graph.items():
	results_four_cycle[key] = four_cycles(coauthorship_graph, key)

file = open("results_four_cycle.txt", "w")
file.write(results_four_cycle)

print("Four Cycle")

for key, value in coauthorship_graph.items():
	results_five_cycle[key] = five_cycles(coauthorship_graph, key)

file = open("results_five_cycle.txt", "w")
file.write(results_five_cycle)

print("Five Cycle")



random_graph = make_random_graph(1559, 0.2) # EDIT need to have similar number of edges

for key, value in random_graph.items():
	results_random_four_cycle[key] = four_cycles(random_graph, key)

file = open("results_random_four_cycle.txt", "w")
file.write(results_random_four_cycle)

print("Random Four Cycle")

for key, value in random_graph.items():
	results_random_five_cycle[key] = five_cycles(random_graph, key)

file = open("results_random_five_cycle.txt", "w")
file.write(results_random_five_cycle)

print("Random Five Cycle")



PA_graph = make_PA_Graph(1559, 0.2) # EDIT need to have similar number of edges

for key, value in PA_graph.items():
	results_PA_four_cycle[key] = four_cycles(PA_graph, key)

file = open("results_PA_four_cycle.txt", "w")
file.write(results_PA_four_cycle)

print("PA Four Cycle")

for key, value in PA_graph.items():
	results_PA_five_cycle[key] = five_cycles(PA_graph, key)

file = open("results_PA_five_cycle.txt", "w")
file.write(results_PA_five_cycle)

print("PA Five Cycle")



group_graph = make_group_graph(40,40,0.2,0.2) # EDIT need to have similat number of edges

for key, value in group_graph.items():
	results_group_graph_four_cycle[key] = four_cycles(group_graph, key)

file = open("results_group_graph_four_cycle.txt", "w")
file.write(results_group_graph_four_cycle)

print("Group Four Cycle")

for key, value in group_graph.items():
	results_group_graph_five_cycle[key] = five_cycles(group_graph, key)

file = open("results_group_graph_five_cycle.txt", "w")
file.write(results_group_graph_five_cycle)

print("Group Five Cycle")

####################################################################################################################################