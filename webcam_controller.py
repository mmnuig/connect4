import cv2
import time

def tidy_up():
  camera.release()
  cv2.destroyAllWindows()

camera = cv2.VideoCapture(0)
if not camera.isOpened():
    print("Cannot open camera")
    tidy_up()
    exit()
else:
    print("Camera is opened")

upside_down = False

while True:
    ret, img = camera.read()
    if ret:
        if upside_down:
            img = cv2.flip(img, -1)
        cv2.imshow("camera", img)
        time.sleep(0.01)
        
        keypressed = cv2.waitKey(1)
        if keypressed == ord("q"):
            break
        elif keypressed == ord("u"):
            upside_down = not upside_down
        elif keypressed == ord("s"):
            filename = time.strftime("IMG_%Y%m%d_%H%M%S.jpg", time.localtime())
            cv2.imwrite(filename, img)
    else:
        print("No image from camera")
        tidy_up()
        break

tidy_up()
