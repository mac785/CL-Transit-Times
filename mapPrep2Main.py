import numpy as np
import cv2
import json


def next_name():
    return city_names_file.readline()[:-1]

def printClick(event, x, y, flags, param):
    global current_city
    if event == cv2.EVENT_LBUTTONUP:
        data = "{0}\t{1}\t{2}\n".format(current_city,x,y)
        print (data)
        # city_names_output.write(data)
        current_city = next_name()
        if current_city is not None:
            print (current_city)
        else:
            print ("Done.")

map_image = cv2.imread("Major_US_Cities-pinned.png")
city_names_file = open("City Data - Sheet1.txt","r")
# city_names_output = open("City Data with coords.txt","w")
current_city = next_name()

print(current_city)

cv2.imshow("Map",map_image)

cv2.setMouseCallback("Map",printClick)

cv2.waitKey()
cv2.destroyAllWindows()
city_names_file.close()
# city_names_output.close()