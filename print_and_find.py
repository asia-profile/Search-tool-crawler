from crawler import *
import requests
from bs4 import BeautifulSoup
from bs4.element import Comment
import re
import string
from nltk.stem.porter import PorterStemmer
import csv
import pandas as pd
import collections

#This command prints the inverted index for a particular word, for example:
#print Peso
#will print the inverted index for the word ‘Peso’
#Note: ...should I just print stuff there directly by putting in the code, because otherwise we shadow the normal print
def print_index(phrase, dictionary):
    phrase = phrase.lower() #make sure the phrase is lowercase now, just as everything in index
    #print(dictionary[phrase]) #używanie tego tylko działa
    for word_key in dictionary.keys():
        if word_key == phrase:
            print("Index for " + phrase + ": ")
            print(dictionary[word_key])


#This command is used to find a certain query phrase in the inverted index and returns a list of all pages containing this phrase, for example:
#find Dinar
#will return a list of all pages containing the word ‘Dinar’, while
#find Area Afghanistan
#will return all pages containing the words ‘Area’ and ‘Afghanistan’.
#For simplicity assume that the search is case sensitive, so ‘Euro’ is not the same word as ‘euro’.
def find(phrase, dictionary):
    all_got_urls = []
    x_list=[]
    phrase = phrase.lower()
    list_indexed_tuples = []
    words = phrase.split() #take specific words for the phrase
    for word in words:
        for key in dictionary.keys():
            if word==key:
                list_indexed_tuples.append(dictionary[word])
    #print(list_indexed_tuples[0][1])
    #print(type(list_indexed_tuples[0][1])) #okay, czyli całość tutaj to string... nie wiem jak by to zamieniać,
    #gdyby chcieć porównywać pojedyńczo, trzeba by dla każdego url robić jedno porównanie słowa
    #tj gdy słowo jest w trzech urls, mamy 3 entries, bo to dla każdego to będzie coś
    for i in range(len(list_indexed_tuples)):
        x = list_indexed_tuples[i][1].strip("[' ']")
        x_list.append(x)
        #print(x)

    for j in range(len(x_list)):
        # split string by ,
        #print(x_list[j])
        chunks = x_list[j].split(',')
        for ch in chunks:
            ch = ch.strip("[' ']")
            #print(ch)
            all_got_urls.append(ch)

    print("Urls with the words: ")
    #print out repeating urls
    print([item for item, count in collections.Counter(all_got_urls).items() if count > 1])

    #now that we have clear urls, we need to iterate over them and see if the url addresses repeat
    #if they do, then store them in the final list, which will then be shown


    #print(list_indexed_tuples[1]) #here we access the tuple
    #print(list_indexed_tuples[1][1]) #here we're accessing the second part of the tuple i.e. the list of tuples with http and numbers
    #print(list_indexed_tuples[1][1][1]) #but here...here we already have that that this is treaten as separate characters



