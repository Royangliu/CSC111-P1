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
    """executes menu actions found within the menu. These include displaying the stats of the player and map, and
    handling the 'look' and 'quit' actions
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
            line = '\t'.join([f'{loc}' for loc in row])
            print(line)

    elif action == 'quit':
        print("Thanks for playing!")
        player.has_quit = True


def do_location_action(action: str, player: Player, curr_loc: Location) -> None:
    """executes location actions found within the menu. These include searching for items, entering puzzles and shop
    menus, dropping milk tea for one quest, and starting the exam.
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
        check_exam_items(player)


def check_exam_items(player: Player) -> None:
    """Helper method for do_location_action for checking if the player has all necessary items to start the exam.
    Makes player.victory into True if so.

    items required: t-card, lucky pen, cheat sheet
    """
    inven_name_list = [item.name for item in player.inventory]

    if 't-card' in inven_name_list and 'lucky pen' in inven_name_list and 'cheat sheet' in inven_name_list:
        player.victory = True
    else:
        print("You don't have all the items to start the exam.")


if __name__ == "__main__":
    # instantiates world and player objects
    with open('map.txt') as map_file, open('locations.txt') as location_file, open('items.txt') as item_file:
        w = World(map_file, location_file, item_file)
    p = Player(0, 0, 35)   # starting position and total movement opportunities allowed

    # initializes lists of main actions
    menu = ["look", "inventory", "money", "score", "map", "steps", "quit", "go [direction]"]
    directions = ["north", "east", "south", "west"]
    move_commands = {'go ' + d for d in directions}

    # print intro
    with open('intro.txt') as intro:
        print(intro.read() + '\n')
    print("To win, have the items 'lucky pen', 'cheat sheet', and 't-card' in your inventory")
    print("and start the exam at the Exam hall (#12 on the map).")
    print("Note that certain special items may aid or ruin you during the exam!.\n")

    # Main gameplay loop and breaks when player is victorious or has run out of steps
    while not p.victory and p.steps >= 0 and not p.has_quit:
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
            choice = input("Enter action: ")
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

            if p.has_quit or p.victory:
                loc_change = True

    # Gameover where the player ran out of steps
    if p.steps < 0:
        print("You ran out of time and the exam began without you.")
        print("\nGame over")

    # Gives the player different endings depending on certain items in their inventory
    elif p.victory:
        # adds extra points depending on remaining steps and money
        p.score += p.steps * 2
        p.score += p.money * 5

        p_item_list = {item.name for item in p.inventory}

        # Bad ending: Has the 'cheap answer giving airpods' in their inventory
        if "cheap answer giving airpods" in p_item_list:
            print("As you were writing the test, a TA caught you using the forsaken cheap airpods.")
            print("The exam was stripped away from you and you got were expelled from supposedly using dark magic.")
            print("\nGame over")
            p.score -= 100
        # Good ending: Has the 'lucky eraser' and 'lucky sharp pencil' in their inventory
        elif "lucky eraser" in p_item_list and "lucky sharp pencil" in p_item_list:
            print("The exam was difficult; however, using your newly aquired utilities, you were able to")
            print("breeze through the exam using the lucky eraser and lucky sharp pencil to write your answers.")
            print("\nYou got an A+ on the exam! You ultra win!")
            p.score += 1000
        # Neutral good ending: Only has the 't-card', 'cheat sheet', and 'lucky pen' in their inventory
        else:
            print("With your t-card, cheat sheet, and lucky pen, you were ready for the exam.")
            print("Through the exam's trials, the companion ship of your pen and cheat sheet")
            print("allowed you to finish the exam.")
            print("\nYou Passed the Exam with a B! You win!")

    print(f"\nScore: {p.score}")
