#!/usr/local/bin/python3
#
# route_pichu.py : a maze solver
#
# Submitted by : Shubhavi Arya, Username: aryas
#
# Based on skeleton code provided in CSCI B551, Fall 2021.

import sys
import itertools

# Parse the map from a given filename
def parse_map(filename):
        with open(filename, "r") as f:
                return [[char for char in line] for line in f.read().rstrip("\n").split("\n")][3:]
                
# Check if a row,col index pair is on the map
def valid_index(pos, n, m):
        return 0 <= pos[0] < n  and 0 <= pos[1] < m

# Find the possible moves from position (row, col)
def moves(map, row, col):
        moves=((row+1,col), (row-1,col), (row,col-1), (row,col+1))
        #U,L,R,D

        # Return only moves that are within the house_map and legal (i.e. go through open space ".")
        return [ move for move in moves if valid_index(move, len(map), len(map[0])) and (map[move[0]][move[1]] in ".@" ) ]

def find_direction(house_map,curr_move, move, curr_direction):
        print(house_map[curr_move[0]][curr_move[1]]) 
        if house_map[curr_move[0]][curr_move[1]]==".":
                if house_map[move[1]][move[0]]== ".":
                        [curr_direction].append(["U"])
                if house_map[move[-1]][move[0]]==".":
                        [curr_direction].append(["L"])
                if house_map[move[0]][move[-1]]==".":
                        [curr_direction].append(["R"])
                if house_map[move[0]][move[1]]==".":
                        [curr_direction].append==(["D"])
        print ([curr_direction])
        return [curr_direction]

# Perform search on the map
#
# This function MUST take a single parameter as input -- the house map --
# and return a tuple of the form (move_count, move_string), where:
# - move_count is the number of moves required to navigate from start to finish, or -1
#    if no such route exists
# - move_string is a string indicating the path, consisting of U, L, R, and D characters
#    (for up, left, right, and down)

def search(house_map):
        #variables to store rows and columns
        ROW, COL = len(house_map), len(house_map[0])

        # Find pichu start position
        pichu_loc=[(row_i,col_i) for col_i in range(len(house_map[0])) for row_i in range(len(house_map)) if house_map[row_i][col_i]=="p"][0]
        
        # I put in a new third element to mark the direction
        fringe=[(pichu_loc,0,"")]
        #print(fringe)

        #Stores the visited moves
        have_visited = [[False] * COL for _ in range(ROW)]

        #Store the directors U,L,R,D
        directions = [[1,0],[-1,0],[0,-1],[0,1]]
        directions_string = ["D","U","L","R"]
        
        while fringe:
                #Implementing BFS
                
                (curr_move, curr_dist, curr_direction)=fringe.pop()


                move_string = curr_direction
                #print(move_string)

                have_visited[curr_move[0]][curr_move[1]] = True



                if house_map[curr_move[0]][curr_move[1]]=="@":
                        #print(move_string)
                        return ((curr_dist), move_string)
  
                
                for i in range(4):
                        new_r, new_c = curr_move[0]+(directions[i])[0], curr_move[1]+(directions[i])[1]
                        if (new_r < 0 or new_r >= ROW or new_c < 0 or new_c >= COL or house_map[new_r][new_c] == "X" or (house_map[new_r][new_c] not in ".@" )or have_visited[new_r][new_c]): continue


                        fringe.append(((new_r, new_c),curr_dist+1,move_string+ directions_string[i]))


                                
        return (-1,"")

    

# Main Function
if __name__ == "__main__":
        house_map=parse_map(sys.argv[1])
        print("Shhhh... quiet while I navigate!")
        solution = search(house_map)
        print("Here's the solution I found:")
        print(str(solution[0]) + " " + solution[1])

