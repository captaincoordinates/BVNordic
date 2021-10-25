from os import path
from pathlib import Path

import cv2
import numpy as np
from skimage.metrics import structural_similarity

image_base = path.join(
    path.dirname(__file__),
    "..",
    "output",
    "compare-14400d26f17d1ea056bb1fb61d96eaf0d38607f8-0edcff437292cbfa470b6c734a6a3135c9d0c8fa",  # noqa: E501
)
image_1 = path.abspath(
    path.join(image_base, "14400d26f17d1ea056bb1fb61d96eaf0d38607f8", "main", "Print.png")
)
image_2 = path.abspath(
    path.join(image_base, "0edcff437292cbfa470b6c734a6a3135c9d0c8fa", "main", "Print.png")
)
result_base = path.join(image_base, "result")
Path(result_base).mkdir(parents=True, exist_ok=True)

before = cv2.imread(image_1)
after = cv2.imread(image_2)

# Convert images to grayscale
before_gray = cv2.cvtColor(before, cv2.COLOR_BGR2GRAY)
after_gray = cv2.cvtColor(after, cv2.COLOR_BGR2GRAY)

# Compute SSIM between two images
(score, diff) = structural_similarity(before_gray, after_gray, full=True)

if score == 1:
    print("identical images")
    exit()

# The diff image contains the actual image differences between the two images
# and is represented as a floating point data type in the range [0,1]
# so we must convert the array to 8-bit unsigned integers in the range
# [0,255] before we can use it with OpenCV
diff = (diff * 255).astype("uint8")

# Threshold the difference image, followed by finding contours to
# obtain the regions of the two input images that differ
thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = contours[0] if len(contours) == 2 else contours[1]

mask = np.zeros(before.shape, dtype="uint8")
filled_after = after.copy()

for c in contours:
    area = cv2.contourArea(c)
    if area > 40:
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(before, (x, y), (x + w, y + h), (36, 255, 12), 2)
        cv2.rectangle(after, (x, y), (x + w, y + h), (36, 255, 12), 2)
        cv2.drawContours(mask, [c], 0, (0, 255, 0), -1)
        cv2.drawContours(filled_after, [c], 0, (0, 255, 0), -1)

# cv2.imshow('before', before)
# cv2.imshow('after', after)
# cv2.imshow('diff',diff)
cv2.imshow("mask", mask)
# cv2.imshow('filled after',filled_after)
cv2.waitKey(0)
