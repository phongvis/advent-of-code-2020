import math
import re
from collections import deque, defaultdict, Counter, namedtuple
from itertools import chain, combinations, product, accumulate, cycle
from heapq import heappop, heappush

flatten = chain.from_iterable

def get_input(day):
    "Return the input file."
    return open('input{}.txt'.format(day))

def get_input_string(day):
    "Return the content of the input file as a string."
    return get_input(day).read()

def get_input_rows(day):
    "Return the content of the input file as a list of string, each for a row."
    return get_input_string(day).splitlines()

def get_input_ints(day):
    "Return the content of the input file as a list of integers, each for a row."
    return [int(x) for x in get_input_rows(day)]

def parse_ints(text):
    return [int(n) for n in re.findall(r'\d+', text)]

def parse_signed_ints(text):
    return [int(n) for n in re.findall(r'-?\d+', text)]

# 2D points
UP, LEFT, DOWN, RIGHT = (0, -1), (-1, 0), (0, 1), (1, 0)

def neighbors4(point): 
    "The four neighbors (without diagonals)."
    x, y = point
    return ((x+1, y), (x-1, y), (x, y+1), (x, y-1))

def neighbors8(point): 
    "The eight neighbors (with diagonals)."
    x, y = point 
    return ((x+1, y), (x-1, y), (x, y+1), (x, y-1),
            (x+1, y+1), (x-1, y-1), (x+1, y-1), (x-1, y+1))

def breadth_first(start, goal, moves_func):
    "Find a shortest sequence of states from start to the goal."
    frontier = deque([start]) # A queue of states
    previous = {start: None}  # start has no previous state; other states will
    while frontier:
        s = frontier.popleft()
        if s == goal:
            return path(previous, s)
        for s2 in moves_func(s):
            if s2 not in previous:
                frontier.append(s2)
                previous[s2] = s
                
def path(previous, s): 
    "Return a list of states that lead to state s, according to the previous dict."
    return [] if (s is None) else path(previous, previous[s]) + [s]

def astar_search(start, h_func, moves_func):
    "Find a shortest sequence of states from start to a goal state (a state s with h_func(s) == 0)."
    frontier  = [(h_func(start), start)] # A priority queue, ordered by path length, f = g + h
    previous  = {start: None}  # start state has no previous state; other states will
    path_cost = {start: 0}     # The cost of the best path to a state.

    while frontier:
        (f, s) = heappop(frontier)
        if h_func(s) == 0:
            return path(previous, s)
        for s2 in moves_func(s):
            new_cost = path_cost[s] + 1
            if s2 not in path_cost or new_cost < path_cost[s2]:
                heappush(frontier, (new_cost + h_func(s2), s2))
                path_cost[s2] = new_cost
                previous[s2] = s
                
    return dict(fail=True, front=len(frontier), prev=len(previous))