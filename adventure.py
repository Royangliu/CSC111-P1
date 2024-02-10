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

from game_data import SpecialLocation, ShopLocation, World, Item, Location, Player


def move_player(direction: str, player: Player, world: World) -> bool:
    """Moves the player by changing the player's x and y coordinates if the chosen direction is valid.
    Returns True or False depending on if the player was successfully moved.

    Preconditions:
        - direction in {'north', 'south', 'east', 'west'}
    """
    temp_y, temp_x = player.y, player.x

    if direction == "east":
        temp_x += 1
    elif direction == "south":
        temp_y += 1
    elif direction == "north":
        temp_y -= 1
    elif direction == "west":
        temp_x -= 1

    if world.get_location(temp_x, temp_y) is None:
        return False
    else:
        player.x, player.y = temp_x, temp_y
        return True


def do_menu_action(action: str, player: Player, curr_loc: Location, world: World) -> None:
    """executes menu actions found within the menu
    """
    if action == "look":
        print(curr_loc.long_desc)

    elif action == "inventory":
        print("Inventory:")
        print([item.name for item in player.inventory])

    elif action == 'money':
        print("Money:")
        print("$" + str(player.money))

    elif action == "score":
        print(f"Current score: {player.score}")

    elif action == "steps":
        print(f"Remaining movements: {player.steps}")

    elif action == "map":
        for row in world.map:
            line = ''
            for loc in row:
                line += f'\t{loc}'
            print(line)

    elif action == 'quit':
        print("Thanks for playing!")
        player.has_quit = True

def do_location_action(action: str, player: Player, curr_loc: Location) -> None:
    """executes location actions found within the menu
    """
    # adds any items found within the location's items_list to the player's inventory with their score
    if action == 'search':
        for item in curr_loc.items_list:
            if item.currency_amount > 0:
                player.money += item.currency_amount
            else:
                player.inventory.append(item)
            player.score += item.score
            print(item.item_desc)
            print(f"\nYou gained {item.score} points for getting (a) {item.name}!")
            
            curr_loc.items_list.remove(item)

    # runs the methods corresponding to the function found within the location subclasses
    elif action == 'puzzle' and isinstance(curr_loc, SpecialLocation):
        addition = curr_loc.do_puzzle()
        player.inventory += addition
        for item in addition:
            player.score += item.score
            print(f"\nYou gained {item.score} points for getting (a) {item.name}!")
    
    elif action == "shop" and isinstance(curr_loc, ShopLocation):
        curr_loc.do_buy(player)

    # handles one quest for giving a student milk tea to receive an item for a 'good ending'
    elif action == "drop milk tea":
        for item in player.inventory:
            if item.name == "milk tea":
                player.inventory.remove(item)
        eraser = Item("lucky eraser", curr_loc.location_num, 0, 0, 15, "")
        player.inventory.append(eraser)
        player.score += eraser.score
        print("Thank you so much for the caffeine boost! The line was so long!")
        print("I know this isn't much but you can have my lucky eraser for your troubles.")
        print("You got 1 lucky eraser.")
        print(f"\nYou gained {eraser.score} points for getting (a) {eraser.name}!")

    # handles the action at the exam centre to start the exam/hand in items
    elif action == "start exam":
        has_t_card = False
        has_lucky_pen = False
        has_cheat_sheet = False
        
        for item in player.inventory:
            if item.name == "t-card":
                has_t_card = True
            elif item.name == "lucky pen":
                has_lucky_pen = True
            elif item.name == "cheat sheet":
                has_cheat_sheet = True
    
        if has_t_card and has_lucky_pen and has_cheat_sheet:
            player.victory = True
        else:
            print("You don't have all the items to start the exam.")
            

if __name__ == "__main__":
    # instantiates world and player objects
    with open('map.txt') as map_file, open('locations.txt') as location_file, open('items.txt') as item_file:
        w = World(map_file, location_file, item_file)
    p = Player(0, 0, 30)   # starting position and total movement opportunities allowed

    # initializes lists of main actions
    menu = ["look", "inventory", "money", "score", "map", "steps", "quit", "go [direction]"]
    directions = ["north", "east", "south", "west"]
    move_commands = {'go ' + d for d in directions}

    # print intro
    intro = open('intro.txt')
    print(intro.read() + '\n')
    intro.close()
    print("To win, have the items 'lucky pen', 'cheat sheet', and 't-card' your inventory")
    print("and start the exam at the Exam hall (#12 on the map).\n")

    # Main gameplay loop and breaks when player is victorious or has run out of steps
    while not p.victory and p.steps >= 0 and p.has_quit == False:
        location = w.get_location(p.x, p.y)

        # Print location description
        print(location.location_name)
        if location.has_visited:
            print(location.brief_desc)
        else:
            print(location.long_desc)
            p.score += location.score
            print(f"\nYou gained {location.score} points for visiting the new area!")
            location.has_visited = True

        # Loops for player actions at a location until their location is changed
        loc_change = False
        while not loc_change:

            print("\nWhat to do? Type \'[menu]\' for the list of actions.")
            choice = input("Enter action: ").lower()
            print()

            location_actions = location.available_actions()
            # adds additional location actions for exam centre and milk tea quest
            if location.location_num == 12:
                location_actions.append("start exam")
            if location.location_num == 4 and any(item.name == 'milk tea' for item in p.inventory):
                location_actions.append("drop milk tea")
            
            # Prints all available actions if '[menu]' was picked
            if choice == "[menu]":
                print("Menu Options: ")
                for option in menu:
                    print('\t' + option)
                print("Movement Directions: ")
                for option in directions:
                    print('\t' + option)
                print("Location Actions: ")
                if location_actions:
                    for option in location_actions:
                        print('\t' + option)
                else:
                    print("\tNone")

            # Handles all actions through helper functions above according to input
            elif choice in menu:
                do_menu_action(choice, p, location, w)
            elif choice in location_actions:
                do_location_action(choice, p, location)
            elif choice in move_commands:
                if move_player(choice[3:], p, w):
                    p.steps -= 1
                    loc_change = True
                else:
                    print("Invalid movement input. Try again.")
            else:
                print("Invalid action. Try again.")

    # Gameover where the player ran out of steps
    if p.steps < 0:
        print("You ran out of time and the exam began without you.") 
        print("\nGame over")

    # Gives the player different endings depending on certain items in their inventory
    elif p.victory:
        p.score += p.steps * 2
        
        # Bad ending: Has the 'cheap answer giving airpods' in their inventory
        if any(item.name == "cheap answer giving airpods" for item in p.inventory):
            print("As you were writing the test, a TA caught you using the forsaken cheap airpods.") 
            print("The exam was stripped away from you and you got were expelled from supposedly using dark magic.")
            print("\nGame over")
            p.score -= 1000
        # Good ending: Has the 'lucky eraser' and 'lucky sharp pencil' in their inventory
        elif (any(item.name == "lucky eraser" for item in p.inventory) and
            any(item.name == "lucky sharp pencil" for item in p.inventory)):
            print("The exam was difficult; however, using your newly aquired utilities, you were able to breeze through the exam")
            print("using the lucky eraser and lucky sharp pencil to write your answers.")
            print("You got an A+ on the exam! You ultra win!")
            p.score += 1000
        # Neutral good ending: Only has the 't-card', 'cheat sheet', and 'lucky pen' in their inventory
        else:
            print("With your ")
        

        print("Congratulations! You have won the game!")
        print("Your final score is: " + str(p.score))
    else:
        print("You have run out of steps. Game over.")

    print(f"\nScore: {p.score}")

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
