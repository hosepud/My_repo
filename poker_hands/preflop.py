from cards_eval import *
from random import randint

UTG_raise = [["A", "A"],["K","K"], ["A", "K", 1], ["Q", "Q"], ["A", "K", 0], ["J", "J"], ["A", "Q", 1], ["A", "Q", 0], ["A", "J", 1]]
UTG_call = []

early_raise = UTG_raise + [["T", "T"], ["A", "J", 0], ["K", "Q", 1]]
early_call = [["K", "Q", 0]]

middle_raise = early_raise + [["K", "Q", 0], ["K", "J", 1], ["Q", "J", 1]]
middle_call = [["A", "T", 1], ["A", "T", 0], ["K", "J", 0], ["Q", "J", 0], ["K", "T", 1], [9,9], [8,8]]

late_raise = middle_raise + [["A", "T", 1], ["K", "T", 1], ["K", "J", 0], ["Q", "J", 0], [9,9], [8,8]]
late_call = [[7,7], [6,6], [5,5], ["Q", "T", 1], ["Q", "T", 0], ["K", "T", 0], ["J", "T", 1], ["J", "T", 0], ["J", 9, 1]]

def fits_hand(hand, temp):
	if len(temp) == 2:
		return [hand[0][0], hand[1][0]] == temp
	else:
		s = int(hand[0][1] == hand[1][1])
		return [hand[0][0], hand[1][0], s] == temp

def test_pre_flop():
	pos_dict = {0:"UTG", 1:"early", 2:"middle", 3:"late"}
	action_dict = {0:"raise", 1:"call", 2:"fold"}
	pos = randint(0, 3)
	print pos_dict[pos]
	card_arrs = [[UTG_raise, UTG_call], [early_raise, early_call], [middle_raise, middle_call], [late_raise, late_call]]
	r = card_arrs[pos][0]
	c = card_arrs[pos][1]
	ctr = 0
	while ctr < 100:
		shuffle(deck)
		hand = deck[:2]
		print card_to_str(hand[0]),
		print card_to_str(hand[1])
		action = 2
		for i in r:
			if fits_hand(hand, i):
				action = 0
				break
		for i in c:
			if fits_hand(hand, i):
				action = 1
				break
		user_action = raw_input()
		print user_action, action_dict[action],
		if user_action == action_dict[action]:
			print "SUCCESS"
		else:
			print "FAIL"

		ctr += 1

test_pre_flop()
