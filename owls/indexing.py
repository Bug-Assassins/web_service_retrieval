import os
import sys
import glob
import subprocess
import string
from os import listdir
try:
    from bs4 import BeautifulSoup
except ImportError:
    print "BeautifulSoup is missing"
    sys.exit(1)

# This Cut off is used to determine the similarity above which an edge is added between two
# service and below this no edge is added i.e., No path and no composition possible
GRAPH_EDGE_CUTOFF = 0.9

# This function accepts 2 7-dimensional vector and returns the cosine similarity between them
def cosine_similarity(u, v) :

    usq = 0
    vsq = 0
    num = 0

    for element in u :
        usq += (element ** 2)

    for element in v :
        vsq += (element ** 2)

    #Numerator is the dot Product
    for i in range(len(u)) :
        num += u[i] * v[i]

    #Denominator is the length of both vecs
    usq = (usq ** 0.5)
    vsq = (vsq ** 0.5)

    if num == 0 :
        sim = 0
    else :
        sim = num / (usq * vsq)

    return sim

#This function indexes OWls data using Keyword Approach
def keyword_indexing():
    file_count = 0
    fp = open("indexed_services","w+")
    file_list = os.listdir("docs")
    file_list.sort()
    for fname in file_list:
        try : 
            owl = open( "docs/" + fname ,'r').read()
        except IOError:
            print "Error Processing File : docs/" + fname
        soup = BeautifulSoup(owl)
        profile_in = soup.find_all('profile:hasinput')
        profile_out = soup.find_all('profile:hasoutput')

        in_str = []
        op_str = []

        keyerr = 0
        for inp in profile_in :
            in_attrs = dict(inp.attrs)
            try :
                in_str.append(in_attrs['rdf:resource'])
            except KeyError, e:
                keyerr = 1

        if keyerr == 1:
            process_in = soup.find_all('process:hasinput')
            in_str = []
            for inp in process_in : 
                in_attrs = dict(inp.attrs)
                try :
                    in_str.append(in_attrs['rdf:resource'])
                except KeyError, e:
                    print "Error Input (Key): " + fname

        inp_string = " ".join(set(in_str))
        inp_vec = subprocess.check_output(['./index_unit.sh', inp_string, "input"])

        keyerr = 0
        for out in profile_out :
            out_attrs = dict(out.attrs)
            try :
                op_str.append(out_attrs['rdf:resource'])
            except KeyError, e:
                keyerr = 1

        if keyerr == 1:
            process_out = soup.find_all('process:hasoutput')
            op_str = []
            for out in process_out : 
                out_attrs = dict(out.attrs)
                try :
                    op_str.append(out_attrs['rdf:resource'])
                except KeyError, e:
                    print "Error Output (Key): " + fname

        out_string = " ".join(set(op_str))

        out_vec = subprocess.check_output(['./index_unit.sh', out_string, "output"])
        fp.write(fname + " : " + inp_vec + " : " + out_vec + "\n")
        file_count += 1
        print "Processed File No ", file_count, " - ", fname
        
    print "Total Files Processed : ", file_count
    fp.close()


# A utility Function to check if there is a path from a given node to another given node
def check_cycle(graph, start, end) :

    visited = [False] * len(graph)
    dfs_stack = [start]

    while len(dfs_stack) > 0 :
        v = dfs_stack.pop()
        if visited[v] == False :
            visited[v] = True
            for node in graph[v][3] : 
                dfs_stack.append(node)
        if v == end :
            return True

    return False


# This function constructs an in-memory Directed Graph (may be cyclic) of all services
# Such that input matches output of another services
def construct_service_graph() :

    #Open the KeyWord Indexed File
    ind_file = open("indexed_services","r")

    # First Element in this list is Service Name
    # Second Element is Input Vector
    # Third Element is Output Vector
    # Fourth Element contains a list of indexes to which the node has outgoing edges

    graph = []
    no_of_edges = 0

    for line in ind_file :

        # Extract the indexed Vector
        text = line.split(':')
        inp_vec_text = string.translate(text[1].strip(), None, "\n").split()
        op_vec_text = string.translate(text[2].strip(), None, "\n").split()

        for i in range(7) :
            inp_vec_text[i] = int(inp_vec_text[i])
            op_vec_text[i] = int(op_vec_text[i])

        # Add one node to graph for each service
        node = []
        node.append(text[0])
        node.append(inp_vec_text)
        node.append(op_vec_text)
        node.append([])

        graph.append(node)

    print len(graph) , " Nodes Added to Graph !!"

    # Finding Destination and Appending
    for i in range(len(graph)) :

        for j in range(len(graph)) :

            if i == j :
                continue

            sim = cosine_similarity(graph[i][2], graph[j][1])
            if sim > GRAPH_EDGE_CUTOFF and check_cycle(graph, i, j) == False:
                graph[i][3].append(j)
                no_of_edges += 1

    print no_of_edges , " Edges added to the Graph !!"

    return graph