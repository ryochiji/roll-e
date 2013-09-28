"""
This script is to test the basic shape matching algorithm in shapes.py.
This script expects two paramters: a training image, and a test image. The 
training image should have a more or less easily discernable red shape near
the center. The test image should contain a similar shape (also red) somewhere 
in it.
"""

import sys
from SimpleCV import Image, Color, DrawingLayer
import time
import shapes

def filter_image(img, color=Color.RED, threshold=50):
    white = img.colorDistance(Color.WHITE).invert()
    nonwhite = img - white
    return nonwhite.hueDistance(color).binarize(50)

def calculate_distance(img, x, y):
    return ((img.width / 2) - x)**2 + ((img.height / 2) - y)**2

def find_centermost_blob(img, blobs):
    min_d = calculate_distance(img, img.width, img.height)
    center_blob = None
    for b in blobs:
        if b.area() < 500: continue
        d = calculate_distance(img, b.x, b.y)
        if d<min_d:
            min_d = d
            center_blob = b
    return center_blob

def crop_blob(img, blob):
    box = blob.boundingBox()
    return img.crop(box[0]-2, box[1]-2, box[2]+4, box[3]+4) 

def blob2matrix(img, blob):
    cropped = crop_blob(img, blob)
    edges = cropped.edges()
    return shapes.PatternMatrix(edges)

if __name__=="__main__":
    if len(sys.argv)<3:
        print "Usage: redblobs.py <training_image> <test_image>"
        sys.exit(1)


    # Process training image and find a blob nearest to the center
    input_image = sys.argv[-2]
    img = Image(input_image)
    colored = filter_image(img)
    blobs = colored.findBlobs()
    blob = find_centermost_blob(img, blobs)
    matrix = blob2matrix(colored, blob)

    # Process test image and find blob most similar to the shape found
    # in the training image
    test = Image(sys.argv[-1])
    colored2 = filter_image(test)
    blobs = colored2.findBlobs()
    max_sim = 0.0
    best_blob = None
    for blob in blobs:
        if blob.area() < 500: continue
        test_matrix = blob2matrix(colored2, blob)
        similarity = matrix.similarity(test_matrix)
        print "%s %s" % (blob, similarity)
        if similarity > max_sim:
            best_blob = blob
            max_sim = similarity
    best_blob.show()
    while True:
        pass
