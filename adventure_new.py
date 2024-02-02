"""CSC111 Project 1: Text Adventure Game

Instructions (READ THIS FIRST!)
===============================

This Python module contains the code for Project 1. Please consult
the project handout for instructions and details.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2024 CSC111 Teaching Team
"""

# Note: You may add in other import statements here as needed
from game_data import World, Item, Location, Player

# Note: You may add helper functions, classes, etc. here as needed

# Note: You may modify the code below as needed; the following starter template are just suggestions
if __name__ == "__main__":
    w = World(open("map.txt"), open("locations.txt"), open("items.txt"))
    p = Player(100000000, 0)  # set starting location of player; you may change the x, y coordinates here as appropriate
    steps = 30
    score = 0
    menu = ["look", "inventory", "score", "map", "quit"]

    previous_x = p.x
    previous_y = p.y

    while not p.victory and steps > 0:
        location = w.get_location(p.x, p.y)

        if location is None:
            raise ValueError("Invalid location")
        else:

        # TODO: ENTER CODE HERE TO PRINT LOCATION DESCRIPTION
        if location.has_visited:
            print(location.brief_desc)
        else:
            print(location.long_desc)
            location.has_visited = True
        # Depending on whether or not it's been visited before,
        # print either full description (first time visit) or brief description (every subsequent visit)

        print("What to do? \n")
        print("[menu]")

        choice = input("\nEnter action: ")

        loc_change = False
        while not loc_change:



            if choice not in menu and choice not in location.available_actions():
                choice = input("\nInvalid action. Try again: ")
            elif choice not in movement_options(p.x, p.y, w.map):
                choice = input("\nInvalid movement. Try again: ")
            elif choice == "[menu]":
                print("Menu Options: \n")
                for option in menu:
                    print(option)
                choice = input("\nChoose action: ")
            elif choice == "look":
                print(location.long_desc)
                choice = input("\nChoose action: ")
            elif choice == "inventory":
                print(p.inventory)
                choice = input("\nChoose action: ")
            elif choice == "score":
                print(" \n the score is " + str(score))
                choice = input("\nChoose action: ")
            elif choice == "map":
                for row in w.map:
                    print("\n" + str(row))
            # TODO: CREATE MORE POTENTIAL ACTIONS




        # TODO: CALL A FUNCTION HERE TO HANDLE WHAT HAPPENS UPON THE PLAYER'S CHOICE
        #  REMEMBER: the location = w.get_location(p.x, p.y) at the top of this loop will update the location if
        #  the choice the player made was just a movement, so only updating player's position is enough to change the
        #  location to the next appropriate location
        #  Possibilities:
        #  A helper function such as do_action(w, p, location, choice)
        #  OR A method in World class w.do_action(p, location, choice)
        #  OR Check what type of action it is, then modify only player or location accordingly
        #  OR Method in Player class for move or updating inventory
        #  OR Method in Location class for updating location item info, or other location data etc....
def move_player(direction: str, p: Player) -> None:
    if direction == "east":
        p.x += 1
    elif direction == "south":
        p.y += 1
    elif direction == "north":
        p.y -= 1
    elif direction == "west":
        p.x -= 1

def
