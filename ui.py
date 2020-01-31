import os
from pygame import mixer
import pyfiglet
from termcolor import colored, cprint
from time import sleep
import util


def display_board(board_list, board_name, player, quests, show_inventory, show_legend,legend, message):
    '''
    Displays complete game board on the screen. Coordinates displaying other elements of screen.
    Args: board_list (list of lists), board_name (string), player, quests, legend (dictionaries),
    show_inventory and show_legend (booleans) and message (string). 
    Returns: Nothing.
    '''

    console_width = os.get_terminal_size().columns

    display_title(board_name, console_width)
    display_description(player, quests, console_width)
    print_rows(board_list, console_width)
    display_stats(player, console_width)
    display_equipment(player, console_width, show_inventory)
    display_legend(legend, console_width, show_legend)
    display_message(message, console_width)


def print_rows(board_list, console_width):
    """
    Joins elements of rows in single strings and prints them.
    Args: board_list (list of lists) and console_width (int).
    Returns: Nothing.
    """

    for row in board_list:
        row = "".join(row)
        print(row.center(console_width))


def display_title(board_name, console_width):
    '''
    Displays board's name over the printed board.
    Args: board_name (string) and console_width (int).
    Returns: Nothing.
    '''

    caption = pyfiglet.figlet_format("*** " + board_name + " ***", font="digital")
    caption = "*** " + board_name + " ***"
    print("")
    print(colored(caption.center(console_width),"blue")) 
    print("")


def display_description(player, quests, console_width):
    '''
    Displays quest's description over the printed board.
    Args: player, quests (dictionaries) and console_width (string).
    Returns: Nothing.
    '''
    
    description_list = quests[str(player["quest"])]["quest_description"]

    for line in description_list:  
        print(line.center(console_width))
    print("")


def display_stats(player, console_width):
    '''
    Displays player's statistics under the printed board.
    Args: player (dictionary) and console_width (int).
    Returns: Nothing
    '''

    keys_to_display = ["name", "quest", "health"]
    stats_to_display = []
    for key in keys_to_display:
        pair_of_stats = [key, player[key]]
        stats_to_display.append(pair_of_stats)

    if "inventory" in player.keys():
        number_of_items = sum(player["inventory"].values())
        pair_of_stats = ["inventory items (press 'i' for more)", number_of_items]
        stats_to_display.append(pair_of_stats)

    for pair in stats_to_display:
        stats_to_display[stats_to_display.index(pair)] = str(pair[0]).upper() + ": " + str(pair[1])
        
    string_to_display = (" | ").join(stats_to_display)

    print("")
    print(colored(string_to_display.center(console_width), "green"))
    

def display_equipment(player, console_width, show_inventory):
    """
    Displays user's inventory under the board when user requests for it.
    Args: player (dictionary), console_width (int) and show_inventory (boolean).
    Returns: Nothing.
    """

    if show_inventory:
        equipment = player["inventory"]
        headers = ["name:", "count:"]
        title = "YOUR INVENTORY"
        print_table(title, equipment, headers, console_width)


def display_legend(legend, console_width, show_legend):
    """
    Displays game's legend under the board and inventory when user requests for it.
    Args: legend (dictionary), console_width (int) and show_legend (boolean).
    Returns: Nothing.
    """

    if show_legend:
        headers = ["symbol:", "description:"]
        title = "LEGEND (Press 'L' to hide)"
        print_table(title, legend, headers, console_width)


def display_message(message, console_width):
    """
    Displays messae under the board. Message should be returned by other functions and passed here via main().
    Args: message (string) and console_width (int).
    Returns: Nothing
    """
    
    print("")
    for line in message:  
        print(line.center(console_width))


def set_table_width(dictionary, headers):
    """ 
    Defines a width of table's both columns so the table fits to the longest elements.
    Args: dictionary (dictionary) and headers (list).
    Returns: first_width, second_width (both integers).
    """ 

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
    """
    Display the contents of the inventory in an ordered, well-organized table with each column right-aligned.
    Args: title (string)m dictionary (dictionary), headers (list) and console_width (int).
    Returns: Nothing.
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
    """
    Prints avengers' logo in the console.
    Args: art (list of lists).
    Returns: Nothing
    """

    print("\n\n")
    for line in art:
        print("{}".format(line), end="")
        sleep(0.1)
    print("\n\n")
    sleep(0.2)
    messege = "Avengers: The Final Battle"
    print(pyfiglet.figlet_format("*** " + messege + " ***",font="digital"))


def type_writter_effect(list_of_words):
    """
    Adds a live writing effect to the text.
    Args: list_of_words (list).
    Returns: Nothing.
    """

    print("\n\n")
    for word in list_of_words:
        print("\t\t\t", end="")
        for letter in word:
            print(letter, end="", flush=True)
            sleep(0.01)
        print("\n\n\t\t\t", end="")


def player_has_lost():
    """
    Displays message and plays sad music when player loose the game.
    Args: None, Returns: Nothing.
    """

    util.clear_screen()
    messege= "You have lost!"
    print(pyfiglet.figlet_format("*** " + messege + " ***"))
    sleep(5)
    play_music("game_over.wav")


def display_authors():
    """
    Displays authors of the game.
    Args: None, Returns: Nothing.
    """
    
    messege = "Game created by Karolina, Magda, Mateusz, Ricardo"
    print(pyfiglet.figlet_format("*** " + messege + " ***",font="digital"))
    
    
def player_has_won():
    """
    Displays message and ends the program when player wins the game.
    Args: None, Returns: Nothing.
    """

    util.clear_screen()
    messege = "You have won:) Congratulations !!!!"
    print(pyfiglet.figlet_format("*** " + messege + " ***", font="digital"))
    sleep(3)
    exit()
