# 1.2. Turrets placement using DFS Traversal

P-<#> : Problem-#1 (for example)\
R-<#> : Reason-#1 (for example)\
SA-<#> : Solution Approach-#1 (for example)\
ST : Solution Approach Taken

    Placing Turrets question

        PROBLEMS:
            P-1: The turrets were placed not according to the condition mentioned in the question. The turrets were placed in the same column and rows even though there was no wall - 'X' or '@'- destination.
            R-1: There seemed to be no validator in place which checks if the turrets placed satisfy the condition.
            ST:  Added a validator which checks if a turret can be placed first by traversing in 8 directions - up, down, right, left, north-east, north-west, south-east and south-west in DFS manner, untill we hit a 'p' and as long as we are in bounds of the map.

            P-2: It might have run into a situation where it wouldn't find any valid goal state when solution exists. 
            R-2: This is because there is no state which stores the previous valid state with n-1 turrets, where nth turret is being tried to be placed which can be used to backtrack.
            ST: Using fringe as a stack and when a state is explored and the successor function is called to explore the next states, the previous state is stored in case there is no solution through the current state and can be backtracked. (using a DFS approach)

        
        OBSERVATION:    
            If the graph is sparse - map has less number of 'X' and k is comparatively less, DFS would be a better approach, as there would be more probability of finding the solution in lesser time rather than a BFS approach.

            However, worst case is same for both
            Time complexity is O(b^m) -> b : branching factor , m : levels 
            Space complexity is O(1) -> No extra storage

        -----------------------------------------------------------------------------------------------------------------------------------------------------

        SEARCH ABSTRACTION ANALYSIS:

            Map Example :

            ....XXX
            .XXX...
            ....X..
            .X.X...
            .X.X.X.
            pX...X@

            STATE SPACE: 
                (Set of valid states) - The maps which are in the fringe stack yet to be explored with < = k turrets.
            
            INITIAL STATE: 
                The initial state is input given with 1 turret placed in the map.

            FINAL STATE: (GOAL STATE DEFINITION)
                The final state is the final map, which has k turrets.

            SUCCESSOR FUNCTION:
                The move function in the program responsible for exploring the adjacent nodes : Up, Down, Left, Right, North-East, North-West, South-East and South-West are the successor functions. Here the method : successor() 

            COST FUNCTION:
                The cost of moving from one cell to another is constant, lets assume 1. It takes 1 step to move between two adjacent cells.

-------------------------------------------------------------------------------------------------------------------------------------------------------------
