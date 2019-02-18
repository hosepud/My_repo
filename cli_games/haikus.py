def is_vowel(letter):
    return letter in "auioe"

def is_consonant(letter):
    return not is_vowel(letter)
    
def is_y_vowel(word, i):
    if word[i] != 'y':
        return False
    if i == 0:
        return False
    elif i == len(word)-1 and is_vowel(word[i-1]):
        return False
    elif i == len(word)-1:
        return True
    else:
        if is_consonant(word[i-1]):
            return True
        elif is_vowel(word[i-1]):
            return False

def ends_silent_e(word):
    exceptions = {'ante':None, 'she':None, 'recipe':None, 'canape': None, 'catastrophe':None, 'apostrophe':None, 'acne':None, 'forte':None, 'cliche':None, 'simile':None, 'rationale':None, 'hyperbole':None, 'the': None}
    if word[-1] != 'e':
        return False
    if word in exceptions:
        return False
    if len(word) < 3:
        return False
    elif len(word) >= 3 and is_consonant(word[-2]):
        return True
    elif len(word) >= 3 and is_vowel(word[-2]):
        return False

def has_ending(word, i):
    endings = ['ish', 'ishingly', 'ing']
    if word[i+1:i+4] in endings or word[i+1:1+7] in endings:
        return True
         
def diphtong_count(word):
    ctr = 0
    for i in range(1, len(word)):
        if is_vowel(word[i]) and is_vowel(word[i-1]):
            if not has_ending(word, i):
                ctr+=1
    return ctr

def le_les_ends(word):
    try:
        if word[-2:] == 'le' and is_consonant(word[-3]):
            return True
        elif word[-3:] == 'les' and is_consonant(word[-4]):
            return True
        else:
            return False
    except:
        return False

def ted_ded_ends(word, i):
    if word[i] != 'e':
        return True
    if len(word) <= 3:
        return True
    if word[i-1] == 'e':
        return True
    if i != len(word) - 2:
        return True
    if word[i+1] != 'd':
        return True
    if word[i-1:i+2] == 'ted' or word[i-1:i+2] == 'ded':
        return True
    return False

def is_e_silent(word, i):
    try:
        if word[i+1:i+3] == 'ly':
            return True
        if word[i+1:i+4] == 'ful':
            return True
        if word[i+1:i+5] == 'ness':
            return True
        if word[i+1:i+5] == 'some':
            return True
    except:
        return False

def syllables(word):
    #fails for words like limerick, finetune and many others
    if word == '':
        return 0
    syls = 0
    for i in range(len(word)):
        if word[i] == 'e':
            if is_e_silent(word, i):
                continue
            if ted_ded_ends(word, i):
                syls += 1
        elif is_vowel(word[i]):
            syls += 1
        elif is_y_vowel(word, i):
            syls += 1
    syls -= diphtong_count(word)
    if ends_silent_e(word):
        syls -= 1
    return syls


singular_exceptions = {'foot':'feet', 'child':'children', 'goose':'geese', 'mouse':'mice', 'tooth':'teeth', 'man':'men', 'woman':'women', 'wolf':'wolves', 'calf':'calves', 'half':'halves', 'headquarters':'headquarters','sheep':'sheep', 'species':'species', 'news':'news', 'advice':'advice', 'luggage':'luggage', 'information':'information', 'cattle':'cattle', 'scissors':'scissors', 'trousers':'trousers', 'tweezers':'tweezers', 'congratulations':'congratulations', 'pyjamas':'pyjamas', 'ox':'oxen', 'oblivion':'oblivion', 'joy':'joy', 'space':'space', 'loneliness':'loneliness', 'life': 'lives'}


def get_plural_noun(noun):   
        #mistakes for words of spanish origin ending in -o as well as exceptional words
    if noun in singular_exceptions:
        return singular_exceptions[noun]
    elif noun[-2:] == 'is':
        return noun[:-2] + 'es'
    elif noun[-1] in 'xos' or noun[-2:] in ['ch', 'sh','us']:
        return noun + 'es'
    elif noun[-1] == 'z':
        return noun + 'zes'
    elif noun[-1] == 'y':
        return noun[:-1] + 'ies'        
    else:
        return noun + 's'

def get_singular_verb(verb):
        #only third person plural
    if verb == ' ':
        return ''
    if verb == 'are':
        return 'is'
    elif verb[-2:] == 'is':
        return verb + 'es'
    elif verb[-1] in 'xos' or verb[-2:] in ['ch', 'sh', 'us']:
         return verb + 'es'
    elif verb[-1] == 'z':
         return verb + 'zes'
    elif verb[-1] == 'y' and is_consonant(verb[-2]):
         return verb[:-1] + 'ies'    
    else:
         return verb + 's'

nouns = ['rose', 'flower', 'death', 'end', 'oblivion', 'space', 'sky', 'eternity', 'eye', 'life', 'sea', 'island', 'joy', 'misery', 'loneliness', 'rosebud']
adjectives = ['immortal', 'mortal', 'painful', 'painless', 'red', 'blue', 'fateful', 'hateful', 'vanishing', 'pale', 'dark', 'deep', 'shallow', 'sad', 'low', 'tall', 'beautiful', 'old', 'ancient', 'young', 'youthful','dire', 'black', 'green', 'sunny', 'endless', 'horrible', 'wistful', 'timeless', 'ephemeral', 'purple']
adjectives += [' ']*(int(len(adjectives)/2))
verbs = ['are','die', 'live', 'speak', 'listen', 'build', 'destroy', 'rebel', 'obey', 'hate', 'love', 'suffer', 'enjoy', 'suffocate', 'breathe', 'care', 'abandon', 'dread', 'choke', 'build']
verbs += [' ']*len(verbs)

from random import randint
def make_line(n):
    definite = randint(0,1)
    plural = randint(0,1)
    adjective = adjectives[randint(0, len(adjectives)-1)]
    noun = nouns[randint(0, len(nouns)-1)]
    verb = verbs[randint(0, len(verbs)-1)]
    if plural:
        pn = get_plural_noun(noun)
        if pn == noun:
            verb = get_singular_verb(verb)
        else:
            noun = pn
    else:
        verb = get_singular_verb(verb)
        if is_vowel(adjective[0]) or (adjective == ' ' and is_vowel(noun[0])):
            article = 'an'
        else:
            article = 'a'
    if definite or plural:
        article = 'the'    
    coin = randint(0, 1)
    if coin:
        article = ' '
    if (syllables(article) + syllables(adjective) + syllables(noun) + syllables(verb)) == n:
        return [article, adjective, noun, verb]
    else:
        return make_line(n)

def capitalize_first_words(string):
    newstr = []
    for i in string:
        if i != ' ':
            for j in range(len(i)):
                if j == 0:
                    newstr.append(i[j].upper())
                else:
                    newstr.append(i[j])
            newstr.append(' ')
    return ''.join(newstr)

def make_haiku():
    haiku = map(lambda x: capitalize_first_words(x), [make_line(5), make_line(7), make_line(5)])
    for line in haiku:
        print(line)
    
make_haiku()

