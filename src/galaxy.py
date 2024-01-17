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
        self.grid = []
        self.size = 0
        self.populated = False
        LETTER_NAME = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o']
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
        """ Create a dictionnary containing spiraling position on a grid up to 16 squares"""

        pos_register = {'0': [0, 0], '1': [0, 1], '2': [1, 0], '3':[0, -1], '4': [-1, 0],
                        '5': [-1, 1], '6': [1, 1], '7': [1, -1], '8': [-1, -1], '9': [0, 2],
                        '10': [2, 0], '11': [0, -2], '12': [-2, 0], '13': [-1, 2], '14': [1, 2],
                        '15': [2, 1], '16':[2,-1], '17':[1,-2], '18':[-1,-2], '19':[-2,-1],
                        '20':[-2,1]}
        if self.type == "rocky planet":
            self.size = random.randint(2,5)
            for i in range(0,self.size):
                square = Square(pos_register[str(i)])
                rand = random.randint(0, 6)
                match rand:
                    case 1:
                        square.ressource = "ice"
                    case 2:
                        square.ressource = "coal"
                    case 3:
                        square.ressource = "iron"
                    case 4:
                        square.ressource = "oil"
                    case 5:
                        square.ressource = "uranium"
                    case 6:
                        square.ressource = "titanium"
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
                        square.ressource = "methane"
                    case 2:
                        square.ressource = "helium"
                    case 3:
                        square.ressource = "hydrogen"
                        
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
                        square.ressource = "hydrogen"
                    case 2:
                        square.ressource = "methane"
                    case 3:
                        square.ressource = "helium"

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
                        square.ressource = "ice"
                    case 2:
                        square.ressource = "titanium"
                    case 3:
                        square.ressource = "iron"
                        
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
        

        