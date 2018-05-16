import cv2
from copy import deepcopy
from enum import Enum
import numpy as np

class ClickHandlerMode(Enum):
    FIRST_CLICK = 0
    SECOND_CLICK = 1
    SEARCHING = 2
    DONE = 3


class MapConnector:

    def __init__(self):
        """
        Loads the map graphic, as well as the files for the cities and the connections between them.

        """
        self.original_map_image = cv2.imread("Major_US_Cities.png") #by default this reads as color.

        # city data consists of tab-delimited: id#, city name, state, x-coord, y-coord
        city_data_file = open("City Data with coords.txt","r")

        # connection data consists of tab-delimited: node1_id, node2_id, distance_in_meters, travel_time_in_seconds
        connection_file = open("connections.txt","r")
        self.vertices = [] # an array of 5-element arrays
        self.edges = [] # an array of 4-element arrays

        for line in city_data_file:
            parts = line.split("\t")
            self.vertices.append(parts)
        city_data_file.close()

        # -----------------------------------------
        for i in connection_file:
            parts = i.split("\t")
            self.edges.append(parts)
        connection_file.close()
        # -----------------------------------------
        self.current_map = self.draw_cities_and_connections()
        #display the map you just made in a window called "Map"
        # cv2.imshow("Map",self.current_map)
        cv2.imshow("Map", np.repeat(np.repeat(self.current_map, 2, axis=0), 2, axis=1))
    def start_process(self):
        """
        this is essentially our game loop - it sets up the mouse listener,
        and then enters an infinite loop where it waits for the user to select
        the two cities before it performs a search and displays the result.
        :return:
        """
        #if anybody does anything mouse-related in the "Map" window,
        # call self.handleClick.
        cv2.setMouseCallback("Map", self.handleClick)
        self.reset()
        while True:
            while self.click_mode != ClickHandlerMode.SEARCHING:
                cv2.waitKey(1)
            path = self.perform_search(self.first_city_id,self.second_city_id)
            self.display_path(path)

            # TODO: consider the following. No action is required.
            # Optional: if you would like to save a copy of the graphic that results,
            # you can say:
            #  cv2.imsave("pickAFilename.png",self.current_map).


            print("Click on screen once to start again.")
            self.click_mode = ClickHandlerMode.DONE

    def reset(self):
        """
        set the image to be shown to be one that shows vertices and edges.
        set the click mode to wait for the first click.
        :return:
        """
        self.current_map = self.draw_cities_and_connections()
        self.click_mode = ClickHandlerMode.FIRST_CLICK

    def draw_city(self, map, city, color = (0,0,128), size = 4):
        """
        draws a dot into the graphic "map" for the given city 5-element array
        :param map: the graphic to alter
        :param city: the 5-element array from which to get location info
        :param color:
        :param size:
        :return: None
        """
        cv2.circle(img = map, center = (int(city[3]),int(city[4])),radius = size, color = color,
                   thickness = -1)#note color is BGR, 0-255

    def draw_edge(self, map, city1_id, city2_id, color = (0,0,0)):
        """
        draws a line into the graphic "map" for the given connection
        :param map: the graphic to alter
        :param city1_id: the 5-element array for the first city
        :param city2_id: the 5-element array for the second city, to which we connect.
        :param color:
        :return: None
        """
        point1 = (int(self.vertices[city1_id][3]), int(self.vertices[city1_id][4]))
        point2 = (int(self.vertices[city2_id][3]), int(self.vertices[city2_id][4]))
        cv2.line(img=map, pt1=point1, pt2=point2, color = color)  # note color is BGR, 0-255.

    def draw_cities_and_connections(self,draw_cities = True, draw_connections = True):
        """
        makes a new graphic, based on a copy of the original map file, with
        the cities and connections drawn in it.
        :param draw_cities:
        :param draw_connections:
        :return: the new copy with the drawings in it.
        """
        map = deepcopy(self.original_map_image)
        if draw_cities:
            for city in self.vertices:
                self.draw_city(map, city)
        if draw_connections:
            for edge in self.edges:
                self.draw_edge(map, int(edge[0]), int(edge[1])) #note edge is a list of strings,
                                                                # so we have to cast to ints.
        return map

    def display_path(self, path):
        """
        draws the edges that connect the cities in the list of cities in a
         color that makes them obvious. If the path is None, then you should
         display a message that indicates that there is no path.
         Modifies the existing self.current_map graphics variable.
        :param path: a list of city ids or None, if no path can be found.
        :return: None
        """
        # -----------------------------------------
        for i in range(0,len(path)-1):
            self.draw_edge(self.current_map,path[i],path[i+1],[255,0,0])
        cv2.imshow("Map", np.repeat(np.repeat(self.current_map, 2, axis=0), 2, axis=1))
        # -----------------------------------------

    def find_closest_city(self,pos):
        """
        identifies which city is closest to the coordinate given.
        :param pos: the coordinate of interest (x,y)
        :return: the index of the closest city.
        """
        dist = float("inf")
        which_city = None
        counter = 0
        for city in self.vertices:
            d_squared = (pos[0]-int(city[3]))**2 + (pos[1]-int(city[4]))**2
            if d_squared < dist:
                dist = d_squared
                which_city = counter
            counter += 1
        return which_city

    def handleClick(self,event,x,y,flags,param):
        """
        this method gets called whenever the user moves or clicks or does
        anything mouse-related while the mouse is in the "Map" window.
        In this particular case, it will only do stuff if the mouse is being
        released. What it does depends on the self.click_mode enumerated variable.
        :param event: what kind of mouse event was this?
        :param x:
        :param y:
        :param flags: I suspect this will be info about modifier keys (e.g. shift)
        :param param: additional info from cv2... probably unused.
        :return: None
        """
        if event == cv2.EVENT_LBUTTONUP: #only worry about when the mouse is released inside this window.
            if self.click_mode == ClickHandlerMode.FIRST_CLICK:
                # we were waiting for the user to click on the first city, and she has just done so.
                # identify which city was selected, set the self.first_city_id variable
                # and display the selected city on screen.
                self.first_city_id = self.find_closest_city((x/2,y/2))
                cv2.putText(img=self.current_map,\
                            text="from: {0}, {1}".format(self.vertices[self.first_city_id][1],
                                                   self.vertices[self.first_city_id][2]), \
                            org=(0,400),\
                            fontFace = cv2.FONT_HERSHEY_SIMPLEX, fontScale = 0.5,\
                            thickness = 2,\
                            color=(0,128,0),bottomLeftOrigin=False)
                # update the screen with these changes.
                # cv2.imshow("Map", self.current_map)
                cv2.imshow("Map", np.repeat(np.repeat(self.current_map, 2, axis= 0), 2, axis = 1))
                # now prepare to receive the second city.
                self.click_mode = ClickHandlerMode.SECOND_CLICK
                return

            elif self.click_mode == ClickHandlerMode.SECOND_CLICK:
                # we were waiting for the user to click on the second city, and she has just done so.
                # identify which city was selected, set the self.second_city_id variable
                # and display the selected city on screen.
                self.second_city_id = self.find_closest_city((x/2,y/2))
                cv2.putText(img=self.current_map, \
                            text="to: {0}, {1}".format(self.vertices[self.second_city_id][1],
                                                   self.vertices[self.second_city_id][2]), \
                            org=(0, 420), \
                            fontFace = cv2.FONT_HERSHEY_SIMPLEX, fontScale = 0.5,
                            thickness = 2, \
                            color=(0, 0, 128), bottomLeftOrigin=False)
                #update the screen with these changes
                # cv2.imshow("Map", self.current_map)
                cv2.imshow("Map", np.repeat(np.repeat(self.current_map, 2, axis= 0), 2, axis = 1))
                # now prepare for the search process. Any further clicks while
                #   the search is in progress will be used to advance the search
                #   step by step.
                self.click_mode = ClickHandlerMode.SEARCHING
                return
            elif self.click_mode == ClickHandlerMode.SEARCHING:
                #advance to the next step
                self.waiting_for_click = False
                return

            elif self.click_mode == ClickHandlerMode.DONE:
                # we just finished the search, and user has clicked, so let's start over
                self.reset()
                return

    def wait_for_click(self):
        """
        makes the program freeze until the user releases the mouse in the window.
        :return: None
        """
        self.waiting_for_click = True
        while self.waiting_for_click:
            cv2.waitKey(1)


    def perform_search(self,city1,city2):
        """
        finds the shortest path from self.first_city_id to self.second_city_id.
        Whether this is the shortest driving distance or the shortest time duration
        is the programmer's choice.
        :return: an array of ids that represents the path, or None, if no such
        path can be found.
        """
        result_path = []

        # -----------------------------------------
        frontier = []
        visited = []
        result_path.append(city1)
        frontier.append([0, city1, result_path])
        while(len(frontier) != 0):
            current = frontier[0]
            del(frontier[0])
            visited.append(current[1])
            distance = current[0]
            neighbors = self.get_neighbors(current[1])
            if(current[1] == city2):
                result_path = current[2]
                result_path.append(city2)
                break
            for i in neighbors:
                if (i[0] not in visited):
                    path = deepcopy(current[2])
                    path.append(i[0])
                    new_distance = distance + i[1]
                    did_loop_work = False
                    for j in range(0,len(frontier)):
                        if frontier[j][0]>= new_distance:
                            frontier.insert(j,[new_distance,i[0],path])
                            did_loop_work = True
                            break
                    if not did_loop_work or len(frontier) == 0:
                        frontier.append([new_distance,i[0],path])

        # the code shown here can be turned on to demonstrate the self.wait_for_click()
        # method. This is an OPTIONAL method you can use inside your search to allow
        # you to step through the search, waiting for the mouse to click. (I thought it
        # might be helpful.)
        """
        while True:
            print ("waiting for click")
            self.wait_for_click()
            print ("Advancing")
        """
        # -----------------------------------------
        return result_path

    def get_neighbors(self, city):
        neighbors = []
        for i in self.edges:
            if int(i[0]) == city:
                neighbors.append([int(i[1]),int(i[2])])
            elif int(i[1]) == city:
                neighbors.append([int(i[0]),int(i[2])])
        return neighbors

mp = MapConnector()
mp.start_process()

# traditionally, this will wait indefinitely until the user presses a key and
# then close the windows and quit. The loop in this program will make it so that
# it never really gets here, but it's a good habit.
cv2.waitKey()
cv2.destroyAllWindows()