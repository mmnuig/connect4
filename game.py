
import numpy, math, time, json, img_proc, webcam

debugOn = False

board = numpy.zeros([6, 7])
playerChip = "temp"
aiChip = "temp"
firstMove = "temp"
aiDepth = 0
pause = 0


def LoadGame(): 
    
    jsFile = open("config.json", "r")
    jsData = json.load(jsFile)
    jsFile.close()
    
    global playerChip, aiChip, firstMove, aiDepth, pause

    playerChip = jsData["Player Chip"]
    aiChip = jsData["AI Chip"]
    firstMove = jsData["First Move"]
    aiDepth = jsData["AI Depth"]
    pause = jsData["AI Pause Length"]
    
    jsData.clear()
    
    #board = numpy.zeros([6, 7])
    
    n = 0
    while n < 3:
        time.sleep(0.5)
        if numpy.array_equal(board, CreateBoardArray()):
            n += 1
        else:
            VisualBoard(CreateBoardArray())
            print("Board not blank")
            n = 0

    print("Game Loaded")

def CreateBoardArray():
    img = webcam.Image()
    newBoard = numpy.zeros([6, 7])
    for r in range(6):
        for c in range(7):
            chip = img_proc.GetTileType(img, r, c)
            SetPos(r, c, chip, newBoard)
    return newBoard



def SetPos(r, c, chip, boardChoice = board):
    if chip == 'r':   boardChoice[r, c] = 1
    elif chip == 'y': boardChoice[r, c] = 10
    elif chip == 'e': boardChoice[r, c] = 0
    
def GetPos(r, c):
    if r < 0 or r > 5 or c < 0 or c > 6: return 'x'
    chip = board[r, c]
    if chip == 0:    return 'e'
    elif chip == 1:  return 'r'
    elif chip == 10: return 'y'
    
def Drop(c, chip):
    r = 5
    while r >= 0:
        if GetPos(r, c) == 'e':
            SetPos(r, c, chip)
            return
        r -= 1
    raise Exception("Column is full. Cannot drop chip.")

def AntiDrop(c):
    for r in range(6):
        if GetPos(r, c) != 'e':
            SetPos(r, c, 'e')
            return
    raise Exception("Trying to remove chip from empty column.")

def GetAvailableColumns():
    arr = []
    for c in range(7):
        if GetPos(0, c) == 'e':
            arr.append(c)
    return arr



def minimax(isMaximising, depth):
    
    if debugOn: print("depth is ", depth)
    
    if(isMaximising):
        
        chip = aiChip
        bestScore = -math.inf
        
        options = GetAvailableColumns()
        if debugOn: print("maximising options are: ", options)
        for column in options:
            Drop(column, chip)
            if debugOn: print("depth is ", depth, " & try drop in col ",column); VisualBoard()
            score = GetScore()
            if score == math.inf:
                bestScore = math.inf
                AntiDrop(column)
                if debugOn: print("pruned score (maximiser win)")
                break
            elif depth == 1:
                bestScore = max(bestScore, score)
            else:
                bestScore = max(bestScore, minimax(not isMaximising, depth - 1))
            AntiDrop(column)
            if debugOn: print("score = ", score, ", undo drop in col ",column); VisualBoard()
        
        if debugOn: print("maximising best score ", bestScore)
        return bestScore
        
    else:
        
        chip = playerChip
        bestScore = math.inf
        
        options = GetAvailableColumns()
        if debugOn: print("minimising options are: ", options)
        
        for column in options:
            Drop(column, chip)
            if debugOn: print("depth is ", depth, " & try drop in col ",column); VisualBoard()
            score = GetScore()
            if score == -math.inf:
                bestScore = -math.inf
                AntiDrop(column)
                if debugOn: print("pruned score (minimiser win)")
                break
            elif depth == 1:
                bestScore = min(bestScore, score)
            else:
                bestScore = min(bestScore, minimax(not isMaximising, depth - 1))
            AntiDrop(column)
            if debugOn: print("score = ", score, ", undo drop in col ",column); VisualBoard()
        
        if debugOn: print("minimising best score ", bestScore)
        return bestScore
    
def GetBestMove(depth):
    
    bestScore = -math.inf
    bestMove = -1
    
    options = GetAvailableColumns()
    for column in options:
        Drop(column, aiChip)
        if debugOn: print("depth is ", depth, " & try drop in col ",column); VisualBoard()
        score = GetScore()
        if score == math.inf:
            bestScore = math.inf
            bestMove = column
            AntiDrop(column)
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
        AntiDrop(column)
        if debugOn: print("score = ", score, ", undo drop in col ",column); VisualBoard()
    
    return bestMove        
        


dirList = numpy.array([[1, -1], [1, 0], [1, 1], [0, 1]])
chipScore = numpy.array([[0, 3, 5, math.inf], [1, 5, 30, math.inf], [3, 10, 60, math.inf]])

def GetScore():
    aiScore = ScoreCalculator(aiChip)
    playerScore = ScoreCalculator(playerChip)
    
    if aiScore == math.inf and playerScore == math.inf:
        raise Exception ("Simulataneous win and lose")
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
        VisualBoard()
        print("AI wins!\n")
        return True
    elif testScore == -math.inf:
        VisualBoard()
        print("Human wins!\n")
        return True
    return False


map = {0: '⬜', 1: '🔴', 10: '🟡'}

def VisualBoard(boardChoice = board):
    str = '\n'
    for r in range(6):
        for c in range(7):
            str += map[boardChoice[r, c]]
        str += '\n'
    print(str)



def RunGame():
    if firstMove == 'ai':
        AIMove()
    while True:
        PlayerMove()
        if CheckWin(): break
        AIMove()
        if CheckWin(): break
        
def AIMove():
    selection = GetBestMove(aiDepth)
    print("Robot choosese column", selection)
    Drop(selection, aiChip)
    print("wait for robot")
    n = 0
    while n < 3:
        time.sleep(0.5)
        if numpy.array_equal(board, CreateBoardArray()):
            n += 1
        else:
            n = 0
    VisualBoard()

def PlayerMove():
    print("wait for player")
    n = 0
    colToDropIn = -1
    while n < 3:
        test = False
        while test is False:
            time.sleep(0.5)
            newBoard = CreateBoardArray()
            test = False
            for col in range(7):
                Drop(col, playerChip)
                if numpy.array_equal(board, newBoard):
                    test = True
                    colToDropIn = col
                AntiDrop(col)
        for i in range(3):
            time.sleep(0.5)
            if numpy.array_equal(newBoard, CreateBoardArray()):
                n += 1
            else:
                n = 0
                break
    Drop(colToDropIn, playerChip)
    VisualBoard()
    
    



while True:
    LoadGame()
    RunGame()
    print("Play again? (y/n)", end=' ')
    if input() != 'y':
        break