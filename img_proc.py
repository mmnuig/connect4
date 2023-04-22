
import cv2, numpy, json, webcam

yellowRange = [20, 50]
redRange = [160, 10]

jsFile = open("config.json", "r")
jsData = json.load(jsFile)
jsFile.close()

tl = jsData["Top Left Pos"]
tr = jsData["Top Right Pos"]
bl = jsData["Bottom Left Pos"]
br = jsData["Bottom Right Pos"]
corners = [tl, tr, bl, br]

jsData.clear()

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
        return 'e'

def GetTileType(img, row, col, debug=False):
    pixelLoc = CalculateCircleCentre([row, col])
    pix_bgr = img[pixelLoc[1], pixelLoc[0]]
    np_val = numpy.uint8([[pix_bgr]])
    pix_hsv = cv2.cvtColor(np_val, cv2.COLOR_BGR2HSV)
    hue = pix_hsv[0][0][0]
    pix_type = CheckPixelColor(hue)
    if debug: print(pix_type, hue); webcam.Display([pixelLoc], img)
    return pix_type