# a1-forrelease

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


### 2. Road Trip

#### 2.1. Search Problem Formulation

#### 2.1.1. State Space

The state space is equal to the set of all cities and road junctions in `road-segments.txt` that are the endpoint of a road segment. The start state is the origin city specified by the user.

#### 2.1.2. Successor Function

The set of successor states to a particular state is equal to the set of states which correspond to cities and junctions that can be reached from the particular state by road without passing through any intermediary state (city or junction).

#### 2.1.3. Edge Weights

The set of edges between nodes in the state graph is equal to the set of road segments in `road-segments.txt`. The weight of each edge is the cost of traversing the corresponding road segment as calculated by the user-specified cost function. For the `segments` cost function, each edge has unit weight. For the `distance` cost function, each edge weight is equal to the length of the road segment in miles. For the `time` cost function, each edge weight is equal to the time in hours to drive the length of the road segment (segment length times inverse speed limit). For the `delivery` cost function, the weights of edges corresponding to road segments with speed limits less than 50 mph are equal to their weight for the `time` cost function; the weights of edges whose corresponding road segments have speed limits greater than or equal to 50 mph are calculated dynamically whenever the successor function encounters them as an option to traverse according to the formula provided in the assignment.

#### 2.1.4. Goal State

The goal state is the destination city provided by the user.

#### 2.1.5. Heuristic

In our tests a heuristic was not necessary as breadth-first search provided running times of one or two seconds for cities on opposite sides of the country.

#### 2.2. How the Algorithm Works

The algorithm uses a breadth-first search with the only special adjustment being that cities and junctions that have already been optimally visited (that we have already found the shortest path to) cannot be revisited.

### 2.3. Discussion

The following is a brief narrative describing how we approached the problem. We decided to first solve the problem for the `segments` cost function. To do this, we first tried to come up with an admissible heuristic but couldn't easily think of one other than the unuseful unifrom zero-cost-remaining prediction, so we decided to first implement Dijkstra's algorithm and check the performance. We tested Dijsktra's algorithm for several pairs of cities on opposite sides of the country and the running time was always less than a second, so we decided to move on to the remaining cost functions. We tested the remaining three cost functions using Dijkstra's algorithm for several pairs of cities on opposite sides of the country and the running time was always less than two or three seconds, so we decided to stick with this approach.

### Part 3: Choosing teams  
#### A description of how you formulated the search problem:  
1. State space -   
   Any arrangement of groups of students where each student is present and in one and only one team where a team can be of size 1,2 or 3.  

2. Successor function -   
   Staring with a group arrangement where each student is assigned to a group of size 3 where the other two members of the team are '-'   
   i.e. not present/assigned.  
   So there are n groups where n is the number of students with one team member(student) in each team.  
   Successors are generated by selecting all pair-wise teams and forming all valid combinations of each pair by exchanging a student between these pairs and combining the new teams formed with the existing teams minus old teams to get one successor.    
   Thus, successors of each state will be formed by exchanging students among teams such that all students are present only once in one and only one team.   
   Here one student is added / removed or no exchange happens based on if cost is minimized.  
   Valid successors contain all students only once in only one team.  
   Only the **minimum cost successors** are used and further combined in similar way to get next successors.  

3. Goal state:   
   Goal state is an arrangement of teams where each student belongs to at least and at most one team.   
   The cost to create such arrangement should be as low as possible.  

4. Cost function:   
   Formation of one permutation of team arrangement with one exchange of students will have a cost of 1.  

5. Heuristic Function:   
   A successor which has less cost than the predecessor is chosen, considering it will lead to minimum cost solution.

6. Initial State:  
   An arrangement of teams such that each student has his team consisting of only the student. Thus, there will be n teams where n is the number of students with each team consisting of only 1 student and one student should appear in one and only one team.  

#### A brief description of how your search algorithm works;  
The goal is to form teams of students such that the maximum team size is 3 and each student is part of one and only one team.  
The teams should be formed with the intention of keeping the cost to form the team arrangement as low as possible.  
Cost consists of 4 components:   
i. Cost of 5 is assigned for checking submission of each team. So for n teams the cost is 5*n   
ii. Cost of 10 is assigned when a student has to work with another student who he does not wish to work with.   
Hence, if there are m such students, the cost is m*10.   
iii. Cost of 2 is assigned if a student does not get the group size he requested for.   
Hence, if there are k such students, the cost is k*2.   
vi. Cost of 3 is assigned to students who did not receive the teammates they requested for.   
Total cost in this case is 5*n + 10*m + 2*k + 3*l.    
The goal is to minimize this cost.  

Staring with a group arrangement where each student is assigned to a group of size 3 where the other two members of the team are '-'  
i.e. not present/assigned.  
So there are n groups where n is the number of students with one team member(student) in each team.  
Successors are generated by selecting all pair-wise teams and forming all valid combinations of each pair by exchanging a student between these pairs and combining the new teams formed with the existing teams minus old teams to get one successor.  
Thus, successors of each state will be formed by exchanging students among teams such that all students are present only once in one and only one team.  
Valid successors contain all students only once in only one team.  
Among all the successors generated only minimum cost successor/successors are used for further processing.  
These minimum cost successors will then be permuted and grouped in a similar way to generate the next successor.   
Thus, minimum cost successor is searched locally and used.   
This is done until the cost does not change for a fixed number of iterations.  

#### Discussion of any problems you faced, any assumptions,simplifications, and/or design decisions you made.  
I started with a brute force approach by generating all possible combination of arrangements of groups of students and getting the arrangement with least cost.   
It worked for less number of students but didn't finish within time threshold for higher number of students specifically for test2.txt file with 13 students.  
For this the challenge faced was how to generate all permutations. For that I learnt about itertools.  
I had to think of several hacks like generating permutations of list and combining adjacent elements using ziplongest of 3 consecutive elements.  
  
To make this faster, I first thought of using the conditions like heuristic to reduce the successor space.  
So, first priority was given to make sure students don't work with students they do not wish to work as that would cost the most.   
Then creating a team of 3 people even if the student requests for 2 or 1 to reduce the number of teams and hence the time to correct each submission.   
Third priority would be to assign students who want to work with each other and lastly the preferred group for the student.   
The cost can vary with several combinations like if 3 students are assigned to a group the cost is less by 5 compared to two groups.   
But if each of those students don't want a group of three, the cost will increase by 6. So net cost will increase by 1.  
So I decided to concentrate on first and second priority and test. I coded this approach to see if the computation speed increases and I can find a solution within time threshold.  
But, I still couldn't find the solution within time threshold.  
  
So I decided on dropping the top-down approach as it involved too many arrangements.  
I thought of starting with 1 student and generating all combinations of 1, 2, and 3 with other students to form the groups.  
Use the minimum cost group as successor. So the students in the successor will be added to team.    
The remaining students are then  added in a similar way by generating different arrangements and then selecting the least cost one.   
and the process repeats. This did not give the correct answer as all valid combinations were not considered in each iteration.  
  
Next, to consider all combinations of the given teams arrangement,   
Started with all students in individual groups of one.   
Created all permutations of these groups by exchanging the students from one group into another and selected the minimum cost successor from all valid successors.   
That is the team arrangements where have all students present exactly ones in a team.  
Amongst all the successors generated only minimum cost successor/successors are used for further processing.  
Considered the assumption/heuristic that successor which has less cost than the predecessor will lead to minimum cost solution.  
These minimum cost successors will then be combined in a similar way to generate the next successor with the constraint of max team size being 3.   
Thus, minimum cost successor is searched locally.  
  
Finding all successors/permutations was the most challenging part.  
Also removing duplicates reduced the number of successors considerably.    
Used a visited list to avoid repeated computation.  
For coding, most of the time was spent to understand how to form all valid successor team arrangements for a given successor and reduce the number of computations.  
