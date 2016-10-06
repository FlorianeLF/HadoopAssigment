# -*- coding: utf-8 -*-

import re

import collections

import itertools


#split the text received in words and associate 1 to each of
def map(sentence):
    
    words = re.findall(r'[a-zA-Z]+',sentence) # split the sentence in words
    
    words = ([ [word, 1] for word in words ]) # associate 1 to each word
    
    return words

# create a dictionary with each word as value and a list of 1 as key
# then split it to send each sub dictionary to a reducer
def shuffle(words, REDUCERS_NUMBER):
    
    dictionary = {} # initialize an empty dictionary

    for word in words:
        
        if word[0] in dictionary: # check if the word is already in the dictionary
            
            dictionary[word[0]].append(1) # add 1 to the list of the word's values
            
        else:
            
            dictionary[word[0]] = [1] # add the word into the dictionary

    dictionary = collections.OrderedDict(sorted(dictionary.items())) # sort alphabetically the dictionary
        
    nmberWords = (len(dictionary)//REDUCERS_NUMBER)+1 # compute number of words per reducer

    it = iter(dictionary) #create an iterable
    
    for i in range(0, len(dictionary), nmberWords):
        
        yield {k:dictionary[k] for k in itertools.islice(it, nmberWords)} # return REDUCERS_NUMBER sub dictionaries


# compute the number of 1 associated to each word
def reduce(words):
    
    for key,value in words.items():
        
        words[key] = len(value)
        
    print(words)
   

REDUCERS_NUMBER = 5 #set number of reducers
MAPPERS_NUMBER = 4 #set number of mappers

# Read the text from a file
file = open("text.txt", "r")
text = file.read()
file.close()

# split the text into sentences
sentences = re.split('(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)(\s|[A-Z].*)',text)

# compute sentences number for each mapper
numberSentences = len(sentences)//MAPPERS_NUMBER

result = []
   
# send each sentences block to a mapper and compute the result of all mappers
for i in range(0, len(sentences), numberSentences):
    sentence = ""
    for j in range (i, i+numberSentences-1):
        sentence+=sentences[j].lower() # add the computed number of sentences for a mapper and remove all capital letters
    result.extend(map(sentence)) #gathering all mappers' results in one array
    
reducNumber = 1

# shuffle and reduce then print the outputs
for item in  shuffle(result, REDUCERS_NUMBER):
    print ("----------------------------------")
    print("Reducer ", reducNumber)
    reduce(item)
    reducNumber = reducNumber+1
