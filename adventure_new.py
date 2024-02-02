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
def move_player(direction: str, p: Player) -> None:
    """moves the player by changing the player's x and y coordinates
    """
    if direction == "east":
        p.x += 1
    elif direction == "south":
        p.y += 1
    elif direction == "north":
        p.y -= 1
    elif direction == "west":
        p.x -= 1

def do_menu_action(action: str, player: Player, location: Location, world: World):
    """executes actions found within the menu
    """
    if action == "look":
        print(location.long_desc)
        action = input("\nChoose action: ")
    elif action == "inventory":
        print(player.inventory)
        action = input("\nChoose action: ")
    elif action == "score":
        print(" \n the score is " + str(score))
        action = input("\nChoose action: ")
    elif action == "map":
        for row in world.map:
            print("\n" + str(row))
        
        
# Note: You may modify the code below as needed; the following starter template are just suggestions
if __name__ == "__main__":
    with open('map.txt') as map_file, open('locations.txt') as location_file, open('items.txt') as item_file:
        w = World(map_file, location_file, item_file)

    p = Player(0, 0)  # set starting location of player; you may change the x, y coordinates here as appropriate
    steps = 30
    score = 0
    menu = ["look", "inventory", "score", "map", "quit"]
    directions = ["north", "east", "south", "west"]

    previous_x = p.x
    previous_y = p.y

    while not p.victory and steps > 0:
        location = w.get_location(p.x, p.y)
        
        if location is None:
            p.x = previous_x
            p.y = previous_y
            steps += 1
            print("Invalid movement input. Try again.\n")
        else:
            if location.has_visited:
                print(location.brief_desc)
            else:
                print(location.long_desc)
                location.has_visited = True

        
            loc_change = False
            while not loc_change:
                print("What to do? \n")
                choice = input("\nEnter action: ").lower()
                
                if choice == "[menu]":
                    print("Menu Options: \n")
                    for option in menu + location.actions_list:
                        print(option)
                elif choice in menu:
                    do_menu_action(choice, p, location, w)
                elif choice in location.actions_list:
                    pass # TODO
                elif choice in directions:
                    previous_x = p.x
                    previous_y = p.y
                    move_player(choice, p)
                    loc_change = True
                    steps -= 1
                else:
                    print("Invalid action. Try again.\n")
            
    




            
        # TODO: ENTER CODE HERE TO PRINT LOCATION DESCRIPTION

        # Depending on whether or not it's been visited before,
        # print either full description (first time visit) or brief description (every subsequent visit)





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