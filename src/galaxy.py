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

class Galaxy:
    """
    Galaxy class object
    """

    def __init__(self):
        self.size = 4
        self.stars = {}
        self.way = {}
        self.generate()


    def generate(self):
        database_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database'))
        names_list = set(line.strip() for line in open(os.path.join(database_dir,'star_names.txt')))
        crd_so_far = {}
        while len(self.stars) < self.size**2:
            check_flag = True
            new_crd = [0,0]
            while check_flag: #condition of coordinates
                new_crd = [random.uniform(0.1, self.size),random.uniform(0.1, self.size)]
                check_flag = False
                for coord in crd_so_far:
                    if (new_crd[0] - crd_so_far[0])**2 + (new_crd[1] - crd_so_far[1])**2 < 0.5:
                        check_flag = True
                        break
                            
            selected_name = random.choice(list(names_list))
            names_list.remove(selected_name)
            self.stars.update({selected_name:Star(selected_name,new_crd)})
    
        for system in self.stars.values():
            print(system.coordinates)
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
