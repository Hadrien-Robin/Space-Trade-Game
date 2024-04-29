"""
This file contains all definition related to the game map, its generation and its updates.

The Galaxy class contains all the data of the galaxy map.

The Galaxy class has the following methods:
    generate: generate a map
    update_object: update an object in the map

The Galaxy class has the following attributes:
    stars: list containing all the stars on the map.
    way: list of all the interstellar pathways.
"""

import random
import os
import math
from components import ressource_path



class Galaxy:
    """
    Galaxy class object
    """

    def __init__(self):
        self.size = 4
        self.stars = {}
        self.way = []
        self.generate()
        print(self.stars)
        this_one = list(self.stars.keys())[0]
        self.stars[this_one].explore()
        self.initiate_camera()

    def generate(self):
        ALPHA = 1       #this control the distance impact on the probabily of having a pathway between two stars.
        MIN_DIST = 0.5  #minimum distance between two stars
        database_dir = os.path.abspath(os.path.join(ressource_path(), '..', 'database'))
        names_list = set(line.strip() for line in open(os.path.join(database_dir,'star_names.txt')))

        crd_so_far = []
        while len(self.stars) < self.size**2:
            check_flag = True
            new_crd = [0,0]
            while check_flag: #condition of coordinates
                new_crd = [random.uniform(0.1, self.size),random.uniform(0.1, self.size)]
                check_flag = False
                for coord in crd_so_far:
                    if ((new_crd[0] - coord[0])**2 + (new_crd[1] - coord[1])**2) < MIN_DIST**2:
                        check_flag = True
                        break        
            crd_so_far.append(new_crd)
            selected_name = random.choice(list(names_list))
            names_list.remove(selected_name)
            self.stars.update({selected_name:Star(selected_name,new_crd)})
    
        for system in self.stars.values():
            print(system.name,system.coordinates)
        
        system_list = list(self.stars)
        star_numb = self.size**2
        self.way = [[0 for _ in range(star_numb)] for _ in range(star_numb)]

        
        for i in range(star_numb):
            for j in range(star_numb):
                if j > i:
                    x1,y1 = self.stars[system_list[i]].coordinates
                    x2,y2 = self.stars[system_list[j]].coordinates
                    dis = math.sqrt((x1-x2)**2 + (y1-y2)**2)
                    Prob = math.exp(-ALPHA*(dis - MIN_DIST))
                    rand = random.uniform(0,1)
                    if rand <= Prob:
                         self.way[i][j] = 1 
                if j < i:
                    self.way[i][j] = self.way[j][i]
                        
        for row in self.way:
            print(row)

        node_visited = []
        queue = []

        def check_bfs(visited, matrix, node=0):
            node_visited = []
            queue = []
            visited.append(node)
            queue.append(node)

            while queue:
                m = queue.pop(0)
                print(m,end = " ")

                for neighbour in [idx for idx, val in enumerate(matrix[m]) if val != 0]:
                    if neighbour not in visited:
                        visited.append(neighbour)
                        queue.append(neighbour)
            print("length :",len(visited))
            return visited
        
        node_visited = check_bfs(node_visited,self.way)
        while (len(node_visited) != star_numb):
            node = set(range(0,star_numb)).difference(node_visited)
            for i in node:
                for j in range(star_numb):
                    if j > i:
                        x1,y1 = self.stars[system_list[i]].coordinates
                        x2,y2 = self.stars[system_list[j]].coordinates
                        dis = math.sqrt((x1-x2)**2 + (y1-y2)**2)
                        Prob = math.exp(-ALPHA*(dis - MIN_DIST))
                        rand = random.uniform(0,1)
                        if rand <= Prob:
                             self.way[i][j] = 1 
            for j in node:
                for i in range(star_numb):
                    if j > i:
                        self.way[i][j] = self.way[j][i]
            node_visited = check_bfs(node_visited,self.way)

            for row in self.way:
                print(row)
                
    def initiate_camera(self):
        self.zoom_level = {1:self.size, 2:(self.size+1)/2, 3:1}
        self.current_zoom = self.size
        self.camera_pos = [0,0]
    
    def move_camera(self,direction):
        match direction:
            case "right":            
                self.camera_pos = self.camera_pos + [0.05,0]*self.current_zoom
                if self.camera_pos[1] > self.size - self.current_zoom:
                    self.camera_pos = self.size - self.current_zoom
            case "left":
                self.camera_pos = self.camera_pos - [0.05,0]*self.current_zoom
                if self.camera_pos[1] < 0:
                    self.camera_pos = 0
            case "down":
                self.camera_pos = self.camera_pos - [0,0.05]*self.current_zoom
                if self.camera_pos[0] < 0:
                    self.camera_pos = 0
            case "up":
                self.camera_pos = self.camera_pos + [0,0.05]*self.current_zoom
                if self.camera_pos[0] > self.size - self.current_zoom:
                    self.camera_pos = self.size - self.current_zoom
            case "zoom":
                for key,value in self.current_zoom.items():
                    if value == 1:
                        self.current_zoom = self.zoom_level[1]
                        break
                    elif value == self.current_zoom:
                        self.current_zoom = self.zoom_level[key+1]
                        break
            
    def select_visible_star(self):
        minX = self.camera_pos[0] 
        maxX = self.camera_pos[0] + self.current_zoom
            
        minY = self.camera_pos[1]
        maxY = self.camera_pos[1] + self.current_zoom
        
        self.visible_stars = [False for i in range(len(self.stars))]
        self.vs_way = [[False for i in range(len(self.stars))] for j in range(len(self.stars))]
        ind = 0
        for star in self.stars.values():
            x,y = star.coordinates
            if minX <= x <= maxX and minY <= y <= maxY:
                self.visible_stars[ind] = True
                for i in range(0, ind):
                    if self.visible_stars[i] and self.way[ind][i]:
                        self.vs_way[ind][i] = True
            ind += 1

        print("len(visible_stars)",len(self.visible_stars))
        

        return self.visible_stars
    
class Star:
    """
    Star class object

    """

    def __init__(self,name,crd):
        self.coordinates = crd
        self.name = name
        self.type = 'M'
        self.objects = []
        
    def explore(self):
        """
        Explore the system and populate it
        """
        print("populating",self.name)

        while len(self.objects) <= 10:
            if random.uniform(0,1) <= 0.8:
                self.objects.append(System_object(self,"rocky planet"))
            else:
                break

        rand = random.uniform(0,1)
        if  rand <= 0.8:
            self.objects.append(System_object(self,"asteroid belt"))

        for it in range(0,2):
            if random.uniform(0,1) <= 0.5:
                self.objects.append(System_object(self,"gas giant"))

        if rand <= 0.1:
            self.objects.append(System_object(self,"asteroid belt"))

        for it in range(0,2):
            if random.uniform(0,1) <= 0.5:
                self.objects.append(System_object(self,"icy giant"))

        print("populated with ",len(self.objects), " object(s).")
        
class System_object:
    """
    System objects class
    """

    def __init__(self,star,obj_type):
        self.type = obj_type
        self.name = star.name
        self.permit = False
        self.grid = []
        self.size = 0
        self.image_id = None
        self.populated = False
        LETTER_NAME = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p']
        self.generate_surface()
        if obj_type != "asteroid belt":
            self.name += ' ' + LETTER_NAME[len(star.objects) - sum(1 for Ob in star.objects if Ob.type == "asteroid belt") + 1]
        else:
            self.name = star.name +"'s asteroid belt"
            for it in star.objects:
                if it.name == "asteroid belt":
                    self.name += " II"
        print("Generated a(n) ",self.type, " named ", self.name)

    def generate_surface(self):
        """ Create a dictionnary containing spiraling position on a grid up to 21 squares"""

        pos_register = {'0': [3, 3], '1': [3, 4], '2': [4, 3], '3':[3, 2], '4': [2, 3],
                        '5': [2, 4], '6': [4, 4], '7': [4, 2], '8': [2, 2], '9': [3, 5],
                        '10': [5, 3], '11': [3, 1], '12': [1, 3], '13': [2, 5], '14': [4, 5],
                        '15': [5, 4], '16':[5,2], '17':[4,1], '18':[2,1], '19':[1,2],
                        '20':[1,4]}
        if self.type == "rocky planet":
            self.size = random.randint(2,5)
            for i in range(0,self.size):
                square = Square(pos_register[str(i)])
                rand = random.randint(0, 6)
                match rand:
                    case 1:
                        square.ressource = "Ice"
                    case 2:
                        square.ressource = "Coal"
                    case 3:
                        square.ressource = "Iron"
                    case 4:
                        square.ressource = "Oil"
                    case 5:
                        square.ressource = "Uranium"
                    case 6:
                        square.ressource = "Titanium"
                self.grid.append(square)
            check_pop = random.randint(0, 3)
            if check_pop == 0:
                self.populated = True    
                
        elif self.type == "gas giant":
            self.size = random.randint(10,16)
            for i in range(0, self.size):
                square = Square(pos_register[str(i)])
                rand = random.randint(0, 3)
                match rand:
                    case 1:
                        square.ressource = "Methane"
                    case 2:
                        square.ressource = "Helium"
                    case 3:
                        square.ressource = "Hydrogen"
                        
                self.grid.append(square)
            check_pop = random.randint(0, 6)
            if check_pop == 0:
                self.populated = True
                
        elif self.type == "icy giant":
            self.size = random.randint(8,12)
            for i in range(0, self.size):
                square = Square(pos_register[str(i)])
                rand = random.randint(0, 3)
                match rand:
                    case 1:
                        square.ressource = "Hydrogen"
                    case 2:
                        square.ressource = "Methane"
                    case 3:
                        square.ressource = "Helium"

                self.grid.append(square)
            check_pop = random.randint(0, 5)
            if check_pop == 0:
                self.populated = True

        elif self.type == "asteroid belt":
            self.size = random.randint(1,3)
            for i in range(0, self.size):
                square = Square(pos_register[str(i)])
                rand = random.randint(0, 3)
                match rand:
                    case 1:
                        square.ressource = "Ice"
                    case 2:
                        square.ressource = "Titanium"
                    case 3:
                        square.ressource = "Iron"
                        
                self.grid.append(square)
            check_pop = random.randint(0, 9)
            if check_pop == 0:
                self.populated = True
        
        if self.populated:
            self.grid[0].content = 'settlement'
            
class Square:
    def __init__(self,pos):
        
        self.content = -1
        self.ressource = -1
        
        self.position = pos
   