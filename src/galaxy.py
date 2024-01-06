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



class Galaxy:
    """
    Galaxy class object
    """

    def __init__(self):
        self.size = 4
        self.stars = {}
        self.way = []
        self.generate()


    def generate(self):
        ALPHA = 1       #this control the distance impact on the probabily of having a pathway between two stars.
        MIN_DIST = 0.5  #minimum distance between two stars
        database_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database'))
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
        
    def explore(self):
        """
        Explore the system and populate it
        """
        print("populating",self.name)