
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

def gap_lens(gap_idx, gap_count ,gap_sm):
    if(gap_count == 0): return []
    if(gap_sm == 0): return [0] * gap_count
    if(gap_idx == 0): return [gap_sm] + [0]*(gap_count-1)

    firstlen = gap_sm-1
    tmp_idx = 1
    large_tmp_idx = 1

    

    for i in range(1, gap_sum+1):
        large_tmp_idx += gap_possib(gap_count-1, i)
        if gap_idx >= large_tmp_idx:
            firstlen-=1
            tmp_idx = large_tmp_idx
        else: 
            return [firstlen] + gap_lens(gap_idx - tmp_idx, gap_count-1, gap_sm- firstlen)
        
    print("error")

def gap_possib(gap_count,gap_sm):
    if(gap_sm == 0): return 1
    if(gap_count <= 1): return 1

    ret = 0
    for i in range(gap_sm+1):
        ret += gap_possib(gap_count-1, gap_sm-i)
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

poss_sum = 0
for line in input_lines:
    data,conseq_str = line.split(' ')
    conseqs_str = conseq_str.split(',')
    consecs = [int(c) for c in conseqs_str]

    gap_sum = len(data)-sum(consecs)-len(consecs)+1

    for i in range(gap_possib(len(consecs)+1, gap_sum)):
        if(is_compatible(data, string_from_lists(gap_lens(i,len(consecs)+1, gap_sum), consecs))):
            poss_sum+=1

print(poss_sum)