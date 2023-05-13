
import cv2, time

def Tidy():
  camera.release()
  cv2.destroyAllWindows()
  
camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Cannot open camera")
    Tidy()
    exit()
else:
    print("Camera is opened")

def Image():
    ret, img = camera.read()
    if not ret:
        print("No image from camera")
        Tidy()
        return
    time.sleep(0.01)
    return img

def Feed(marks = []):
    while True:
        img = Image()
        for mark in marks:
            cv2.circle(img, mark, 5, [0, 0, 0], -1)
        cv2.imshow("camera", img)
        time.sleep(0.01)
        keypressed = cv2.waitKey(1)
        if keypressed == ord("q"):
            Tidy(); break
        elif keypressed == ord("s"):
            Screenshot()
            
def Screenshot():
    filename = time.strftime("IMG_%Y%m%d_%H%M%S.jpg", time.localtime())
    cv2.imwrite(filename, Image())
    
def Display(marks = [], img = Image()):
    for mark in marks:
        cv2.circle(img, mark, 5, (0, 0, 0), -1)
    cv2.imshow("image", img)
    cv2.waitKey(0)