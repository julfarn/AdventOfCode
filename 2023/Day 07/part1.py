
input_lines = open("input.txt", "r").read().splitlines()

cards = "23456789TJQKA"
card_count = len(cards)

def card_value(card):
    return cards.index(card)

# Determines type of a hand, from 1 = High Card to 7 = Five of a kind
def hand_type(hand):
    sorted_hand = list(hand)
    sorted_hand.sort(key=card_value)
    pairs = 0
    triples = 0
    quads = 0
    quints = 0
    curr_streak = 1
    for i in range(1,len(hand)):
        if sorted_hand[i] == sorted_hand[i-1]:
            curr_streak+=1
            if i < len(hand)-1: continue
        
        if(curr_streak == 2):
            pairs +=1
        elif curr_streak == 3:
            triples = 1
        elif curr_streak == 4:
            quads = 1
        elif curr_streak == 5:
            quints = 1
        
        curr_streak=1
    
    if (quints == 1): return 7                  # Five of a kind
    if (quads == 1): return 6                   # Four of a kind
    if (pairs == 1 and triples == 1): return 5  # Full house
    if (pairs == 0 and triples == 1): return 4  # Three of a kind
    if (pairs == 2): return 3                   # Two pair
    if (pairs == 1): return 2                   # One pair
    return 1                                    # High card

# Assigns the hand a value, does not take type into account
def hand_value_naive(hand):
    val = 0
    for i in range(len(hand)):
        val += pow(card_count, len(hand)-i-1) * card_value(hand[i])
    return val

# Assigns the hand a value, takes hand type into account. Not every value has a corresponding hand. 
def hand_value(hand):
    t = hand_type(hand)
    max_naive_value = pow(card_count, len(hand))

    return (t-1) * max_naive_value + hand_value_naive(hand)
   

# Read File
bidlist = []
for line in input_lines:
    bidpair_str =  line.split(" ")
    bidpair = {"hand": bidpair_str[0], "bid": int(bidpair_str[1])}
    bidlist.append(bidpair)

# Sort list of hand-bid-pairs according to hand value.
bidlist.sort(key=lambda bp : hand_value(bp["hand"]))

# Sum up winnings
total_winnings = 0
for i in range(len(bidlist)):
    total_winnings += bidlist[i]["bid"] * (i+1)

print(total_winnings)