from utils import shuffle_deck, evaluate_winner
from montecarlo import compute_raw_win_prob, pot_odds_call, maximal_raise
import numpy as np

class BotHardCoded():
    def __init__(self):
        # To be updated
        self.handrange = None
    
    @classmethod
    def call_bet_fold(self,bot_hand, community_cards, player_bet, opponent_bet, pot, history):
        # If they had put a large amount at the start, update hand range.
        
        raw_win_probability = compute_raw_win_prob(bot_hand, community_cards)
        pot_odds = pot_odds_call(player_bet, opponent_bet, pot)
        p = np.random.uniform(0,1)
        
        if raw_win_probability >= 0.85:
            # Consider checking even with high pot odds
            # Compute probability based on narrower hand_range
            # find number of ways they can one up you (TODO)
            if (p<0.5):
                return "check"
            else:
                return "raise"
            
        elif raw_win_probability > pot_odds:
            # Consider check/raising, folding with small prob
            # Raise if the pot odds were low
            # Check if the pot odds were high
            if (p<(raw_win_probability-pot_odds)):
                return "raise"
            elif(p<0.95):
                return "check"
            else:
                return "fold"
            # max_raise = maximal_raise(raw_win_probability, player_bet, opponent_bet, pot)
        else:
            #Randomly determine whether to check or fold
            if (p<pot_odds-raw_win_probability):
                return "fold"
            else:
                return "check"
            

        