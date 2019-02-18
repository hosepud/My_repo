from cards_eval import *

def flush_cmp(fl1, fl2):
	for i in range(5):
		ret = card_cmp(fl1[i], fl2[i])
		if ret:
			return ret
	return 0

def max_card(cards):
	card_sort(cards)
	return cards[0]

def get_kicker_list(cards, ignore):
	card_sort(cards)
	kickers = []
	for i in cards:
		if not (i[0] in ignore):
			kickers.append(i)
	card_sort(kickers)
	return kickers
		
def threes_cmp(h1,h2,card_res1,card_res2, board):
	t_cmp = card_cmp(card_res1, card_res2)
	if not t_cmp:
		cards1 = h1 + board
		card_sort(cards1)
		cards2 = h2 + board
		card_sort(cards2)
		kickers1 = list(filter(lambda x: x[0] != card_res1, cards1))[0:2]
		kickers2 = list(filter(lambda x: x[0] != card_res2, cards2))[0:2]
		for i in range(len(kickers1)):
			k_cmp = card_cmp(kickers1[i], kickers2[i])
			if k_cmp:
				return k_cmp
	return t_cmp

def straight_flush_cmp(card_res1,card_res2):
	return card_cmp(card_res1[0], card_res2[0])

def quads_cmp(h1, h2, card_res1, card_res2, board):
	fours_cmp = card_cmp(card_res1, card_res2)
	if not fours_cmp:		
		kickers1 = get_kicker_list(h1+board, [card_res1])
		kickers2 = get_kicker_list(h2+board, [card_res2])
		return card_cmp(kickers1[0], kickers2[0])
	else:
		return fours_cmp

def two_pair_cmp(h1, h2, card_res1, card_res2, board):
	first_p = card_cmp(card_res1[0], card_res2[0])
	if first_p:
		return first_p
	else:
		second_p = card_cmp(card_res1[1], card_res2[1])
		if second_p:
			return second_p
		else:
			if len(board) == 4 and (len(card_res1) == 3 or len(card_res2)):
				return 0
			kicker1 = get_kicker_list(h1+board, card_res1)[0]
			kicker2 = get_kicker_list(h2+board, card_res2)[0]
			return card_cmp(kicker1,kicker2)	

def pair_cmp(h1, h2, card_res1, card_res2, board):
	p_cmp = card_cmp(card_res1, card_res2)
	if p_cmp:
		return p_cmp
	cards1 = h1 + board
	card_sort(cards1)
	cards2 = h2 + board
	card_sort(cards2)
	kickers1 = list(filter(lambda x: x[0] != card_res1, cards1))[0:3]
	kickers2 = list(filter(lambda x: x[0] != card_res2, cards2))[0:3]
	for i in range(len(kickers1)):
		k_cmp = card_cmp(kickers1[i], kickers2[i])
		if k_cmp:
			return k_cmp
	return 0

def high_card_cmp(h1, h2, board):
	cards1 = h1+board
	cards2 = h2+board
	card_sort(cards1); card_sort(cards2)
	for i in range(len(cards1)):
		if i == 5:
			break
		c_cmp = card_cmp(cards1[i], cards2[i])
		if c_cmp:
			return c_cmp
	return 0
		
def tiebreak(h1, h2, card_res1, card_res2, code, board):
	if code == 0:
		return straight_flush_cmp(card_res1, card_res2)
	elif code == 1:
		return quads_cmp(h1,h2,card_res1,card_res2, board)		
	elif code == 2:
		threes = card_cmp(card_res1[0], card_res2[0])
		if not threes:
			twos = card_cmp(card_res1[1], card_res2[1])
			return twos
		else:
			return threes
	elif code == 3:
		return flush_cmp(card_res1, card_res2)
	elif code == 4:
		return card_cmp(card_res1[0], card_res2[0])
	elif code == 5:
		return threes_cmp(h1,h2,card_res1, card_res2, board)
	elif code == 6:
		return two_pair_cmp(h1,h2, card_res1, card_res2, board)
	elif code == 7:
		return pair_cmp(h1, h2, card_res1, card_res2, board)
	elif code == 8:
		return high_card_cmp(h1,h2,board)
	

def hand_cmp(h1, h2, board):
	code1, card_res1 = eval_cards(h1+board)
	code2, card_res2 = eval_cards(h2+board)
	if code1 < code2:
		return 1
	elif code1 > code2:
		return -1
	else:
		return tiebreak(h1, h2, card_res1, card_res2, code1, board)


def print_card_lst(cards):
	for i in range(len(cards)):
		print(card_to_str(cards[i]), end = " ")
	print('\n')
	
		
def get_deck():
	deck = []
	for s in suits:
		for n in card_names:
			deck.append((n,s))
	shuffle(deck)
	return deck

def get_hands(n, deck):
	hands = []
	for i in range(n):
		hands.append([deck.pop(), deck.pop()])
	return hands

def mock_poker(n, deck):
	hands = get_hands(n, deck)
	flop = [deck.pop(), deck.pop(), deck.pop()]
	turn = [deck.pop()]
	river = [deck.pop()]


