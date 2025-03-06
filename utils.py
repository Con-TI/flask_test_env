import random
SUITS = ("♠", "♥", "♦", "♣")
RANKS = ("2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A")
DECK = tuple([rank + suit for rank in RANKS for suit in SUITS])
HAND_RANKS = {"royal flush":1, "straight flush":2, "four of a kind":3,"full house":4,"flush":5, "straight":6, "three of a kind":7, "two pair": 8, "pair": 9, "high card": 10}


def shuffle_deck():
    deck = [rank + suit for rank in RANKS for suit in SUITS]
    random.shuffle(deck)
    return deck

def flush(hand,community_cards):
    all_cards = hand + community_cards
    all_suits = [card[1] for card in all_cards]
    for suit in SUITS:
        num_suits = all_suits.count(suit)
        if num_suits>=5:
            same_suited = [card[0] for card in all_cards if card[1] == suit]
            if RANKS[-5:] in same_suited:
                return True, "royal flush", None
            for i in range(len(RANKS)-5,-1,-1):
                if RANKS[i:i+5] in same_suited:
                    return True, "straight flush", i
            return True, "flush", same_suited
    return False, None, None

def four_kind(hand, community_cards):
    all_cards = hand + community_cards
    for rank in RANKS[::-1]:
        if all_cards.count(rank) == 4:
            return True, "four of a kind", rank
    return False, None, None

def full_house(hand, community_cards):
    all_cards = hand + community_cards
    all_cards = [card[0] for card in all_cards]
    for rank_i in RANKS[::-1]:
        if all_cards.count(rank_i) == 3:
            for rank_j in RANKS[::-1]:
                if rank_j != rank_i:
                    if all_cards.count(rank_j) == 2:
                        return True, "full_house", [rank_i,rank_j]
    return False, None, None

def straight(hand, community_cards):
    all_cards = hand + community_cards
    card_ranks = [card[0] for card in all_cards]
    for i in range(len(RANKS)-5,-1,-1):
        if RANKS[i:i+5] in card_ranks:
            return True, "straight", i
    return False, None, None

def three_kind(hand, community_cards):
    all_cards = hand + community_cards
    card_ranks = [card[0] for card in all_cards]
    for rank in RANKS[::-1]:
        if card_ranks.count(rank) == 3:
            return True, "three of a kind", rank
    return False, None, None

def pair(hand, community_cards):
    all_cards = hand + community_cards
    card_ranks = [card[0] for card in all_cards]
    for rank_i in RANKS[::-1]:
        if card_ranks.count(rank_i) == 2:
            for rank_j in RANKS[::-1]:
                if rank_j != rank_i:
                    if card_ranks.count(rank_j) == 2:
                        return True, "two pair", [rank_i,rank_j]
            return True, "pair", rank_i
    return False, None, None

def high_card(hand, community_cards):
    all_cards = hand + community_cards
    card_ranks = [card[0] for card in all_cards]
    for rank_i in RANKS[::-1]:
        if rank_i in card_ranks:
            return True, "high card", rank_i
    
def evaluate_hand(hand, community_cards):
    # Check for flush
    truth, hand_rank, flush_rank = flush(hand, community_cards)
    if truth:
        if hand_rank == "royal flush":
            return HAND_RANKS[hand_rank], None
        elif hand_rank == "straight flush":
            return HAND_RANKS[hand_rank], flush_rank
        else:
            # Check for fours and full houses
            truth2, hand_rank_i, four_rank = four_kind(hand, community_cards)
            if truth2:
                return HAND_RANKS[hand_rank_i], four_rank
            truth2, hand_rank_i, full_rank = full_house(hand, community_cards)
            if truth2:
                return HAND_RANKS[hand_rank_i], full_rank
            else:
                return HAND_RANKS[hand_rank], flush_rank
    else:
        # Check for straight, threes, pairs, highs
        truth, hand_rank, straight_rank = straight(hand, community_cards)
        if truth:
            return HAND_RANKS[hand_rank], straight_rank
        truth, hand_rank, three_rank = three_kind(hand, community_cards)
        if truth:
            return HAND_RANKS[hand_rank], three_rank
        truth, hand_rank, pair_rank = pair(hand, community_cards)
        if truth:
            return HAND_RANKS[hand_rank], pair_rank
        truth, hand_rank, high_rank = high_card(hand, community_cards)
        return HAND_RANKS[hand_rank], high_rank

def compare_same_ranks(hand_rank, rank1, rank2):
    if hand_rank == 2:
        if rank1 > rank2:
            return 1
        elif rank1 < rank2:
            return -1
        else:
            return 0
    elif hand_rank == 3:
        if RANKS.index(rank1) > RANKS.index(rank2):
            return 1
        elif RANKS.index(rank1) < RANKS.index(rank2):
            return -1
        else:
            return 0 
    elif hand_rank == 4:
        if RANKS.index(rank1[0]) > RANKS.index(rank2[0]):
            return 1
        elif RANKS.index(rank1[0]) < RANKS.index(rank2[0]):
            return -1
        else:
            if RANKS.index(rank1[1]) > RANKS.index(rank2[1]):
                return 1
            elif RANKS.index(rank1[1]) < RANKS.index(rank2[1]):
                return -1
            else:
                return 0
    elif hand_rank == 5:
        highest1 = [RANKS.index(r) for r in rank1]
        highest2 = [RANKS.index(r) for r in rank2]
        highest1 = sorted(highest1)
        highest2 = sorted(highest2)
        highest1 = highest1[-5:]
        highest2 = highest2[-5:]
        while highest1:
            if highest1[-1] > highest2[-1]:
                return 1
            elif highest1[-1] < highest2[-1]:
                return -1
            highest1.pop()
            highest2.pop()
        return 0
    elif hand_rank == 6:
        if rank1 > rank2:
            return 1
        elif rank1 < rank2:
            return -1
        else:
            return 0 
    elif hand_rank == 7:
        if RANKS.index(rank1) > RANKS.index(rank2):
            return 1
        elif RANKS.index(rank1) < RANKS.index(rank2):
            return -1
        else:
            return 0 
    elif hand_rank == 8:
        if RANKS.index(rank1[0]) > RANKS.index(rank2[0]):
            return 1
        elif RANKS.index(rank1[0]) < RANKS.index(rank2[0]):
            return -1
        else:
            if RANKS.index(rank1[1]) > RANKS.index(rank2[1]):
                return 1
            elif RANKS.index(rank1[1]) < RANKS.index(rank2[1]):
                return -1
            else:
                return 0
    elif hand_rank == 9:
        if RANKS.index(rank1) > RANKS.index(rank2):
            return 1
        elif RANKS.index(rank1) < RANKS.index(rank2):
            return -1
        else:
            return 0 
    elif hand_rank == 10:
        if RANKS.index(rank1) > RANKS.index(rank2):
            return 1
        elif RANKS.index(rank1) < RANKS.index(rank2):
            return -1
        else:
            return 0 
        
def remove_cards(hand_rank, player_view, bot_view, player_rank, bot_rank):
    if hand_rank==2:
        player_suits = [card[1] for card in player_view]
        for suit in SUITS:
            if player_suits.count(suit)>=5:
                player_suit = suit
                break
        player_view = set(player_view)
        player_sf = set([RANKS[i] + player_suit for i in range(player_rank,player_rank+5)])
        player_view = player_view - player_sf
        
        bot_suits = [card[1] for card in bot_view]
        for suit in SUITS:
            if bot_suits.count(suit)>=5:
                bot_suit = suit
                break
        bot_view = set(bot_view)
        bot_sf = set([RANKS[i] + bot_suit for i in range(bot_rank,bot_rank+5)])
        bot_view = bot_view - bot_sf
    elif hand_rank == 3:
        player_view = set(player_view)
        player_four = set([player_rank + suit for suit in SUITS])
        player_view = player_view - player_four
        bot_view = set(bot_view)
        bot_four = set([bot_rank + suit for suit in SUITS])
        bot_view = bot_view - bot_four
    elif hand_rank == 4:
        player_view = set(player_view)
        player_view = player_view - set([player_rank[0]+suit for suit in SUITS])
        n = len(player_view)
        for suit in SUITS:
            if len(player_view) == n-2:
                break
            player_view = player_view - set([player_rank[1]+suit])
        bot_view = set(bot_view)
        bot_view = bot_view - set([bot_rank[0]+suit for suit in SUITS])
        n = len(bot_view)
        for suit in SUITS:
            if len(bot_view) == n-2:
                break
            bot_view = bot_view - set([bot_rank[1] + suit])
    elif hand_rank == 5:
        highest1 = [RANKS.index(r) for r in player_rank]
        highest2 = [RANKS.index(r) for r in bot_rank]
        highest1 = sorted(highest1)
        highest2 = sorted(highest2)
        highest1 = set(highest1[-5:])
        highest2 = set(highest2[-5:])
        player_view = set(player_view) - highest1
        bot_view = set(bot_view) - highest2
    elif hand_rank == 6:
        player_view = set(player_view)
        player_st = RANKS[player_rank:player_rank+5]
        for rank in player_st:
            n = len(player_view)
            for suit in SUITS:
                player_view = player_view - set([rank+suit])
                if len(player_view) == n-1:
                    break
        bot_view = set(bot_view)
        bot_st = RANKS[bot_rank:bot_rank+5]
        for rank in bot_st:
            n = len(bot_view)
            for suit in SUITS:
                bot_view = bot_view - set([rank+suit])
                if len(bot_view) == n-1:
                    break
    elif hand_rank == 7:
        player_view = set(player_view) - set([player_rank +suit for suit in SUITS])
        bot_view = set(bot_view) - set([bot_rank + suit for suit in SUITS])
    elif hand_rank == 8:
        player_view = set(player_view) - set([rank + suit for rank in player_rank for suit in SUITS])
        bot_view = set(bot_view) - set([rank + suit for rank in bot_rank for suit in SUITS])
    elif hand_rank == 9:
        player_view = set(player_view) - set([player_rank + suit for suit in SUITS])
        bot_view = set(bot_view) - set([bot_rank + suit for suit in SUITS])
    elif hand_rank == 10:
        player_view = set(player_view) - set([player_rank + suit for suit in SUITS])
        bot_view = set(bot_view) - set([bot_rank + suit for suit in SUITS])
    return list(player_view), list(bot_view)  
      
def compare_left_over(hand_rank, player_view, bot_view, player_rank, bot_rank):
    player_view, bot_view = remove_cards(hand_rank, player_view, bot_view, player_rank, bot_rank)
    comm_cards = set(player_view).intersection(set(bot_view))
    player_view = set(player_view) - comm_cards
    bot_view = set(bot_view) - comm_cards
    if len(comm_cards) == 0 or (hand_rank in [1,2,4,5,6]):
        return "tie"
    elif hand_rank in [3,8]:
        # eval the high card
        comm_cards_ranks = [RANKS.index(card[0]) for card in comm_cards]
        player_view_ranks = [RANKS.index(card[0]) for card in player_view]
        bot_view_ranks = [RANKS.index(card[0]) for card in bot_view]
        highest_ranked = max(comm_cards_ranks+player_view_ranks+bot_view_ranks)
        if (highest_ranked in bot_view_ranks) and (highest_ranked not in player_view_ranks) and (highest_ranked not in comm_cards_ranks):
            return "bot win"
        elif (highest_ranked in player_view_ranks) and (highest_ranked not in bot_view_ranks) and (highest_ranked not in comm_cards_ranks):
            return "player win"
        else:
            return "tie"
    elif hand_rank == 7:
        comm_cards_ranks = [RANKS.index(card[0]) for card in comm_cards]
        player_view_ranks = [RANKS.index(card[0]) for card in player_view]
        bot_view_ranks = [RANKS.index(card[0]) for card in bot_view]
        highest_ranked = max(comm_cards_ranks+player_view_ranks+bot_view_ranks)
        if (highest_ranked in bot_view_ranks) and (highest_ranked not in player_view_ranks) and (highest_ranked not in comm_cards_ranks):
            return "bot win"
        elif (highest_ranked in player_view_ranks) and (highest_ranked not in bot_view_ranks) and (highest_ranked not in comm_cards_ranks):
            return "player win"
        else:
            # Can safely do this since either highest_ranked in both hands but not in comm_cards, or highest_ranked in comm_cards
            if highest_ranked in player_view_ranks:
                player_view_ranks.remove(highest_ranked)
            if highest_ranked in bot_view_ranks:
                bot_view_ranks.remove(highest_ranked)
            if highest_ranked in comm_cards_ranks:
                comm_cards_ranks.remove(highest_ranked)
            highest_ranked = max(comm_cards_ranks+player_view_ranks+bot_view_ranks)
            if (highest_ranked in bot_view_ranks) and (highest_ranked not in player_view_ranks) and (highest_ranked not in comm_cards_ranks):
                return "bot win"
            elif (highest_ranked in player_view_ranks) and (highest_ranked not in bot_view_ranks) and (highest_ranked not in comm_cards_ranks):
                return "player win"
            else:
                return "tie"            
    elif hand_rank == 9:
        comm_cards_ranks = [RANKS.index(card[0]) for card in comm_cards]
        player_view_ranks = [RANKS.index(card[0]) for card in player_view]
        bot_view_ranks = [RANKS.index(card[0]) for card in bot_view]
        highest_ranked = max(comm_cards_ranks+player_view_ranks+bot_view_ranks)
        if (highest_ranked in bot_view_ranks) and (highest_ranked not in player_view_ranks) and (highest_ranked not in comm_cards_ranks):
            return "bot win"
        elif (highest_ranked in player_view_ranks) and (highest_ranked not in bot_view_ranks) and (highest_ranked not in comm_cards_ranks):
            return "player win"
        else:
            if highest_ranked in player_view_ranks:
                player_view_ranks.remove(highest_ranked)
            if highest_ranked in bot_view_ranks:
                bot_view_ranks.remove(highest_ranked)
            if highest_ranked in comm_cards_ranks:
                comm_cards_ranks.remove(highest_ranked)
            highest_ranked = max(comm_cards_ranks+player_view_ranks+bot_view_ranks)
            if (highest_ranked in bot_view_ranks) and (highest_ranked not in player_view_ranks) and (highest_ranked not in comm_cards_ranks):
                return "bot win"
            elif (highest_ranked in player_view_ranks) and (highest_ranked not in bot_view_ranks) and (highest_ranked not in comm_cards_ranks):
                return "player win"
            else:
                if highest_ranked in player_view_ranks:
                    player_view_ranks.remove(highest_ranked)
                if highest_ranked in bot_view_ranks:
                    bot_view_ranks.remove(highest_ranked)
                if highest_ranked in comm_cards_ranks:
                    comm_cards_ranks.remove(highest_ranked)
                highest_ranked = max(comm_cards_ranks+player_view_ranks+bot_view_ranks)
                if (highest_ranked in bot_view_ranks) and (highest_ranked not in player_view_ranks) and (highest_ranked not in comm_cards_ranks):
                    return "bot win"
                elif (highest_ranked in player_view_ranks) and (highest_ranked not in bot_view_ranks) and (highest_ranked not in comm_cards_ranks):
                    return "player win"
                else:
                    return "tie" 
    elif hand_rank == 10:
        comm_cards_ranks = [RANKS.index(card[0]) for card in comm_cards]
        player_view_ranks = [RANKS.index(card[0]) for card in player_view]
        bot_view_ranks = [RANKS.index(card[0]) for card in bot_view]
        highest_ranked = max(comm_cards_ranks+player_view_ranks+bot_view_ranks)
        if (highest_ranked in bot_view_ranks) and (highest_ranked not in player_view_ranks) and (highest_ranked not in comm_cards_ranks):
            return "bot win"
        elif (highest_ranked in player_view_ranks) and (highest_ranked not in bot_view_ranks) and (highest_ranked not in comm_cards_ranks):
            return "player win"
        else:
            if highest_ranked in player_view_ranks:
                player_view_ranks.remove(highest_ranked)
            if highest_ranked in bot_view_ranks:
                bot_view_ranks.remove(highest_ranked)
            if highest_ranked in comm_cards_ranks:
                comm_cards_ranks.remove(highest_ranked)
            highest_ranked = max(comm_cards_ranks+player_view_ranks+bot_view_ranks)
            if (highest_ranked in bot_view_ranks) and (highest_ranked not in player_view_ranks) and (highest_ranked not in comm_cards_ranks):
                return "bot win"
            elif (highest_ranked in player_view_ranks) and (highest_ranked not in bot_view_ranks) and (highest_ranked not in comm_cards_ranks):
                return "player win"
            else:
                if highest_ranked in player_view_ranks:
                    player_view_ranks.remove(highest_ranked)
                if highest_ranked in bot_view_ranks:
                    bot_view_ranks.remove(highest_ranked)
                if highest_ranked in comm_cards_ranks:
                    comm_cards_ranks.remove(highest_ranked)
                highest_ranked = max(comm_cards_ranks+player_view_ranks+bot_view_ranks)
                if (highest_ranked in bot_view_ranks) and (highest_ranked not in player_view_ranks) and (highest_ranked not in comm_cards_ranks):
                    return "bot win"
                elif (highest_ranked in player_view_ranks) and (highest_ranked not in bot_view_ranks) and (highest_ranked not in comm_cards_ranks):
                    return "player win"
                else:
                    if highest_ranked in player_view_ranks:
                        player_view_ranks.remove(highest_ranked)
                    if highest_ranked in bot_view_ranks:
                        bot_view_ranks.remove(highest_ranked)
                    if highest_ranked in comm_cards_ranks:
                        comm_cards_ranks.remove(highest_ranked)
                    highest_ranked = max(comm_cards_ranks+player_view_ranks+bot_view_ranks)
                    if (highest_ranked in bot_view_ranks) and (highest_ranked not in player_view_ranks) and (highest_ranked not in comm_cards_ranks):
                        return "bot win"
                    elif (highest_ranked in player_view_ranks) and (highest_ranked not in bot_view_ranks) and (highest_ranked not in comm_cards_ranks):
                        return "player win"
                    else:
                        return "tie" 

def compare_with_comm_card_best(hand_rank, player_hand, bot_hand, community_cards, player_hand_rank,bot_hand_rank,comm_cards_rank):
    player_vs_comm = compare_same_ranks(hand_rank, player_hand_rank, comm_cards_rank)
    if player_vs_comm == 0:
        player_view, comm_view = remove_cards(hand_rank, player_hand + community_cards, community_cards, player_hand_rank, comm_cards_rank)
        if len(comm_view) == 0:
            # player and comm would tie
            player_vs_comm = 0
        elif 1 <= len(comm_view) <= 4:
            # See if player_view beats comm_view in high rank
            while True:
                player_ranks = max([RANKS.index(card[0]) for card in player_view])
                comm_ranks = max([RANKS.index(card[0]) for card in comm_view])
                if comm_ranks > player_ranks:
                    player_vs_comm = -1
                    break
                elif comm_ranks == player_ranks:
                    player_view, comm_view = remove_cards(10, player_view, comm_view, RANKS[player_ranks], RANKS[comm_ranks])
                    # player and comm would tie
                    if len(comm_view) == 0:
                        player_vs_comm = 0
                        break
                else:
                    player_vs_comm = 1
                    break
    
    bot_vs_comm = compare_same_ranks(hand_rank, bot_hand_rank, comm_cards_rank)
    if bot_vs_comm == 0:
        bot_view, comm_view = remove_cards(hand_rank, bot_hand + community_cards, community_cards, bot_hand_rank, comm_cards_rank)
        if len(comm_view) == 0:
            # bot and comm would tie
            bot_vs_comm = 0
        elif 1 <= len(comm_view) <= 4:
            # See if bot_view beats comm_view in high rank
            while True:
                bot_ranks = max([RANKS.index(card[0]) for card in bot_view])
                comm_ranks = max([RANKS.index(card[0]) for card in comm_view])
                if comm_ranks > bot_ranks:
                    bot_vs_comm = -1
                    break
                elif comm_ranks == bot_ranks:
                    bot_view, comm_view = remove_cards(10, bot_view, comm_view, RANKS[bot_ranks], RANKS[comm_ranks])
                    # bot and comm would tie
                    if len(comm_view) == 0:
                        bot_vs_comm = 0
                        break
                else:
                    bot_vs_comm = 1
                    break
    
    if player_vs_comm > bot_vs_comm:
        return "player win"
    elif player_vs_comm < bot_vs_comm:
        return "bot win"
    else:
        if (player_vs_comm == -1) or (player_vs_comm == 0):
            return "tie"
        elif player_vs_comm == 1:
            # If both hands beat the community cards:
            winner = compare_same_ranks(hand_rank, player_hand_rank, bot_hand_rank)
            if winner == 1:
                return "player win"
            elif winner == -1:
                return "bot win"
            else:
                # comparing leftover cards
                player_view = player_hand+community_cards
                bot_view = bot_hand+community_cards
                winner = compare_left_over(hand_rank, player_view, bot_view, player_hand_rank, bot_hand_rank)
                return winner
        
def evaluate_winner(player_hand, bot_hand, community_cards):
    player_hand_score = evaluate_hand(player_hand, community_cards)
    bot_hand_score = evaluate_hand(bot_hand, community_cards)
    comm_cards_score = evaluate_hand([],community_cards)
    if (comm_cards_score[0] < player_hand_score[0]) and (comm_cards_score[0] < bot_hand_score[0]):
        return "tie"
    elif (comm_cards_score[0] == player_hand_score[0] == bot_hand_score[0]):
        hand_rank = player_hand_score[0]
        winner = compare_with_comm_card_best(hand_rank, player_hand, bot_hand, community_cards, player_hand_score[1],bot_hand_score[1],comm_cards_score[1])
        return winner
    elif player_hand_score[0]<bot_hand_score[0]:
        return "player win"
    elif player_hand_score[0]>bot_hand_score[0]:
        return "bot win"
    else:
        hand_rank = player_hand_score[0]
        # Comparing similar hands
        winner = compare_same_ranks(hand_rank, player_hand_score[1], bot_hand_score[1])
        if winner == 1:
            return "player win"
        elif winner == -1:
            return "bot win"
        else:
            # comparing leftover cards
            player_view = player_hand+community_cards
            bot_view = bot_hand+community_cards
            winner = compare_left_over(hand_rank, player_view, bot_view, player_hand_score[1], bot_hand_score[1])
            return winner
                    
if __name__ == "__main__":
    i = 0
    print(DECK)
    # import time
    # start = time.time()
    # while True:
    #     deck = shuffle_deck()
    #     player_hand = [deck.pop(), deck.pop()]
    #     bot_hand = [deck.pop(), deck.pop()]
    #     community_cards = [deck.pop() for i in range(5)]
    #     winner = evaluate_winner(player_hand, bot_hand, community_cards)    
    #     i+= 1
    #     if i==100000:
    #         break
    # end = time.time()
    # print(end-start)