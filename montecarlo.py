'''
File that has a lot of for loops :)
'''


from utils import DECK, evaluate_winner, shuffle_deck, evaluate_hand
import random
from copy import copy
import math

def compute_raw_win_prob(hand, community_cards, iter=100000):
    # 100000 (default) iterations of randomly sampled poker hands
    deck = set(DECK)
    print(deck)
    available_cards = list(deck - set(hand) - set(community_cards))
    win_count = 0
    for i in range(iter):
        assert len(available_cards) == len(deck) - len(hand) - len(community_cards)
        sim_cards = random.sample(available_cards, 5 - len(community_cards) + 2)
        sim_comm_cards = community_cards + sim_cards[:5 - len(community_cards)]
        player_hand = sim_cards[5 - len(community_cards):]  
        if evaluate_winner(player_hand, hand, sim_comm_cards) == "bot win":
            win_count += 1
    return win_count/iter

def find_one_up_rank(hand_rank, hand, community_cards):
    #TODO
    deck = set(copy(DECK))
    available_cards = list(deck - set(hand) - set(community_cards))
    pass
    

    

def pot_odds_call(player_bet, opponent_bet, pot):
    amount_to_call = opponent_bet - player_bet
    return (amount_to_call / (pot+opponent_bet+player_bet))

def pot_odds_raise(raise_amount, player_bet, opponent_bet, pot):
    return (raise_amount / (pot+opponent_bet+player_bet)) * 100
    
def maximal_raise(win_prob, player_bet, opponent_bet, pot):
    return math.floor(win_prob*(player_bet+opponent_bet+pot))
    
def count_outs(hand, community_cards, iter = 100000):
    '''
    Finds the ways you can improve the absolute rank of your hand (e.g. pair to three, or pair to straight) as a fraction
    '''
    curr_hand_rank = evaluate_hand(hand,community_cards)
    outs = 0
    deck = set(copy(DECK))
    available_cards = list(deck - set(hand) - set(community_cards))
    n = 5 - len(community_cards)
    for i in range(iter):
        sim_comm_cards = community_cards + random.sample(available_cards, n)
        hand_rank = evaluate_hand(bot_hand, sim_comm_cards)
        if hand_rank < curr_hand_rank:
            outs+=1
    return outs/iter    

if __name__ == "__main__":
    deck = shuffle_deck()
    bot_hand = [deck.pop(), deck.pop()]
    community_cards = [deck.pop() for i in range(3)]
    outs = count_outs(bot_hand, community_cards)
    print(bot_hand, community_cards, outs)