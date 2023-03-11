import webcam
import cv2
import numpy

def CalculateCircleCentre(target):
    
    leftx = tl[0] + target[0] * (bl[0] - tl[0]) / 5
    lefty = tl[1] + target[0] * (bl[1] - tl[1]) / 5
    left = [leftx, lefty]
    
    rightx = tr[0] + target[0] * (br[0] - tr[0]) / 5
    righty = tr[1] + target[0] * (br[1] - tr[1]) / 5
    right = [rightx, righty]
    
    finalx = left[0] + target[1] * (right[0] - left[0]) / 6
    finaly = left[1] + target[1] * (right[1] - left[1]) / 6
    final = [round(finalx), round(finaly)]
    
    return final

def CheckPixelColor(pix):
    if pix >= yellowRange[0] and pix <= yellowRange[1]:
        return 'y'
    elif pix >= redRange[0] and pix <= 179:
        return 'r'
    elif pix >= 0 and pix <= redRange[1]:
        return 'r'
    else:
        return 'x'
    
def GetTileType(xPos, yPos, debug=False):
    pixelLoc = CalculateCircleCentre([xPos, yPos])
    pix_bgr = img[pixelLoc[1], pixelLoc[0]]
    np_val = numpy.uint8([[pix_bgr]])
    pix_hsv = cv2.cvtColor(np_val, cv2.COLOR_BGR2HSV)
    hue = pix_hsv[0][0][0]
    pix_type = CheckPixelColor(hue)
    if debug: print(pix_type, hue); webcam.Display(img, [pixelLoc])
    return pix_type
    
tl = [139, 45]
tr = [540, 39]
bl = [105, 353]
br = [572, 350]
corners = [tl, tr, bl, br]

yellowRange = [20, 50]
redRange = [160, 10]

img = webcam.Image()

for i in range(7):
    GetTileType(5, i, True)