"""
This module contains the definitions, variables and everything else necessary for handling save files

The Memory class contains  all the game variables.

The Memory class has the following methods:
    load: called when a file should be read and transfer to the current Memory instance
    save: called when the current Memory instance should be transfer to a (new) file


The Memory class has the following attributes:
    player: all info concerning the player
    map: the map of the galaxy in its current state (not implemented)
"""
import os
import json
from galaxy import Galaxy

class Memory:
    """
    Memory class object
    """

    def __init__(self):
        self.Pilote = {}
        self.Business ={}
        self.Player = {}
        self.Galaxy = Galaxy()

    def save(self, file_name):
        print(file_name)
        file_name += '.json'
        save_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'save'))
        try:
            with open(os.path.join(save_dir,file_name), 'wb') as file:
                json.dump(self, file)
                print("Game state saved successfully!")
        except (IOError,ValueError):
            print("Error: Unable to save game state.")

    
    def load(self, file_name):
        print(file_name)
        file_name += '.json'
        save_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'save'))
        try:
            with open(file_name, 'rb') as file:
                game_state = json.load(file)
                print("Game state loaded successfully!")
                return game_state
        except (IOError,ValueError):
            print("Error: Unable to load game state.")
        
    def move_player(self,system):
        self.Player.update({"System":system})
        
