import engine
import ui
import util
import random
import sys
import data_menager
import pygame
from pygame import mixer
import pyfiglet
from time import sleep

legend = {
    "x": "closed exit",
    "+": "open exit",
    "T": "tree",
    "0": "stone",
    "$": "gold",
    "U": "beer",
    "=": "hamburger",
    ":": "hot-dog",
    "?": "specials",
    "*": "infinity stones",
    "L": "Loki",
    "S": "Skull",
    "C": "Colector"
}

boards = {
    "board_1": {
        "name": "EARTH",
        "width": 20,
        "height": 12,
        "exits": {
            "north": {
                "index_x": 8,
                "index_y": 0,
                "leads_to": "board_2",
                "icon": "+"
            }
        },
        "static_elements": {
            "trees": {
                "obstacle_name": "tree",
                "icon": "T",
                "coor": [[1, 4], [2, 4], [3, 4], [2, 6], [3, 6], [4, 6], [5, 6], [13, 9], [13, 8], 
                        [13, 10], [15, 1], [15, 2], [15, 3], [15, 4]]
            },
        },
        "items": {
            "gold": {
                "number": 30,
                "index_x": 4,
                "index_y": 8,
                "icon": "$"
            },
            "thor's hammer": {
                "number": 1,
                "index_x": 16,
                "index_y": 10,
                "icon": "?"
            },
            "captain's america' shield": {
                "number": 1,
                "index_x": 1,
                "index_y": 10,
                "icon": "?"
            },
        },
        "characters": {
            "Loki": {
                "index_x": 13,
                "index_y": 4,
                "icon": "L",
                "health": 100
            },
        },
        "food": {
            "hamburger": {
                "health": 20,
                "index_x": 17,
                "index_y": 1,
                "icon": "=",
            },
            "hot-dog": {
                "health": 20,
                "index_x": 10,
                "index_y": 10,
                "icon": ":"
            },
            "beer": {
                "health": 50,
                "index_x": 13,
                "index_y": 7,
                "icon": "U"
            },
        },
    },
    "board_2": {
        "name": "ASGARD",
        "width": 16,
        "height": 12,
        "exits": {
            "south": {
                "index_x": 9,
                "index_y": 11,
                "leads_to": "board_1",
                "icon": "+"
            },
            "north": {
                "index_x": 5,
                "index_y": 0,
                "leads_to": "board_3",
                "icon": "+"
            }
        },
        "static_elements": {
            "trees": {
                "obstacle_name": "tree",
                "icon": "T",
                "coor": [[8, 1], [6, 4], [5, 8], [11, 8]]
            },
            "labyrinth": {
                "obstacle_name": "rock",
                "icon": "O",
                "coor": [[7, 1], [13, 1], [12, 2], [3, 3], [4, 10], [6, 10],
                         [6, 3], [6, 3], [6, 3], [2, 4], [1, 9], [2, 9],
                         [4, 4], [11, 4], [5, 5], [4, 5], [11, 5],
                         [12, 5], [2, 6], [4, 6], [7, 6], [12, 6],
                         [3, 7], [6, 7], [8, 7], [12, 7], [9, 8],
                         [9, 9], [11, 10], [13, 10], [8, 3]]
            }
        },
        "items": {
            "armor": {
                "number": 1,
                "index_x": 6,
                "index_y": 2,
                "icon": "?"
            },
            "space stone": {
                "number": 1,
                "index_x": 2,
                "index_y": 5,
                "icon": "*"
            },
            "reality stone": {
                "number": 1,
                "index_x": 11,
                "index_y": 3,
                "icon": "*"
            }
        },
    },
    "board_3": {
        "name": "VORMIR",
        "width": 20,
        "height": 12,
        "exits": {
            "south": {
                "index_x": 4,
                "index_y": 11,
                "leads_to": "board_2",
                "icon": "x"
            },
            "north": {
                "index_x": 13,
                "index_y": 0,
                "leads_to": "board_4",
                "icon": "x"
            }
        },
        "food": {
            "hamburger": {
                "health": 20,
                "index_x": 14,
                "index_y": 5,
                "icon": "="
            },
            "hot-dog": {
                "health": 20,
                "index_x": 10,
                "index_y": 10,
                "icon": ":"
            },
            "beer": {
                "health": 50,
                "index_x": 13,
                "index_y": 7,
                "icon": "U"
            },
        },
        "items": {
            "gold": {
                "number": 2,
                "index_x": 4,
                "index_y": 8,
                "icon": "$"
            },
        },
        "characters": {
            "Collector": {
                "index_x": 16,
                "index_y": 2,
                "icon": "C",
                "health": 30,
                "riddle": ["What animal walks with 4 legs, then with 2, and at end with 3?"],
                "answer": ("human", "human being", "man", "person"),
                "stone": "power stone"
            },
            "Skull": {
                "index_x": 7,
                "index_y": 8,
                "icon": "S",
                "health": 30,
                "riddle": ["Everyone has it, but some don't like it.", "It makes a kid lough, saddens old man, pleases young girl.", "When You laugh it laughswith You, when You weep it weeps as well."],
                "answer": ("reflection", "mirror reflection", "mirror"),
                "stone": "soul stone"
            }
        },
        "static_elements": {
            "trees": {
                "obstacle_name": "tree",
                "icon": "T",
                "coor": [[8, 1], [6, 4], [5, 8], [5, 9], [6, 9], [7, 9],
                        [8, 9], [5, 8], [12, 1], [12, 2], [12, 3], [12, 4], [12, 5],
                        [10, 1], [10, 2], [10, 3], [5, 7]]
            },
        },
    },
    "board_4": {
        "name": "TITAN",
        "width": 25,
        "height": 25,
        "exits": {
            "south": {
                "index_x": 13,
                "index_y": 24,
                "leads_to": "board_3",
                "icon": "x"
            }
        },
        "food": {
            "hamburger_1": {
                "health": 20,
                "index_x": 2,
                "index_y": 22,
                "icon": "="
            },
            "hamburger_2": {
                "health": 20,
                "index_x": 2,
                "index_y": 23,
                "icon": "="
            },
            "beer_1": {
                "health": 50,
                "index_x": 1,
                "index_y": 21,
                "icon": "U"
            },
            "beer_2": {
                "health": 50,
                "index_x": 1,
                "index_y": 22,
                "icon": "U"
            },
            "beer_3": {
                "health": 50,
                "index_x": 1,
                "index_y": 23,
                "icon": "U"
            },
        },
        "items": {
            "AK-47": {
                "number": 1,
                "index_x": 20,
                "index_y": 23,
                "icon":"?"
            },
            "Rocket-Launcher": {
                "number": 1,
                "index_x":20,
                "index_y": 2,
                "icon":"?"
            },
        },
        "static_elements": {
            "trees": {
                "obstacle_name": "tree",
                "icon": "T",
                "coor": [[8, 1]]
            },
            
        },
        "boss": {  
            "name": "Thanos",
            "health": 500,
            "position_x": 4,
            "position_y": 5,
            "icons": [["[", "\\", " ", "/", "]"],
                    ["[", " ", "O", " ", "]"],
                    ["[", "#", "#", "#", "E"],
                    ["[", " ", "#", " ", "]"],
                    ["[", "/", " ", "\\", "]"]]
        }
    }
}

quests = {
    "1": {
        "quest_description": ["You are an Avenger, fighting Thanos and his troops.",
                              "Your task is to find infinity stones located on 3 worlds, starting from Earth.",
                              "To find the stones placed here, you'll need to beat the sneakiest of them all - Loki.",
                              "Only then you'll be able to get to other worlds.",
                              "But be careful, you need to prepare for this meeting..."]
    },
    "2": {
        "quest_description": ["The space and reality stones are hidden on the board.", 
                              "To get them You need to move pass labyrinth.", 
                              "After collecting both stones, gates to Vormir will open."]
    },
    "3": {
        "quest_description": ["Two last infinity stones are in possession of the Collector and the Skull.", 
                              " The characters will give You the stones if You will answer their riddles"]
    },
    "4": {
        "quest_description": ["It's a final battle!", 
                              "Although you have frozen time with your stones and Thanos can't move, he's stil dangerous.",
                              "Try to prepare as much as you can. You'll need all the help you can get..."]
    }
}


def create_player():
    '''
    Creates a 'player' dictionary for storing all player related information - i.e. player icon, player position.

    Returns:
    dictionary
    '''

    user_name, user_icon = ask_for_details()
    player = {
        "name": user_name,
        "quest": 1,
        "health": 60,
        "position_x": 3,
        "position_y": 6,
        "current_board": "board_1",
        "player_icon": user_icon,
        "inventory": {},
        "riddle_counter": 0
    }
    return player


def ask_for_details():
    """
    Asks player for name and icon.

    Returns:
    User's details
    """

    questions = ["Type your name or choose between Spider-Man [type 'S'] and Iron-Man [type 'I'], or press 'r' to pick randomly",
                 "Choose the icon you want to be. Pick between '@', '&', '#' and '%' or press 'r' to choose randomly."]
    
    ui.type_writter_effect([questions[0]])
    user_name = input("> ")
    user_name = validate_user_name(user_name)
    
    ui.type_writter_effect([questions[1]])
    user_icon = input("> ")
    user_icon = validate_user_icon(user_icon)
    
    return user_name, user_icon


def validate_user_name(user_name):
    """
    Briefly validates user's name input.

    Returns:
    Corrected name (if the name required correction. Otherwise it returns its initial argument).
    """
    
    if user_name in ["s", "S"]:
        user_name = "Spider-Man"
    elif user_name in ["i", "I"]:
        user_name = "Iron-Man"
    elif user_name in ["r", "R"] or len(user_name) < 1:
        user_name = random.choice(["Spider-Man", "Iron-Man"])
    
    return user_name


def validate_user_icon(user_icon):
    """
    Briefly validates user's icon input.

    Returns:
    Random icon from the allowed list, if a user didn't pick proper symbol.
    """

    possible_icons = ["@", "&", "#", "%"]
    if user_icon not in possible_icons:
        user_icon = random.choice(possible_icons)
    
    return user_icon


def game_introduction():
    """
    Responsible for displaying logo, credits and playing music when game starts.

    Returns: Nothing
    """
    
    # pygame.init()
    # mixer.music.load("The Avengers Theme Song.ogg")
    # mixer.music.play(-1)
    # util.clear_screen()
    # asci_logo = data_menager.read_file("avengers.txt")
    # ui.display_logo(asci_logo)
    # util.clear_screen()
    # ui.display_authors()
    # sleep(4)
    # util.clear_screen()


def react_to_pressed_key(key, board, boards, player, show_inventory, show_legend, is_running):
    """
    Transforms user's keyboard activity into corresponding actions.

    Arguments: key (string), board (list of lists), boards (dictionary), player (dictionary)
    and three last arguments - booleans.

    Returns: Player (dictionary), three boolean variables and boards (dictionary).
    """
    
    if key in ["W", "w", "s", "S", "a", "A", "D", "d"]:
        player = engine.move_player(board, player, key, boards)
    elif key in ["i", "I"]:
        show_inventory = not show_inventory
    elif key in ["l", "L"]:
        show_legend = not show_legend
    elif key in ["q", "Q"]:
        is_running = False
    
    return player, show_inventory, show_legend, is_running, boards


def main():
    """
    Main function of the game, transforms user's input into player's movement and plot changes.

    Returns: Nothing
    """

    message, message_type, name = "", "no_type", ""
    show_inventory = False
    show_legend = True
    is_running = True
    global boards

    game_introduction()
    player = create_player()

    while is_running:
        util.clear_screen()
        board = engine.create_board(boards[player["current_board"]], player)
        ui.display_board(board, boards[player["current_board"]]["name"],
                         player, quests, show_inventory, show_legend, legend, message)
        engine.validate_answer(name, player, boards, message_type)
        key = util.key_pressed()
        board = engine.remove_player_from_board(board, player)
        player, show_inventory, show_legend, is_running, boards = react_to_pressed_key(key, board, boards, player, 
                                                                  show_inventory, show_legend, is_running)
        message, message_type, name = engine.plot_development(player, boards, board)
        is_running = engine.check_health_is_zero_or_below(player, is_running)
        

if __name__ == '__main__':
    main()
