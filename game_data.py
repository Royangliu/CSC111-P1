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
        - score: The amount of score gained when receiving the item
        - item_desc: the string description of the item

    Representation Invariants:
        - self.name != ''
        - self.start_postion must be a location's number in 'locations.txt' # TODO
        - self.price >= 0
        - self.currency_amount >= 0
        - self.score >= 0
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
        self.name = name
        self.start_position = start
        self.price = price
        self.currency_amount = currency_amount
        self.score = score
        self.item_desc = description


class Player:
    """A Player in the text advanture game.

    Instance Attributes:
        - x: The x coordinate of the player
        - y: The y coordinate of the player
        - steps: The remaining location movements the player has left
        - inventory: A list of all items in the player's possession
        - score: The score of the player
        - money: The player's money in dollars
        - victory: A bool indicating if the player has won
        - has_quit: A bool indicating if the player has quit

    Representation Invariants:
        - self.x >= 0
        - self.y >= 0
        - self.steps >= 0
        - self.money >= 0
    """
    x: int
    y: int
    steps: int
    inventory: list[Item]
    score: int = 0
    money: int = 0
    victory: bool = False
    has_quit: bool = False

    def __init__(self, x: int, y: int, steps: int) -> None:
        """Initializes a new Player at position (x, y) with a limited amount of allowed steps.
        """
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
        - items_list: A list of all items located at this location that can be found through the 'search' action

    Representation Invariants:
        - self.location_num >= 0
        - self.score >= 0
        - self.brief_desc != ''
        - len(self.long_dec) > len(self.brief_desc))
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

    def available_actions(self) -> list[str]:
        """Return the available actions in this location in a list.
        """
        actions = []
        if self.items_list:
            actions.append("search")

        return actions


class SpecialLocation(Location):
    """A Location subclass that contains a riddle puzzle.

    Instance Attributes:
        - contains all attributes found in the Location Class
        - answer: The string representing the answer to the puzzle
        - hint: A string representing a hint to the puzzle
        - success: A string representing the message to be displayed when the player solves the puzzle
        - puzzle: A string representing the actual puzzle
        - puzzle_complete: A boolean value indicating
        - puzzle_prize: A list of all items that the player gets when the puzzle is solved

    Representation Invariants:
        - self.answer != ''
        - self.hint != ''
        - self.success != ''
        - self.puzzle != ''

    """
    answer: str
    hint: str
    success: str
    puzzle: str
    puzzle_complete: bool
    puzzle_prize: list[Item]

    def __init__(self, location_num: int, name: str, score: int, brief_desc: str, long_desc: str,
                 answer: str, hint: str, success: str, puzzle: str) -> None:
        """Initializes a special location with its superclass. The SpecialLocation contains
        all superclass Location's attributes, as well as attributes for a riddle puzzle.
        """
        Location.__init__(self, location_num, name, score, brief_desc, long_desc)
        self.answer = answer
        self.hint = hint
        self.success = success
        self.puzzle = puzzle
        self.puzzle_complete = False
        self.puzzle_prize = []

    def available_actions(self) -> list[str]:
        """Return the available actions in this location in a list.
        Adds all possible actions from the superclass Location and
        adds the option of "puzzle" if this SpecialLocation's puzzle is not completed.
        """
        actions = []
        actions += Location.available_actions(self)
        if not self.puzzle_complete:
            actions.append('puzzle')

        return actions

    def do_puzzle(self) -> list[Item]:
        """A function allowing user to attempt a puzzle.
        If they succeed, give them the appropriate item.
        It also allows for hints to be given, or the appropriate reponse to be given if they fail.
        """
        puzzle_items = []

        print('Puzzle/Riddle:')
        print(self.puzzle)
        print("\nOther Actions: \'leave\', \'hint\'")

        in_puzzle = True
        while in_puzzle:
            response = input("Enter your answer: ")
            print()
            if response == self.answer:
                print(self.success)
                puzzle_items = self.puzzle_prize
                self.puzzle_complete = True
                self.puzzle_prize = []
                in_puzzle = False
            elif response == 'hint':
                print(self.hint)
            elif response == 'leave':
                in_puzzle = False
            else:
                print("Incorrect answer")

        return puzzle_items


class ShopLocation(Location):
    """A Location subclass that represents a shop and contains methods for the player to exchange money for items.
    Items stored in shop_list indicate the items that can be bought.

    Instance Attributes:
        - contains all attributes found in the Location Class
        - shop_list: A list of all items that can be bought at the shop.

    Representation Invariants:
        - # TODO
    """
    shop_list: list[Item]

    def __init__(self, location_num: int, name: str, score: int, brief_desc: str, long_desc: str) -> None:
        """Initializes a new shop location with its superclass. The ShopLocation contains
        all superclass Location's attributes, as well as shop_list.
        """
        Location.__init__(self, location_num, name, score, brief_desc, long_desc)
        self.shop_list = []

    def available_actions(self) -> list[str]:
        """Return the available actions in this location in a list.
        Adds all possible actions from the superclass Location and
        adds the option of "shop" if this ShopLocation's shop_list is not empty

        Preconditions:
            - # TODO
        """
        actions = []
        actions += Location.available_actions(self)
        if self.shop_list:
            actions.append("shop")

        return actions

    def do_buy(self, player: Player) -> None:
        """Function that handles the buying of an item by putting the player into an input loop until they leave.

        If an item is successfully bought from the shop, the item is appended into the player's inventory, the
        item is deleted from this shop's shop_list, and the player's money is deduced according to the item's price.

        Precondtions:
            - # TODO
        """
        print("To leave the shop menu, enter: \'leave\'")
        print("To view the items available, enter: \'shop list\'")

        in_shop = True
        while in_shop:
            choice = input("\nWhat would you like to buy?: ")
            print()

            # Handles other shop menu options
            if choice == 'leave':
                in_shop = False
            elif choice == 'shop list':
                print("Shop List:")
                for item in self.shop_list:
                    print(f"{item.name}: ${item.price}")

            elif self.item_in_shop_list(choice):
                item = self.remove_item_in_shop(choice)

                # buys the item if the player has enough money
                if player.money >= item.price:
                    print(item.item_desc)
                    player.money -= item.price
                    player.score += item.score
                    print(f"\nYou got {item.score} points for getting (a) {item.name}!")
                    player.inventory.append(item)

                # restores the item if the item exists, but the player doesn't have enough money
                else:
                    print("Insufficient money; you are broke.")
                    self.items_list.append(item)

            else:
                print("Item not found.")

    def item_in_shop_list(self, item_name: str) -> bool:
        """Returns whether the item with the specified name exists in this object's shop_list

        Preconditions:
            - item_name != ''
        """
        for i in range(len(self.shop_list)):
            if self.shop_list[i].name == item_name:
                return True

        return False

    def remove_item_in_shop(self, item_name: str) -> Optional[Item]:
        """Removes the item with the specified item_name from this object's shop_list and return's it.
        If it's not in shop_list, return None.

        Preconditions:
            - item_name != ''
        """
        for i in range(len(self.shop_list)):
            if self.shop_list[i].name == item_name:
                return self.shop_list.pop(i)

        return None


class World:
    """A text adventure game world storing all location, item and map data.

    Instance Attributes:
        - map: a nested list representation of this world's map
        - locations_dict: dictionary of all locations. Each key is the location's number and
            its item is the corresponding location object

    Representation Invariants:
        - # TODO
    """
    map: list[list[int]]
    locations_dict: dict[int, Location | SpecialLocation | ShopLocation]

    def __init__(self, map_data: TextIO, location_data: TextIO, items_data: TextIO) -> None:
        """
        Initialize a new World for a text adventure game, based on the data in the given open files.

        - location_data: name of text file containing location data (format left up to you)
        - items_data: name of text file containing item data (format left up to you)
        """
        self.map = self.load_map(map_data)
        self.locations_dict = self.load_locations(location_data)
        self.load_items(items_data)

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

    def load_locations(self, location_data: TextIO) -> dict[int, Location]:
        """Returns a dictionary of locations from the given open file location_data. A key in the dictionary is
        the location's number, and the key's item is the corresponding location object.

        The locations should be formatted as such in the locations.txt file:
        - Normal Location:
            <location number>
            <name>
            <points upon first enter>
            <brief description>
            <long description (can be multilined)>
            END
        - Shop Location:
            <location number>
            <name>
            <points upon first enter>
            <brief description>
            <long description (can be multilined)>
            SHOP
        - Puzzle Location:
            <location number>
            <name>
            <points upon first enter>
            <brief description>
            <long description (can be multilined)>
            PUZZLE
            <Code>
            <hint>
            <success message>
            <puzzle_desc (can be multilined)>
            END
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
            while line not in {'END', 'SPECIAL', 'SHOP'}:
                long_desc += line + '\n'
                line = location_data.readline().strip()

            long_desc = long_desc[:-1]  # removes last '\n' character.

            # instanciates the location object depending on the type specified in the locations data file
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
                puzzle_desc = puzzle_desc[:-1]  # removes last '\n' character.

                curr_dict[num] = SpecialLocation(num, name, score, brief_desc, long_desc,
                                                 code, hint, success, puzzle_desc)
            elif line == 'SHOP':
                curr_dict[num] = ShopLocation(num, name, score, brief_desc, long_desc)

            else:
                curr_dict[num] = Location(num, name, score, brief_desc, long_desc)

            location_data.readline()
            line = location_data.readline().strip()

        return curr_dict

    def load_items(self, items_data: TextIO) -> None:
        """Loads the items found within items.txt to their respective locations in this object's location_dict

        Where the item is stored in the Location object depends on its specified type in the items.txt file.
        - The item is stored within the location's item_list if its type is 'TAKE'.
        - The item is stored within the location's puzzle_prize if its type is 'PUZZLE'.
        - The item is stored within the location's shop_list if its type is 'SHOP'.

        Each item should have the following format in the items.txt file:
            <name>
            <start_position>
            <price_in_shop (default 0)>
            <currency_value (default 0)>
            <score_on_pickup>
            <item_type>
            <item_desc (can be multilined)>
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
            item_type = items_data.readline().strip()

            # initializes the description of the item
            line = items_data.readline().strip()
            item_desc = ''
            while line != '':
                item_desc += line + '\n'
                line = items_data.readline().strip()
            item_desc = item_desc[:-1]  # removes last '\n' character.

            # instanciates the item object and adds it to the starting location's items list
            if item_type == 'TAKE':
                self.locations_dict[start_location].items_list.append(Item(name, start_location, price,
                                                                           currency_value, score, item_desc))

            elif item_type == 'PUZZLE' and isinstance(self.locations_dict[start_location], SpecialLocation):
                self.locations_dict[start_location].puzzle_prize.append(Item(name, start_location, price,
                                                                             currency_value, score, item_desc))

            elif item_type == 'SHOP' and isinstance(self.locations_dict[start_location], ShopLocation):
                self.locations_dict[start_location].shop_list.append(Item(name, start_location, price,
                                                                          currency_value, score, item_desc))

            line = items_data.readline().strip()

    # NOTE: The method below is REQUIRED. Complete it exactly as specified.
    def get_location(self, x: int, y: int) -> Optional[Location]:
        """Return Location object associated with the coordinates (x, y) in the world map, if a valid location exists at
         that position. Otherwise, return None. (Remember, locations represented by the number -1 on the map should
         return None.)
        """
        if x < 0 or y < 0 or x >= len(self.map[y]) or y >= len(self.map) or self.map[y][x] == -1:
            return None
        else:
            return self.locations_dict[self.map[y][x]]


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)

    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (In PyCharm, select the lines below and press Ctrl/Cmd + / to toggle comments.)
    # You can use "Run file in Python Console" to run PythonTA,
    # and then also test your methods manually in the console.
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120
    })
