from crawler import *
import requests
from bs4 import BeautifulSoup
from bs4.element import Comment
import re
import string
from nltk.stem.porter import PorterStemmer
import csv
import pandas as pd

index = {}
#urls = []
dict_from_csv = {}


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
                index[i] = [(url, counter)]
                counter = counter + len(i) + 1
            else:
                index[i].append((url, counter))
                counter = counter + len(i) + 1

    return None


#This command loads the index from the file system.
#Obviously, this command will only work if the index has previously been created using the ‘build’ command
#so, here i try loading index from file into a dictionary
def load():
    dict_from_csv = pd.read_csv('scraping.csv', header=None, index_col=0, squeeze=True).to_dict()
    #dict_from_csv.append(pd.read_csv('scraping.csv', header=None, index_col=0, squeeze=True).to_dict())
    print(dict_from_csv)
    #działa :)


while True:
        command_line = input('Enter command to run: ')
        #okay doesn't seem to get annythin doing after entering command, doesn't print stuff
        words = command_line.split() #take all the input string here divided into specific words
        command = words[0]
        words.pop(0) #removed the first word from the list, now we can again get the whole phrase for print/find commands
        phrase = listToStr = ' '.join([str(elem) for elem in words])
            #phrase = phrase.join(words) #okay, no, beacuse it gives it like a joined word
        #print(command_line)
        #print(words)
        #works now, print become shadowed by the print function implemented - so the menu is all right
        crawler = Crawler(urls=['http://example.python-scraping.com/'])

        if command == "quit":
            print('Exiting the program') #doesn't print stuff; quit works for breaking of the program but doesn't print stuff there
            exit(1)
        elif command == "build":
            #print(urls)
            #urls.append(crawler.run()) #nope = appends a list to a list
            urls = crawler.run() #dla sprawdzenia, przed zaczęciem inverted index
            #print(urls) #prints - stuff. Now trying to loop through this and make index
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

            #f = open("output2.txt", "w") #z tym działa! mamy inverted index file
            #output_line = "Word".ljust(15) + "Frequency".ljust(15) + "Posting List".ljust(15) + "\n"
            #f.writelines(output_line)
            #f.writelines('-------------------------------------------------------------------------\n\n')
            #for i in sorted_keys:
            #    print(i, len(index[i]), index[i])
            #    output_string = str(i).ljust(15) + str(len(index[i])).ljust(15) + str(index[i]).ljust(15) + "\n"
            #    f.writelines(output_string)
            #    f.writelines('\n')

            #f.close()


        elif command == "load":
            load()
            #crawler.print_visited()
            #print(urls) #prints only empty stuff, doesn't seem to be kept from CHOCIAŻ ostatni raze wydało się zadziałać
        #elif command == "print":
        #    print(phrase) #('phase')
        #elif command == "find":
        #    print(find(phrase))
        else:
            print("Command not found")



