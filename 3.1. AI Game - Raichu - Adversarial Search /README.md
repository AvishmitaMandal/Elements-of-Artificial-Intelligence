# 3.1. AI Game - Raichu - Adversarial Search

1.  **Initial State:** The initial state of the board is given as an N*N matrix which represents the size of the board, the game consists of 3 types of players(Pichu, Pikachu and Raichu), and has 2 players white and black. At any given point in time, there is exactly one player who is currently playing.
2.  **Goal State:** The Goal state will be to make a move to maximize the win of the current player.
3.  **Successor Function:** Here the successor function is the list of possible moves for a player piece, like suppose for Pichu we can have 4 possible moves and Richu can have 8 possible moves in each direction.
4.  **Cost Function:** As a part of Evaluation function we have calculated the cost function as explained below in detail. (Based on the number of players in own team and the opponent team)

###  (1) a description of how you formulated each problem;

The game has 3 main players with defined moves and capabilities as below:
1. **Pichu** - 'w','b'. they can move diagonally forward in both directions(left and right) taking 1 or 2 steps. total no of possible moves = 4
2. **Pikachu** - 'W', 'B' they can move right, left and forward in both directions in 1 or 2 steps, total possible moves = 9(1 step right,1 step left,1 step forward,2 steps right,2 steps left,2 steps forward, 2 steps right with capture,2 steps left with capture,2 steps forward with capture).
it can capture a Pichu or Pikachu
3. **Raichu** - more like a superpower player who can move all 8 directions in any no of steps and can capture a Pichu, Pikachu or Raichu

For the player, a white and black set of players can be defined as :
white = ['w','W','@']
Black = ['b','B','$']

Main Tasks we will have to address:
1. Moves for each player
2. Minmax search tree which will help us find the best next move
3. Evaluation function to determine which is the best move
4. function to test the player is within the board(has valid moves and position)

Details:
Task 1: Moves for each player: here we will describe the possible moves for the player pieces, and list all possible moves for the player based on the current player white if the current player is -> w else black.
Task 2: Create a min-max algorithm, to calculate the min value based on the alpha-beta pruning and out of the search tree consider the best move.
Task 3: The evaluation function here returns a value for a given placement of board and with respect to the current player on how good/efficient the move is. we consider the number of players in their own team, opp team and how far it is in becoming a Raichu(reaching the end)
for our evaluation function, we have considered 3 parts:
    a. the no of players in one own team and opp team and each player piece has a weight associated with it 
    Pichu - > 10, Pikachu->30, and Raichu ->80 (these are decided on based their power to move around the board)
    b. if there are no players from the own team, it indicates a high losing probability and hence returns a very high negative value
    c. last it calculates the no of pieces of each type of player and the distance of a piece from its position to the end of the board(this indicates the averaged value to becoming a Raichu which is a superpower player)
Task 4: Supporting functions to handle corner tcs and check boundaries, print and converting board to string functions

how the min-max tree works:
The Minimax tree with alpha-beta pruning is a technique used in two-player, zero-sum games to determine the best move for a player. It involves building a game tree that represents all possible moves and outcomes, with alternating "max" and "min" players. At each level, the "max" player aims to maximize the score, while the "min" player tries to minimize it. Terminal nodes are evaluated using a heuristic function. The algorithm backpropagates scores and uses alpha-beta pruning to reduce unnecessary node evaluations. This technique efficiently finds optimal moves by minimizing search space and approximating optimal play in games like chess and checkers.
### (2) a brief description of how your program works; 
0. validate input arguments() checks if the provided input is in the correct format

1. The program findNextBestRecommendedMove calls the minimax tree, starting with a max node for the current player, alpha and beta values are set to possible worst negative and positive values, and updated later. this algorithm is called recursively each time for minplayer and maxplayer until we either
    case 1: reach the maxSearchTreeDepth we have defined 
    case 2: The player has won
    case 3: or we have run out of time

2. For each iteration at the last terminal node the evaluation function is called for each successor state:
    a. generateAllPossibleSuccessors defines functions getValidPichuMoves,getValidPikachuMoves and getValidRaichuMoves which define all possible moves for the player piece. In each of these functions, we have AllPossibleMoves list which captures the list of the possible placement of the board recommended and defines the player pieces and opponent pieced and returns AllPossibleMoves
    b. evaluateFunction method returns a value based on no of players in the own team and the opponent team, taking into consideration the board placement of the player to the end of the opposing side of the board which indicates how close it is to becoming a Raichu.

3. The algorithm tries to find the optimal solution that maximizes the player's chances of winning and returns the recommended move.

### (3) and discussion of any problems you faced, any assumptions, simplifications, and/or design decisions you made.

1. Assumption: The weight of each player piece Pichu, Pikachu, and Raichu respectively have weights of 10,20,100
2. Challenges:
    2.1. Formulation and defining the moves of each player, the steps were complicated as they needed to be defined for both players(i.e. black and white) the white pieces moved in direction 1 and black direction -1.
    2.2. defining the evaluation function the heuristics needed to be complex enough to determine which is the best possible move, initially we had just 1 heuristic which calculated the no of players on their own and the opposite team but the case will not help serve a good purpose if the move did not include any capture of the opponent piece.

References: 
1. https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-4-alpha-beta-pruning/
2. https://youtu.be/CZZrW54Yd0g?si=OWRBMiotakbI3NeR




