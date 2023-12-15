import re

input_lines = open("input_ex.txt").read().splitlines()

def gap_index(gap_lengths):
    idx = 0
    gap_sm = sum(gap_lengths)
    if gap_lengths[0] == gap_sm:
        return 0
    idx += 1
    for i in range(1, gap_sum+1):
        if gap_lengths[0] == gap_sm - i:
            return idx + gap_index(gap_lengths[1:])
        idx += gap_possib(len(gap_lengths)-1, i)

dict_gap_lens = {}
def gap_lens(gap_idx, gap_count ,gap_sm):
    if(gap_count == 0): return []
    if(gap_sm == 0): return [0] * gap_count
    if(gap_idx == 0): return [gap_sm] + [0]*(gap_count-1)

    if ((gap_idx, gap_count ,gap_sm) in dict_gap_lens):
        return dict_gap_lens[(gap_idx, gap_count ,gap_sm)]

    firstlen = gap_sm-1
    tmp_idx = 1
    large_tmp_idx = 1

    

    for i in range(1, gap_sum+1):
        large_tmp_idx += gap_possib(gap_count-1, i)
        if gap_idx >= large_tmp_idx:
            firstlen-=1
            tmp_idx = large_tmp_idx
        else: 
            dict_gap_lens[(gap_idx, gap_count ,gap_sm)] = [firstlen] + gap_lens(gap_idx - tmp_idx, gap_count-1, gap_sm- firstlen)
            return dict_gap_lens[(gap_idx, gap_count ,gap_sm)]
        
    print("error")

dict_gap_possible = {}
def gap_possib(gap_count,gap_sm):
    if(gap_sm == 0): return 1
    if(gap_count <= 1): return 1

    if ((gap_count, gap_sm) in dict_gap_possible):
        return dict_gap_possible[(gap_count, gap_sm)]

    ret = 0
    for i in range(gap_sm+1):
        ret += gap_possib(gap_count-1, gap_sm-i)
    dict_gap_possible[(gap_count, gap_sm)] = ret
    return ret

def string_from_lists(gaps,cons):
    ret = ''
    for i in range(len(cons)):
        ret += '.'*gaps[i] + '#'*cons[i] + ('.' if i< len(cons)-1 else '')
    ret += '.'*gaps[-1]

    return ret

def is_compatible(damaged, candidate):
    for i in range(len(damaged)):
        if(damaged[i] == '?'):
            continue
        if(damaged[i] != candidate[i]):
            return False
    return True



def count_possibilities(data, seqs):
    ## Rule out some obvious cases
    if len(data) < sum(seqs)+ len(seqs)-1: return 0
    if len(data) == sum(seqs)+ len(seqs)-1:
        return ?? # 1 if '.' is precisely at the gaps, 0 otherwise

    ## All seqs of same length? Then be smart

    ## Where do the seqs of highest length fit in? 
    # Find indices of longest sequences
    longest_seq = max(seqs)
    longest_ids = []
    for i in range(len(seqs)):
        if seqs[i] == longest_seq: longest_ids.append(i)

    # Find strings of # and ? in data
    m_it = re.finditer(r"([#?]+)", data)
    data_seqs = []
    for m in m_it:
        if m.end()-m.start() >= longest_seq:
            data_seqs.append({"data": m.group(), "start": m.start(), "end":m.end(), "len": m.end()-m.start()})
    
    ## For each possibility, cut up the data into several pieces and apply this function recursively
    possib = 0
    start_indices = possible_start_indices(longest_seq, len(longest_ids), data_seqs)
    for starts in start_indices:
        poss_of_these_startids = 1
        for gap in range(len(longest_ids)+1):
            gap_start, gap_len = 0, 0
            gap_data = ""
            gap_seqs = []
            if gap == 0:
                gap_start = 0
                gap_len = starts[0]-1
                gap_seqs = seqs[:longest_ids[0]]
            elif gap == len(longest_ids):
                gap_start = starts[-1] + longest_seq + 1
                gap_len = len(data) - gap_start
                gap_seqs = [longest_ids[-1]+1: ]
            else:
                gap_start = starts[gap-1] + longest_seq + 1
                gap_len = starts[gap]-1 - gap_start
                gap_seqs = 
            
            if(gap_len <= 0): gap_data = ''
            else: gap_data = data[gap_start:gap_len]

            if(this_gap_possibs == 0):
                poss_of_these_startids = 0
                break
            poss_of_these_startids *= this_gap_possib
        possib += poss_of_these_startids

    
    return possib

poss_sum = 0
for line in input_lines:
    data,conseq_str = line.split(' ')
    conseqs_str = conseq_str.split(',')
    consecs = [int(c) for c in conseqs_str]
    
    consecs = consecs*5
    data = data + "?" + data + "?" + data + "?" + data + "?" + data

    gap_sum = len(data)-sum(consecs)-len(consecs)+1

    line_sum = 0
    for i in range(gap_possib(len(consecs)+1, gap_sum)):
        if(is_compatible(data, string_from_lists(gap_lens(i,len(consecs)+1, gap_sum), consecs))):
            line_sum+=1
    print("Line sum: " + str(line_sum))
    poss_sum+= line_sum

print(poss_sum)