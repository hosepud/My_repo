from random import shuffle, randint
from ansi_colors import *
from time import sleep

class Card(object):
    def __init__(self, name, value, suit):
        self.name = name
        self.suit = suit
        self.value = value
        self.hidden = False 
        self.ace = False
    def hide(self):
        self.hidden = True

    def __repr__(self):
        if self.hidden:
            return 'Hole Card'
        else:
            return self.name + ' of ' + self.suit + ': ' + str(self.value)
    
class Deck(object):
    def __init__(self):
        self.cards = []
        for suit in ['diamonds', 'hearts', 'spades', 'clubs']:
            for name in range(2,11):
                self.cards.append(Card(str(name), name, suit))
            for j in ['J', 'K', 'Q']:
                self.cards.append(Card(j, 10, suit))
            ace = Card('A', 11, suit)
            ace.ace = True
            self.cards.append(ace)
        self.shuffle()
    def draw(self):
        return self.cards.pop()
    def shuffle(self):
        shuffle(self.cards)

def get_hand(deck, dealer):
    if dealer:
        hole_card = deck.draw()
        hole_card.hidden = True
        return [dealer, hole_card, deck.draw()]
    return [dealer, deck.draw(), deck.draw()]

def show_hand(hand):
    if hand[0]:
        print(colored('Dealer\'s hand', 'fg_blue'))
    else:
        print(colored('Player\'s hand', 'fg_red'))
    for i in hand:
        if isinstance(i, Card):
            print('\b',i)

def value_of(hand):  
    if not hand[0]:
        val = 0
        for i in hand:
            if isinstance(i, Card):
                if i.ace:
                    print('Player\'s', i),
                    val += int(input('Value 1 or 11? '))
                else:
                    val += i.value
        return (val, val)    
    else:
        val = 0
        val2 = 0
        for i in hand:
            if isinstance(i, Card):
                if i.ace:
                    val2 += 1
                else:
                    val2 += i.value
                val += i.value
        return (val,val2)
    
def player_turn(deck, hand):
    while True:
        action = input('Hit or Stand? ')
        if action.lower() == 'hit':
            hand.append(deck.draw())
            show_hand(hand)
            print('\n'),
        elif action.lower() == 'stand':
            return       

def dealer_turn(deck, hand):    
    while True:
        val1, val2 = value_of(hand)
        if val1 > 21:
            val = val2
        elif val1 < 21:
            val = val1
        else:
            val = val1
        if val < 17:
            action = 'hit'
        elif val >= 17:
            action = 'stand'
        if action == 'hit':
            hand.append(deck.draw())
            show_hand(hand)
            sleep(1)
        else:
            return

def outcome_hand(hand):
    p = ''
    val = None
    val1, val2 = value_of(hand)
    if val1 == 21 and len(hand) == 3:
        p = 'blackjack'
        val = 21
        return p, val
    if val1 > 21:
        val = val2
    else:
        val = val1
    if val > 21:
        p = 'bust'
    return p, val

def determine_outcome(p_hand, d_hand):
    p, p_val = outcome_hand(p_hand)
    d, d_val = outcome_hand(d_hand)
    print('Player\'s hand stats: ',p,p_val, '| Dealer\'s hand stats: ',d, d_val)
    if (p == d and p == 'blackjack') or (p == d and p == 'bust'):
        return 'push'
    elif d == 'bust':
        return 'player' 
    elif p == 'bust':
        return 'dealer'    
    elif p == 'blackjack':
        return 'blackjack'
    elif d == 'blackjack':
        return 'dealer'
    else:
        if p_val < d_val:
            return 'dealer'
        elif d_val < p_val:
            return 'player'
        else:
            return 'push'
    
def bj_round():
    deck = Deck()
    p_hand = get_hand(deck, False)
    d_hand = get_hand(deck, True)
    print(colored('Player\'s turn\n', 'fg_red'))
    show_hand(p_hand)
    show_hand(d_hand)
    player_turn(deck, p_hand)
    print('\n'),
    print(colored('Dealer\'s turn\n', 'fg_blue'))
    print(colored('Flipping hole card.', 'fg_blue'))
    d_hand[1].hidden = False
    show_hand(p_hand)
    show_hand(d_hand)
    dealer_turn(deck, d_hand)
    print('\n'),
    print(colored('Showing final hands\n' , 'fg_green'))
    show_hand(p_hand)
    show_hand(d_hand)
    
    return determine_outcome(p_hand,d_hand)

def game():
    player_money = int(input('Start money? '))
    dealer_money = player_money
    while True:
        a = 'Player money: %d | Dealer money %d' % (player_money,dealer_money)
        print(colored(a, 'fg_green'))
        print(colored('Round commencing', 'fg_green'))
        bet = int(input('Bet? '))
        dealer_bet = bet
        outcome = bj_round()
        sleep(1)
        if outcome == 'blackjack':
            print(colored('Blackjack!', 'fg_red'))
            player_money += (1.5*bet + bet)
            dealer_money -= (1.5*bet + bet)
        elif outcome == 'player':
            print(colored('Player wins', 'fg_red'))
            player_money += bet
            dealer_money -= bet
        elif outcome == 'dealer':
            print(colored('Dealer wins', 'fg_blue'))
            player_money -= bet
            dealer_money += bet
        elif outcome == 'push':
            print('Push')
       
if __name__ == '__main__':
    game()
