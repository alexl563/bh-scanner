from __future__ import print_function
from skimage import data
from skimage.filters import try_all_threshold
from skimage.filters import threshold_local
from skimage import img_as_ubyte
from datetime import datetime
import pymongo
from pymongo import MongoClient
import pyzbar.pyzbar as pyzbar
import numpy as np
import cv2
import sys

#mongo setup and checkin code

def augment_time():
    hours = datetime.now().hour
    minutes = datetime.now().minute
    add_on = "am"

    if hours > 12:
        hours -= 12
        add_on = "pm"

    time = f"{hours}:{minutes} {add_on}"

    return time


def mongo(student):
    cluster = MongoClient("")
    db = cluster['bh-scanner']
    collection = db['bh-scanner']

    #post = {"_id" : 1, "number" : "ST20842", "name" : "Wagner, Max", "checked-in" : 0}
    #collection.insert_one(post)

    #currently messed up cause I needed to do some fixing

    student_numbers = ["ST20602", "ST20842"]
    for student in range(1):
        results = collection.find({"number" : "ST20602"})

        for result in results:
            print(result["name"])
            print(f'{result["name"]} is checked in!')
            collection.update_one({"name" : result["name"]}, {"$set" : {"checked-in" : 1}})
            collection.update_one({"name" : result["name"]}, {"$set" : {"time" : augment_time()}})
            collection.update_one({"name" : result["name"]}, {"$set" : {"date" : str(datetime.now().date())}})

#image work beings
""" def prepro(img, thold):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret,img = cv2.threshold(img, thold, 255, cv2.THRESH_BINARY)
    img = cv2.resize(img, (int(img.shape[1]/4), int(img.shape[0]/4)))

    return img
 """
def prepro(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    blocksize = 49
    localThresh = threshold_local(img, blocksize, offset=10)
    binary_local = img > localThresh
    finalimg = img_as_ubyte(binary_local)

    return finalimg

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
    
    finalimg = prepro(img)

    decodedObjects = decode(finalimg)

    student_value = ""

    for object in decodedObjects:
        student_value = object.data.decode("utf-8")

    #changes value in database
    mongo(student_value)



  


