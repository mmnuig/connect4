
import numpy as np
board = np.zeros((6, 7))



def SetPos(r, c, chip):
    if chip == 'r':
        board[r, c] = 1
    elif chip == 'y':
        board[r, c] = 10
    
def GetPos(r, c):
    if r < 0 or r > 5 or c < 0 or c > 6:
        return 'x'
    chip = board[r, c]
    if chip == 0:
        return 'e'
    elif chip == 1:
        return 'r'
    elif chip == 10:
        return 'y'

def Drop(c, chip):
    r = 5
    while r >= 0:
        if GetPos(r, c) == 'e':
            SetPos(r, c, chip)
            #return
            return [r, c]
        r -= 1
    #raise Exception("Column is full. Cannot drop chip.")
    return False



dirList = np.array([[1, -1], [1, 0], [1, 1], [0, 1]])
chipScore = np.array([[0, 3, 5, 9999], [1, 5, 30, 9999], [3, 10, 60, 9999]])

def GetScore(chip):
    score = 0;
    for r in range(6):
        for c in range (7):
            if GetPos(r, c) == chip:
                for dir in dirList:
                    openEnds = 0
                    backSpace = GetPos(r - dir[0], c - dir[1])
                    if backSpace != chip:
                        if backSpace == 'e':
                            openEnds += 1;
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



map = {0: '⚫', 1: '🔴', 10: '🟡'}

def VisualBoard():
    str = ''
    for r in range(6):
        for c in range(7):
            str += map[board[r, c]]
        str += '\n'
    print(str)


Drop(1, 'r')
Drop(2, 'r')
Drop(2, 'r')
Drop(4, 'y')
Drop(5, 'y')
Drop(5, 'y')

VisualBoard()