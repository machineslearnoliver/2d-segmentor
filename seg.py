import mimetypes
import numpy as np
import cv2 as cv
import datetime
import base64
import os
import data_uri_creator
from datauri import DataURI 

# Segment image without mask
def segment_image(img, thresh_val):
    img = cv.imread(img, 0)  # this is the original image.
    # threshold_value = 127 # this is the threshold set by the user for segmentation in the web app. you can create a slider for the user to change this value.
    # (in See-Mode this could be a deep learning model, or a computational setup to simulate the blood flow in a patient's brain. you know, fun stuff.)
    _, threshold_mask = cv.threshold(img, thresh_val, 255, cv.THRESH_BINARY)
    savePath = 'static/masked.png'
    filePath = 'masked.png'

    # this is the segmentation result that should be shown to the user in the web app.
    
    base64_uri = DataURI.from_file(savePath)
    cv.imwrite(savePath, threshold_mask)
    return base64_uri

# Segment image with mask
def segment_image_with_mask(img, drawing, thresh_val):
    print(img)
    img = cv.imread(img)  # this is the original image.
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    _, threshold_mask = cv.threshold(img, thresh_val, 255, cv.THRESH_BINARY)
    mask = create_mask_from_drawing(drawing)
    output = mask_image(threshold_mask, mask)

    savePath = 'static/masked.png'
    filePath = 'masked.png'
    #base64_uri = convert_file_to_base64(savePath)
    base64_uri = DataURI.from_file(savePath)
    cv.imwrite(savePath, output)
    print('wrote image')
    print(base64_uri)
    return base64_uri


# Draw contours and create an image mask from the contours
def create_mask_from_drawing(drawing):
    drawing = cv.imread(drawing)
    input_img = cv.cvtColor(drawing, cv.COLOR_BGR2GRAY)
    input_img, contours, hierarchy = cv.findContours(
        input_img, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    if len(contours) > 1:
        cv.drawContours(input_img, contours, 1, (0, 0, 0), -1)
    else:
        input_img = input_img + 255

    return cv.bitwise_not(input_img)

# Perform bitwise masking
def mask_image(img, mask):
    result = cv.bitwise_and(img, img, mask=mask)
    return result
