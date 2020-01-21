import os
from pygame import mixer
import pyfiglet
from termcolor import colored, cprint

def display_board(board_list, board_name, player, quests, show_inventory, show_legend,legend):
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
        display_equipment(player["inventory"], console_width)
    if show_legend:
        display_legend(legend,console_width)
   


def display_title(board_list, board_name, console_width):
    '''
    Displays board's name over the printed board.

    Returns:
    Nothing
    '''

    caption = pyfiglet.figlet_format("*** " + board_name + " ***", font="digital")
    captions = caption.split("\n")
    print("")
    for caption in captions:
        print(colored(caption.center(console_width),"blue"))
    


def display_description(player, quests, console_width):
    '''
    Displays quest's description over the printed board.

    Returns:
    Nothing
    '''
    description_list = quests[str(player["quest"])]["quest_description"]
    for line in description_list:  
        print(line.center(console_width))
    print("")


def display_stats(player, console_width):
    '''
    Displays player's statistics under the printed board.

    Returns:
    Nothing
    '''
    #dodać liczenie infinity stones w engine
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
    
def display_equipment(player, console_width):
    print()
    print(colored("inventory : ".center(console_width), "red"))
    for k, v in player.items():
        item = '{} | {}'.format(k,v)
        print(item.center(console_width))
        
    print()
def display_legend(legend, console_width):
    print()
    print(colored("Icons: ".center(console_width), "yellow"))
    for k, v in legend.items():
        item = '{:2} : {:15}'.format(k,v)
        print(item.center(console_width))
