'''This script will accept user's input string and convert it into a list of
lemmas using wordnet. The script inputs a string as parameter and returns a
vector of lemmas'''

try:
    from operator import itemgetter
    from nltk.corpus import wordnet as wn
    from nltk.corpus import genesis
    import string
    import sys
    import re
    import os
    import glob
    import subprocess
    import socket
    from bs4 import BeautifulSoup
    from os import listdir
    from indexing import *
except :
    print "Dependencies Unmet !!"
    sys.exit(1)

#A list of delimiters to be used to split the user's input sting
delims = "\"", "'", ".", "\\", "/", "?", " ", "\t", "\r", "\n", "(", ")", "{", "}", ";", "&", "@", "~", "^", "*", "-"

#The Synsets of our categories
categories = [
            wn.synset('communication.n.01'),
            wn.synset('economy.n.01'),
            wn.synset('education.n.01'),
            wn.synset('food.n.01'),
            wn.synset('medicine.n.02'),
            wn.synset('travel.n.01'),
            wn.synset('weapon.n.01')
            ]

#Loading Information Content
genesis_ic = wn.ic(genesis, False, 0.0)

#Path for the owls documents
owls_path = "docs"
index_file_path = "indexed_services_semantic"

#Socket Configuration
HOST = '' #Empty string = accept connection from any host
PORT = 12002 #Port Number to be used for listening
COMPOSITE_PORT = 12010

# Composite Query variables
COMPOSITE_SIMILARITY_CUTOFF = 0.8
graph = None

#Compare function to sort lists according to length
def compare_len(x, y) :
    return len(x) - len(y)

#Function that disambiguates a word sense based on established context
def disambiguate(info_context, sense_list) :

    max_val = -1
    max_ind = -1

    #Iterating through all the senses of the word
    #print "Passed Sense List = ", sense_list
    for i, sense in enumerate(sense_list) :

        sim = 0

        #Finding Summation Similarity with Established Context
        for context in info_context :
            sim = sim + sense.jcn_similarity(context, genesis_ic)

        if sim >= max_val :
            max_val = sim
            max_ind = i

    #Returning Disambiguated Sense
    return sense_list[i]

#Function that converts a given input string to a list of senses
def getsenses(str, pos_flag) :

    delim = "[\"\.'\\/ \t\r\n\(\){};&@~^\*-+]+"
    d = "[ \t\n\r]"
    #Split the string based on the list of the separators
    regexPattern = '|'.join(map(re.escape, delims))
    keyword_list = re.split(regexPattern, str)

    input_syn_list = []
    #Iterating through all keywords
    for keyword in keyword_list :
        #Stripping keyword
        keyword = keyword.strip()
        if len(keyword) < 3 :
            continue

        synset_list = wn.synsets(keyword, pos_flag)
        if len(synset_list) == 0 :
            #No Synset Found. Leaving this keyword!!
            continue
        else :
            input_syn_list.append(synset_list)

    if len(input_syn_list) == 0 :
        return []

    input_syn_list.sort(cmp = compare_len)
    query = []
    #print "Input Keyword List = ", input_syn_list

    if len(input_syn_list[0]) == 1 :
        #This means a context can be established as 1st keyword is already disambiguated\
        #print "Context = ", input_syn_list[0][0]
        query.append(input_syn_list[0][0])

        #Iterating through all other words and disambiguating the meaning
        for keyword in input_syn_list[1:] :
            query.append(disambiguate(query, keyword))

    else :
        #This Means No Context can be established initially
        if len(input_syn_list) == 1 :
            #If only one keyword then use the most frequently used sense
            query.append(input_syn_list[0])

        else :
            #Using first 2 keywords to establish context
            max_sim = -1
            max_ind_i = -1
            max_ind_j = -1
            for i, sen1 in enumerate(input_syn_list[0]) :
                for j, sen2 in enumerate(input_syn_list[1]) :
                    sim = sen1.jcn_similarity(sen2, genesis_ic)
                    #print "Match for ", sen1, sen2, " Val = ", sim
                    if sim > max_sim :
                        #print "Max"
                        max_sim = sim
                        max_ind_i = i
                        max_ind_j = j

            query.append(input_syn_list[0][max_ind_i])
            query.append(input_syn_list[1][max_ind_j])
            #print "Sense for ", keyword_list[0], " Sense = ", input_syn_list[0][i]
            #print "Sense for ", keyword_list[1], " Sense = ", input_syn_list[1][i]

            #Disambiguating remaining keywords based on established context
            for keyword in input_syn_list[2:] :
                query.append(disambiguate(query, keyword))

    return query

# This function index all the OWLs files in docs folder and indexed data is
# written in a text file
def semantic_indexing():

    file_count = 0
    fp = open(index_file_path, "w+")

    for fname in os.listdir(owls_path):
        try : 
            owl = open(os.path.join(owls_path, fname),'r').read()
        except IOError:
            print "Error Processing File : "+ os.path.join(owls_path, fname)
        soup = BeautifulSoup(owl)

        #Finding all Text Description of the OWLs file
        text_descriptions = soup.find_all('profile:textdescription')

        if len(text_descriptions) == 0 :
            print "No Description Found for " + fname
            continue
        elif len(text_descriptions) > 1 :
            print "Multiple Text Description Found For " + fname
            continue

        description = text_descriptions[0].text.strip()

        #Getting Lemmas of the text description of this file
        owl_lemmas = getsenses(description, pos_flag = wn.NOUN)

        sstr = ""
        for i in range(len(owl_lemmas) - 1) :
            sstr += owl_lemmas[i].name() + ","
        sstr += owl_lemmas[len(owl_lemmas) - 1].name()

        fp.write(fname + " : " + sstr + "\n")

        file_count = file_count + 1
        # print file_count, " " + fname + "\n"

    print "No of Files OWLs Documents Indexed = ", file_count

# This function searches the semantically index web services linearly to find a match
def linear_query(query_string) :

    query_lemmas = getsenses(query_string, pos_flag = wn.NOUN)

    ind_file = open(index_file_path, "r")
    result = []

    for line in ind_file :
        text = line.split(':')
        owl_lemmas = string.translate(text[1].strip(), None, "\n").split(',')

        total_sim = 0

        for s in owl_lemmas :
            ol = wn.synset(s)
            for ql in query_lemmas :
                sim = ol.jcn_similarity(ql, genesis_ic)
                if sim > 1 :
                    total_sim += 1
                else :
                    total_sim += sim

        total_sim = total_sim / (len(owl_lemmas) * len(query_lemmas))
        if total_sim > 2 :
            print "owl_lemmas = ", owl_lemmas
            print "query_lemmas = ", query_lemmas

        temp = [total_sim]
        temp.append(text[0])

        result.append(temp)

    #Sort according to similarity
    result.sort(key = itemgetter(0))
    result.reverse()
    for i in range(len(result)) :
        result[i].append(i)

    #Sort by name - 3rd element is rank
    result.sort(key = itemgetter(1))
    return result

def keyword_query(service_input, service_output) :

    #Executing Script
    subprocess.check_output(["./main.sh", service_input, service_output, '0'])

    #Read Keyword Result
    res = open('result.temp', 'r')

    keyword_res = []

    ind = int(1)
    for ser in res :
        text = ser.split(':')
        temp = [text[0].strip()]
        temp.append(ind)
        temp.append(float(text[2].strip())) # Input Score
        temp.append(float(text[3].strip())) # Output Score
        keyword_res.append(temp)
        ind += 1

    res.close()

    return keyword_res

#This function takes in directly the user query string and applies both
#semantic and keyowrd based approach to determine matching owls docs
def combined_query(query) :

    #Executing semantic Query and Keyword Query
    semantic_res = linear_query(query[0] + " " + query[1])
    keyword_res = keyword_query(query[0], query[1])

    keyword_res.sort(key = itemgetter(0))

    if len(keyword_res) != len(semantic_res) :
        print "Wrong Length of Result - keyword = ", len(keyword_res), " sem = ", len(semantic_res)
        sys.exit(1)

    for i in range(len(semantic_res)) :

        if semantic_res[i][1].strip() != keyword_res[i][0].strip() :
            print "Names Unequal = ", semantic_res[i][1], ", ", keyword_res[i][0]
            sys.exit(1)

        keyword_res[i][1] += semantic_res[i][2]
        keyword_res[i][1] /= 2

    keyword_res.sort(key = itemgetter(1))

    return keyword_res

# This function tries to find a composite service
def composite_query(query) :

    keyword_res = keyword_query(query[0], query[1]).sort(key = itemgetter(2))

    # Filtering Results
    filtered_res = None
    if len(keyword_res) < 10 :
        filtered_res = keyword_res
    else :
        filtered_res = keyword_res[0:10]

    visited = []
    for i in range(10) :
        visited.append(False)



# Main Function to that keeps listening for input
if __name__ == '__main__':

    if len(sys.argv) > 1 :
        if sys.argv[1] == "semanticindex" :
            print "Indexing Services Semantically !!"
            semantic_indexing()
            print "Semantic Indexing of Services Done !!"

        elif sys.argv[1] == "vectorindex" :
            print "Indexing Services using Keywords !!"
            keyword_indexing()
            print "Keyword Indexing of Sevices Done !!"

        elif sys.argv[1] == "runserver" :

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Constructing Graph if composite services has to be discovered
            if len(sys.argv) > 2 and sys.argv[2] == "composite" :
                print "Constructing Composite Graph"
                graph = construct_service_graph()
                s.bind((HOST, COMPOSITE_PORT))
                print "Composite Graph Constructed"
            else :
                s.bind((HOST, PORT))

            s.listen(1)
            print "Server Up and Running!!"
            while True :
                try :
                    # Receiving Data
                    conn, addr = s.accept()
                    data = conn.recv(10000)
                    if not data :
                        print "No data received"
                        conn.close()
                        return

                    #Spliting data into input and output
                    data = str(data).split('#')
                    print "Request by - ", addr, " Query = ", data
                    res = combined_query(data)
                    
                    reply = ''
                    for item in res :
                        reply = reply + item[0] + ','

                    conn.sendall(reply)
                    conn.close()

                except Exception :
                    print "Problem is Processing Query !!"

            for result in keyword_res :
                print result[0], " ", result[1]

    else :
        print "Invalid Arguments Passed"

    #if len(sys.argv) != 2 :
    #    print "Invalid Number of Arguments Passed"
    #    exit()

    #input_lemmas = getsenses(sys.argv[1], pos_flag = wn.NOUN)
    #print input_lemmas