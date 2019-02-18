import time
from multiprocessing import Process, Value
from random import randint, shuffle

still_on = Value('i', 1)

def load_words():
    f = open('words.txt')
    indeces = {}
    ctr = 0
    words = []
    for i in range(200):
        indeces[randint(0, 83667)] = None
    for i in f:
        if ctr in indeces:
            words.append(i.rstrip('\n').lower())
        ctr += 1
    f.close()
    shuffle(words)
    return words

def update_status():
    global still_on
    time.sleep(60)
    still_on.value = 0
    print('\nTime up. Enter for results.\n')
    return

def get_user_words(words):
    global words_entered
    global still_on
    i = 0 
    while still_on.value and i < len(words):
        print(words[i] +': ', end = " ")
        words_entered.append(input())
        i += 1
    
def evaluate_words(words_entered, words):
    word_ctr = 0
    for i in range(len(words_entered)):
        if words[i].lower() == words_entered[i]:
            word_ctr += 1
    return 'Correct words per minute: '+str(word_ctr)

if __name__ == '__main__':
    words_entered = []
    words = load_words()
    timer = Process(target = update_status, args = ())
    timer.start()
    get_user_words(words)
    print(evaluate_words(words_entered, words))


