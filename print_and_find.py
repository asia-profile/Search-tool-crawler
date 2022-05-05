import collections

#This command prints the inverted index for a particular word, for example:
#print Peso
#will print the inverted index for the word ‘Peso’
def print_index(phrase, dictionary):
    for word_key in dictionary.keys():
        if word_key == phrase:
            print("Index for " + phrase + ": ")
            print(dictionary[word_key])


#This command is used to find a certain query phrase in the inverted index and returns a list of all pages containing this phrase, for example:
#find Dinar
#will return a list of all pages containing the word ‘Dinar’, while
#find Area Afghanistan
#will return all pages containing the words ‘Area’ and ‘Afghanistan’.
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


    for i in range(len(list_indexed_tuples)):
        x = list_indexed_tuples[i][1].strip("[' ']")
        x_list.append(x)

    for j in range(len(x_list)):
        chunks = x_list[j].split(',')
        for ch in chunks:
            ch = ch.strip("[' ']")
            all_got_urls.append(ch)

    print("Urls with the words: ")
    print([item for item, count in collections.Counter(all_got_urls).items() if count > 1])
    #now that we have clear urls, we need to iterate over them and see if the url addresses repeat

