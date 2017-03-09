# networks assignment
# question three
# alex gillies

import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import random
import queue
import PA # VERY IMPORTANT TO HAVE AS WELL

####################################################################################################################################

def make_random_graph(num_nodes, prob):
    """Returns a dictionary to a random graph with the specified number of nodes
    and edge probability.  The nodes of the graph are numbered 0 to
    num_nodes - 1.  For every pair of nodes, i and j, the pair is considered
    twice: once to add an edge (i,j) with probability prob, and then to add an
    edge (j,i) with probability prob. 
    """

    random_graph = {}

    for x in range(num_nodes):
        random_graph[x] = set([])

    for x in range(num_nodes):
        # iterate through every node
        for y in range(num_nodes):
            if x != y:
                # iterate through every other node
                random_number = random.random()
                # get a random number
                if random_number < prob:
                    # if there should be an edge
                    random_graph[x].add(y)
                    random_graph[y].add(x)
                    # add the edges to the correct places

    return random_graph

####################################################################################################################################

def make_PA_Graph(total_nodes, out_degree):
    """creates a PA_Graph on total_nodes where each vertex is iteratively
    connected to a number of existing nodes equal to out_degree"""
    #initialize graph by creating complete graph and trial object
    PA_graph = PA.make_complete_graph(out_degree)
    trial = PA.PATrial(out_degree)
    for vertex in range(out_degree, total_nodes):
        PA_graph[vertex] = trial.run_trial(out_degree)

    for x, edges in PA_graph.items():
        for y in list(edges):
            # iterate through each node and it's neighbours
            if not x in PA_graph[y]:
                PA_graph[y].add(x)

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

                    print(str(x) + " added to " + str(y))
                    print(str(y) + " added to " + str(x))
                    print("")

    print("#############################")
    
    # iterate through all the nodes in a given nodes group
    # get some random numnber, if it passes then add this vertex to the list of connected nodes, this needs to be done both ways

    for x in range(1,m*k+1):
        for y in range(x,m*k+1):
            test_random = random.random()

            if test_random < q and (not y in graph[x]) and (not x in graph[y]):
                graph[x].append(y)
                graph[y].append(x)

                print(str(x) + " added to " + str(y))
                print(str(y) + " added to " + str(x))
                print("")

    # iterate through all nodes not in a given nodes group

    # get some random number, if it passes then add this vertex to the list of connected nodes, this needs to be done both ways

    # print (str(m) + ", " + str(k) + ", " + str(p) + ", " + str(q))
    # print (graph)

    return graph

random.seed("test")

print(make_group_graph(5,5,0.4,0.1))

####################################################################################################################################

def search_random_graph(numberOfNodes, connectivity, start, end):
    """ given the number of nodes in a random graph and the integers of the start and end nodes. find the shortest path form the start node to the end node """

    # create random graph from parameter values
    # go the the start value and find the path to the end value

    graph = make_random_graph(numberOfNodes, connectivity)
    print(graph)

    startNode = start
    currentNode = start
    endNode = end

    visitedNodes = []

    # from current node
    # if connected to end node
    # move to end node
    # else
    # choose random unvisited node
    # else go to random visited node

    while currentNode != endNode:
        visitedNodes.append(currentNode)
        # add the current node to the visited nodes
        neighbours = graph[currentNode]
        # a list of the neighbours
        numberOfNeighbours = len(neighbours)
        # the number of neighbours
        if endNode in neighbours:
            # if the current node is connected to the end node
            currentNode = endNode
            # go to the end node
        else:
            unvisitedNodesSet = set(neighbours) - set(visitedNodes)
            unvisitedNodes = list(unvisitedNodesSet)
            # find all unvisited nodes of the current node
            if len(unvisitedNodes) > 0:
                # if there are unvisited nodes
                currentNode = unvisitedNodes[random.randrange(0,len(unvisitedNodes))]
                # go to a random one of them
            else:
                # else there are no unvisited nodes
                currentNode = list(neighbours)[random.randrange(len(neighbours))]
                # go to a random visited neighbour

    print(visitedNodes)
    return len(visitedNodes)

####################################################################################################################################

# def search_PA_graph(numberOfNodes, outDegree, start, end):
#     """ given the number of nodes in a random graph and the integers of the start and end nodes. find the shortest path form the start node to the end node """

#     # create a PA graph
#     # from the start node find the end node and output the number of steps

#     graph = make_PA_Graph(numberOfNodes, outDegree)
#     print(graph)

#     # if node in neighbours of start node
#     # move to that node
#     # else if
#     # univisted nodes in complete subgraph
#     # move to one of these at random
#     # else if
#     # unvisited nodes outside of complete subgraph
#     # move to one of these
#     # else if
#     # move to random visited node in compete subgraph
#     # else if
#     # move to random visited node outside complete subgraph

#     startNode = start
#     currentNode = start
#     endNode = end

#     visitedNodes = []

#     while currentNode != endNode:
#         visitedNodes.append(currentNode)
#         # add the current node to the list of visited nodes
#         neighbours = graph[currentNode]
#         # get a list of neighbours of the current node
#         numberOfNeighbours = len(neighbours)
#         # get the number of neighbours
#         if endNode in neighbours:
#             # if the end node is in the list of neighbours
#             currentNode = endNode
#             # we have reached the end
#         else:
            

####################################################################################################################################

def search_group_graph(m, k, p, q, start, end):
    """ given the number of nodes in a random graph and the integers of the start and end nodes. find the shortest path form the start node to the end node """

    # create a group graph
    # from the start node find the end node and output the number of steps

    graph = make_group_graph(m, k, p, q)
    print(graph)

    startNode = start
    currentNode = start
    endNode = end
    currentGroup = get_group(startNode, m, k)
    endGroup = get_group(endNode, m, k)

    visitedNodes = []

    if p >= 0.4:
        # if there is significant p probability meaning that it is more likely to have a connection inside the group
        while currentNode != endNode:
            visitedNodes.append(currentNode)
            # add the current node to the visited nodes

            # find all nodes in the destination group
            # if we can reach them then go to one
            # if we can't then go to somewhere in the same group
            # if we can't do that then go to a random node

            neighbours = graph[currentNode]
            # get all neighbours of the current node

            if endNode in neighbours:
                # if the end node is connected to the current node
                currentNode = endNode
                # we have reached the end
            else:
                accessableEndGroup = set(neighbours) - set(endGroup)
                if len(accessableEndGroup) > 0:
                    # if we can go to the group that the end node is in
                    index = random.randrange(len(accessableEndGroup))
                    # get a random index of a node in the end group
                    currentNode = list(accessableEndGroup)[index]
                    # go to that node
                else:
                    # get a random neighbour and go to that one
                    index = random.randrange(len(neighbours))
                    currentNode = neighbours[index]

    print(visitedNodes)
    return len(visitedNodes)

    # if there is significant q probability meaning that it is more likely to have a connection outside the group

####################################################################################################################################

def get_group(node, m, k):
    """ get all nodes that are in any given group """

    graph = []

    for x in range(m*k):
        graph.append(x)

    group = int(node/k)
    group_range = graph[group*m:(group+1)*m]

    # print(group)
    # print(group_range)

    return group_range

####################################################################################################################################
"""
# SEARCHING IN RANDOM

size = 20
connectivity = random.random()
start = random.randrange(0, size)
end = random.randrange(0, size)

if start != end:
    print("Start: " + str(start) + " End: " + str(end) + " Connectivity: " + str(connectivity))
    print("Number of steps taken: " + str(search_random_graph(size,connectivity,start,end)))

####################################################################################################################################

# SEARCHING IN PA 

size = 20
outDegree = random.randrange(1, size) # this should be tested
start = random.randrange(0, size)
end = random.randrange(0, size)

if start != end:
    print("Start: " + str(start) + " End: " + str(end) + " OutDegree: " + str(outDegree))
    print("Number of steps taken: " + str(search_PA_graph(size,outDegree,start,end)))

####################################################################################################################################

# SEARCHING IN GROUP

m = 5
k = 5
p = 0.4
q = 0.1
start = random.randrange(0, m*k)
end = random.randrange(0, m*k)

if start != end:
    print("Start: " + str(start) + " End: " + str(end) + "          " + " M: " + str(m) + " K: " + str(k) + " P: " + str(p) + " Q: " + str(q))
    print("Number of steps taken: " + str(search_group_graph(m, k, p, q, start, end)))
"""
####################################################################################################################################
