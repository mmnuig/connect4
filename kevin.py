""" My image processing functions

Written over time and added to this personal library to import as needed.
Kevin Madden, 2018.

"""
import cv2
import numpy


def hsv_range(rgb_val):
    """Return a range in HSV format of a single colour passed in RGB format

        OpenCV uses BGR, so we convert the RGB to that first.
        cv2.cvtColor expects an image (an array), not a single value.
        We make a single pixel to do the conversion.
    """
    bgr_val = rgb_val[::-1]
    np_val = numpy.uint8([[bgr_val]])
    hsv_val = cv2.cvtColor(np_val, cv2.COLOR_BGR2HSV)
    h = hsv_val[0, 0, 0]
    print(("rgb = {}").format(rgb_val))
    print(("bgr = {}").format(bgr_val))
    print(("hsv = [{0}, {1}, {2}]").format(hsv_val[0, 0, 0], hsv_val[0, 0, 1],
                                           hsv_val[0, 0, 2]))
    lower_range = numpy.array([h-10, 100, 100], dtype=numpy.uint8)
    upper_range = numpy.array([h+10, 255, 255], dtype=numpy.uint8)
    print(("lower_range = {}").format(lower_range))
    print(("upper_range = {}").format(upper_range))
    return lower_range, upper_range


def get_centroid(image):
    """Get the midpoint of our coloured blob

        Draw contours around all the objects in our image (white areas).
        Find the largest by area contour - assumes that the larger white blob
        is the one we are interested in.
        Get its centroid and return that.
        RETR_EXTERNAL returns outer contours only - contours entirely within
        other contours are ignored.
        CHAIN_APPROX_SIMPLE removes intermediate points in straight lines.
    """
    contours, hierarchy = cv2.findContours(image,
                                           cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_SIMPLE)
    print(contours)
    # Find the contour with the largest area
    areas = [cv2.contourArea(contour) for contour in contours]
    largest_contour_index = numpy.argmax(areas)
    largest_contour = contours[largest_contour_index]
    # print(largest_contour)
    M = cv2.moments(largest_contour)
    # print(M)
    cx, cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
    return (cx, cy)


def get_outline(image):
    """Get the outline of our coloured blob

        Draw contours around all the objects in our image (white areas).
        Find the largest by area contour - assumes that the larger white blob
        is the one we are interested in.
        return this contour
    """
    contours, hierarchy = cv2.findContours(image,
                                           cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_SIMPLE)
    # Find the contour with the largest area
    areas = [cv2.contourArea(contour) for contour in contours]
    largest_contour_index = numpy.argmax(areas)
    largest_contour = contours[largest_contour_index]
    return largest_contour


def get_area(image):
    """Get the area of our coloured blob

        Draw contours around all the objects in our image (white areas).
        Find the largest by area contour - assumes that the larger white blob
        is the one we are interested in.
        return this area
    """
    contours, hierarchy = cv2.findContours(image,
                                           cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_SIMPLE)
    # Find the contour with the largest area
    areas = [cv2.contourArea(contour) for contour in contours]
    largest_contour_index = numpy.argmax(areas)
    largest_contour = contours[largest_contour_index]
    M = cv2.moments(largest_contour)
    a = M['m00']
    return a


def extract_centroid(M):
    cx, cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
    return(cx, cy)


def get_contour_centres(image):
    """Get the centres of all the countours in an image

        Draw contours around all the objects in our image (white areas).
        Get the centroids of the contours.  Return a list.
        Best used with a mask image.
    """
    contours, hierarchy = cv2.findContours(image,
                                           cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_SIMPLE)
    # Find the contour with the largest area
    # areas = [cv2.contourArea(contour) for contour in contours]
    # largest_contour_index = numpy.argmax(areas)
    # largest_contour = contours[largest_contour_index]
    # M = cv2.moments(largest_contour)
    moments = [cv2.moments(contour) for contour in contours]
    centroids = [extract_centroid(moment) for moment in moments]
    # a = M['m00']
    return centroids
