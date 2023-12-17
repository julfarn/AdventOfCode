
input_strings = open("input_ex.txt").read().splitlines()

def hash(s):
    cuva = 0
    for c in s:
        cuva += ord(c)
        cuva *= 17
        cuva %= 256
    return cuva

hashs = [hash(s) for s in input_strings]
print(sum(hashs))