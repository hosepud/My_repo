from hand_cmp import *
from cards_eval import *

def post_flop_strength(h, board, deck):
	win = 1
	tie = 0
	loss = -1
	
	w_arr = []
	l_arr = []
	t_arr = []
	for c1 in deck:
		for c2 in deck:
			res = hand_cmp(h, [c1,c2], board)
			if res == win:
				w_arr.append([c1,c2])
			elif res == loss:
				l_arr.append([c1,c2])
			else:
				t_arr.append([c1,c2])
	return (w_arr, l_arr, t_arr), float(len(w_arr))/(len(l_arr) + len(t_arr)+ len(w_arr))

def post_flop_turn_potential(h, board, res_arr, deck):
	w_arr = res_arr[0]
	l_arr = res_arr[1]
	t_arr = res_arr[2]

	win_to_loss = 0.0	
	loss_to_win = 0.0
	
	for h2 in w_arr:
		for c in deck:
			if c in h2:
				continue
			new_b = board+[c]
			res = hand_cmp(h[:], h2[:], new_b[:])
			if res != 1:
				win_to_loss += 1
	for h2 in l_arr:
		for c in deck:
			if c in h2:
				continue
			new_b = board+[c]
			res = hand_cmp(h[:], h2[:], new_b[:])
			if res != -1:
				loss_to_win += 1

	for h2 in t_arr:
		for c in deck:
			if c in h2:
				continue
			new_b = board+[c]
			res = hand_cmp(h[:], h2[:], new_b[:])
			if res == 1:
				loss_to_win += 1
			if res == -1:
				win_to_loss += 1

	if len(l_arr) == 0:
		return 1.0, 0.0, 1.0, 0.0
	if len(w_arr) == 0:
		return 0.0, 1.0, 0.0, 1.0

	pre_wins = float(len(w_arr))*(len(deck)-2)
	pre_losses = float(len(l_arr))*(len(deck)-2)
	pr_s6_given_s5 = (pre_wins - win_to_loss)/pre_wins
	p_s5 = pre_wins/(pre_wins + pre_losses + len(t_arr)*(len(deck)-2))
	pr_s6_given_ns5 = (loss_to_win)/pre_losses	
	p_ns5 = 1 - p_s5
	ppot = pr_s6_given_s5*p_s5 + pr_s6_given_ns5*p_ns5
	
	pr_ns6_given_s5 = win_to_loss/pre_wins
	pr_ns6_given_ns5 = (pre_losses - loss_to_win)/pre_losses
	npot = pr_ns6_given_s5*p_s5 + pr_ns6_given_ns5*p_ns5
	return ppot, npot, p_s5, p_ns5

def post_draw_strengths(h, board, deck):
	pos = 0
	neg = 0
	tie = 0
	total = 0.0
	for i in range(len(deck)):
		for j in range(i+1, len(deck)):
			h2 = [deck[i],deck[j]]
			res = hand_cmp(h,h2,board)
			if res == 1:
				pos += 1
			if res == -1:
				neg += 1
			if res == 0:
				tie += 1
			total += 1
	return [pos/total, neg/total, tie/total]

			
def post_draw_potentials(h, board, deck):
	probsS = {}
	probsNs = {}
	probsT = {}
	priori_ps = post_draw_strengths(h, board, deck)
	for i in range(len(deck)):
		newb = board[:]
		draw = deck[i]
		newdeck = list(filter(lambda x: not(x == draw), deck))	
		newb+=[draw]
		probsS[draw], probsNs[draw], probsT[draw] = post_draw_strengths(h, newb, newdeck)
	posteriori_ps = [0, 0, 0]
	for i in range(len(deck)):
		posteriori_ps[0] += probsS[deck[i]]
		posteriori_ps[1] += probsNs[deck[i]]
		posteriori_ps[2] += probsT[deck[i]]
	posteriori_ps = list(map(lambda x: x/len(deck), posteriori_ps))
	ppot = 0
	for i in range(3):
		ppot += priori_ps[i]*posteriori_ps[0]
	npot = 0
	for i in range(3):
		npot += priori_ps[i]*posteriori_ps[1]
	tpot = 0
	for i in range(3):
		tpot += priori_ps[i]*posteriori_ps[2]
	return [ppot, npot, tpot]



