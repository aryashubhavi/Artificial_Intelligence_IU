## PART 1
# Q3
<p>The program often fails to find a solution because it did not take into account the different directions the </br>
pichu could move in the map and does not keep track of the visited locations. I implemented <br>
Breadth first search to solve this problem. I kept track of the visited locations and appended them<br>
to the fringe. Then I also added a separate element to keep track of the directions the pichu could move. <br>
And I finally returned my move string with all the appended directions and length of the total added distance</p><br>

The program is using Breadth First Search as the search abstraction. <br>
Valid states: Any kind of house map with one pichu, one of us (@) and pichu making moves at places where there are no walls.<br>
Successor function: The successor function is the move pichu makes out of (row, col-1), (row, col+1), (row+1, col) and (row-1, col) where <br>
there are no walls and where pichu has not previously visited.
Cost function: Every move of the pichu has a cost and the cost function is the total number of such minimum number <br>
of moves <br>
Goal state: Position when pichu reaches us @ <br>
Initial state: Map where pichy can start from any position and move in any direction and positions where<br>
there are no walls (X)<br>

## PART 2
# Q4
<p>I have used depth first search as my search abstraction to solve this problem. My solutions runs <br>
very fast and gives the answer in 1-3 sec. <br>
State Space: Permutations = (rxc)!/((rxc)-k)! where the k number of pichus can not be placed <br>
on the same diagonals, rows or columns<br>
Initial State: 1 pichu, x walls + 1 @ (own location) on the map<br>
Goal State: k pichus are on the map with no pichus able to see each other<br>
Successor function: each of the successors is obtained by adding one pichu on a map<br>
with x walls and checking if it is safe to be placed (i.e. can not see another pichu) <br>
at that location<br>
Cost Function: irrelevant<br>