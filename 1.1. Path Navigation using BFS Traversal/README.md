P-<#> : Problem-#1 (for example)\
R-<#> : Reason-#1 (for example)\
SA-<#> : Solution Approach-#1 (for example)\
ST : Solution Approach Taken

PART-1 :

    Magical Castle Question:

        PROBLEMS:
            P-1.  The program when run would always end up with an infinite loop.
            R-1.  Once a particular cell is explored, there is no track of if its adjacent nodes were explored.
                  The cells would be explored repeatatively and would run into an infinite loop.
            SA-1. Either store the cells in memory and lookup if the cell was visited earlier.
            SA-2. Mark the cells visited as some other string like 'c'. So after exploration '.' -> 'c'.
            ST.   SA-2 : Marked the visited cells as 'c' instead of '.'.
                  Also updated the category for whitelisted features of legal cells from '.@' -> '.@c'

        OPTIMISATIONS:
            P-1. The program did not return the best solution necessarily. Just gave a good path.
            R-1. The program used fringe as a stack, so the adjacent cells of the last cell that has been explored, will be the next to be visited.
                 This is a DFS approach and will not guarantee a shortest path.
            ST.  Optimal solution will be guaranteed if the exploration happens level by level.
                 It will directly return the first path it finds which will be the shortest path (BFS approach)
                 Changed the fringe from stack to queue.

        OTHER CHANGES:
            1. Added the strings "U", "L", "R" and "D" for when the movement is Up, Left, Right and Down. 
                1.1. And making sure to store the sequence of these string which indicates the path.
            2. Handled corner case when there is no path to return -1 and the path as an empty string 

        OBSERVATIONS:
            1. When changed the program to use a BFS approach rather than DFS approach, the program execution time increased.
                1.1. This indicates that DFS -> good path -> in average it might give the solution faster.
                1.2. BFS -> best path -> will always take the same amount of time for a given case. 
            
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
                (Set of valid states) - The cells in the maps (blocked - represented using 'X' or open - '.') is the state space.
            
            INITIAL STATE: 
                The initial state is the starting cell which is indicated using 'p'.

            FINAL STATE: (GOAL STATE DEFINITION)
                The final state is destination cell indicated using '@'.

            SUCCESSOR FUNCTION:
                The move function in the program responsible for exploring the adjacent nodes : Up, Down, Left and Right are the successor functions.
                Here the method move().

            COST FUNCTION:
                The cost of moving from one cell to another is constant, lets assume 1. It takes 1 step to move between two adjacent cells.

