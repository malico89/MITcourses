###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name:
# Collaborators:
# Time:

from ps1_partition import get_partitions
import time

#================================
# Part A: Transporting Space Cows
#================================

# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    # empty cow dict
    cows = {}
    
    # open and read file in read mode
    with open(filename) as file:
        # loop over lines in file, write into dict
        for line in file:
            line = line.split(',')
            cows[line[0]] = int(line[1])
    
    # return dict of cow: weight pairs
    return cows         

# Problem 2
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # list of lists (each list is a trip)
    trips = []
    
    # make a copy of the cow dict to keep track of cows left
    cows_avail = cows.copy()
    
    # while there are cows available, make trips
    while len(cows_avail) > 0: 
        # set available weight as the limit. This will get updated as we
        # load cows.
        avail_weight = limit
        
        # curr_trip hold the cows in the current trip
        curr_trip = []

        # keep loading current trip as long as at least the smallest cow fits
        # and there are cows left to add (last iteration)
        #while avail_weight >= min(cows_avail.values()):
        while avail_weight > 0:
            # take largest cow you can fit:
            # minimize available space minus cow weight (as long as >=0)
            # this ensures you are taking the largest cow possible
            
            # initialize value to minimize ot some max value. +1 so that we take
            # the largest cow if its weight = max weight
            min_val = limit + 1
            
            # loop over leftover cows to minimize conditions above
            for key, value in cows_avail.items():
                # calculate the space left after adding this cow
                val = avail_weight - value
                # if space left is minimized and space left is >=0:
                if val < min_val and val >= 0:
                    # update min value
                    min_val = val
                    # record as max cow possible
                    max_cow = key         
            # to avoid using min(dict) in the while statement, used this try-except
            # if we couldn't find another cow that fits, max_cow will be the same
            # as prior iteration. Since cow names are unique, try block will
            # throw a KeyError since that cow will no longer be in dict.
            # this means no cow fits and we can break out of current trip.
            try:              
                # update available space
                avail_weight -= cows_avail[max_cow]
                
                # remove added cow from available cows
                del cows_avail[max_cow]
                
                # add largest cow to current trip           
                curr_trip.append(max_cow)
                
            except KeyError:
                break
        
        # add curr_trip to list of trips
        #print("this trip:", curr_trip)
        trips.append(curr_trip)
    # return list of trips      
    return trips

# Problem 3
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # trips is list of lists, where each list is a trip
    trips = []
    
    # use get_partitions to generate all set partitions for the cow keys
    # as defined it will try to minimize number of subsets, so go until we 
    # find a solution that works
    for partition in get_partitions(cows.keys()):
        # iterate over each subset in the partition to check if weight limit is exceeded
        for trip in partition:
            weight = 0
            # add up weights of all cows in that trip
            for cow in trip:
                weight += cows[cow]
            # if the weight of that trip exceeds break and go to next partition
            if weight > limit:
                break
        # if we looped over every trip and didn't break for overweight, then 
        # that's the best brute force partition so far
        else:
            trips = partition
            break
    
    return trips
        
# Problem 4
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    filename = "ps1_cow_data.txt"
    #filename = "ps1_cow_data_2.txt"
    #filename = "ps1_cow_data_3.txt"
    print(filename)
    
    # create a dictionary out of cows (call load_cows function)
    cows = load_cows(filename)
    
    # greedy algorithm. get list of cows taken each trip 
    start = time.time()
    greedy_trips = greedy_cow_transport(cows)
    end = time.time()
    print("Greedy algorithm:", len(greedy_trips), "trips,", end-start, "seconds.")
    
    # brute force algorithm, get list of cows taken each trip
    start = time.time()
    brute_trips = brute_force_cow_transport(cows)
    end = time.time()
    print("Brute force algorithm:", len(brute_trips), "trips,", end-start, "seconds.")
    
    return
    
if __name__ == '__main__':
    #compare_cow_transport_algorithms
    #why does calling the function not go into the function??
    
    filename = "ps1_cow_data.txt"
    #filename = "ps1_cow_data_2.txt"
    #filename = "ps1_cow_data_3.txt"
    print(filename)
    
    # create a dictionary out of cows (call load_cows function)
    cows = load_cows(filename)
    
    # greedy algorithm. get list of cows taken each trip 
    start = time.time()
    greedy_trips = greedy_cow_transport(cows)
    end = time.time()
    print("Greedy algorithm:", len(greedy_trips), "trips,", end-start, "seconds.")
    
    # brute force algorithm, get list of cows taken each trip
    start = time.time()
    brute_trips = brute_force_cow_transport(cows)
    end = time.time()
    print("Brute force algorithm:", len(brute_trips), "trips,", end-start, "seconds.")