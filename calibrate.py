
import cv2, json, webcam

corners = []

def MouseEvent(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f'({x}, {y})')
        corners.append([x, y])
        cv2.circle(img, (x, y), 5, (0, 0, 0), -1)

img = webcam.Image()
cv2.namedWindow('image')
cv2.setMouseCallback('image', MouseEvent)

while len(corners) < 4:
    cv2.imshow('image', img)
    if cv2.waitKey(1) == ord('q'):
        break
    
cv2.destroyAllWindows()

jsFile = open('config.json', 'r')
jsData = json.load(jsFile)
jsFile.close()

jsData['Top Left Pos'] = corners[0]
jsData['Top Right Pos'] = corners[1]
jsData['Bottom Left Pos'] = corners[2]
jsData['Bottom Right Pos'] = corners[3]

jsFile = open('config.json', 'w')
jsFile.write(json.dumps(jsData))
jsFile.close()