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


class Item:
    """An item in our text adventure game world.

    Instance Attributes:
        - name: a string name of the item
        - start_position: starting position of the item
        - price: the price of the item at a store location
        - currency_amount: the number of money the player gets for picking the item up
        - item_desc: the string description of the item
        - # TODO

    Representation Invariants:
        - start_postion is a valid position in the world map(turn this into code)
    """
    name: str
    start_position: int
    price: int
    currency_amount: int
    score: int
    item_desc: str

    def __init__(self, name: str, start: int, price: int,
                 currency_amount: int, score: int, description: str) -> None:
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
        self.price = price
        self.currency_amount = currency_amount
        self.score = score
        self.item_desc = description


class Player:
    """
    A Player in the text advanture game.

    Instance Attributes:
        - x: The x coordinate of the player
        - y: The y coordinate of the player
        - steps: The remaining location movements the player has left
        - inventory: A list of all items in the player's possession
        - score: The score of the player
        - money: The player's money in dollars
        - victory: A bool indicating if the player has won
        - # TODO

    Representation Invariants:
        - x >= 0
        - y >= 0
        - # TODO
    """
    x: int
    y: int
    steps: int
    inventory: list[Item]
    score: int = 0
    money: int = 0
    victory: bool = False

    def __init__(self, x: int, y: int, steps: int) -> None:
        """
        Initializes a new Player at position (x, y).
        """

        # NOTES:
        # This is a suggested starter class for Player.
        # You may change these parameters and the data available for the Player object as you see fit.

        self.x = x
        self.y = y
        self.steps = steps
        self.inventory = []


class Location:
    """A location in our text adventure game world.

    Instance Attributes:
        - location_num: The designated integer number for the location in the locations.txt file
        - location_name: The name of the location
        - score: The score the player gets upon entering the location for the first time
        - brief_description: A short description of the location provided every time a player vists
        - long_description: A longer description of the location (stated only on the first visit to the location)
        - has_visited: A boolean value that indicates whether the player has visited this location before
        - items_list: A list of all items located at this location

    Representation Invariants:
        - # TODO
    """
    location_num: int
    location_name: str
    score: int
    brief_desc: str
    long_desc: str
    has_visited: bool
    items_list: list[Item]

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
        self.items_list = []
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
        if self.items_list != []:
            actions.append("search")

        return actions

        # NOTE: This is just a suggested method
        # i.e. You may remove/modify/rename this as you like, and complete the
        # function header (e.g. add in parameters, complete the type contract) as needed

        # TODO: Complete this method, if you'd like or remove/replace it if you're not using it


class SpecialLocation(Location):
    """A location subclass that contains a riddle puzzle.
    Instance Attributes:
        - location_num: The designated integer number for the location in the locations.txt file
        - location_name: The name of the location
        - score: The score the player gets upon entering the location for the first time
        - brief_description: A short description of the location provided every time a player vists
        - long_description: A longer description of the location (stated only on the first visit to the location)
        - has_visited: A boolean value that indicates whether the player has visited this location
 before
        - items_list: A list of all items located at this location
        - answer: The string representing the answer to the puzzle
        - hint: A string representing a hint to the puzzle
        - success: A string representing the message to be displayed when the player solves the puzzle
        - puzzle: A string representing the actual puzzle
        - puzzle_complete: A boolean value indicating

    """
    #TODO THERE IS STUFF THAT NEEDS TO BE FINISHED HERE
    answer: str
    hint: str
    success: str
    puzzle: str
    puzzle_complete: bool

    def __init__(self, location_num: int, name: str, score: int, brief_desc: str, long_desc: str, answer: str, hint: str, success: str,  puzzle: str) -> None:
        # TODO FINISH ADDING INITIALIZATION AND INHERITANCE CODE
        Location.__init__(self, location_num, name, score, brief_desc, long_desc)
        self.answer = answer
        self.hint = hint
        self.success = success
        self.puzzle = puzzle
        self.puzzle_complete = False

    def available_actions(self) -> list[str]:
        """
        Return the available actions in this location.
        """
        actions = []
        if not self.puzzle_complete:
            actions.append('puzzle')

        return actions

    def do_puzzle(self) -> list[Item]:
        """
        A function allowing user to attempt a puzzle.
        If they succeed, give them the appropriate item.
        It also allows for hints to be given, or the appropriate reponse to be given if they fail.
        """
        print('Puzzle/Riddle:')
        print(self.puzzle)
        print("\nOther Actions: \'leave\', \'hint\'")
        response = input("Enter your answer: ")
        print()
        while response != 'leave':
            if response == self.answer:
                #TODO: add code to give item to player and change if puzzle is available
                print(self.success)
                return self.items_list
            elif response == 'hint':
                print(self.hint)
            else:
                print("Incorrect answer")
            response = input("\nEnter your answer: ")
        return []


class ShopLocation(Location):
    """A location subclass that contains a shop. Items stored in this class indicates the items that can be bought.

    Instance Attributes:
        -
    """
    def __init__(self, location_num: int, name: str, score: int, brief_desc: str, long_desc: str) -> None:
        # TODO
        Location.__init__(self, location_num, name, score, brief_desc, long_desc)

    def available_actions(self) -> list[str]:
        """
        Return the available actions in this location.
        """
        actions = []
        if self.items_list:
            actions.append("shop")

        return actions

    def do_buy(self, player: Player) -> None:
        """Handels the buying of an item.
        """
        bought_item = False

        print("To leave the shop menu, enter: \'leave\'")
        print("To view the items available, enter: \'shop list\'")
        while not bought_item:
            choice = input("\nWhat would you like to buy?: ").lower()
            print()
            
            if choice == 'leave':
                bought_item = True
            elif choice == 'shop list':
                print("Shop List:")
                for item in self.items_list:
                    print(f"{item.name}: ${item.price}")
            else:
                item_found = False
                
                for i in range(len(self.items_list)):
                    if choice == self.items_list[i].name and player.money >= self.items_list[i].price:
                        player.money -= self.items_list[i].price
                        player.score += self.items_list[i].score
                        print(self.items_list[i].item_desc)
                        player.inventory.append(self.items_list.pop(i))
                    elif choice == self.items_list[i].name and player.money < self.items_list[i].price:
                        print("Insufficient money; you are broke.")  
                        
            if not item_found:
                print("Item not found.")


class World:
    """A text adventure game world storing all location, item and map data.

    Instance Attributes:
        - map: a nested list representation of this world's map
        - current_location: the location that the player is currently at
        - locations_dict: dictionary of all locations
        - # TODO add more instance attributes as needed; do NOT remove the map attribute
        -

    Representation Invariants:
        - # TODO
    """
    map: list[list[int]]
    current_location: Location
    locations_dict: dict[int, Location]

    def __init__(self, map_data: TextIO, location_data: TextIO, items_data: TextIO) -> None:
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
        self.load_items(items_data)

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

        # stops upon reaching the end of the file
        while line != '':
            # initiailizes attributes of the location
            num = int(line)
            name = location_data.readline().strip()
            score = int(location_data.readline().strip())
            brief_desc = location_data.readline().strip()

            # initializes the long description of the location
            line = location_data.readline().strip()
            long_desc = ''
            while line != 'END' and line != 'SPECIAL' and line != 'SHOP':
                long_desc += line + '\n'
                line = location_data.readline().strip()

            long_desc = long_desc[:-1] # removes last '\n' character.

            # instanciates the location object depending on if it is a special location or not
            if line == 'SPECIAL':
                # initializes puzzle attributes in the location
                code = location_data.readline().strip()
                hint = location_data.readline().strip()
                success = location_data.readline().strip()

                # initializes the puzzle description of the location
                line = location_data.readline().strip()
                puzzle_desc = ''
                while line != 'END':
                    puzzle_desc += line + '\n'
                    line = location_data.readline().strip()
                puzzle_desc = puzzle_desc[:-1] # removes last '\n' character.

                curr_dict[num] = SpecialLocation(num, name, score, brief_desc, long_desc, code, hint, success, puzzle_desc)
            elif line == 'SHOP':
                curr_dict[num] = ShopLocation(num, name, score, brief_desc, long_desc)
            else:
                curr_dict[num] = Location(num, name, score, brief_desc, long_desc)

            location_data.readline()
            line = location_data.readline().strip()

        return curr_dict

    def load_items(self, items_data: TextIO):
        """Loads the items found within items.txt to their respective locations
        """
        line = items_data.readline().strip()

        # stops upon reaching the end of the file
        while line != '':
            # initiailizes attributes of the item
            name = line
            start_location = int(items_data.readline().strip())
            price = int(items_data.readline().strip())
            currency_value = int(items_data.readline().strip())
            score = int(items_data.readline().strip())

            # initializes the description of the item
            line = items_data.readline().strip()
            item_desc = ''
            while line != '':
                item_desc += line + '\n'
                line = items_data.readline().strip()
            item_desc = item_desc[:-1] # removes last '\n' character.

            # instanciates the item object and adds it to the starting location's items list
            self.locations_dict[start_location].items_list.append(Item(name, start_location, price, currency_value, score, item_desc))

            line = items_data.readline().strip()

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
