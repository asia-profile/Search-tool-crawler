import requests
from bs4 import BeautifulSoup
import csv
from functools import reduce
import re
import operator
from collections import Counter
import pandas as pd
from nltk.stem.porter import PorterStemmer

#dict_from_csv = {} #dictionary for index to fill with load command

#This command instructs the search tool to crawl the website,
#build the index, and save the resulting index into the file system
#An inverted index that stores the frequency of occurrence of each word in each page must be created by the tool
#as it crawls the pages of the website
def build():
    # empty list to store the contents of
    # the website fetched from our web-crawler
    url = "http://example.python-scraping.com/"
    wordlist = []
    source_code = requests.get(url)#.text
    data = source_code.text
    # BeautifulSoup object which will
    # ping the requested url for data
    soup = BeautifulSoup(data, 'html.parser') #soup = BeautifulSoup(source_code, 'html.parser')

    # Text in given web-page is stored under
    # the <div> tags with class <entry-content>
    for each_text in soup.findAll('div', {'class': 'entry-content'}): #might change here a bit
        content = each_text.text

        # use split() to break the sentence into
        # words and convert them into lowercase
        words = content.lower().split()

        for each_word in words:
            wordlist.append(each_word)
        clean_wordlist(wordlist, soup)


# Function removes any unwanted symbols
def clean_wordlist(wordlist, soup):
    clean_list = []
    for word in wordlist:
        symbols = "!@#$%^&*()_-+={[}]|\;:\"<>?/., "

        for i in range(len(symbols)):
            word = word.replace(symbols[i], '')

        if len(word) > 0:
            clean_list.append(word)
    #create_dictionary(clean_list)
    save_dictionary(clean_list, soup)

def save_dictionary(clean_list, soup):

    #csv_file = open('scraping.csv', 'w')
    #csv_writer=csv.writer(csv_file)
    #csv_writer.writerow(['index', 'data']) #our headers for now i think - the column

    dictionary = {}
    #this one is based on creating inverted index for a file function
    #where they work with files in a directory
    #tried to work it out for me
    for word in clean_list:
        #checking if word is new of not
        if word not in dictionary.keys():
            #if new make an entry in dictionary for this word
            dictionary[word] = {}
            #dictionary[word]['fileNames'] = {}
            #dictionary[word]['filePaths'] = {}
            dictionary[word]['pageNames'] = {}
            dictionary[word]['occurrenceNumber'] = {}
            
        #adding the file and its path to the dictionary
        #now how to add the page names and the occurence number to the dictionary
        dictionary[word]['pageNames'] += []
        dictionary[word]['occurrenceNumber'] += [len( soup.find_all( "div", string=lambda text: word in text.lower()) )]



    #for i in range(clean_list): #need some fixing here i think
    #    check = array[i].lower()
    #    for item in tokens_without_sw:

    #        if item in check:
    #            if item not in dict:
    #                dictionary[item] = []
                    #csv_writer.writerow(dictionary[item])

    #            if item in dict:
    #                dictionary[item].append(i+1)
                    #csv_writer.writerow(dictionary[item])

    #csv_file.close()
    write_to_file(dictionary)

def write_to_file(dictionary):
    #might change names from fileNames and filePaths, since we have a website, so ig it would be a bit different
    with open('scraping.csv', 'w') as indexFile:
        #declare field names
        #fieldNames = ['word', 'filename', 'filepaths']
        fieldNames = ['word', 'pageName', 'occurrenceNumber']
        #create writeDirectory object
        csvWriter  = csv.DictWriter(indexFile, fieldnames=fieldNames)
        #writing the header
        csvWriter.writeheader()

        for word, fileDetails in dictionary.items():
            #creating string of all the file names and all the file paths
            #fileNameString = reduce(lambda x, y: x + ", " + y, fileDetails['fileNames'])
            #filePathsString = reduce(lambda x, y: x + ", " + y, fileDetails['filePaths'])
            pageNameString = reduce(lambda x, y: x + ", " + y, fileDetails['pageNames'])
            occurenceNumberString = reduce(lambda x, y: x + ", " + y, fileDetails['occurrenceNumber'])

            #writing the row
            #csvWriter.writerow({'word': word, 'filename': fileNameString, 'pathname': filePathsString})
            csvWriter.writerow({'word': word, 'pagename': pageNameString, 'occurrence': occurenceNumberString})


#This command loads the index from the file system.
#Obviously, this command will only work if the index has previously been created using the ‘build’ command
#so, here i try loading index from file into a dictionary
def load():

    dict_from_csv = pd.read_csv('csv_file.csv', header=None, index_col=0, squeeze=True).to_dict()
    print(dict_from_csv)

