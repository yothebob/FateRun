import math
import random
import time

st = time.time()


rng = 50
variance = random.randrange(1,10)
array_map = [[random.randrange(0, abs((rng^2 - abs(i^2 - (rng - random.randrange((ii - variance),(ii + variance)))) + abs(ii^2 - (rng - i))))) for ii in range(rng)] for i in range(int(rng/2))] 
# reduced_array_map = [[(random.randrange(0, abs((rng^2 - abs(i^2 - (rng - random.randrange((ii - variance),(ii + variance)))) + abs(ii^2 - (rng - i))))) - variance) for ii in range(rng)] for i in range(int(rng/2))] 
# inverted_array_map = [[abs(random.randrange(0, abs((rng^2 - abs(i^2 - (rng - random.randrange((ii - variance),(ii + variance)))) + abs(ii^2 - (rng - i))))) - rng) for ii in range(rng)] for i in range(int(rng/2))] 

def map_to_char(val):
    if val < 5:
        return "_"
    if val < 10:
        return "."
    if val < 20:
        return "*"
    if val < 30:
        return "+"
    if val < 40:
        return "%"
    return "#"

def map_list_to_char(lst):
    res = []
    for item in lst:
        res.append(map_to_char(item))
    return "".join(res)

[print(map_list_to_char(i)) for i in array_map]

et = time.time()

print("run time: ", et - st, " seconds")
