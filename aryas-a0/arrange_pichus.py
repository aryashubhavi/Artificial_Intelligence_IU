#!/usr/local/bin/python3
#
# arrange_pichus.py : arrange agents on a grid, avoiding conflicts
#
# Submitted by : SHUBHAVI ARYA, Username: aryas
#
# Based on skeleton code in CSCI B551, Fall 2021.

import sys

# Parse the map from a given filename
def parse_map(filename):
    f = open(filename, 'r')
    lines = f.readlines()
    return lines

def parse_map_v2(filename):
	with open(filename, "r") as f:
		return [[char for char in line] for line in f.read().rstrip("\n").split("\n")][3:]

# Count total # of pichus on house_map
def count_pichus(house_map):
    return sum([ row.count('p') for row in house_map ] )

# Count total # of walls on house_map
def count_walls(house_map):
    return sum([ z.count('X') for z in house_map ] )

#Return a string with the house_map rendered in a human-pichuly format
def printable_house_map(house_map):
     return "\n".join(["".join(row) for row in house_map])


def helper_to_solve(house_map,k):
    row_counter = len(house_map) - 3

    for z, row in enumerate(house_map):
        
        if z == 1:
            fringe = []
            for i in range(2, row_counter+2):
                fringe.append(list(house_map[z + i].strip("\n"))) 
            initial_pichu_count = count_pichus(house_map)
            solution = depth_first_search(0, 0, 0, fringe,k,row_counter)
            if solution:
                return (solution, True)
            else:
                return ("No Solution", False)
        
    return ("No Solution", False)
        

#------------------------------------------------------------------------#
#------------------------------------------------------------------------#

def solve(initial_house_map,k):
    return helper_to_solve(initial_house_map,k)

def add_pichu(house_map, row, col):
    return house_map[0:row] + [house_map[row][0:col] + ['p',] + house_map[row][col+1:]] + house_map[row+1:]

def depth_first_search(row, mycol, initial_pichu_count, house_map,k,r):
    count = initial_pichu_count
    house_map_copy = [z[:] for z in house_map]
    sign = 0
    for i in range(mycol,r+1):
        count = initial_pichu_count 
        house_map_copy = [z[:] for z in house_map]
        if pichu_is_protected(house_map_copy,row,i,k,r) and (count<=k):
            sign=1
            house_map_copy[row][i] = 'p'
            count += 1
            if count == k:
                return (house_map_copy)

            for y in range(i + 1, r):
                if (house_map_copy[row][y]) == 'X' or (house_map_copy[row][y]) == '@':
                    house_map_copy = depth_first_search(row, y + 1, count, house_map_copy,k,r)
                    return (house_map_copy)

            if row < r - 1:
                house_map_copy = depth_first_search(row + 1, 0, count, house_map_copy,k,r)
                return (house_map_copy)

            if row == r - 1 and i == r - 1:
                return False

    if sign == 0 and row < r - 1:
        house_map_copy = depth_first_search(row + 1, 0, count, house_map_copy,k,r)
    return house_map_copy

def pichu_is_protected(house_map, row, c,k,r):
    previous_row = previous_row_pichus(house_map,r,row,c)
    down_column = down_column_pichus(house_map,r,row,c)
    up_column = up_column_pichus(house_map,r,row,c)
    left_diag = left_diag_pichus(house_map,r,row,c)
    right_diag = right_diag_pichus(house_map,r,row,c)

    if (house_map[row][c] == 'p' or house_map[row][c] == 'X' or house_map[row][c] =='@'):
        return False
    
    elif (previous_row is False):
        return False

    
    elif (down_column is False):
        return False

    
    elif (up_column is False):
        return False

    
    elif (left_diag is False):
        return False

    
    elif (right_diag is False):
        return False

    else:
        return True


def previous_row_pichus(house_map,r,row,c):
    if c != 0:
        for y in range (c-1,-1,-1):
            if (house_map[row][y] == 'X' or house_map[row][y] == '@'):
                return True
            if (house_map[row][y] == 'p') :
                return False
            else:
                continue
        return True
    else:
        return True


def up_column_pichus(house_map,r,row,c):
    if r != 0:
        for y in range (r-1,-1,-1):
            if (house_map[y][c] == 'p') :
                return False
            if (house_map[y][c] == 'X' or house_map[y][c] == '@'):
                return True
            else:
                continue
        return True
    else:
        return True

def down_column_pichus(house_map,r,row,c):
    if r != 0:
        for y in range (r): 
            if (house_map[y][c] == 'X' or house_map[y][c] == '@'):
                return True
            if (house_map[y][c] == 'p') :
                return False
            else:
                continue
        return True
    else:
        return True


def left_diag_pichus(house_map,r,row,c):
    x = row - 1
    y = c - 1

    while x >= 0 and y >=0:
  
        if (house_map[x][y] == 'X' or house_map[x][y] == '@'):
            return True
        if house_map[x][y] == 'p':
            return False
        else:
            x = x-1
            y = y-1
            continue

    return True

    


def right_diag_pichus(house_map,r,row,c): #(2,3) (1,4)
#(1,5) (0,6) -> 
#(2,3) (1,4) (2,4) (1,5) (0,6)
# (3,3) (2,4) (1,5) (0,6)

    x = row
    y = c

    while x >= 0 and y < r:

        if (house_map[x][y] == 'X' or house_map[x][y] == '@'):
            return True
        if house_map[x][y] == 'p':
            return False
        else:
            x = x-1
            y = y+1
            continue
    return True



#------------------------------------------------------------------------#
#Main Function
if __name__ == "__main__":
    house_map=parse_map(sys.argv[1])
    # This is k, the number of agents
    k = int(sys.argv[2])
    print ("Starting from initial house map:\n" + printable_house_map(house_map) + "\n\nLooking for solution...\n")
    solution = solve(house_map,k)
    print ("Here's what we found:")
    print (printable_house_map(solution[0]) if solution[1] else "False")