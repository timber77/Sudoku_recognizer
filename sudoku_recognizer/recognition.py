# two assumptions for this programm to work: The outer lines of the grid are the biggest square in the picture and the grid is not rotated.
# you need tesseract-ocr installed in order for this programm to work
import cv2
import numpy as np
import os
import pytesseract
from PIL import Image
import image_slicer
from sudoku_solver import solve, render_grid
import math


print("Enter path to image including the imagename with the file extension:")
path = input()
path.replace("\\", "/")
print("...")
original_img = cv2.imread(path)
img_copy = original_img.copy()
height, width = original_img.shape[0:2]


# Convert Image to grayscale and applying threshold
grayscaled = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)
gauss_thresh_inv = cv2.adaptiveThreshold(
    grayscaled, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 21, 10)
gauss_thresh_norm = cv2.adaptiveThreshold(
    grayscaled, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 10)
print("preprocessing done")

# find the main square with findContours
img_contours, contours, hierarchy = cv2.findContours(
    gauss_thresh_inv, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
max_size_square = 0
for i in range(len(contours)):
    approximation = cv2.approxPolyDP(contours[i], 4, True)
    # has it 4 sides?
    if(not (len(approximation) == 4)):
        continue
    # is it convex?
    if (not cv2.isContourConvex(approximation)):
        continue
    # size of it
    rectangle_size = cv2.contourArea(approximation)
    # store biggest
    if rectangle_size > max_size_square:
        max_size_square = rectangle_size
        big_rectangle = approximation
approximation = big_rectangle
# this part isn't actually necessary and is only used for debugging. It draws the contours of the chosen square on the copied image.
for i in range(len(approximation)):
    cv2.line(img_copy,
             (big_rectangle[(i % 4)][0][0], big_rectangle[(i % 4)][0][1]),
             (big_rectangle[((i + 1) % 4)][0][0],
              big_rectangle[((i + 1) % 4)][0][1]),
             (255, 0, 0), 2)

print("finding biggest square done")
# resizing the image, so that the image only contains the Sudoku
x1, y1 = approximation[0][0]
x2, y2 = approximation[2][0]
resized_gauss_thresh_inv = gauss_thresh_inv[y1:y2, x1:x2]
resized_gauss_thresh_norm = gauss_thresh_norm[y1:y2, x1:x2]
resized_original_img = original_img[y1:y2, x1:x2]

print("resizing done")

# finding the lines of the grid
minLineLength = (width + height) / 4
maxLineGap = 15
lines = cv2.HoughLinesP(resized_gauss_thresh_inv, 1,
                        np.pi / 180, 90, np.array([]), minLineLength, maxLineGap)
# "erasing" the lines from the image so that only the numbers remain
for x in range(0, len(lines)):
    for x1, y1, x2, y2 in lines[x]:
        cv2.line(resized_gauss_thresh_norm, (x1, y1),
                 (x2, y2), (255, 255, 255), 5)

        # not necessary only used to see which lines are detected
        cv2.line(resized_original_img, (x1, y1), (x2, y2), (0, 255, 0), 5)
print("finding lines done")

# scaling the image so that it can  be properly splitted
cv2.imwrite("unscaled.jpg", resized_gauss_thresh_norm)
height_2, width_2 = resized_gauss_thresh_norm.shape[0:2]
unscaled_img = Image.open("unscaled.jpg")
new_size = math.ceil(width_2 / 9) * 9
scaled_img = unscaled_img.resize((new_size, new_size), Image.NEAREST)
os.remove("unscaled.jpg")
# splitting the image into 81 equal sqares
scaled_img.save("parts.jpg", "JPEG")
parts = image_slicer.slice("parts.jpg", 81, save=False)
os.remove("parts.jpg")
print("splitting done")


# running googles tesseract-ocr over each of the 81 images to recognise the number
print("detecting numbers")
numbers = []
for part in parts:
    im = part.image
    # enlarge the small images to reach better results with tesseract-ocr, which is optimized for "big" images
    im = im.resize((100, 100), Image.BICUBIC)
    number = pytesseract.image_to_string(
        im, config="--psm 10 -c tessedit_char_whitelist=123456789")
    if number.isnumeric():  # if there is no number on the image we add 0 to the list with the numbers
        numbers.append(int(number))
    else:
        numbers.append(0)


# creating a 2D list out of the 1D list
numbers2D = [numbers[i:i + 9] for i in range(0, 81, 9)]
print("number recognition done")

# printing the unsolved sudoku
rendered_unsolved = render_grid(numbers2D)
print("Solving:")
print(rendered_unsolved, "\n")


# printing the solved sudoku
solved = solve(numbers2D)
rendered_solved = render_grid(solved)
print("Solved:")
print(rendered_solved)
