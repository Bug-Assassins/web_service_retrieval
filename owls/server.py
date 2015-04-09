'''This script will accept user's input string and convert it into a list of
lemmas using wordnet. The script inputs a string as parameter and returns a
vector of lemmas'''

try:
    from nltk.corpus import wordnet as wn
    from nltk.corpus import genesis
    import sys
    import re
    import os
    import glob
    import subprocess
    from bs4 import BeautifulSoup
except :
    print "Dependencies Unmet !!"
    sys.exit(1)

#A list of delimiters to be used to split the user's input sting
delims = "\"", "'", ".", "\\", "/", "?", " ", "\t", "\r", "\n", "(", ")", "{", "}", ";", "&", "@", "~", "^", "*", "-"

#The Synsets of our categories
categories = [wn.synset('communication.n.01'), wn.synset('economy.n.01'), wn.synset('education.n.01'), wn.synset('food.n.01'), wn.synset('medicine.n.02'), wn.synset('travel.n.01'), wn.synset('weapon.n.01')]

#Loading Information Content
genesis_ic = wn.ic(genesis, False, 0.0)

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

# This function accepts a list of Lemmas and then returns a vector in 7 dimensional space
def vectorize_lemmas(lemma_list) :

    #Initializing Sum
    category_sim_sums = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    no_of_lemmas = len(lemma_list)
    sq_total = 0

    #Adding sums of all the lemma in each dimension
    for lemma in lemma_list :
        for i, category in enumerate(categories) :
            category_sim_sums[i] += lemma.jcn_similarity(category, genesis_ic)

    #Normalizing sum across all categories
    for i in range(7) :
        try :
            sq_total += (category_sim_sums[i] ** 2)
        except OverflowError:
            # Might Occur if similarity is very small
            sq_total += 0

    sq_root_total = sq_total ** 0.5

    if sq_root_total == 0 :
        sq_root_total = 1

    for i in range(7) :
        category_sim_sums[i] = category_sim_sums[i] / sq_root_total

    return category_sim_sums

def index_owls_data():

    file_count = 0
    fp = open("indexed_services_semantic","w+")

    for fname in os.listdir("docs"):
        try : 
            owl = open( "docs/" + fname ,'r').read()
        except IOError:
            print "Error Processing File : docs/" + fname
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

        category_sim_sums = vectorize_lemmas(owl_lemmas)
        st = ""

        for i in range(7) :
            if i > 0 :
                st += " "
            st += str(category_sim_sums[i])

        fp.write(fname + " : " + st + "\n")

        file_count = file_count + 1
        print file_count, " " + fname + "\n"

    print "No of Files OWLs Documents Indexed = ", file_count

if __name__ == '__main__':

    index_owls_data()

    #if len(sys.argv) != 2 :
    #    print "Invalid Number of Arguments Passed"
    #    exit()

    #input_lemmas = getsenses(sys.argv[1], pos_flag = wn.NOUN)
    #print input_lemmas