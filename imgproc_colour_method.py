import cv2, math, numpy, kevin

img = cv2.imread("grid_with_tiles.png")

scale_factor = 66
img_width = int(img.shape[1] * scale_factor / 100)
img_height = int(img.shape[0] * scale_factor / 100)
scaled_img_size = (img_width, img_height)
scaled_img = cv2.resize(img, scaled_img_size)

img = scaled_img
img_copy = img.copy()

tile_rgb = [237, 28, 36]

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
hr = kevin.hsv_range(tile_rgb)
mask = cv2.inRange(hsv, hr[0], hr[1])

cm = kevin.get_centroid(mask)
am = kevin.get_area(mask)
radius = int(math.sqrt(am/math.pi))

centres = kevin.get_contour_centres(mask)
print(centres)