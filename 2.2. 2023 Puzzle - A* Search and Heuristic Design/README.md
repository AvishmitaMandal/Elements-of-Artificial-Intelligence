# 2.2. 2023 Puzzle - A* Search and Heuristic Design

Data structure : Priority Queue (Heap - Sorted Binary Tree)
Algorithm : A* search 
Evaluation Function : Cost Function + Heuristic Function
Cost Function : Adaptive cost or half cost used in pathfinding algorithms 
Heuristic Function : Manhattan distance

(1) Formulation of the search problem:
- There are 25! state spaces possible and if tried to found exhaustively the program would never end !!
- To solve this issue we need to have a sense of how far we are from the goal state and this can be done by calculating a heuristic function.
- A* would be the appropriate algorithm to go with solving the problem.

State space :
- All permutations of distict 5 x 5 grids with unique number ranging from [1,2,3 ... 25]
- Number of possible states : 25!

Successor Function:
- Each row can slide right or left with the residual element getting appended to the begining or the end of the row respectively (generating 10 successors)
- Each column can slide down or up with the residual element getting appended to the begining or the end of the column respectively (generating 10 successors)
- The outer ring can rotate clockwise and anticlockwise (generating 2 successors)
- The inner ring (outer ring of 3 x 3 matrix inside the 5 x 5 grid) can rotate clockwise and anticlockwise (generating 2 successors)
- Total number of successors from each state = 24

Edge weights:
- The edge weight is taken as 1. 
- However, the total cost from reaching from S to state n is calculated as (cost^2)/2 where cost = # states between S and n. 
- This has been done after tweaking the heuristic function numerous times, this found to give really good results.

Goal State:
- 5 x 5 grid in canonical order ranging from 1 to 25 starting from the top left to bottom right.

Heuristic Function:
- Manhattan distance. - sum of the difference between the coordinates
- The heuristic function is not admissible, but when combined with the cost function as evaluation function, works really well hence this heuristic was chosen.
- Other heuristics were tried, will be discussed in the design discussion.


(2) How the program works ?

1. We start from the start state. We calculate an estimate of the cost it will take for us to reach the goal state.
2. This is done using heuristic function - Manhattan distance. And push the state into a priority queue sorted in increasing order of the evaluation function.
3. Our evaluation functions = g(n) + h(n), where g(n) has been taken to be the adaptive cost used in many pathfinding algorithms which is the square of the cost divide by 2
4. The successor function is then called which generates 24 successors as explained above in detail which are also put in the priority queue along with the calculated evaluation function.
5. Then the next state is picked with the least f(n) value and a closed list is maintained to keep track of the visited states.

(3) Problems Faced and Design Decisions were mainly around the heuristics and cost functions:
- Attempt 1. Heuristics = Mismatched tiles 
    For both board0 and board1 the program did not converge indicating clearly that the heuristics were not admissible

- Attempt 2. Heuristic = Custom Function
    1. So for row and column sliding it took care of the min number of times it needs to slide left, right, up or down for each cell.
    eg. If 1 is at the top right (where 5 is supposed to be in goal state) - it would take care by returning 1 (and not 4) - took care of rotating around the grid
    2. For considering rotation costs of the rings - got the difference of the heuristic(current state) and heuristic(next successor after a Oc, Occ, Ic or Icc) giving an estimate if we are going towards the goal state or not
    Played around with the weights to give out a correct representation of the overall cost and making sure the heuristic was not exceeding the actual cost making it admissible.

- Attempt 3. Manhattan Distance
    Performed much better, so decided to go with it. No luck for board1.

- Attempt 4. Euclidean Distance
    Was worser than Euclidean distance. No luck for board 1.

- Attempt 5. Played around with each of the above heuristics with different weights. But no luck for board1

- Attempt 6. Now decided to play around with the cost function and used the adaptive cost approach and played around with the weights once again, did not change much when changed from 0.5 to 0.2 but got worse when 1.

Conclusion : Design

After multiple tries and errors went with 
Heuristic function : Manhattan distance
Cost : Adaptive cost



1. In this problem, what is the branching factor of the search tree?

    24, explained above in the Successor state section.


2. If the solution can be reached in 7 moves, about how many states would we need to explore before we found it if we
used BFS instead of A* search? A rough answer is fine.

    Around 24^7 states would have to explored in the worst case using BFS
