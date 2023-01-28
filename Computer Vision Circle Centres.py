
def CalculateCircleCentre(target, tl, tr, bl, br):
    
    leftx = tl[0] + target[0] * (bl[0] - tl[0]) / 5
    lefty = tl[1] + target[0] * (bl[1] - tl[1]) / 5
    left = [leftx, lefty]
    
    rightx = tr[0] + target[0] * (br[0] - tr[0]) / 5
    righty = tr[1] + target[0] * (br[1] - tr[1]) / 5
    right = [rightx, righty]
    
    finalx = left[0] + target[1] * (right[0] - left[0]) / 6
    finaly = left[1] + target[1] * (right[1] - left[1]) / 6
    final = [finalx, finaly]
    
    return final

print(CalcPoint([2, 4], [332, 78], [1054, 73], [351, 608], [1034, 607]))