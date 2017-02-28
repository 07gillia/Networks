#assignmentsolution2017question1.py
#network analysis
#matthew johnson
#11 february 2017

from graphs import make_group_graph
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

#adapted from lecture 2, na2loadgraph.py (noting that the format of the text file differs)
#note that I edited coauthorship.txt to remove extraneous information so function assumes text file is just a list of edges
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
    print ("Loaded graph with", len(graph), "vertices and", sum([len(graph[vertex]) for vertex in graph])//2 ,"edges")
    return graph

coauthorship_graph = load_graph("coauthorship_edited.txt")

"""
#make adjacency matrix
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
"""

def four_cycles(graph, vertex):
    """counts the number of 4-cycles containing vertex in graph"""
    count = 0
    for idx1 in range(len(graph[vertex])):
        for idx2 in range(idx1 + 1, (len(graph[vertex]))):  #find all distinct pairs of neighbours of vertex
            neighbour1 = graph[vertex][idx1]
            neighbour2 = graph[vertex][idx2]
            for dist2_neighbour in graph[neighbour1]:                                   #look at neighbours of neighbour1
                if dist2_neighbour != vertex and M[dist2_neighbour][neighbour2] == 1:   #see if they are also neighbours of neighbour2
                    count += 1                                                          #if so a 4-cycle has been found
    return count


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


            
#edit of lecture3.py
def plot_diameter_vs_p(num_groups, nodes_per_group, external_prob, trials=1, title=False):
    """plot diameter of group graph versus internal probability by taking average of k trials for each data point"""
    #create arrays for plotting
    xdata = []
    ydata = []
    for internal_prob in [0.1*p for p in range(1,11)]:
        diameters = []
        print (internal_prob)
        for idx in range(trials):
            graph = make_group_graph(num_groups, nodes_per_group, internal_prob, external_prob)
            diam = diameter(graph)
            diameters += [diam]
        xdata += [internal_prob]
        ydata += [1.0*sum(diameters)/trials]
    plt.clf() #clears plot
    plt.xlabel('Internal Probability')
    plt.ylabel('Diameter')
    if title:
        plt.title(title)
    plt.plot(xdata, ydata, marker='.', linestyle='-', color='b')
    plt.savefig('Q1_diameters.png')




def question1(part1=True, part2=True, part3=True):
    if part1:
        print ("construct group graphs with 400 vertices, divided into 20 groups of 20")
        print ("let p take the values 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, and q=0.5 - p")
        print ("for each value create 100 graphs, find on average how many vertices have degree d, and plot the distribution")
        for p in [0.25, 0.3, 0.35, 0.4, 0.45, 0.5]:
            print ("making the plot for p="+str(p))
            q = 0.5 - p
            dist = average_degree_distribution_group_graphs(20, 20, p, q, 100)
            plot_degree_distribution(dist, "Degree Distribution of Group Graph with m=k=20, p="+str(p),"Q1_group_graph_p="+str(p)+"_degrees.png")
        print ("repeat with graphs on 400 vertices, divided into 200 groups of 2 with p=0.4")
        dist = average_degree_distribution_group_graphs(200, 2, 0.4, 0.1, 100)
        plot_degree_distribution(dist, "Degree Distribution of Group Graph with m=200, k=2, p=0.4","Q1_group_graph_m=200_degrees.png")
        print ("repeat with graphs on 400 vertices, divided into 2 groups of 200 with p=0.4")
        dist = average_degree_distribution_group_graphs(2, 200, 0.4, 0.1, 100)
        plot_degree_distribution(dist, "Degree Distribution of Group Graph with m=2, k=200, p=0.4","Q1_group_graph_m=2_degrees.png")
        print ("looking at the figures produced, notice that the shapes of the distributions are all very similar and the degrees are all very close to the average")
        print ()
    if part2:
        print ("to investigate the relationship between the diameter and p, construct, for each value of p, 20 group graphs with 80 groups, each on 5 vertices with q=0.05")
        print ("doing the calculations for p=")
        plot_diameter_vs_p(80, 5, 0.05, 20, "Diameter vs p for Group Graphs containing 80 groups of 5 vertices")
        print ("from the plot we see the relationship is rather uninteresting with the diameter not depending (much) on p")
        print ()
    if part3:
        print ("Level 4 only: to investigate the relationship between the clustering coefficient and p, construct, for each value of p, 20 group graphs with 20 groups, each on 20 vertices with q=0.05")
        print ("doing the calculations for p=")
        plot_diameter_vs_p(20, 20, 0.05, 20, "Clustering coefficient vs p for Group Graphs containing 20 groups of 20 vertices")
        print ("from the plot we see the relationship is rather uninteresting with the diameter not depending (much) on p")
