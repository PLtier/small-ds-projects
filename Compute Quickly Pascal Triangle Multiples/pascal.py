import numpy as np
from functools import lru_cache

@lru_cache()
def search_pascal_multiples_fast(row_limit):
    num_occurrences = {}

    current_column = np.array([6, 4,1], dtype=object)
    hasCurrentColumnMiddleElement = True
    for _ in range(row_limit - 6):
        # if it's row with middle element
        shiftedArrayToLeft = np.append(current_column, 0)
        if(hasCurrentColumnMiddleElement):
            shiftedArrayToRight = np.insert(current_column, 0, 0)
            
            # see, it's sliced!
            current_column = (shiftedArrayToLeft+shiftedArrayToRight)[1:]
            
        # if it's row without middle element
        else:
            shiftedArrayToRightByMiddleElement = np.insert(current_column, 0, current_column[0])
            # print(y, x)
            current_column = (shiftedArrayToLeft+shiftedArrayToRightByMiddleElement)
        
        hasCurrentColumnMiddleElement = not hasCurrentColumnMiddleElement

        # counting
        countArea = current_column[hasCurrentColumnMiddleElement:-2]
            # num_occurrences[el]=num_occurrences.get(el,0)+1
        for element in countArea:
            num_occurrences[element]=num_occurrences.get(element, 0)+1
        
        
    occurring4TimesOrMore = sorted([k for k,v in num_occurrences.items() if v>1])
    return occurring4TimesOrMore

#----------- DO NOT CHANGE ANYTHING BELOW THIS LINE


def search_pascal_multiples_slow(row_limit):

    # Building up Pascal's triangle with a dict of lists
    ptriangle = {}
    ptriangle[0] = [1]
    ptriangle[1] = [1,1]
    ptriangle[2] = [1,2,1]
    for r in range(3, row_limit):
        ptriangle[r] = []
        for i in range(len(ptriangle[r-1])+1):
            if i == 0: # on left border, so we just add 1
                ptriangle[r].append(1)
            elif i == len(ptriangle[r-1]): # on right border, so we just add 1
                ptriangle[r].append(1)
            else: # not on border, so we sum up the two numbers above
                ptriangle[r].append(ptriangle[r-1][i-1] + ptriangle[r-1][i])

    # Putting all numbers into one list, except the outermost 2 numbers in each row
    number_list = []
    for r in range(row_limit):
        row = ptriangle[r]
        for i, number in enumerate(row):
            if i > 1 and i < len(row)-1: # exclude the outermost 2 numbers in each row
                number_list.append(number)

    # Counting the numbers
    number_set = set(number_list) 
    pascal_multiples = []
    for unique_number in number_set:
        count = 0
        for number in number_list:
            if number == unique_number:
                count = count + 1
        if count > 3:
            pascal_multiples.append(unique_number)
    
    return sorted(pascal_multiples)


from timeit import default_timer as timer

def main():
	row_limit = 250

	start = timer()
	print(search_pascal_multiples_slow(row_limit))
	end = timer()
	runtime_slow = end-start

	start = timer()
	print(search_pascal_multiples_fast(row_limit))
	end = timer()
	runtime_fast = end-start

	print(round(runtime_slow / runtime_fast, 2))

if __name__ == "__main__":
	main()