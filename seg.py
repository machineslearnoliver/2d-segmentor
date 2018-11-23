import numpy as np
import cv2 as cv
import datetime


# Segment image without mask
def segment_image(img, thresh_val):
    img = cv.imread(img, 0)  # this is the original image.
    # threshold_value = 127 # this is the threshold set by the user for segmentation in the web app. you can create a slider for the user to change this value.
    # (in See-Mode this could be a deep learning model, or a computational setup to simulate the blood flow in a patient's brain. you know, fun stuff.)
    _, threshold_mask = cv.threshold(img, thresh_val, 255, cv.THRESH_BINARY)
    now = datetime.datetime.now().microsecond
    savePath = 'static/mask' + str(now) + str(thresh_val) + '.png'
    filePath = 'mask' + str(now) + str(thresh_val) + '.png'

    # this is the segmentation result that should be shown to the user in the web app.
    cv.imwrite(savePath, threshold_mask)
    return filePath

# Segment image with mask


def segment_image_with_mask(img, drawing, thresh_val):
    print(img)
    img = cv.imread(img)  # this is the original image.
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    _, threshold_mask = cv.threshold(img, thresh_val, 255, cv.THRESH_BINARY)
    mask = create_mask_from_drawing(drawing)
    output = mask_image(threshold_mask, mask)

    now = datetime.datetime.now().microsecond

    savePath = 'static/mask' + str(now) + str(thresh_val) + '.png'
    filePath = 'mask' + str(now) + str(thresh_val) + '.png'

    cv.imwrite(savePath, output)
    print('wrote image')
    return filePath

# Draw contours and create an image mask from the contours
# this doesn't cover all edge cases,
# it is setup to handle a single well drawn closed path


def create_mask_from_drawing(drawing):
    drawing = cv.imread(drawing)
    input_img = cv.cvtColor(drawing, cv.COLOR_BGR2GRAY)
    input_img, contours, hierarchy = cv.findContours(
        input_img, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    if len(contours) > 1:
        cv.drawContours(input_img, contours, 1, (0, 0, 0), -1)
    else:
        input_img = input_img + 255

    #cv.drawContours(input_img, contours, 1, (0, 0, 0), -1)
    output_img = cv.bitwise_not(input_img)

    return output_img

# Perform bitwise masking


def mask_image(img, mask):
    result = cv.bitwise_and(img, img, mask=mask)
    return result
