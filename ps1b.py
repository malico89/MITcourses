###########################
# 6.0002 Problem Set 1b: Space Change
# Name:
# Collaborators:
# Time:
# Author: charz, cdenise

#================================
# Part B: Golden Eggs
#================================

# Problem 1
def dp_make_weight(egg_weights, target_weight, memo = {}):
    """
    Find number of eggs to bring back, using the smallest number of eggs. Assumes there is
    an infinite supply of eggs of each weight, and there is always a egg of value 1.
    
    Parameters:
    egg_weights - tuple of integers, available egg weights sorted from smallest to largest value (1 = d1 < d2 < ... < dk)
    target_weight - int, amount of weight we want to find eggs to fit
    memo - dictionary, OPTIONAL parameter for memoization (you may not need to use this parameter depending on your implementation)
    
    Returns: int, smallest number of eggs needed to make target weight
    
    Knapsack with dynamic programming implemented with bottom-up tabulation approach.
    Reference used: https://www.youtube.com/watch?v=Y0ZqKpToTic
    Rows: each denomination
    Columns: 0-target_weight
    Each cell: minimum number of eggs needed to achieve that weight.
    """
    # construct table. outer loop: egg weights. inner loop: 0-target_weight
    # table will be stored in memo. key=egg_weight, value=list, indexed from 0-target_weight
    for i, w in enumerate(egg_weights):
        # initialize key-value pair for a given egg weight. Value is empty list to be filled in inner loop.
        memo[w] = []
        for j in range(target_weight + 1):
            # if weight is 0, no eggs
            if j == 0:
                memo[w].append(0)
            # if egg_weight is less than weight, minimize number of eggs
            elif w <= j:
                # to minimize: take the min of (using prior denomination to get same weight, using current denomation to get weight)
                # first item=prior egg value, same weight
                # second item="sub" current egg value by subtracting it from weight and adding 1 to egg total
                
                # if first egg weight, no need to look at "row" above to minimize
                if i == 0:
                    min_eggs = memo[w][j-w] + 1
                else:
                    min_eggs = min(memo[egg_weights[i-1]][j], memo[w][j-w] + 1)
                memo[w].append(min_eggs)
            # else if egg_weight is more than weight, take prior denomination min number of eggs at j
            else:
                memo[w].append(memo[egg_weights[i-1]][j])

    # access bottom right value to get minimum number of coins (largest egg_weight at target_weight)
    # uncomment below to only returns min number of eggs
    #return memo[egg_weights[-1]][target_weight]

    # determine makeup of min number of egg:                
    # cur_weight to keep track as we subtract from total weight
    cur_weight = target_weight
    
    # egg_choices: a dict that holds how many of each egg_weight are in the optimal solution
    egg_choices = {}
    
    #print(memo)
    
    # outer loop goes backwards from highest to smallest egg weight
    for i in range(len(egg_weights)-1, -1, -1):
        # check if equal to memo[i-1][j] (row above, same column). if not equal, i is in the set.
        while egg_weights[i] <= cur_weight:
            # also if smallest egg weight, keep subtracting until we get 0
            if i == 0 or (memo[egg_weights[i]][cur_weight] != memo[egg_weights[i-1]][cur_weight]):
                # if they are not equal, add to the count of i in the egg_choices dict
                if egg_weights[i] in egg_choices.keys():
                    egg_choices[egg_weights[i]] += 1
                else:
                    egg_choices[egg_weights[i]] = 1
                # subtract from current weight the egg weight accounted for
                cur_weight -= egg_weights[i]
            
        # break if all weight accounted for
        if cur_weight == 0:
            break
    
    # string together the min number of eggs and the composition
    out = str(memo[egg_weights[-1]][target_weight]) + ' ('
    
    # list of formatted value * key pairs
    eggs = []
    for key, value in egg_choices.items():
        eggs.append(str(value) + ' * ' + str(key))
    
    # join key/value pairs together
    out += ' + '.join(eggs)
    
    # finish off the string
    out += ' = ' + str(target_weight) + ')'
    return out
        

# EXAMPLE TESTING CODE, feel free to add more if you'd like
if __name__ == '__main__':
    #egg_weights = (1, 5, 10, 25)
    #n = 99
    # print("Egg weights = (1, 5, 10, 25)")
    # print("n = 99")
    # print("Expected ouput: 9 (3 * 25 + 2 * 10 + 4 * 1 = 99)")
    
    # test case #2. 
    egg_weights = (1, 5, 6, 8)
    n = 11
    print("Egg weights = (1, 5, 6, 8)")
    print("n = 11")
    print("Expected ouput: 2 (1 * 5 + 1 * 6)")
    
    print("Actual output:", dp_make_weight(egg_weights, n))
    print()