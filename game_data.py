"""CSC111 Project 1: Text Adventure Game Classes

Instructions (READ THIS FIRST!)
===============================

This Python module contains the main classes for Project 1, to be imported and used by
 the `adventure` module.
 Please consult the project handout for instructions and details.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2024 CSC111 Teaching Team
"""
from typing import Optional, TextIO


class Location:
    """A location in our text adventure game world.

    Instance Attributes:
        - location_num: The designated integer number for the location in the locations.txt file
        - location_name: The name of the location
        - score: The score the player gets upon entering the location for the first time
        - brief_description: A short description of the location provided every time a player vists
        - long_description: A longer description of the location (stated only on the first visit to the location)
        - has_visited: A boolean value that indicates whether the player has visited this location before
        - actions_list: A list of actions that can be taken from this location, including commands and directions
        - x: The x-coordinate of the location
        - y: The y-coordinate of the location

    Representation Invariants:
        -
    """
    location_num: int
    location_name: str
    score: int
    brief_desc: str
    long_desc: str
    has_visited: bool
    actions_list: list[str] = []
    x: int
    y: int

    def __init__(self, location_num: int, name: str, score: int, brief_desc: str, long_desc: str) -> None:
        """Initialize a new location.

        # TODO Add more details here about the initialization if needed
        """
        self.location_num = location_num
        self.location_name = name
        self.score = score
        self.brief_desc = brief_desc
        self.long_desc = long_desc
        self.has_visited = False
        # self.x = x
        # self.y = y
        # self.map = map

        # NOTES:
        # Data that could be associated with each Location object:
        # a position in the world map,
        # a brief description,
        # a long description,
        # a list of available commands/directions to move,
        # items that are available in the location,
        # and whether the location has been visited before.
        # Store these as you see fit, using appropriate data types.
        #
        # This is just a suggested starter class for Location.
        # You may change/add parameters and the data available for each Location object as you see fit.
        #
        # The only thing you must NOT change is the name of this class: Location.
        # All locations in your game MUST be represented as an instance of this class.

        # TODO: Complete this method

    def available_actions(self) -> list[str]:
        """
        Return the available actions in this location.
        The actions should depend on the items available in the location
        and the x,y position of this location on the world map.
        """
        actions = []
        return actions

        # NOTE: This is just a suggested method
        # i.e. You may remove/modify/rename this as you like, and complete the
        # function header (e.g. add in parameters, complete the type contract) as needed

        # TODO: Complete this method, if you'd like or remove/replace it if you're not using it


class SpecialLocation(Location):
    """A location subclass that contains a riddle puzzle.

    """
    #TODO THERE IS STUFF THAT NEEDS TO BE FINISHED HERE
    puzzle: str
    answer: str
    hint: str
    success: str
    def __init__(self, location_num: int, name: str, score: int, brief_desc: str, long_desc: str,
                 puzzle: str, answer: str, hint: str, success: str):
        # TODO FINISH ADDING INITIALIZATION AND INHERITANCE CODE
        Location.__init__(self, location_num, name, score, brief_desc, long_desc)
        self.puzzle = puzzle
        self.answer = answer
        self.hint = hint
        self.success = success
        
    def available_actions(self) -> list[str]:
        actions = ['puzzle', 'hint']
        return actions
        
    def do_puzzle(self):
        print(self.puzzle)
        print("If you want to leave this puzzle,enter \'leave\'")
        print("If you want a hint, enter \'hint\'")
        response = input("Enter your answer: ")
        if response == self.answer:
            #TODO: add code to give item to player and change if puzzle is available
            print(self.success)
        elif response == self.hint:
            print(self.hint)
        else:
            print("Incorrect answer")
            



class Item:
    """An item in our text adventure game world.

    Instance Attributes:
        - name: a string name of the item
        - start_position: starting position of the item
        - # TODO

    Representation Invariants:
        - start_postion is a valid position in the world map(turn this into code)
    """
    name: str
    start_postion: int
    start_target: int
    target_points: int
    item_desc: str

    def __init__(self, name: str, start: int, target: int,
                 target_points: int, description: str) -> None:
        """Initialize a new item.
        """

        # NOTES:
        # This is just a suggested starter class for Item.
        # You may change these parameters and the data available for each Item object as you see fit.
        # (The current parameters correspond to the example in the handout).
        # Consider every method in this Item class as a "suggested method".
        #
        # The only thing you must NOT change is the name of this class: Item.
        # All item objects in your game MUST be represented as an instance of this class.

        self.name = name
        self.start_position = start
        self.target_position = target
        self.target_points = target_points
        self.item_desc = description


class Player:
    """
    A Player in the text advanture game.

    Instance Attributes:
        - x: The x coordinate of the player
        - y: The y coordinate of the player
        - inventory: The list of items the player has
        - steps: The remaining location movements the player has left
        - score: The score of the player
        - victory: A bool indicating if the player has won
        - # TODO

    Representation Invariants:
        - x >= 0
        - y >= 0
        - # TODO
    """
    x: int
    y: int
    inventory: list[Item]
    steps: int
    score: int
    victory: bool

    def __init__(self, x: int, y: int) -> None:
        """
        Initializes a new Player at position (x, y).
        """

        # NOTES:
        # This is a suggested starter class for Player.
        # You may change these parameters and the data available for the Player object as you see fit.

        self.x = x
        self.y = y
        self.inventory = []
        self.victory = False


class World:
    """A text adventure game world storing all location, item and map data.

    Instance Attributes:
        - map: a nested list representation of this world's map
        - current_location: the location that the player is currently at
        - locations_dict: dictionary of all locations
        - items_dict: dictionary of all items
        - # TODO add more instance attributes as needed; do NOT remove the map attribute
        -

    Representation Invariants:
        - # TODO
    """
    map: list[list[int]]
    current_location: Location
    locations_dict: dict[int, Location]
    items_dict: dict[int, Item]

    def __init__(self, map_data: TextIO, location_data: TextIO,
                 items_data: TextIO) -> None:
        """
        Initialize a new World for a text adventure game, based on the data in the given open files.

        - location_data: name of text file containing location data (format left up to you)
        - items_data: name of text file containing item data (format left up to you)
        """

        # NOTES:

        # map_data should refer to an open text file containing map data in a grid format, with integers separated by a
        # space, representing each location, as described in the project handout. Each integer represents a different
        # location, and -1 represents an invalid, inaccessible space.

        # You may ADD parameters/attributes/methods to this class as you see fit.
        # BUT DO NOT RENAME OR REMOVE ANY EXISTING METHODS/ATTRIBUTES IN THIS CLASS

        # The map MUST be stored in a nested list as described in the load_map() function's docstring below
        self.map = self.load_map(map_data)
        self.locations_dict = self.load_locations(location_data)
        self.items_dict = self.load_items(items_data)

        # NOTE: You may choose how to store location and item data; create your own World methods to handle these
        # accordingly. The only requirements:
        # 1. Make sure the Location class is used to represent each location.
        # 2. Make sure the Item class is used to represent each item.

    # NOTE: The method below is REQUIRED. Complete it exactly as specified.
    def load_map(self, map_data: TextIO) -> list[list[int]]:
        """
        Store map from open file map_data as the map attribute of this object, as a nested list of integers like so:

        If map_data is a file containing the following text:
            1 2 5
            3 -1 4
        then load_map should assign this World object's map to be [[1, 2, 5], [3, -1, 4]].

        Return this list representation of the map.
        """

        curr_map = []
        for line in map_data:
            row = line.split()
            curr_map.append([int(x) for x in row])

        return curr_map

        # TODO: Complete this method as specified. Do not modify any of this function's specifications.

    # TODO: Add methods for loading location data and item data (see note above).
    def load_locations(self, location_data: TextIO) -> dict[int, Location]:
        """
        Returns a dictionary of locations from the given open file location_data. A key in the dictionary is
        the location's number, and the key's item is the corresponding location object.
        """
        curr_dict = {}

        line = location_data.readline().strip()

        while line != '':
            num = int(line)
            name = location_data.readline().strip()
            score = int(location_data.readline().strip())
            brief_desc = location_data.readline().strip()

            line = location_data.readline().strip()
            long_desc = ''
            while line != 'END' and line != 'SPECIAL':
                long_desc += line + '\n'
                line = location_data.readline().strip()
                    
            if line == 'SPECIAL':
                code = location_data.readline().strip()
                hint = location_data.readline().strip()
                success = location_data.readline().strip()
                line = location_data.readline().strip()
                puzzle_desc = ''
                while line != 'END':
                    puzzle_desc += line + '\n'
                    line = location_data.readline().strip()
                curr_dict[num] = SpecialLocation(num, name, score, brief_desc, long_desc, code, hint, success, puzzle_desc)
            else:
                curr_dict[num] = Location(num, name, score, brief_desc, long_desc)
                
            location_data.readline()
            line = location_data.readline().strip()

        return curr_dict

    def load_items(self, items_data: TextIO) -> dict[int, Item]:
        """
        Returns a dictionary of items from the given open file items_data. A key in the dictionary is a location's
        number, and the key's item are the corresponding item objects found at the location.
        """
        curr_dict = {}

        line = items_data.readline().strip()
        
        while line != '':
            start_location = int(line)
            drop_location = int(items_data.readline().strip())
            drop_score = int(items_data.readline().strip())
            name = items_data.readline().strip()
            
            line = items_data.readline().strip()
            item_desc = ''
            while line != '':
                item_desc += line + '\n'
                line = items_data.readline().strip()
            curr_dict[start_location] = Item(name, start_location, drop_location, drop_score, item_desc)

            line = items_data.readline().strip()
            
        return curr_dict

    # NOTE: The method below is REQUIRED. Complete it exactly as specified.
    def get_location(self, x: int, y: int) -> Optional[Location]:
        """Return Location object associated with the coordinates (x, y) in the world map, if a valid location exists at
         that position. Otherwise, return None. (Remember, locations represented by the number -1 on the map should
         return None.)
        """
        if x < 0 or y < 0 or x > len(self.map[y]) - 1 or y > len(self.map) - 1 or self.map[y][x] == -1:
            return None
        else:
            return self.locations_dict[self.map[y][x]]

        # TODO: Complete this method as specified. Do not modify any of this function's specifications.
