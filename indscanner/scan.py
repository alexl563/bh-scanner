from __future__ import print_function
import pymongo
from pymongo import MongoClient
import pyzbar.pyzbar as pyzbar
import numpy as np
import cv2
import sys

#mongo setup and checkin code
def mongo(student):
    cluster = MongoClient('mongodb+srv://belmonthill:makerprize@cluster0.yo2fv.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
    db = cluster['bh-scanner']
    collection = db['bh-scanner']

    #post = {"_id" : 0, "number" : "ST20602", "name" : "Lo, Alexander", "checked-in" : 0}

    results = collection.find({"number" : student})

    for result in results:
        print(f'{result["name"]} is checked in!')
        collection.update_one({"name" : result["name"]}, {"$set" : {"checked-in" : 1}})

#image work beings
def prepro(img, thold):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret,img = cv2.threshold(img, thold, 255, cv2.THRESH_BINARY)
    img = cv2.resize(img, (int(img.shape[1]/4), int(img.shape[0]/4)))
    #cv2.imshow('image',img)
    #cv2.waitKey(0)
    return img


def decode(im) : 
    # Find barcodes and QR codes
    decodedObjects = pyzbar.decode(im)

    return decodedObjects


# Display barcode and QR code location  
def display(im, decodedObjects):

    # Loop over all decoded objects
    for decodedObject in decodedObjects: 
        points = decodedObject.polygon

        # If the points do not form a quad, find convex hull
        if len(points) > 4 : 
            hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
            hull = list(map(tuple, np.squeeze(hull)))
        else : 
            hull = points

        # Number of points in the convex hull
        n = len(hull)

        # Draw the convext hull
        for j in range(0,n):
            cv2.line(im, hull[j], hull[ (j+1) % n], (255,0,0), 3)

    # Display results 
    cv2.imshow("Results", im)
    cv2.waitKey(0)


# Main 
if __name__ == '__main__':

    # Read image
    args = sys.argv[1:]
    img = cv2.imread("scan.jpg")
    for i in range(0, 24):
        tempimg = prepro(img, i*5)
        decodedObjects = decode(tempimg)
        if len(decodedObjects) > 0:
            finalimg = tempimg

    decodedObjects = decode(finalimg)

    student_value = ""

    for object in decodedObjects:
        student_value = object.data.decode("utf-8")

    #changes value in database
    mongo(student_value)



  


