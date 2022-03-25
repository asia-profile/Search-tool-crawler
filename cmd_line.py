
while True:
    command_line = input('Enter command to run: ')
    words = command_line.split() #take all the input here divided into specific words
    command = words[0]
    words.pop(0) #removed the first word from the list, now we can again get the whole phrase for print/find commands
    phrase = ''
    #phrase = phrase.join(words) #okay, no, beacuse it gives it like a joined word

    if command == 'quit':
        print('Exiting the program')
        break
    else:
        if command == 'build':
            print('phrase')
        elif command == 'load':
            print('phrase')
        elif command == 'print':
            print('phrase')
        elif command == 'find':
            print(phrase)