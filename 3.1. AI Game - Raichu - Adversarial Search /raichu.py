#Assignment 2
#raichu.py
# avmandal- Avishmita Mandal
# ysampath- Yashaswini Sampath Kumar

from operator import ne
import sys
from copy import  deepcopy
from timeit import default_timer

#function checks if the player is inside the board
def checkBoardPosition(row,col,N):
    return 0 <= row < N and 0 <= col < N

#Converts board to string
def ConvertBoardToString(board, N):
    return "\n".join(board[i:i+N] for i in range(0, len(board), N))

#Converts Matrix to String
def ConvertMatrixToString(board):
    board_str = ''.join(list(map(''.join, board)))
    return board_str
    
#Converts string to matrix
def ConvertStringToMatrix(boardStr,N):
    StringInput = list(boardStr)
    board = [StringInput[i:i+N] for i in range(0,len(StringInput),N)]
    return board

#Get all valid moves for Pichu
#pichu can move in 4 possible directions
def getValidPichuMoves(board, row, col,currentPlayer,N):
    #list to store all possible combination of moves
    AllPossibleMoves = []
    newBoardCopy = deepcopy(board)
    
    #define the current player and possible moves for them depending on the player
    if currentPlayer == 'w':
        SingleStepMoves = [(1, -1), (1, 1)]
        DoubleStepMoves = [(1,-1, 2, -2), (1,1,2,2)]
        CaptureElement = 'b'
        rowLimit = len(board) - 1
    else:
        SingleStepMoves = [(-1, -1), (-1, 1)]
        DoubleStepMoves= [(-1,-1,-2, -2), (-1,1,-2, 2)]
        CaptureElement = 'w'
        rowLimit = 0

    #1 sq jump
    for i in range(2):
        (dr,dc)=SingleStepMoves[i]
        new_r = row + dr
        new_c = col + dc
        newBoardCopy = deepcopy(board)
        if checkBoardPosition(new_r,new_c,N):
            if newBoardCopy[new_r][new_c] == '.':
                newBoardCopy[new_r][new_c] = newBoardCopy[row][col]
                newBoardCopy[row][col] = '.'
                if new_r == rowLimit:
                    newBoardCopy = TransformToRaichu(newBoardCopy)
                AllPossibleMoves.append(ConvertMatrixToString(newBoardCopy))

    #2 sq jump
    for i in range(2):
        (dr1,dc1,dr,dc)=DoubleStepMoves[i]
        r1 = row + dr1
        c1 = col + dc1
        new_r = row + dr
        new_c = col + dc
        newBoardCopy = deepcopy(board)
        if checkBoardPosition(new_r,new_c,N):
            if newBoardCopy[r1][c1] == CaptureElement and newBoardCopy[new_r][new_c] == '.':
                newBoardCopy[new_r][new_c] = newBoardCopy[row][col]
                newBoardCopy[row][col] = '.'
                newBoardCopy[r1][c1] = '.'
                if new_r == rowLimit:
                    newBoardCopy = TransformToRaichu(newBoardCopy)
                AllPossibleMoves.append(ConvertMatrixToString(newBoardCopy))
    return AllPossibleMoves

#pikachu moves
#pikachu can move in total of 12 possible moves
def getValidPickachuMoves(board, row, col,currentPlayer,N):
    AllPossibleMoves  = []
    if currentPlayer == 'w':
        #list all possible direction and steps taken by white Pikachu
        directionSteps = [(0,-1),(0,1),(1,0),(0,-1,0,-2),(0,1,0,2),(1,0,2,0),(0,-1,0,-2,0,-3),(0,1,0,2,0,3),(1,0,2,0,3,0)]
        #capturable elements by white Pikachu
        opponentPlayers = ['b','B']
        rowLimit = N - 1
    else:
        #list all possible direction and steps taken by black Pikachu
        directionSteps = [(0,-1),(0,1),(-1,0),(0,-1,0,-2),(0,1,0,2),(-1,0,-2,0),(0,-1,0,-2,0,-3),(0,1,0,2,0,3),(-1,0,-2,0,-3,0)]
        #capturable elements by black Pikachu
        opponentPlayers = ['w','W']
        rowLimit = 0

    for i in range(9):
        if i < 3: # 1 sq step left,right,forward
            dr,dc = directionSteps[i]
            newRow = row + dr
            newCol = col + dc
            #print(possibleMoves[i])
            NewboardCopy = deepcopy(board)
            if (checkBoardPosition(newRow,newCol,N) and NewboardCopy[newRow][newCol]=='.'):
                #NewboardCopy = deepcopy(board)
                NewboardCopy[newRow][newCol] = NewboardCopy[row][col]
                NewboardCopy[row][col] = '.'
                if(newRow==rowLimit):
                    NewboardCopy = TransformToRaichu(NewboardCopy)
                AllPossibleMoves.append(ConvertMatrixToString(NewboardCopy))

        if i >= 3 and i < 6 : # 2 sq step left,right,forward
            pr1,pc1,dr,dc = directionSteps[i]
            newRow = row + dr
            newCol = col + dc
            prevRow = row + pr1
            prevCol = col + pc1
            NewboardCopy = deepcopy(board)

            # 2 sq jump with no capture
            if (checkBoardPosition(newRow,newCol,N) and NewboardCopy[newRow][newCol]=='.' and NewboardCopy[prevRow][prevCol]=='.'):
                #NewboardCopy = deepcopy(board)
                NewboardCopy[newRow][newCol] = NewboardCopy[row][col]
                NewboardCopy[row][col] = '.'
                if(newRow==rowLimit ):
                    NewboardCopy = TransformToRaichu(NewboardCopy)
                AllPossibleMoves.append(ConvertMatrixToString(NewboardCopy))

            NewboardCopy = deepcopy(board)
            # 2 sq (2 sq jump with 1 capture in step 1)
            if (checkBoardPosition(newRow,newCol,N) and NewboardCopy[newRow][newCol]=='.' and NewboardCopy[prevRow][prevCol] in opponentPlayers):
                #NewboardCopy = deepcopy(board)
                NewboardCopy[newRow][newCol] = NewboardCopy[row][col]
                NewboardCopy[prevRow][prevCol] = '.'
                NewboardCopy[row][col] = '.'
                if(newRow==rowLimit):
                    NewboardCopy = TransformToRaichu(NewboardCopy)
                AllPossibleMoves.append(ConvertMatrixToString(NewboardCopy))

        if i >= 6 and i < 9 : #2 square jump with capture
            pr1,pc1,pr2,pc2,dr,dc= directionSteps[i]
            newRow = row + dr
            newCol = col + dc
            prevRow = row + pr1
            prevCol = col + pc1
            prev1Row, prev1Col = row+pr2,col+pc2
            NewboardCopy = deepcopy(board)
            if(checkBoardPosition(newRow,newCol,N) and NewboardCopy[prev1Row][prev1Col] in opponentPlayers and
                NewboardCopy[prevRow][prevCol]=='.' and NewboardCopy[newRow][newCol]=='.'):
                NewboardCopy[newRow][newCol] = NewboardCopy[row][col]
                NewboardCopy[prev1Row][prev1Col] = '.'
                NewboardCopy[prevRow][prevCol] = '.'
                NewboardCopy[row][col] = '.'
                if(newRow==rowLimit):
                    NewboardCopy = TransformToRaichu(NewboardCopy)
                AllPossibleMoves.append(ConvertMatrixToString(NewboardCopy))
    return AllPossibleMoves

def TransformToRaichu(board):
    #check 1st row if black player has reached
    for i in range(len(board[0])):
        if board[0][i] in ('b', 'B'):
            board[0][i] = '$'
    #check last row if the white player has reached
    for i in range(len(board[-1])):
        if board[-1][i] in ('w', 'W'):
            board[-1][i] = '@'
    return board

#check for player in board
def check_row_col(board, row, col):
    return 0 <= row < len(board) and 0 <= col < len(board[0])

#Define raichu moves who can travel in all 8 directions
def getValidRaichuMoves(board,r,c):
    AllPossibleMoves = []
    if(board[r][c]=='$'):
        ownPlayers = set(['b','B','$'])
        opponentPlayers = set(['w','W','@'])
    if(board[r][c]=='@'):
        ownPlayers = set(['w','W','@'])
        opponentPlayers = set(['b','B','$'])

    #upward direction movement
    row = deepcopy(r)-1
    board1 = deepcopy(board)
    encounteredElementbeforeR = []
    capturedElementBeforeR = True
    while(row>=0):
        if(bool(ownPlayers & set(encounteredElementbeforeR))==False):
            new_board = deepcopy(board1)
            boardUpdated = 0
            temp=0
            if(capturedElementBeforeR==False and new_board[row][c]!='.'):
                break
            if(new_board[row][c]=='.'):
                new_board[row][c] = new_board[r][c]
                new_board[r][c] = '.'
                boardUpdated = 1
            if(check_row_col(new_board,row-1,c) and new_board[row][c] in opponentPlayers and new_board[row-1][c]!='.'):
                break
            if(capturedElementBeforeR and check_row_col(new_board,row-1,c) and new_board[row][c] in opponentPlayers and new_board[row-1][c]=='.'):
                new_board[row][c] = '.'
                board1[row][c] = '.'
                new_board[row-1][c] = new_board[r][c]
                new_board[r][c] = '.' 
                capturedElementBeforeR = False
                boardUpdated = 1
                temp+=1
            if(boardUpdated==1):
                AllPossibleMoves.append(ConvertMatrixToString(new_board))
            encounteredElementbeforeR.append(board1[row][c])
            capturedElementBeforeR = False
        row-=1
        row-=temp

    #downward direction movement
    row = deepcopy(r)+1
    board2 = deepcopy(board)
    encounteredElementAfterR = []
    capturedElementAfterR = True
    while(row<len(board)):
        if(bool(ownPlayers & set(encounteredElementAfterR))==False):
            new_board = deepcopy(board2)
            boardUpdated = 0
            temp=0
            #once element is captured, we break out of loop
            if(capturedElementAfterR==False and new_board[row][c]!='.'):
                break
            if(new_board[row][c]=='.'):
                new_board[row][c] = new_board[r][c]
                new_board[r][c] = '.'
                boardUpdated = 1
            if(check_row_col(new_board,row+1,c) and new_board[row][c] in opponentPlayers and new_board[row+1][c]!='.'):
                break
            if(capturedElementAfterR and check_row_col(new_board,row+1,c) and new_board[row][c] in opponentPlayers and new_board[row+1][c]=='.'):
                new_board[row][c] = '.'
                board2[row][c] = '.'
                new_board[row+1][c] = new_board[r][c]
                new_board[r][c] = '.' 
                capturedElementAfterR = False
                boardUpdated = 1
                temp+=1
            if(boardUpdated==1):
                AllPossibleMoves.append(ConvertMatrixToString(new_board))
            encounteredElementAfterR.append(board2[row][c])
        row+=1
        row+=temp

    # left horizontal movement
    col = deepcopy(c)-1
    board1 = deepcopy(board)
    encounteredElementBeforeC = []
    capturedElementBeforeC = True
    while(col>=0):
        if(bool(ownPlayers & set(encounteredElementBeforeC))==False):
            new_board = deepcopy(board1)
            boardUpdated = 0
            temp=0
            if(capturedElementBeforeC==False and new_board[r][col]!='.'):
                break
            if(new_board[r][col]=='.'):
                new_board[r][col] = new_board[r][c]
                new_board[r][c] = '.'
                boardUpdated=1
            if(check_row_col(new_board,r,col-1) and new_board[r][col] in opponentPlayers and new_board[r][col-1]!='.'):
                break
            if(capturedElementBeforeC and check_row_col(new_board,r,col-1) and new_board[r][col] in opponentPlayers and new_board[r][col-1]=='.'):
                new_board[r][col] = '.'
                board1[r][col] = '.'
                new_board[r][col-1] = new_board[r][c]
                new_board[r][c] = '.' 
                temp+=1
                capturedElement = False
                boardUpdated=1
            if(boardUpdated==1):
                AllPossibleMoves.append(ConvertMatrixToString(new_board))
            encounteredElementBeforeC.append(board1[r][col])
            capturedElementBeforeC = False
        col-=1
        col-=temp
        
    #right horizontal movement 
    col = deepcopy(c)+1
    board2 = deepcopy(board)
    encounteredElementAfterC = []
    capturedElementAfterC = True
    while(col<len(board[0])):
        if(bool(ownPlayers & set(encounteredElementAfterC))==False):
            new_board = deepcopy(board2)
            boardUpdated = 0
            temp = 0
            if(capturedElementAfterC==False and new_board[r][col]!='.'):
                break
            if(new_board[r][col]=='.'):
                new_board[r][col] = new_board[r][c]
                new_board[r][c] = '.'
                boardUpdated=1
            if(check_row_col(new_board,r,col+1) and new_board[r][col] in opponentPlayers and new_board[r][col+1]!='.'):
                break
            if(capturedElementAfterC and check_row_col(new_board,r,col+1) and new_board[r][col] in opponentPlayers and new_board[r][col+1]=='.'):
                new_board[r][col] = '.'
                board2[r][col] = '.'
                new_board[r][col+1] = new_board[r][c]
                new_board[r][c] = '.'
                temp+=1 
                capturedElementAfterC = False
                boardUpdated=1
            if(boardUpdated==1):
                AllPossibleMoves.append(ConvertMatrixToString(new_board))
            encounteredElementAfterC.append(board2[r][col])
        col+=1
        col+=temp
    
    # Left diagonal top movement
    row = deepcopy(r)-1
    col = deepcopy(c)-1
    board1 = deepcopy(board)
    jumped = True
    PreviousDiagonalElement = []
    while(row>=0 and col>=0):
        new_board = deepcopy(board1)
        if(bool(ownPlayers & set(PreviousDiagonalElement))==False):
            boardUpdated = 0
            temp = 0
            if(jumped==False and new_board[row][col]!='.'):
                break
            if(new_board[row][col]=='.'):
                new_board[row][col] = new_board[r][c]
                new_board[r][c] = '.'
                boardUpdated = 1
            if(jumped and row-1>=0 and col-1>=0 and new_board[row][col] in opponentPlayers and new_board[row-1][col-1]=='.'):
                new_board[row][col] = '.'
                board1[row][col] = '.'
                new_board[row-1][col-1] = new_board[r][c]
                new_board[r][c] = '.' 
                jumped = False
                temp+=1
                boardUpdated = 1
            if(boardUpdated==1):
                AllPossibleMoves.append(ConvertMatrixToString(new_board))
        PreviousDiagonalElement.append(board1[row][col])
        row-=1
        row-=temp
        col-=1
        col-=temp

    # Left diagonla bottom movement
    row = deepcopy(r)+1
    col = deepcopy(c)-1
    board1 = deepcopy(board)
    jumped = True
    PreviousDiagonalElement = []
    while(row<len(board) and col>=0):
        new_board = deepcopy(board1)
        if(bool(ownPlayers & set(PreviousDiagonalElement))==False):
            boardUpdated = 0
            temp = 0
            if(jumped==False and new_board[row][col]!='.'):
                break
            if(new_board[row][col]=='.'):
                new_board[row][col] = new_board[r][c]
                new_board[r][c] = '.'
                boardUpdated = 1
            if(jumped and row+1<=len(board)-1 and col-1>=0 and new_board[row][col] in opponentPlayers and new_board[row+1][col-1]=='.'):
                new_board[row][col] = '.'
                board1[row][col] = '.'
                new_board[row+1][col-1] = new_board[r][c]
                new_board[r][c] = '.' 
                jumped = False
                boardUpdated = 1
                temp+=1
            if(boardUpdated==1):
                AllPossibleMoves.append(ConvertMatrixToString(new_board))
        PreviousDiagonalElement.append(board1[row][col])
        row+=1
        row+=temp
        col-=1
        col-=temp

    # Right diagonal top movement
    row = deepcopy(r)-1
    col = deepcopy(c)+1
    board1 = deepcopy(board)
    jumped = True
    PreviousDiagonalElement = []
    while(row>=0 and col<len(board[0])):
        new_board = deepcopy(board1)
        if(bool(ownPlayers & set(PreviousDiagonalElement))==False):
            boardUpdated = 0
            temp = 0
            if(jumped==False and new_board[row][col]!='.'):
                break
            if(new_board[row][col]=='.'):
                new_board[row][col] = new_board[r][c]
                new_board[r][c] = '.'
                boardUpdated = 1
            if(jumped and row-1>=0 and col+1<=len(board[0])-1 and new_board[row][col] in opponentPlayers and new_board[row-1][col+1]=='.'):
                new_board[row][col] = '.'
                board1[row][col] = '.'
                new_board[row-1][col+1] = new_board[r][c]
                new_board[r][c] = '.' 
                jumped = False
                temp+=1
                boardUpdated = 1
            if(boardUpdated==1):
                AllPossibleMoves.append(ConvertMatrixToString(new_board))
        PreviousDiagonalElement.append(board1[row][col])
        row-=1
        row-=temp
        col+=1
        col+=temp

    # Right diagonal bottom movement
    row = deepcopy(r)+1
    col = deepcopy(c)+1
    board1 = deepcopy(board)
    PreviousDiagonalElement = []
    while(row<len(board) and col<len(board[0])):
        new_board = deepcopy(board1)
        if(bool(ownPlayers & set(PreviousDiagonalElement))==False):
            boardUpdated = 0
            temp = 0
            if(jumped==False and new_board[row][col]!='.'):
                break
            if(new_board[row][col]=='.'):
                new_board[row][col] = new_board[r][c]
                new_board[r][c] = '.'
                boardUpdated = 1
            if(jumped and row+1<=len(board)-1 and col+1<=len(board[0])-1 and new_board[row][col] in opponentPlayers and new_board[row+1][col+1]=='.'):
                new_board[row][col] = '.'
                board1[row][col] = '.'
                new_board[row+1][col+1] = new_board[r][c]
                new_board[r][c] = '.' 
                jumped = False
                boardUpdated = 1
                temp+=1
            if(boardUpdated==1):
                AllPossibleMoves.append(ConvertMatrixToString(new_board))
        PreviousDiagonalElement.append(board1[row][col])
        row+=1
        row+=temp
        col+=1
        col+=temp
    #return all possible moves for raichu
    return AllPossibleMoves

#Successor function that generates all possible moves of a given player
def generateAllPossibleSuccessors(board,N,r,c,player):
    element = board[r][c]
    if element in 'wb':
        return getValidPichuMoves(board, r, c,player,N)
    elif element in 'WB':
        return getValidPickachuMoves(board,r,c,player,N)
    elif element in '@$':
        return getValidRaichuMoves(board,r,c)

#To check if a given player has won    
def check_win(board,N,player): 
    boardList = list(board)
    opponent_pieces = set(["b", "B", "$"]) if player == "w" else set(["w", "W", "@"])

    for j in boardList:
        if j in opponent_pieces:
            return False
    return True 

def evaluateFunction(board, N, player):
    #variables to capture count of each player
    ownPichuCount,ownPikachuCount,ownRaichuCount,currDist = 0,0,0,0
    oppPichuCount,oppPikachuCount,oppRaichuCount,oppDist= 0,0,0,0

    #define set of pieces for each player
    ownPichu, ownPikachu, ownRaichu = ('w', 'W', '@') if player == 'w' else ('b', 'B', '$')
    oppPichu, oppPikachu, oppRaichu = ('b', 'B', '$') if player == 'w' else ('w', 'W', '@')

    boardArr = list(board)

    #count distance and count of each player pieces
    for i in range(len(boardArr)):
        if boardArr[i] == ownPichu:
            ownPichuCount += 1
            if player == 'w':
                currDist += (N - (i // N) - 1)
            else:
                currDist += (i // N)
        if boardArr[i] == ownPikachu:
            ownPikachuCount += 1
            if player == 'w':
                currDist += (N - (i // N) - 1 / 2)
            else:
                currDist += ((i // N) / 2)
        if boardArr[i] == ownRaichu:
            ownRaichuCount += 1
        if boardArr[i] == oppPichu:
            oppPichuCount += 1
            if player == 'b':
                oppDist += (i // N)
            else:
                oppDist += (N - (i // N) - 1)
        if boardArr[i] == oppPikachu:
            oppPikachuCount += 1
            if player == 'b':
                oppDist += ((i // N) / 2)
            else:
                oppDist += (N - (i // N) - 1 / 2)
        if boardArr[i] == oppRaichu:
            oppRaichuCount += 1

    #if there are no more own players score is negative
    if ownPichuCount + ownPikachuCount + ownRaichuCount == 0:
        return -sys.maxsize
    #if there are 0 opponent player,winning probabilty is the highest
    if oppPichuCount + oppPikachuCount + oppRaichuCount == 0:
        return sys.maxsize

    #calculate score based on the diff between one of playuers in each team
    result = (10 * (ownPichuCount - oppPichuCount) + (20 * (ownPikachuCount - oppPikachuCount)) +
              (100 * (ownRaichuCount - oppRaichuCount)) - ((currDist * (ownPichuCount + ownPikachuCount) // N) -
                                                  (oppDist * (oppPichuCount + oppPikachuCount) // N)))

    return result

#function to validate if provided input is right
def validateInputArguments(args):
    N = int(sys.argv[1])
    currentPlayer = sys.argv[2]
    boardState = sys.argv[3]
    timelimit = int(sys.argv[4])

    try:
        N = int(N)
        timelimit = int(timelimit)
    except ValueError:
        raise Exception("N and timelimit must be integers.")

    #current player should be in pichu,picahu and raichu
    if currentPlayer not in "wbWB":
        raise Exception("Invalid player,player should ve w,b,W,B.")

    #checking for the input board string lenght to be in size of N*N and only given characters
    if len(boardState) != N * N or any(c not in "wb.WB@$" for c in boardState):
        raise Exception("Bad input board string.")

    return N, currentPlayer, boardState, timelimit

#minmax function
def minimax(board,N,gameTreedepth,alpha,beta,CurrentPlayer,limit,initial):
    return max_val(board,N,gameTreedepth,alpha,beta,CurrentPlayer,limit,initial)

#maxvalue function 
def max_val(board,N,gameTreedepth,alpha,beta,CurrentPlayer,limit,initial):
    ownPlayer = ['w', 'W', '@'] if CurrentPlayer == 'w' else ['b', 'B', '$']
    oppositePlayer = 'b' if CurrentPlayer == 'w' else 'w'

    #check if it reached max depth or win position
    if(gameTreedepth==0 or check_win(board,N,CurrentPlayer) or (default_timer() - initial) > limit):
        return board,evaluateFunction(board,N,CurrentPlayer)
    
    finalBoard = board
    board = ConvertStringToMatrix(board,N)
    maxEvalFunValue = float("-inf")

    for i in range(N):
        for j in range(N):
            if(board[i][j] in ownPlayer):
                SequenceList = list(filter(lambda x: x!=None, generateAllPossibleSuccessors(board,N,i,j,CurrentPlayer)))
                evaluations = list(map(lambda x: evaluateFunction(x,N,CurrentPlayer),SequenceList))
                combinedList = list(zip(SequenceList,evaluations))
                combinedList.sort(key=lambda x: x[1],reverse=True)
                for successor,_ in combinedList:
                    _,eval = min_val(successor,N,gameTreedepth-1,alpha,beta,oppositePlayer,limit,initial)
                    if(eval>maxEvalFunValue):
                        finalBoard,maxEvalFunValue = successor,eval
                    if(maxEvalFunValue>alpha):
                        alpha = maxEvalFunValue
                    if(beta<=alpha):
                        return finalBoard,maxEvalFunValue

    return finalBoard,maxEvalFunValue

#min value function in tree
def min_val(board,N,gameTreedepth,alpha,beta,CurrentPlayer,limit,initial):
    ownPlayer = ['w', 'W', '@'] if CurrentPlayer == 'w' else ['b', 'B', '$']
    oppositePlayer = 'b' if CurrentPlayer == 'w' else 'w'

    #check if it reached max depth or win position
    if(gameTreedepth==0 or check_win(board,N,oppositePlayer) or (default_timer() - initial) > limit):
        return board,evaluateFunction(board,N,oppositePlayer)
    
    finalBoard = board
    board = ConvertStringToMatrix(board,N)
    minEvalFunValue = float("inf")
    
    for i in range(N):
        for j in range(N):
            if(board[i][j] in ownPlayer):
                SequenceList = list(filter(lambda x: x!=None, generateAllPossibleSuccessors(board,N,i,j,CurrentPlayer)))
                evaluations = list(map(lambda x: evaluateFunction(x,N,CurrentPlayer),SequenceList))
                combinedList = list(zip(SequenceList,evaluations))
                combinedList.sort(key=lambda x: x[1])
                for successor,_ in combinedList:
                    _,eval = max_val(successor,N,gameTreedepth-1,alpha,beta,oppositePlayer,limit,initial)
                    if(eval<minEvalFunValue):
                        finalBoard,minEvalFunValue = successor,eval
                    if(minEvalFunValue<beta):
                        beta = minEvalFunValue
                    if(beta<=alpha):
                        return finalBoard,minEvalFunValue

    return finalBoard,minEvalFunValue

def findNextBestRecommendedMove(board, N, player, timelimit):
    #define depth of tree
    gameTreedepth = 4
    #set initial time
    istartTime = default_timer()
    limit = timelimit - 1
    #set alpha beta values for minmax tree pruning
    alpha ,beta = -999999,999999
    #call minmax
    Recommendedboard,_ = minimax(board,N,gameTreedepth,alpha,beta,player,limit,istartTime)
    yield Recommendedboard

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python3 raichu.py <n> <current_player> <board_state> <time_limit>")
        sys.exit(1)

    N, currentPlayer, board, timelimit = validateInputArguments(sys.argv)

    print("Searching for best move for " + currentPlayer +
          " from board state: \n" + ConvertBoardToString(board, N))
    print("Here's what I decided:")
    for new_board in findNextBestRecommendedMove(board, N, currentPlayer, timelimit):
        print(new_board)


