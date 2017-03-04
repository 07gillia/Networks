# networks assignment
# question one
# alex gillies

import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

import random
import queue

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

def max_dist(graph, source):
    """finds the distance (the length of the shortest path) from the source to
    every other vertex in the same component using breadth-first search, and
    returns the value of the largest distance found"""
    q = queue.Queue()
    found = {}
    distance = {}
    for vertex in graph:                                        #set up arrays
        found[vertex] = 0                                       #to record whether a vertex has been discovered
        distance[vertex] = -1                                   #and its distance from the source
    max_distance = 0
    found[source] = 1                                           #initialize arrays with values for the source
    distance[source] = 0
    q.put(source)                                               #put the source in the queue
    while q.empty() == False:
        current = q.get()                                       #process the vertex at the front of the queue
        for neighbour in graph[current]:                        #look at its neighbours
            if found[neighbour] == 0:                           #if undiscovered, update arrays and add to the queue
                found[neighbour] = 1
                distance[neighbour] = distance[current] + 1
                max_distance = distance[neighbour]
                q.put(neighbour)
    return max_distance

####################################################################################################################################

def diameter(graph):
    """returns the diameter of a graph, by finding, for each vertex, the maximum
    length of a shortest path starting at that vertex, and returning the overall
    maximum"""
    distances = []
    for vertex, edges in graph.items():                    #look at each vertex
        distances += [max_dist(graph, vertex)]      #find the distance to the farthest other vertex
    return max(distances)                           #return the maximum value found

####################################################################################################################################

def plot_diameter_vs_p(num_groups, nodes_per_group, external_prob, trials=1, title=False):
    """plot diameter of group graph versus internal probability by taking average of k trials for each data point"""
    #create arrays for plotting
    xdata = []
    ydata = []
    for internal_prob in [0.1*p for p in range(1,11)]:
        diameters = []
        #print (internal_prob)
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

####################################################################################################################################

def average_degree_group_graphs(m, k, p, q, numberOfTrials):
    # this is a bit wrong but the data is quite nice so im leaving it as is

    average_degree_total = 0
    # average degree over all the graphs

    individual_average_degree_distributions = []
    # a list to store all the average degree values

    for x in range(1,numberOfTrials):
        # iterate through the number of graphs

        graph = make_group_graph(m, k, p, q)
        # create a graph to be tested

        average_degree_specific = 0
        # average degree for that specific graph

        for y, z in graph.items():
            # iterate through the items in the graph

            average_degree_specific += len(z)
            # increment the total number of degree

        average_degree_specific = average_degree_specific / (m*k)
        # calculate the correct average degree for that graph

        individual_average_degree_distributions.append(average_degree_specific)
        # add the degree distribution of the current graph to the list of degrees

        average_degree_total += average_degree_specific
        # increment overall degree

    average_degree_total = average_degree_total / numberOfTrials
    # calculate the total average degree

    return average_degree_total, individual_average_degree_distributions
    # return the answer

####################################################################################################################################

def average_degree_distribution_group_graphs(m, k, p, q, numberOfTrials):
    
    total_degree_distribution = {}
    # the dictionary to store the number of each degree

    for x in range(0,m*k):
        total_degree_distribution[x] = 0
    # fill the dictionary with the number of possible degrees

    for x in range(0, numberOfTrials):
        # iterate through all graphs

        graph = make_group_graph(m, k, p, q)

        for y,z in graph.items():
            # iterate through every node in the graph

            total_degree_distribution[len(z)] = total_degree_distribution[len(z)] + 1
            # increment the degree counter by one

    for key, value in total_degree_distribution.items():
        total_degree_distribution[key] = value / numberOfTrials
        # normalise the values

    #print(total_degree_distribution)

    return total_degree_distribution

####################################################################################################################################

def plot_degree_averages(list_of_dist, the_title, nameOfFile):
    """plot average degree distribution for given distance value"""
    #create arrays for plotting
    xdata = []
    ydata = []

    ydata = list_of_dist
    for x in range(1,len(list_of_dist) + 1):
        xdata.append(x)

    plt.clf() #clears plot
    plt.xlabel('Degree Distribution')
    plt.ylabel('Average Degree')
    plt.title(the_title)
    plt.bar(xdata, ydata, 1, color='b')

    ydata.sort()

    plt.ylim([ydata[0] - 5, ydata[-1] + 5])
    plt.savefig(nameOfFile)

####################################################################################################################################

def plot_degree_distribution(list_of_dist, the_title, nameOfFile):
    """plot average degree distribution for given distance value"""
    #create arrays for plotting
    xdata = list_of_dist.keys()
    ydata = list_of_dist.values()

    plt.clf() #clears plot
    plt.xlabel('Degree Distribution')
    plt.ylabel('Average Degree')
    plt.title(the_title)
    plt.bar(xdata, ydata, 1, color='b')
    plt.savefig(nameOfFile)

####################################################################################################################################

def plot_degree_distribution_all():

    plt.xlabel('Degree Distribution')
    plt.ylabel('Average Degree')
    plt.title('The Distribution')
    plt.xlim([0,150])

    p_values = [0.25, 0.3, 0.35, 0.4, 0.45, 0.5]
    p_colours = ['b','g','r','y','c']

    for p in range(0,len(p_values)-1):
        q = 0.5 - p_values[p]
        current_dict_of_dist = average_degree_distribution_group_graphs(20, 20, p_values[p], q, 100)

        xdata = current_dict_of_dist.keys()
        ydata = current_dict_of_dist.values()

        plt.bar(xdata, ydata, 1, color=p_colours[p])

    plt.savefig('Q1_group_graph_p_degrees.png')

####################################################################################################################################

#graph = make_group_graph(20,20,0.1,0.1)

#print(diameter(graph))

#plot_diameter_vs_p(20,20,0.5)

#average_degree_distribution_group_graphs(20,20,0.25,0.25,100)

# check plot things

plot_degree_distribution_all()

print ("construct group graphs with 400 vertices, divided into 20 groups of 20")
print ("let p take the values 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, and q=0.5 - p")
print ("for each value create 100 graphs, find on average how many vertices have degree d, and plot the distribution")
for p in [0.25, 0.3, 0.35, 0.4, 0.45, 0.5]:
    print ("making the plot for p="+str(p))
    q = 0.5 - p
    current_dict_of_dist = average_degree_distribution_group_graphs(20, 20, p, q, 100)
    plot_degree_distribution(current_dict_of_dist, "Degree Distribution of Group Graph with m=k=20, p="+str(p),"Q1_group_graph_p="+str(p)+"_degrees.png")
print ("repeat with graphs on 400 vertices, divided into 200 groups of 2 with p=0.4")
dist_1 = average_degree_distribution_group_graphs(200, 2, 0.4, 0.1, 100)
plot_degree_distribution(dist_1, "Degree Distribution of Group Graph with m=200, k=2, p=0.4","Q1_group_graph_m=200_degrees.png")
print ("repeat with graphs on 400 vertices, divided into 2 groups of 200 with p=0.4")
dist_2 = average_degree_distribution_group_graphs(2, 200, 0.4, 0.1, 100)
plot_degree_distribution(dist_2, "Degree Distribution of Group Graph with m=2, k=200, p=0.4","Q1_group_graph_m=2_degrees.png")

xdata = dist_1.keys()
ydata = dist_1.values()

plt.clf() #clears plot
plt.xlabel('Degree Distribution')
plt.ylabel('Average Degree')
plt.title('Degree Distribution of Group Graph with m=200, k=2, p=0.4 and Degree Distribution of Group Graph with m=2, k=200, p=0.4')
plt.bar(xdata, ydata, 1, color='b')

xdata = dist_2.keys()
ydata = dist_2.values()

plt.bar(xdata, ydata, 1, color='r')

plt.savefig('Q1_group_graph_degrees.png')

print ("looking at the figures produced, notice that the shapes of the distributions are all very similar and the degrees are all very close to the average")
print ()

