import re

input_lines = open("F:\\Projekte\\AdventOfCode\\2023\\Day 12\\input.txt").read().splitlines()

gen_call_count = 0
gen_dict = {}
def count_possibilities(data, seqs):
    global gen_call_count
    gen_call_count += 1
    if len(seqs) == 0: 
        return 0 if '#' in data else 1
    if len(data) == 0: return 0

    # Truncate start and finish
    if data.startswith('.'): return count_possibilities(data[1:], seqs)
    if data.endswith('.'): return count_possibilities(data[:-1], seqs)

    ## Rule out some obvious cases
    if len(data) < sum(seqs)+ len(seqs)-1: return 0
    if len(data) == sum(seqs)+ len(seqs)-1:
        # 1 if '.' is precisely at the gaps, 0 otherwise
        if data.count('.') > len(seqs)-1: return 0
        gap_idx = 0
        dotcount = 0
        for i in range(len(seqs)-1):
            gap_idx += seqs[i]
            if(data[gap_idx]== '#'): return 0
            if(data[gap_idx] == '.'): dotcount+=1
            gap_idx += 1
        if dotcount == data.count('.'): 
            return 1  
        return 0
    
    # Fixings at start and end
    if (seqs[0] == 1):
        if data.startswith('#?') or data.startswith('#.'):
            return count_possibilities(data[2:], seqs[1:])
        if data.startswith('?#?') or data.startswith('?#.'):
            return count_possibilities(data[3:], seqs[1:])
    if (seqs[-1] == 1):
        if data.endswith('?#') or data.endswith('.#'):
            return count_possibilities(data[:-2], seqs[:-1])
        if data.endswith('?#?') or data.endswith('.#?'):
            return count_possibilities(data[:-3], seqs[:-1])
    
    # Is data a sequence of '?'? Treat this separately
    if (not '.' in data) and (not '#' in data):
        return count_possibilities_blank(len(data), seqs)

    longest_seq = max(seqs)
    # return 0 if contains a '#'-chain longer than longest_seq
    long_m = re.search(r"#{" + str(longest_seq+1) + r"}", data)
    if(long_m != None): 
        return 0

    ## All seqs of length 1? Deal with this separately
    if longest_seq == 1:
        return count_possibilities_singular(data, len(seqs))

    # check in dictionary
    #if(len(data)<12):
    #    if(data in gen_dict):
    #        if(tuple(seqs) in gen_dict[data]):
    #            return gen_dict[data][tuple(seqs)]
    
    possib = 0        
    # are there any dots?
    if '.' in data:
        d = data.index('.')
        for i in range(len(seqs)+1):
            if (i -1 + sum(seqs[:i]) <= d) and (len(seqs) - i - 1 + sum(seqs[i:]) <= len(data)-d-1):
                possib += count_possibilities(data[:d], seqs[:i]) * count_possibilities(data[d+1:], seqs[i:])
        return possib

    ## Where do the seqs of highest length fit in? 
    # Find indices of longest sequences
    longest_ids = []
    for i in range(len(seqs)):
        if seqs[i] == longest_seq: longest_ids.append(i)
    
    min_first_longest_pos = sum(seqs[:longest_ids[0]]) + longest_ids[0]
    max_first_longest_pos = len(data) - sum(seqs[longest_ids[0]+1:]) - (len(seqs) -longest_ids[0]) - longest_seq +1

    # Find strings of # and ? in data
    """m_it = re.finditer(r"([#?]+)", data)
    id_set = set([])
    for m in m_it:
        if m.end()-m.start() >= longest_seq:
            id_set = id_set | set(range(m.start(), m.end()-longest_seq+1))
    id_set = id_set & set(range(min_first_longest_pos, max_first_longest_pos+1))
    start_pos_range = list(id_set)"""
    start_pos_range = range(min_first_longest_pos, max_first_longest_pos+1)

    for start_pos in start_pos_range:
        if (start_pos != 0 and data[start_pos-1] == '#') or (start_pos != len(data)-longest_seq and data[start_pos + longest_seq] == '#'):
            continue
        poss_with_this_startpos = 1
        poss_with_this_startpos *= count_possibilities(data[:max(start_pos-1,0)], seqs[:longest_ids[0]])
        if poss_with_this_startpos == 0: continue
        poss_with_this_startpos *= count_possibilities(data[start_pos + longest_seq + 1:], seqs[longest_ids[0]+1:])
        possib += poss_with_this_startpos
    

    # add to dictionary
    #if(len(data)<12):
    #    if(not data in gen_dict):
    #        gen_dict[data] = {}
    #    gen_dict[data][tuple(seqs)] = possib

    return possib

singular_dict = {}
sing_call_count = 0
def count_possibilities_singular(data, count, start=True):
    global sing_call_count
    sing_call_count+= 1
    if(count == 0): 
        return 1
    if(len(data) == 0): return 0

    if(start):
        fixcount = data.count('#')
        if fixcount != 0:
            if(fixcount > count): return 0
            if fixcount == count: 
                return 1
            doctored_data = data
            for i in range(fixcount):
                fixpos = doctored_data.index('#')
                if fixpos == 0: doctored_data = doctored_data[2:]
                elif fixpos == len(doctored_data)-1: doctored_data = doctored_data[:-2]
                else: doctored_data = doctored_data[:fixpos-1] + '.' + doctored_data[fixpos+2:]
            return count_possibilities_singular(doctored_data, count - fixcount, start=False)

    # here, start = false, so no '#' in data.
    if not '.' in data: return count_possibilities_blank_singular(len(data), count)
    if (count == 1): 
        return data.count('?')
    hole_nr = data.count('?')
    if(hole_nr < count) :  
        return 0
    if(hole_nr == len(data) == 2*count-1): 
        return 1
    if(hole_nr == len(data) == 2*count): #
        return count + 1

    """if(len(data)<7):
        if((data, count) in singular_dict):
            return singular_dict[(data,count)]"""
    if data.startswith("?."): return count_possibilities_singular(data[2:], count) +  count_possibilities_singular(data[2:], count-1)
    if data.endswith(".?"): return count_possibilities_singular(data[:-2], count) +  count_possibilities_singular(data[:-2], count-1)

    if data.startswith("??."): return count_possibilities_singular(data[3:], count) + 2 * count_possibilities_singular(data[3:], count-1)
    if data.endswith(".??"): return count_possibilities_singular(data[:-3], count) + 2 * count_possibilities_singular(data[:-3], count-1)

    if ".?." in data:
        x = data.index('.?.')
        docdata = data[:x] + data[x+2:]
        return count_possibilities_singular(docdata, count) + count_possibilities_singular(docdata, count-1)
    if ".??." in data:
        x = data.index('.??.')
        docdata = data[:x] + data[x+3:]
        return count_possibilities_singular(docdata, count) + 2* count_possibilities_singular(docdata, count-1)

    poss_sum = 0
    #for i in range(len(data)- (count-1)*2):
    #    if data[i] == '.': continue
    #    tmp_data = data[i+2:]
    #    poss_sum += count_possibilities_singular(tmp_data, count-1, start=False)
    d = data.index('.') # index of first '.'
    for i in range(max(0, count - int((len(data)-d)/2)), min(int(d/2)+1, count)+1):
        poss_sum += count_possibilities_blank_singular(d, i) * count_possibilities_singular(data[d+1:], count-i, start=False)

    """if(len(data)<7):
        singular_dict[(data,count)] = poss_sum"""

    return poss_sum

def count_possibilities_blank(data_len, seqs):
    for seq in seqs: data_len -= seq-1
    #return count_possibilities_singular('?' * data_len, len(seqs), start=False)
    return count_possibilities_blank_singular(data_len, len(seqs))

blank_call_count = 0
def count_possibilities_blank_singular(data_len, one_count):
    global blank_call_count
    blank_call_count += 1
    if(one_count == 0): return 1
    if(2*one_count-1 > data_len): return 0
    if(2*one_count-1 == data_len): return 1

    if(one_count == 1): return data_len
    if(one_count == 2):
        return (data_len - 2)*data_len - int(((data_len-2) * (data_len+1))/2)
    
    count_sum = 0
    for i in range(2*one_count-3, data_len -1):
        count_sum += count_possibilities_blank_singular(i, one_count-1)
    return count_sum


poss_sum = 0
line_nr = 0
arglist = []
for line in input_lines:
    line_nr +=1
    data,conseq_str = line.split(' ')
    conseqs_str = conseq_str.split(',')
    consecs = [int(c) for c in conseqs_str]
    
    consecs = consecs*5
    data = data + "?" + data + "?" + data + "?" + data + "?" + data
    
    gen_call_count, sing_call_count, blank_call_count = 0,0,0
    line_sum = count_possibilities(data, consecs)
    print("Line " + str(line_nr) + " sum: " + str(line_sum) + ", gen calls: " + str(gen_call_count) + ", sing calls: " + str(sing_call_count) + ", blank calls: " + str(blank_call_count))
    poss_sum+= line_sum


print(poss_sum)