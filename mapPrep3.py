import cv2

map_image = cv2.imread("Major_US_Cities.png")
city_data_file = open("City Data with coords.txt","r")
connection_file = open("connections.txt","r")
nodes = []
edges = []
for line in city_data_file:
    parts = line.split("\t")
    nodes.append(parts)
    print (parts)
    cv2.circle(map_image,(int(parts[3]),int(parts[4])),2,(0,0,128))
city_data_file.close()

for line in connection_file:
    parts = line.split("\t")
    edges.append(parts)
connection_file.close()

for edge in edges:
    pt1 = (int(nodes[int(edge[0])][3]),int(nodes[int(edge[0])][4]))
    pt2 = (int(nodes[int(edge[1])][3]),int(nodes[int(edge[1])][4]))
    cv2.line(map_image,pt1,pt2,(192,0,0))

cv2.imshow("Map",map_image)

cv2.waitKey()
cv2.destroyAllWindows()