from crawler import *
import requests
from bs4 import BeautifulSoup
from bs4.element import Comment
import re
import string
from nltk.stem.porter import PorterStemmer
import csv
import pandas as pd

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


def find_helper(phrase, dictionary):
    words = []
    frequencies = []
    positing_lists = []
    dict_from_csv = pd.read_csv('scraping.csv').to_dict()
    for i in dict_from_csv['Word']:
        words.append(dict_from_csv['Word'][i])
    for j in dict_from_csv['Frequency']:
        frequencies.append(dict_from_csv['Frequency'][j])
    for k in dict_from_csv['Posting List']:
        positing_lists.append(dict_from_csv['Posting List'][k])

    #try loop thtough words list, find numerical index of those words, take their https stuff
    #then go by those index number over posting list and try to get the http stuff
    #phrase = phrase.lower()
    #words_phrase = phrase.split()
    #for word in words_phrase:
    #    for e in words:
    #        if word==e:#



#This command is used to find a certain query phrase in the inverted index and returns a list of all pages containing this phrase, for example:
#find Dinar
#will return a list of all pages containing the word ‘Dinar’, while
#find Area Afghanistan
#will return all pages containing the words ‘Area’ and ‘Afghanistan’.
#For simplicity assume that the search is case sensitive, so ‘Euro’ is not the same word as ‘euro’.
def find(phrase, dictionary):
    phrase = phrase.lower()
    list_indexed_tuples = []
    words = phrase.split() #take specific words for the phrase
    for word in words:
        for key in dictionary.keys():
            if word==key:
                list_indexed_tuples.append(dictionary[word])
    print(list_indexed_tuples[0][1])
    print(type(list_indexed_tuples[0][1])) #okay, czyli całość tutaj to string... nie wiem jak by to zamieniać,
    #gdyby chcieć porównywać pojedyńczo, trzeba by dla każdego url robić jedno porównanie słowa
    #tj gdy słowo jest w trzech urls, mamy 3 entries, bo to dla każdego to będzie coś
    #print(list_indexed_tuples[1]) #here we access the tuple
    #print(list_indexed_tuples[1][1]) #here we're accessing the second part of the tuple i.e. the list of tuples with http and numbers
    #print(list_indexed_tuples[1][1][1]) #but here...here we already have that that this is treaten as separate characters


    #for word in words:
    #    for key in dictionary.keys():
    #        if word == key:
    #            list_indexed_tuples.append(dictionary[word]) #działa, teraz trzeba zrobić iterację na liście w tuples,
                                                            # by zobczyć gdzie śą jednakowe rzeczy

    list_of_tuple_urls = []
    urls_extract = []
    #for x in list_indexed_tuples: #all elements in list - so here one for peso, one for a
        #print(x[1]) #each x[1] is a list of tuples, with first element of each tuple being a url string
    #    list_of_tuple_urls.append(x[1])

    #made_urls = []
    #var= ''
    #for element in list_of_tuple_urls:
    #    for y in element:
    #        var = var+y #...aha, czyli wszystko jest traktowane jako pojedyńcze znaki w każdym elemencie
            #maybe try to piece http into one thing thing? and put them together somewhere then...

    #print(var)
    #chunks = var.split(',')
    #print(chunks[0])

