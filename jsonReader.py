import cv2
import numpy as np
import json
from tkinter import filedialog

json_filename=filedialog.askopenfilename(message = "Find the json file")
if json_filename == "":
    raise IOError("No file found.")

with open(json_filename) as json_data:
    data = json.load(json_data)
    print(data)
names = []

city_data_file = open("City Data with coords.txt")
for line in city_data_file:
    parts = line.split("\t")
    names.append("{0}, {1}".format(parts[1],parts[2]))
city_data_file.close()
for i in range(len(names)):
    print ("{0:2d}\t{1}".format(i,names[i]))

origin_list = data['origin_addresses']
destination_list = data['destination_addresses']
print ("Origins: {0}".format(origin_list))
print ("Destinations: {0}".format(destination_list))

num_origins = len(origin_list)
num_destinations = len(destination_list)

cell_height = 20
cell_width = 100

screen = np.zeros((cell_height * (num_destinations + 1), cell_width * (num_origins + 1), 3), dtype = float)
for i in range(num_origins):
    cv2.putText(screen,origin_list[i][:-5],((i+1)*cell_width, cell_height-10),\
                cv2.FONT_HERSHEY_COMPLEX_SMALL,0.5,(1.0,1.0,1.0))
    cv2.line(screen, ((i+1) * cell_width, 0), ((i+1) * cell_width, (num_destinations + 1) * cell_height), (1.0, 1.0, 1.0))
for j in range(num_destinations):
    cv2.putText(screen,destination_list[j][:-5],(10,(j+2)*cell_height-10),\
                cv2.FONT_HERSHEY_COMPLEX_SMALL,0.5,(1.0,1.0,1.0))
    cv2.line(screen, (0, (j + 1) * cell_height), ((num_origins+1)* cell_width, (j + 1) * cell_height), (1.0, 1.0, 1.0))
cv2.imshow("grid",screen)

def handle_click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONUP:
        origin_index = int(x/cell_width)-1
        destination_index = int(y/cell_height)-1
        cell_info = data["rows"][origin_index]["elements"][destination_index]
        time_in_seconds = cell_info["duration"]["value"]
        distance_in_meters = cell_info["distance"]["value"]
        origin_id = names.index(origin_list[origin_index][:-5])
        destination_id = names.index(destination_list[destination_index][:-5])
        print ("{0}\t{2}\t{4}\t{5}".format(origin_id,origin_list[origin_index][:-5],\
                                                   destination_id, destination_list[destination_index][:-5],\
                                                   time_in_seconds,distance_in_meters))
        cv2.rectangle(screen,(cell_width*int(x/cell_width),cell_height*int(y/cell_height)),\
                      (cell_width*(int(x/cell_width)+1),cell_height*(int(y/cell_height)+1)),\
                      (0.5,0.5,0.5),-1)
        cv2.imshow("grid", screen)


cv2.setMouseCallback("grid",handle_click)

cv2.waitKey()
cv2.destroyAllWindows()