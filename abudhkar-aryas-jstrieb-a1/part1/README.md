### Part 1: Solving 25 Board Puzzle
#### A description of how you formulated the search problem:
1. State space:  
   States will be different arrangements of 1-25 number tiles on a board of size 5x5 alone with the cost and heuristic associated.
  
2. Successor function:  
   Successors for a given state  will be generated using
   1. Sliding of a column up (For 5 columns 5 successors)
   2. Sliding of a column down (For 5 columns 5 successors)
   3. Sliding of a row left (For 5 rows 5 successors)
   4. Sliding of row right (For 5 rows 5 successors)
   5. Clockwise rotation of outer ring of board
   6. Anticlockwise rotation of outer ring of board
   7. Clockwise rotation of inner ring of board
   8. Anticlockwise rotation of outer ring of board  
      Thus, total 24 possible successors for each state
  
3. Goal state:  
   Goal state is board configuration [[1 2 3 4 5],[6 7 8 9 10],[11 12 13 14 15],[16 17 18 19 20],[21 22 23 24 25]]
  
4. Cost function:  
   Cost function consists of sum of following 2 components:    
   g: Number of moves from the initial state to current state     
   h: Heuristic function  
   1. For row and column: manhattan distance/5 as the maximum movement of tiles in one move is 5  
   2. For outer ring: manhattan distance/16 as the maximum movement of tiles in one move is 16  
   3. For inner ring: manhattan distance/8 as the maximum movement of tiles in one move is 8  
   4. For initial board manhattan distance  
      cost = g+h  
  
6. Heuristic Function:    
   h: Heuristic function  
   1. For row and column: manhattan distance/5 as the maximum movement of tiles in one move is 5  
   2. For outer ring: manhattan distance/16 as the maximum movement of tiles in one move is 16  
   3. For inner ring: manhattan distance/8 as the maximum movement of tiles in one move is 8  
   4. For initial board manhattan distance     
      It is admissible as it does not over-estimate the cost as the distance<= minimum movement of tiles to get to goal state  
  
7. Initial state:    
   Initial state is the board arrangement with cost 0 and heuristic(manhattan for the initial state board compared to the goal state board)  

#### A brief description of how your search algorithm works;  
A* search algorithm is used to solve this problem.   
A priority queue is used which will return the low cost state(minimum sum of cost to reach state + heuristic) among all the states in the priority queue.    
A visited dictionary is maintained to avoid duplicate computation.    
First (initial state, moves) is inserted in queue where moves = empty list indicating the moves taken to reach the state.  
1. Remove the priority item from queue.  
2. Generate its successors using transformations as Sliding of a column up (For 5 columns 5 successors), Sliding of a column down (For 5 columns 5 successors), Sliding of a row left (For 5 rows 5 successors), Sliding of row right (For 5 rows 5 successors), Clockwise rotation of outer ring of board, Anticlockwise rotation of outer ring of board, Clockwise rotation of inner ring of board, Anticlockwise rotation of outer ring of board.  
3. If successor is goal state, algorithm ends returning the moves required to reach the state.  
4. Successors are inserted in priority queue along with the list of moves performed to reach the state, if not already visited.  
5. Repeat steps 1-4 until goal state is reached  

#### Discussion of any problems you faced, any assumptions,simplifications, and/or design decisions you made.  
Code to perform matrix transformation, rotate outer rings clockwise and anticlockwise is tricky.    
I tried to use the functions provided by the test code, but they were not working correctly.  I was not able to find the exact errors.   
So hardcoded the functions. But considering the board is static, this way is faster compared to doing various matrix transformations.    
So decided to stick with it.  

For priority queue, provided the comparator in the BoardState class. That was an important step which improved the speed for board 0 and board 0.5.    
Initially, I was using the tuple with (cost+heuristic,board,moves) which was not fast enough.  

Experimented with misplaced tiles distance heuristic. Tried to do combination of manhattan and linear conflict.  

Getting the solution with simple misplaced tiles and simple manhattan heuristic for board 0.txt and board 0.5.txt, but it is not admissible and hence cannot always guarantee optimal solution.  
####  
1. In this problem, what is the branching factor of the search tree?    
   Branching factor is 24 as every state can have 24 successors.  

2. If  the  solution  can  be  reached  in  7  moves,  about  how  many  states  would  we  need  to  explore  before  we found it if we used BFS instead of A* search?  A rough answer is fine.  
   A* would take a branch and further expands nodes in that branch to search for a solution  
   BFS would expand all branches  and traverse all nodes to find the optimal solution  
   Considering a tree of height 7, Worst case might need to explore 24^(8)-1 nodes in a BST  
