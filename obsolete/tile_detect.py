import cv2
import math
import numpy
import klib
import tkinter
import tkinter.filedialog
import unicodedata


def get_row(c):
    # Change the next two lines to the y-coordinate of the top and bottom
    # edges of the tiles
    y_min = 50
    y_max = 700
    rows = 6
    y_range = y_max - y_min
    y_step = int(y_range / rows)
    x_coord, y_coord = c
    row = 999  # Use 999 to indicate an error
    # print("get_row(): y_coord = {}".format(y_coord))
    for i in range(0, rows):
        # uncomment the next 3 lines to see the calculations in action
        # print("i = {}".format(i))
        # print("y_min+y_step*(i+1) = {}".format(y_min+y_step*(i+1)))
        # print("y_min+y_step*i = {}".format(y_min+y_step*i))
        if y_coord > (y_min+y_step*i) and y_coord < (y_min+y_step*(i+1)):
            # The row number is from the top of the image since the y-origin
            # is at the top.
            # Subtract the row value from the max (6) to get the visual row
            # number as seen on the board
            # row = i
            row = rows - 1 - i
            break
    return row


def get_col(c):
    # Change the next two lines to the x-coordinate of the leftmost and
    # rightmost edges of the tiles
    x_min = 250
    x_max = 1100
    columns = 7
    x_range = x_max - x_min
    x_step = int(x_range / columns)
    x_coord, y_coord = c
    col = 999  # Use 999 to indicate an error
    # print("get_col(): x_coord = {}".format(x_coord))
    for i in range(0, columns):
        # uncomment the next 3 lines to see the calculations in action
        # print("i = {}".format(i))
        # print("x_min+x_step*(i+1) = {}".format(x_min+x_step*(i+1)))
        # print("x_min+x_step*i = {}".format(x_min+x_step*i))
        if x_coord > (x_min+x_step*i) and x_coord < (x_min+x_step*(i+1)):
            col = i
            break
    return col


def choose_file():
    file_formats = [
        ('JPEG Image', '*.jpg'),
        ('PNG Image', '*.png'),
        ('All', '*.*'),
    ]
    win = tkinter.Tk()
    win.withdraw()
    imgfile = tkinter.filedialog.askopenfilename(filetypes=file_formats,
                                                 title="Load Board Image",
                                                 defaultextension=".jpg")
    return imgfile


def cal_coords(event, x, y, flags, param):
    print("event = {}".format(event))
    print("x, y = {}, {}".format(x, y))
    print("flags = {}".format(flags))
    print("param = {}".format(param))
    if event == cv2.EVENT_LBUTTONDOWN:
        print("button down")
        param = (x, y)


# Main code starts here
# img = cv2.imread("03.png")
# Select board image
img_file = choose_file()
if not img_file:
    exit()
img = cv2.imread(img_file)
# img = cv2.bilateralFilter(img, 50, 75, 75)
cv2.imshow("Board", img)
cal_xy = ()
cv2.setMouseCallback("Board", cal_coords, cal_xy)
cv2.waitKey(0)
print("main: param = {}".format(cal_xy))

# scale_factor = 100
# img_width = int(img.shape[1] * scale_factor / 100)
# img_height = int(img.shape[0] * scale_factor / 100)
# scaled_img_size = (img_width, img_height)
# scaled_img = cv2.resize(img, scaled_img_size)
# cv2.imshow("Scaled", scaled_img)
# cv2.waitKey(0)

# img = scaled_img
img2 = img.copy()

# Use HSV colour space for colour masking
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

yellow_tile_rgb = [255, 242, 0]
red_tile_rgb = [255, 70, 60]

hr = klib.hsv_range(yellow_tile_rgb)
mask_yellow = cv2.inRange(hsv, hr[0], hr[1])
hr = klib.hsv_range(red_tile_rgb)
mask_red = cv2.inRange(hsv, hr[0], hr[1])
cv2.imshow('Yellow', mask_yellow)
cv2.waitKey(0)
cv2.imshow('Red', mask_red)
cv2.waitKey(0)

blue = (255, 0, 0)  # centre marks
green = (0, 255, 0)  # centre marks

centres_yellow = klib.get_contour_centres(mask_yellow)
for cnt in centres_yellow:
    cv2.circle(img2, cnt, 5, blue, -1)
centres_red = klib.get_contour_centres(mask_red)
for cnt in centres_red:
    cv2.circle(img2, cnt, 5, green, -1)
cv2.imshow('Centres', img2)
cv2.waitKey(0)

# board[] is a 6x7 array representing the token positions
board = numpy.full((6, 7), ".")
# print(board)

font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 0.5
fontColor = (0, 0, 0)
thickness = 1
lineType = 2

for c in centres_yellow:
    row = get_row(c)
    col = get_col(c)
    text_coords = (c[0]-20, c[1]+10)
    text = "R" + str(row) + " C" + str(col)
    cv2.putText(img, text, text_coords,
                font, fontScale, fontColor, thickness, lineType)
    # print("c = {}, row = {}, col = {}".format(c, row, col))
    # The row number is from the top of the image since the y-origin is at
    # the top.
    # Subtract the row value from the max (5) to get the visual row number
    # as seen on the board
    board[5-row, col] = 'Y'
for c in centres_red:
    row = get_row(c)
    col = get_col(c)
    text_coords = (c[0]-20, c[1]+10)
    text = "R" + str(row) + " C" + str(col)
    cv2.putText(img, text, text_coords,
                font, fontScale, fontColor, thickness, lineType)
    # print("c = {}, row = {}, col = {}".format(c, row, col))
    # Arrays (like images) have row zero at the top.  Write the tile colours
    # from the bottom to display an array that looks familiar.
    board[6-1-row, col] = 'R'
print(board)

# emoji version using numpy vectorisation
eboard = numpy.empty_like(board)
eboard[numpy.where(board == 'R')] = unicodedata.lookup("large red circle")
eboard[numpy.where(board == 'Y')] = unicodedata.lookup("large yellow circle")
# The white circle (empty) is smaller than the red and yellow ones, so it
# doesn't line up nicely with them.  The blue circle does.
# eboard[numpy.where(board == '.')] = unicodedata.lookup("white circle")
eboard[numpy.where(board == '.')] = unicodedata.lookup("large blue circle")
print(eboard)
cv2.imshow("markup", img)
cv2.waitKey(0)

cv2.destroyAllWindows()
exit()
