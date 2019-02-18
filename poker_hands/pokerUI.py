from sys import argv
from stats import *

def inp_card(c):
	c = c[1:-1]
	n = c[0]
	color = c[2:]
	colordict = {'spades':spades, 'hearts':hearts, 'diamonds':diamonds, 'clubs': clubs}
	if n in '23456789':
		n = int(n)
	return (n, colordict[color])

def eval_input(card_str):
	if card_str == "()":
		return []
	card_str = card_str.split(',')
	ret = []
	for c in card_str:
		ret.append(inp_card(c))
	return ret
				
def main():
	#inp = (K:spades),(A:hearts)
	print("Input required looks like:\n(K:spades),(A:hearts)")
	print("Spacing should be as illustrated above\n")
	h_str = input("Your hand> ")
	h = eval_input(h_str)
	b_str = input("The board> ")
	board = eval_input(b_str)
	cards = h+board
	deck = list(filter(lambda x: not(x in cards), get_deck()))
	ppr, npr, tpr = post_draw_strengths(h, board, deck)
	print("Probability of being stronger right now", ppr)
	print("Probability of being weaker right now", npr)
	print("Probability of a tie", tpr)
	print("\n", end = " ")
	ppot, npot, tpot = post_draw_potentials(h, board, deck)
	print("Probability of being stronger after ONE draw", ppot)
	print("Probability of being weaker after ONE draw", npot)
	print("Probability of a tie after ONE draw", tpot)
	print("\n", end = " ")

if __name__ == '__main__':
	main()

