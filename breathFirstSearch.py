'''
Class: CPSC 427 
Team Member 1: Andrew Abbott
Team Member 2: None
Submitted By Andrew Abbott
GU Username: aabbott
File Name: proj6.py
Generates a breath first search of an 8-puzzle from an initial state
then print out the path taken to get to the solution
Reference: An Eight-Puzzle Solver in Python, https://gist.github.com/flatline/8382021
Usage: python proj6.py
'''

from copy import deepcopy
from collections import deque

class EightPuzzle:
    def __init__(self,parent):
        #state_lst now holds the root, the parent state
        self.state_lst = [[row for row in parent]]

    #displays all states in state_lst
    def display(self):
        i = 0
        for state in self.state_lst:
            print('Node: ' + str(i + 1))
            i = i + 1
            for row in state:
                print row
            print ""
        
    #returns (row,col) of value in state indexed by state_idx  
    def find_coord(self, value, state_idx):
        for row in range(3):
            for col in range(3):
                if self.state_lst[state_idx][row][col] == value:
                    return (row,col)
        
                
    #returns list of (row, col) tuples which can be swapped for blank
    #these form the legal moves of the state indexed by state_idx
    def get_new_moves(self, state_idx):
        row, col = self.find_coord(0,state_idx) #get row, col of blank
        
        moves = []
        if col > 0:
            moves.append((row, col - 1))    #go left
        if row > 0:
            moves.append((row - 1, col))    #go up
        if row < 2:
            moves.append((row + 1, col))    #go down
        if col < 2:
            moves.append((row, col + 1))    #go right
        return moves

    #Generates all child states for the state indexed by state_idx
    #in state_lst.  Appends child states to the list
    def breadth_first(self,state_idx,goal):
        #create queues
        open_queue = deque()
        closed_queue = deque()
        children_queue = deque()

        #append new moves to the open queue
        open_queue.append(self.get_new_moves(state_idx))
       
        #blank is a tuple, holding coordinates of the blank tile
        blank = self.find_coord(0,state_idx)

        #tile is a tuple, holding coordinates of the tile to be swapped
        #with the blank
        for tile in iter(open_queue.popleft()):
            #create a new state using deep copy 
            #ensures that matrices are completely independent
            child = deepcopy(self.state_lst[state_idx])

            #move tile to position of the blank
            child[blank[0]][blank[1]] = child[tile[0]][tile[1]]

            #set tile position to 0                          
            child[tile[0]][tile[1]] = 0
            
            #append child state to the child queue.
            children_queue.append(child)

            #while the children queue is not empty, deque the child 
            while children_queue:
                kiddo = children_queue.popleft()
                #if the dequed child is not already in the lists, add it
                if kiddo not in self.state_lst and kiddo not in closed_queue:
                    self.state_lst.append(kiddo)
                    open_queue.append(kiddo)
            #if the new child is our goal, return true
            if kiddo == goal:
                return True
            #append the item to the closed queue if it is not the goal
            closed_queue.append(child)
        return False
        
def main():
    #nested list representation of 8 puzzle. 0 is the blank.
    #This configuration is found on slide 8, E: Two Search Algorithms
    parent = [[2,8,3],
              [1,6,4],
              [7,0,5]]
    #creates the goal state of the 8-puzzle
    goal = [[1,2,3],
            [8,0,4],
            [7,6,5]]
    
    #the initial level of the puzzle to check
    level = 0
                         
    #initialize the list of states (state_lst) with the parent
    p = EightPuzzle(parent)
    
    #Generate the states reachable from the parent, then increments when checked
    #and exausted the first level, then continues on to the next level
    while not p.breadth_first(level,goal):
        level = level + 1
    
    #display all states in state_lst                    
    p.display()

main()

