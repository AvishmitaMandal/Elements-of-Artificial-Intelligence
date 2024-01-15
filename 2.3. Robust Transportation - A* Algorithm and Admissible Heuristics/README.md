Robust Transportation - A-star and Heuristic Design

Data structure : Heap priority queue

Algorithm : Fringe path algorithm using Heap Queue

(1) Formulation of the search problem: 

State space : Travel from one city to other city

Initial state : Source city

Successor Function: Adjacent cities are the successor states.

Goal State: End city

Cost Function : The cost function is based on the given choice of cost such as segments, distance, time and delivery.
-	Segment Cost Function: A count is maintained for each city visited and increased by 1.
-	Distance Cost Function: Distance is calculated between cities using Euclidean formula
-	Time cost function: Time counter is maintained by calculating distance between two cities according to Euclidean formula divided by the maximum speed limit.
-	Delivery cost function: If the speed limit is greater than 50, given operation is performed for a certain driver else calculating euclidean distance between cities.

(2) How the program works?

A fringe which is a priority queue is maintained starting from the start city and the associated cost of it is maintained. Each time, the city with the least cost is pushed out and its adjacent cities are visited. Also, the cost of the associated cities is also calculated and added to the fringe. The city with the optimal cost is selected and this process is continued. This process is continued until the fringe becomes empty. If we reach the end city, the associated results and the path taken is returned. If the adjacent city is already visited, it is checked whether it can be visited with lesser cost and added to the fringe, else ignored.

(3) Problems Faced:

Attempt 1

Initially, tried to solve each cost function differently. Tried the bfs algorithm to find the shortest path for the segments function

Attempt 2

Then tried the uniform cost search algorithm to find the shortest path between start city and end city with the least distance.

Attempt 3

Finally, found a pattern between all the algorithms, and combined them into single data structure using heapq. The associated cost is calculated using the function return_cost and pushed into the queue. The city with the optimal cost is chosen and the adjacent cities are added to the fringe along with its associated costs.

Conclusion

Although the cost functions are different, the problem seems to have a high level coherence in the algorithm. Hence, a priority queue is used to push the city and its associated cost. The city with optimal cost is chosen and and the adjacent cities are visited and their costs are calculated and added to the fringe.

