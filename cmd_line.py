from crawler import *
from print_and_find import print_index, find
import requests
from bs4 import BeautifulSoup
from bs4.element import Comment
import re
import string
from nltk.stem.porter import PorterStemmer
import csv
import pandas as pd
import sys
maxInt = sys.maxsize


index = {}
#urls = []
dict_from_csv = {}
new_index = {}



def visible_text(element):
    if element.parent.name in ['style', 'title', 'script', 'head', '[document]', 'class', 'a', 'li']:
        return False
    elif isinstance(element, Comment):
        return False
    elif re.match(r"[\s\r\n]+", str(element)):
        return False
    return True


def read_url(url):
    ps = PorterStemmer()

    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    text = soup.findAll(text=True)
    result = list(filter(visible_text, text))
    counter = 0;
    words = []
    for i in result:
        temp = i.split(' ')
        for word in temp:
            k = []
            temp_word = word.lower()
            for c in temp_word:
                if c not in list(string.punctuation):
                    k.append(c)
            temp_word = ''.join(k)
            words.append(temp_word)
    for i in words:
        if (i.isalpha()):
            i = ps.stem(i)
            if not i in index.keys(): #or - if i not in index.keys():
                index[i] = [url] #index[i] = [(url, counter)] #jeszcze sprawdź co to jest counter - znaczy,
                counter = counter + len(i) + 1
            else:
                index[i].append(url) #index[i].append((url, counter))
                counter = counter + len(i) + 1

    return None


#This command loads the index from the file system.
#Obviously, this command will only work if the index has previously been created using the ‘build’ command
#so, here i try loading index from file into a dictionary
def load():
    dict_from_csv = pd.read_csv('scraping.csv').to_dict()
    #print(dict_from_csv.keys()) #shows keys as Word, Frequency, List when dict_from_csv = pd.read_csv('scraping.csv').to_dict()
    #print(dict_from_csv['Word'][0]) #this prints a
    words = []
    frequencies = []
    positing_lists = []
    for i in dict_from_csv['Word']:
        words.append(dict_from_csv['Word'][i])
    for j in dict_from_csv['Frequency']:
        frequencies.append(dict_from_csv['Frequency'][j])
    for k in dict_from_csv['Posting List']:
        positing_lists.append(dict_from_csv['Posting List'][k])
    #okay, now trying to make a new dictionary index out of those lists
    new_index = dict(zip(words, zip(frequencies, positing_lists))) #this would only take the stuff with 2 values
    #so we put lists second and third together for now
    return new_index


while True:
    # decrease the maxInt value by factor 10
    # as long as the OverflowError occurs.

        command_line = input('Enter command to run: ')
        words = command_line.split() #take all the input string here divided into specific words
        command = words[0]
        words.pop(0) #removed the first word from the list, now we can again get the whole phrase for print/find commands
        phrase = listToStr = ' '.join([str(elem) for elem in words])
        crawler = Crawler(urls=['http://example.python-scraping.com/'])

        if command == "quit":
            print('Exiting the program') #doesn't print stuff; quit works for breaking of the program but doesn't print stuff there
            exit(1)

        elif command == "build":
            urls = crawler.run() #dla sprawdzenia, przed zaczęciem inverted index
            for url in urls:
                if url != '#':
                    read_url(url)

            sorted_keys = sorted(index.keys())
            with open('scraping.csv', 'w') as indexFile: #works now!
                fieldNames = ['Word', 'Frequency', 'Posting List']
                csvWriter = csv.DictWriter(indexFile, fieldnames=fieldNames)  # create writeDirectory object
                csvWriter.writeheader()  # writing the header
                for i in sorted_keys:
                    csvWriter.writerow({'Word': i, 'Frequency': len(index[i]), 'Posting List': index[i]})

        elif command == "load":
            new_index=load()
        elif command == "print":
            print_index(phrase, new_index)
        elif command == "find":
            find(phrase, new_index)
        else:
            print("Command not found")



