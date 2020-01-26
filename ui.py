import os
from pygame import mixer
import pyfiglet
from termcolor import colored, cprint
from time import sleep

def display_board(board_list, board_name, player, quests, show_inventory, show_legend,legend, message):
    '''
    Displays complete game board on the screen

    Returns:
    Nothing
    '''
    console_width = os.get_terminal_size().columns

    display_title(board_list, board_name, console_width)
    display_description(player, quests, console_width)

    for row in board_list:
        row = "".join(row)
        print(row.center(console_width))

    display_stats(player, console_width)
    
    if show_inventory:
        display_equipment(player, console_width)
    if show_legend:
        display_legend(legend, console_width)

    display_message(message, console_width)


def display_title(board_list, board_name, console_width):
    '''
    Displays board's name over the printed board.

    Returns:
    Nothing
    '''
    # caption = pyfiglet.figlet_format("*** " + board_name + " ***", font="digital") - odkomentować na prezentację
    caption = "*** " + board_name + " ***"
    captions = caption.split("\n")
    print("")
    for caption in captions:
        print(colored(caption.center(console_width),"blue")) 
        # - odkomentować na prezentację
        print(caption.center(console_width))


def display_description(player, quests, console_width):
    '''
    Displays quest's description over the printed board.

    Returns:
    Nothing
    '''
    
    description_list = quests[str(player["quest"])]["quest_description"]
    # description_list=description_list.split("\n")

    for line in description_list:  
        print(line.center(console_width))
    print("")


def display_stats(player, console_width):
    '''
    Displays player's statistics under the printed board.

    Returns:
    Nothing
    '''
    keys_to_display = ["name", "quest", "infinity_stones", "health"]
    stats_to_display = []
    for key in keys_to_display:
        if key in player:
            pair_of_stats = [key, player[key]]
            stats_to_display.append(pair_of_stats)

    if "inventory" in player.keys():
        number_of_items = 0
        for key in player["inventory"]:
            number_of_items += player["inventory"][key]
        pair_of_stats = ["inventory items (press 'i' for more)", number_of_items]
        stats_to_display.append(pair_of_stats)

    for pair in stats_to_display:
        stats_to_display[stats_to_display.index(pair)] = str(pair[0]).upper() + ": " + str(pair[1])
        
    string_to_display = (" | ").join(stats_to_display)

    print("")
    print(colored(string_to_display.center(console_width), "green"))
    #- odkomentwać na prezentację
    # print(string_to_display.center(console_width))
    

def display_equipment(player, console_width):
 
    equipment = player["inventory"]
    headers = ["name:", "count:"]
    title = "YOUR INVENTORY"
    print_table(title, equipment, headers, console_width)


def display_legend(legend, console_width):

    headers = ["symbol:", "description:"]
    title = "LEGEND (Press 'L' to hide)"
    print_table(title, legend, headers, console_width)


def display_message(message, console_width):
    print("")
    print(message.center(console_width))


def set_table_width(dictionary, headers):
    """ Defines a width of columns so the table fits to the longest elements.""" 
    first_width = len(headers[0])
    for key in dictionary:
        if len(key) > first_width:
            first_width = len(key)

    second_width = len(headers[1])
    for key in dictionary:
        if len(str(dictionary[key])) > second_width:
            second_width = len(str(dictionary[key]))

    return (first_width, second_width)


def print_table(title, dictionary, headers, console_width):
    """Display the contents of the inventory in an ordered, well-organized table with
    each column right-aligned.
    """

    first_width, second_width = set_table_width(dictionary, headers)
    vertical_break = " | "
    total_width = first_width + len(vertical_break) + second_width
    print()

    print((title).center(console_width))
    print(((total_width) * "-").center(console_width))
    print((f"{headers[0]:>{first_width}}{vertical_break}{headers[1]:>{second_width}}").center(console_width))
    print(((total_width) * "-").center(console_width))

    for key in dictionary:
        print((f"{key:>{first_width}}{vertical_break}{dictionary[key]:>{second_width}}").center(console_width))

    print(((total_width) * "-").center(console_width))

def display_logo(art):
    print("\n\n")
    for line in art:
        print("\t\t\t\t\t\t\t{}".format(line), end="")
        # sleep(0.2)
    print("\n\n")

def type_writter_effect(list_of_words):
    print("\n\n")
    for word in list_of_words:
        print("\t\t\t", end="")
        for letter in word:
            print(letter, end="", flush=True)
            # sleep(0.05)
        print()

def player_has_lost():
    messege= "You have lost!"
    print(pyfiglet.figlet_format("*** " + messege + " ***"))
    sleep(5)
    # play_music("game_over.wav")