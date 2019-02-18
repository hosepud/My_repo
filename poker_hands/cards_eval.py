from random import shuffle
from time import sleep, time

spades_str = u'\u2660'
hearts_str = u'\u2661'
diamonds_str = u'\u2662'
clubs_str = u'\u2663'

suits = spades,hearts,diamonds,clubs = [1,2,3,4]
card_names = [2,3,4,5,6,7,8,9,'T','J','Q','K','A']
card_names_dict = {0:-1}
for i in range(len(card_names)):
	card_names_dict[card_names[i]] = i

reverse_names = card_names[::-1]
deck = []
for s in suits:
	for n in card_names:
		deck.append((n,s))

def card_to_str(card):
	suits_str = {1:u'\u2660', 2:u'\u2661', 3:u'\u2662', 4:u'\u2663'}
	return "|%s%s|"%(card[0], suits_str[card[1]])

def hand_to_str(hand):
	return "("+card_to_str(hand[0])+", "+card_to_str(hand[1])+")"


def cmp(a, b):
    return (a > b) - (a < b)

def card_sort(cards):
	for i in range(1, len(cards)):
		for j in range(0, i):
			if card_cmp(cards[j], cards[i]) == -1:
				tmp = cards[i]
				cards[i] = cards[j]
				cards[j] = tmp
	return cards

def card_cmp(c1, c2):
	if isinstance(c1, int) or isinstance(c1, str):
		c1 = (c1, -1)
		c2 = (c2, -1)	
	return cmp(card_names_dict[c1[0]], card_names_dict[c2[0]])

def combs(lst):
	if not lst:
		return [[]]
	last = lst[-1]
	lst.pop()
	ret = combs(lst)
	ret.extend(map(lambda x: x+[last], ret[:]))
	return ret

def is_same_suit(cards):
	suit = cards[0][1]
	for i in range(1, len(cards)):
		if cards[i][1] != suit:
			return False
	return True

def is_flush(cards, suit_dict):
	suit = 0
	flush = []
	for i in suit_dict:
		if suit_dict[i] >= 5:
			suit = i
	for i in cards:
		if i[1] == suit:
			flush.append(i)
		if len(flush) == 5:
			break
	return flush

def is_same_kind(cards):
	kind = cards[0][0]
	for i in range(1, len(cards)):
		if cards[i][0] != kind:
			return False
	return True	

def is_four_of_kind(cards, card_dict):
	for i in card_dict:
		if card_dict[i] == 4:
			return i
	return []			

def dictified(cards):
	card_dict = {}
	for i in card_names:
		card_dict[i] = 0
	for i in cards:
		card_dict[i[0]] += 1
	return card_dict
	
def is_full_house(cards, card_dict):
	threes = 0
	pair = 0
	for i in card_dict:
		if card_dict[i] == 3 and card_cmp(i, threes) == 1:
			threes = i						
		if card_dict[i] == 2 and card_cmp(i, pair) == 1:
			pair = i
	if threes and pair:
		return [threes, pair]
	else:
		return []

def card_sublist(cards):
	for i in range(len(reverse_names)):
		if reverse_names[i] == cards[0][0]:
			if i+5<=len(reverse_names):
				return map(lambda x: x[0], cards) == reverse_names[i:i+5]
	return False

def is_smallest_straight(cards):
	c = map(lambda x: x[0], cards)
	for i in ["A", 2,3,4,5]:
		if not(i in c):
			return False
	return True

def is_straight(cards, c):
	straight = []
	smallest = []
	for comb in c:
		card_sort(comb)
		if card_sublist(comb):
			if straight == [] or card_cmp(straight[0], comb[0]) == -1:
				straight = comb
		elif is_smallest_straight(comb):
			smallest = comb[1:] + [comb[0]]
	if straight:
		return straight
	else:
		return smallest

def is_straight_flush(cards, c):
	straight_flushes = []
	smallest = []
	for comb in c:
		if is_same_suit(comb):
			card_sort(comb)
			if card_sublist(comb):
				straight_flushes.append(comb[:])
			elif is_smallest_straight(comb):
				smallest = comb[1:] + [comb[0]]
	if straight_flushes:
		return sorted(straight_flushes, lambda x,y: card_cmp(y[0], x[0]))[0]
	else:
		return smallest

def is_three_of_kind(cards, card_dict):
	threes = 0
	for i in card_dict:
		if card_dict[i] == 3 and card_cmp(i, threes) == 1:
			threes = i
	return threes

def is_two_pairs(cards, card_dict):
	pairs = []
	for i in card_dict:
		if card_dict[i] == 2:
			pairs.append(i)
	if len(pairs) <= 1:
		return []
	else:
		card_sort(pairs)
		return pairs[0:3]

def is_pair(cards, card_dict):
	p = 0
	for i in card_dict:
		if card_dict[i] == 2 and card_cmp(i, p) == 1:
			p = i
	return p	

def suit_dictified(cards):
	d = {spades:0, diamonds:0, clubs:0, hearts:0}
	for i in cards:
		d[i[1]] += 1
	for i in d:
		if d[i] >= 5:
			return d, True
	return d, False

def eval_cards(cards):
	five_combs = list(filter(lambda x:len(x)==5, combs(cards[:])))
	st_fl = is_straight_flush(cards[:], five_combs)
	card_sort(cards)
	card_dict = dictified(cards)
	suit_dict, flush = suit_dictified(cards)
	if flush:
		st_fl = is_straight_flush(cards, five_combs)
		if st_fl:
			return 0, st_fl
	fours = is_four_of_kind(cards, card_dict)
	if fours:
		return 1, fours
	full_house = is_full_house(cards, card_dict)
	if full_house:
		return 2, full_house
	if flush:
		fl = is_flush(cards, suit_dict)
		return 3,fl
	st = is_straight(cards, five_combs)
	if st:
		return 4,st
	three = is_three_of_kind(cards, card_dict)
	if three:
		return 5, three
	tp = is_two_pairs(cards, card_dict)
	if tp:
		return 6, tp
	p = is_pair(cards, card_dict)
	if p:
		return 7,p
	return 8, cards[0]
		
def print_res(code, res):
	if code == 8:
		print(card_to_str(res))
	elif code > 4 or code == 2:
		print(res)
	else:
		for i in res:
			print(card_to_str(i), end = " ")
		print('\n', end = " ")
	return
								
def test_func():
	ctr = 0
	flush_ctr = 0
	fours_ctr = 0
	full_house_ctr = 0
	straight_ctr = 0
	straight_flush_ctr = 0
	res = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0}
	codes = {0: "Straight Flush", 1: "Four of a kind", 2:"Full house", 3:"Flush", 4:"Straight", 5:"Three of a kind", 6:"Two pairs", 7: "A pair", 8:"High card"}
	while ctr < 1000:
		shuffle(deck)
		cards = deck[:7]
		ret, card_res = eval_cards(cards)
		res[ret]+=1
		for i in cards:
			print(card_to_str(i), end = " ")
		print('  %s '%(codes[ret]), end = " ") 
		print_res(ret,card_res)
		raw_input()
		ctr += 1
	print(float(res[0])/ctr, " : Straight flush %")
	print(float(res[1])/ctr, " : Fours %")	
	print(float(res[2])/ctr, " : Full house %")
	print(float(res[3])/ctr, " : Flush %")
	print(float(res[4])/ctr, " : Straights %")
	print(float(res[5])/ctr, " : Three of a kind %")
	print(float(res[6])/ctr, " : Two pairs %")
	print(float(res[7])/ctr, " : A pair %")
	print(float(res[8])/ctr, " : High card %")
	print(ctr)



