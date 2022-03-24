## 2. Road Trip

### 2.1. Search Problem Formulation

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

### 2.2. How the Algorithm Works

The algorithm uses a breadth-first search with the only special adjustment being that cities and junctions that have already been optimally visited (that we have already found the shortest path to) cannot be revisited.

### 2.3. Discussion

The following is a brief narrative describing how we approached the problem. We decided to first solve the problem for the `segments` cost function. To do this, we first tried to come up with an admissible heuristic but couldn't easily think of one other than the unuseful unifrom zero-cost-remaining prediction, so we decided to first implement Dijkstra's algorithm and check the performance. We tested Dijsktra's algorithm for several pairs of cities on opposite sides of the country and the running time was always less than a second, so we decided to move on to the remaining cost functions. We tested the remaining three cost functions using Dijkstra's algorithm for several pairs of cities on opposite sides of the country and the running time was always less than two or three seconds, so we decided to stick with this approach.
