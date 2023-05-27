
import numpy, math, time

debugOn = False

board = numpy.zeros([6, 7])
playerChip = 'temp'
aiChip = 'temp'
firstMove = 'temp'
aiDepth = 0

def LoadGame():
    
    global board, playerChip, aiChip, firstMove, aiDepth
    
    print('Player Chip (r/y)', end=' ')
    playerChip = input()
    
    print('AI Chip (r/y)', end=' ')
    aiChip = input()
    
    print('First Move (p/a)', end=' ')
    firstMove = input()
    
    print('AI Depth? (2-4)', end=' ')
    aiDepth = int(input())
    
    board = numpy.zeros([6, 7])



def SetPos(r, c, chip):
    if chip == 'r':   board[r, c] = 1
    elif chip == 'y': board[r, c] = 2
    elif chip == 'e': board[r, c] = 0
    return board
    
def GetPos(r, c):
    if r < 0 or r > 5 or c < 0 or c > 6: return 'x'
    chip = board[r, c]
    if chip == 0:   return 'e'
    elif chip == 1: return 'r'
    elif chip == 2: return 'y'
    
def Drop(c, chip):
    r = 5
    while r >= 0:
        if GetPos(r, c) == 'e':
            board = SetPos(r, c, chip)
            return board
        r -= 1
    raise Exception('Column is full. Cannot drop chip.')

def AntiDrop(c):
    for r in range(6):
        if GetPos(r, c) != 'e':
            board = SetPos(r, c, 'e')
            return board
    raise Exception('Trying to remove chip from empty column.')

def GetAvailableColumns():
    arr = []
    for c in range(7):
        if GetPos(0, c) == 'e':
            arr.append(c)
    return arr

map = {0: '⬜', 1: '🔴', 2: '🟡'}

def VisualBoard():
    str = '\n'
    for r in range(6):
        for c in range(7):
            str += map[board[r, c]]
        str += '\n'
    print(str)



def minimax(isMaximising, depth):
    
    global board
    
    if debugOn: print('depth is ', depth)
    
    if(isMaximising):
        
        chip = aiChip
        bestScore = -math.inf
        
        options = GetAvailableColumns()
        if debugOn: print('maximising options are: ', options)
        for column in options:
            board = Drop(column, chip)
            if debugOn: print('depth is ', depth, ' & try drop in col ', column); VisualBoard()
            score = GetScore()
            if score == math.inf:
                bestScore = math.inf
                board = AntiDrop(column)
                if debugOn: print('pruned score (maximiser win)')
                break
            elif depth == 1:
                bestScore = max(bestScore, score)
            else:
                bestScore = max(bestScore, minimax(not isMaximising, depth - 1))
            board = AntiDrop(column)
            if debugOn: print('score = ', score, ', undo drop in col ',column); VisualBoard()
        
        if debugOn: print('maximising best score ', bestScore)
        return bestScore
        
    else:
        
        chip = playerChip
        bestScore = math.inf
        
        options = GetAvailableColumns()
        if debugOn: print('minimising options are: ', options)
        
        for column in options:
            board = Drop(column, chip)
            if debugOn: print('depth is ', depth, ' & try drop in col ',column); VisualBoard()
            score = GetScore()
            if score == -math.inf:
                bestScore = -math.inf
                board = AntiDrop(column)
                if debugOn: print('pruned score (minimiser win)')
                break
            elif depth == 1:
                bestScore = min(bestScore, score)
            else:
                bestScore = min(bestScore, minimax(not isMaximising, depth - 1))
            board = AntiDrop(column)
            if debugOn: print('score = ', score, ', undo drop in col ',column); VisualBoard()
        
        if debugOn: print('minimising best score ', bestScore)
        return bestScore
    
def GetBestMove(depth):
    
    global board
    
    bestScore = -math.inf
    bestMove = -1
    
    options = GetAvailableColumns()
    for column in options:
        board = Drop(column, aiChip)
        if debugOn: print('depth is ', depth, ' & try drop in col ',column); VisualBoard()
        score = GetScore()
        if score == math.inf:
            bestScore = math.inf
            bestMove = column
            board = AntiDrop(column)
            break
        elif depth == 1:
            if score >= bestScore:
                bestScore = score
                bestMove = column
        else:
            minimaxScore = minimax(False, depth - 1)
            if minimaxScore >= bestScore:
                bestScore = minimaxScore
                bestMove = column
        board = AntiDrop(column)
        if debugOn: print('score = ', score, ', undo drop in col ',column); VisualBoard()
    
    return bestMove        
        


dirList = numpy.array([[1, -1], [1, 0], [1, 1], [0, 1]])
chipScore = numpy.array([[0, 3, 5, math.inf], [1, 5, 30, math.inf], [3, 10, 60, math.inf]])

def GetScore():
    aiScore = ScoreCalculator(aiChip)
    playerScore = ScoreCalculator(playerChip)
    
    if aiScore == math.inf and playerScore == math.inf:
        raise Exception ('Simulataneous win and lose')
    elif aiScore == math.inf:
        return math.inf
    elif playerScore == math.inf:
        return -math.inf
    else:
        return aiScore - playerScore

def ScoreCalculator(chip):
    score = 0
    for r in range(6):
        for c in range (7):
            if GetPos(r, c) == chip:
                for dir in dirList:
                    openEnds = 0
                    backSpace = GetPos(r - dir[0], c - dir[1])
                    if backSpace != chip:
                        if backSpace == 'e':
                            openEnds += 1
                        it = 1
                        while it <= 3:
                            nextSpace = GetPos(r + it * dir[0], c + it * dir[1])
                            if nextSpace == 'e':
                                #print(chipScore[openEnds + 1][it - 1])
                                score += chipScore[openEnds + 1][it - 1]
                                break
                            elif nextSpace != chip:
                                #print(chipScore[openEnds][it - 1])
                                score += chipScore[openEnds][it - 1]
                                break
                            elif it == 3:
                                #print(chipScore[0][it])
                                score += chipScore[0][it]
                            it += 1
    return score

def CheckWin():
    testScore = GetScore()
    if testScore == math.inf:
        print('AI wins!\n')
        return True
    elif testScore == -math.inf:
        print('Human wins!\n')
        return True
    return False





def RunGame():
    print(board)
    VisualBoard()
    if firstMove == 'a':
        AIMove()
    while True:
        PlayerMove()
        if CheckWin(): break
        AIMove()
        if CheckWin(): break
        
def AIMove():
    global board
    selection = GetBestMove(aiDepth)
    print('Robot chooses column', selection)
    board = Drop(selection, aiChip)
    VisualBoard()

def PlayerMove():
    global board
    print('Player chooses column', end=' ')
    colToDropIn = int(input())
    board = Drop(colToDropIn, playerChip)
    VisualBoard()
    time.sleep(1)

while True:
    LoadGame()
    RunGame()
    print('Play again? (y/n)', end=' ')
    if input() != 'y':
        break