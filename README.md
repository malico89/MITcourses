# MITcourses

PDF files include problem statements (source: https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-0002-introduction-to-computational-thinking-and-data-science-fall-2016/assignments/).

PSET1, Knapsack:
  * PS1A: loading cows for trips, aka knapsack problem. Implemented as greedy and brute force.
  * PS1_cow_data are different cow names/weights to test with code.
  * PS1_partition supports brute force implementation by generating all permutations of cows.
  * PS1B: Knapsack with dynamic programming to solve a version of the optimal coin change problem. Using bottom-up tabulation method.

PSET2, Directed Depth-First Search:
  * PS2.py: traveling salesman problem using depth-first dearch in a directed graph. Includes optimizations for not exceeding best distances/max distances. Issues working on this: how to store best_dist and pass it to other recursive calls (this is what I got stuck on for a while, but took a while to isolate the issue). What helped: printing the whole traversal of the graph to the console, to see where things were not behaving as expected. This helped find how best_dist kept getting updated to current distance, making it impossible to find a better path.
  * graph.py: includes Node, Edge, WeightedEdge, and Digraph classes to be used in PS2.py to create the graph of buildings/distances provided in *mit_map.txt*. Graph is stored as  a dictionary with source nodes as keys and outgoing edges as their values.
  
PSET3, Random Walk:
* ps3.py: problem set I worked on. Includes Room and Robot classes, as well as methods to handle walk, cleaning and random re-orientation. Supporting files used for visualization and simulations of many robots/rooms (not written by me but included in this repository for functionality).


