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
    for word_key in dictionary.keys():
        if dictionary[word_key] == phrase:
            print(dictionary[word_key])


#This command is used to find a certain query phrase in the inverted index and returns a list of all pages containing this phrase, for example:
#find Dinar
#will return a list of all pages containing the word ‘Dinar’, while
#find Area Afghanistan
#will return all pages containing the words ‘Area’ and ‘Afghanistan’.
#For simplicity assume that the search is case sensitive, so ‘Euro’ is not the same word as ‘euro’.
def find(phrase, dictionary):
    print(phrase)