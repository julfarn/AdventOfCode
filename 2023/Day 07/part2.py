
input_lines = open("input.txt", "r").read().splitlines()

cards = "J23456789TQKA"
card_count = len(cards)

def card_value(card):
    return cards.index(card)

# Determines type of a hand, from 1 = High Card to 7 = Five of a kind
def hand_type(hand):
    sorted_hand = list(hand)
    sorted_hand.sort(key=card_value)
    j_count = 0
    pairs = 0
    triples = 0
    quads = 0
    quints = 0
    curr_streak = 1
    if(sorted_hand[0] == 'J'):
        j_count += 1
    for i in range(1,len(hand)):
        if(sorted_hand[i] == 'J'):
            j_count += 1
            continue
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
    
    preJscore = 0
    if (quints == 1): preJscore =  7                  # Five of a kind
    elif (quads == 1): preJscore =  6                   # Four of a kind
    elif (pairs == 1 and triples == 1): preJscore =  5  # Full house
    elif (pairs == 0 and triples == 1): preJscore =  4  # Three of a kind
    elif (pairs == 2): preJscore =  3                   # Two pair
    elif (pairs == 1): preJscore =  2                   # One pair
    else : preJscore =  1                                    # High card

    if(j_count == 5):
        return 7
    for i in range(j_count):
        preJscore = jAugmentScore(preJscore)
    return preJscore

def jAugmentScore(preJscore):
    if(preJscore == 0): 
        return 1
    if(preJscore == 1): return 2
    if(preJscore == 2): return 4
    if(preJscore == 3): return 5
    if(preJscore == 4): return 6
    if(preJscore == 5): 
        print("error")
        return 1
    if(preJscore == 6): return 7

    print("error")
    return 1

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