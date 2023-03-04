import cv2
#import time

def tidy_up():
  camera.release()
  cv2.destroyAllWindows()

camera = cv2.VideoCapture(1, cv2.CAP_DSHOW)
if not camera.isOpened():
    print("Cannot open camera")
    tidy_up()
    exit()
else:
    print("Camera is opened")



def CalculateCircleCentre(target, tl, tr, bl, br):
    
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

def GetImage():
    ret, img = camera.read()
    if not ret:
        print("No image from camera")
        tidy_up()
        return
    #img = cv2.flip(img, -1)
    #time.sleep(0.01)
    return img


yellow_tile_rgb = [255, 242, 0]
red_tile_rgb = [255, 70, 60]

topLeft = [105, 31]
topRight = [563, 22]
bottomLeft = [67, 390]
bottomRight = [599, 386]

img = GetImage()
cv2.imshow("camera", img)
cv2.waitKey(0)

pixelLoc = CalculateCircleCentre([4, 4], topLeft, topRight, bottomLeft, bottomRight)
print(pixelLoc)

pix = img[pixelLoc[0], pixelLoc[1]]
print(pix)

green = (0, 255, 0)  # centre marks

cv2.circle(img, pixelLoc, 5, green, -1)
cv2.imshow('Centres', img)
cv2.waitKey(0)