import util
import engine
import ui
import random
import sys
import data_menager
# import pygame
# from pygame import mixer
# import pyfiglet

legend = {
    "x": "exit",
    "T": "tree",
    "$": "gold",
    "U": "beer",
    "=": "hamburger",
    ":": "hot-dog",
    "B": "boots",
    "?": "specials",
    "*": "infinity stones"
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
                "icon" : "x"
            },
            "east": {
                "index_x": 19,
                "index_y": 9,
                "leads_to": "board_3",
                "icon" : "x"
            }
        },
        "nature": {
            "tree_1": {
                "index_x": 2,
                "index_y": 2,
                "icon" : "T"
            },
            "tree_2": {
                "index_x": 1,
                "index_y": 4,
                "icon" : "T"
            },
            "tree_3": {
                "index_x": 13,
                "index_y": 9,
                "icon" : "T"
            },
            "tree_4": {
                "index_x": 13,
                "index_y": 8,
                "icon" : "T"
            },
            "tree_5": {
                "index_x": 13,
                "index_y": 10,
                "icon" : "T"
            },
        },
        "items": {
            "gold": {
                "number": 2,
                "index_x": 4,
                "index_y": 8,
                "icon" : "$"
            },
            "thor's hammer": {
                "number": 1,
                "index_x": 14,
                "index_y": 10,
                "icon":"?"   
            },
            "captain's america' shield": {
                "number": 1,
                "index_x": 1,
                "index_y": 10,
                "icon":"?"   
            },
        },
        "characters": {
            "Loki": {
                "index_x": 13,
                "index_y": 4,
                "icon": "L"
            },
        },
        "food": {
            "hamburger": {
                "health": 20,
                "index_x": 14,
                "index_y": 5,
                "icon": "=",
                "number":1   
            },
            "hot-dog": {
                "health": 20,
                "index_x": 10,
                "index_y": 10,
                "icon": ":",
                "number":1 
            },
            "beer": {
                "health": 50,
                "index_x": 13,
                "index_y": 7,
                "icon": "U",
                "number":1   
            },  
        },
    },
    "board_2": {
        "name": "ASGARD",
        "width": 20,
        "height": 30,
        "exits": {
            "south": {
                "index_x": 15,
                "index_y": 29,
                "leads_to": "board_1",
                "icon" : "x"
            }
        },
        "nature": {
            "tree_1": {
                "index_x": 4,
                "index_y": 9,
                "icon" : "T"
            },
            "tree_2": {
                "index_x": 10,
                "index_y": 3,
                "icon" : "T"
            },
        },
        "items": {
            "knife": {
                "number":1,
                "index_x": 7,
                "index_y": 4,
                "icon" : "1"
            },
            "armor": {
                "number": 30,
                "index_x": 8,
                "index_y": 3,
                "icon": "?"   
            }
        },
    },
    "board_3": {
        "name": "VORMIR",
        "width": 20,
        "height": 30,
        "exits": {
            "west": {
                "index_x": 0,
                "index_y": 20,
                "leads_to": "board_1",
                "icon" : "x"
            }
        },
        "food": {
            "hamburger": {
                "health": 20,
                "index_x": 14,
                "index_y": 5,
                "icon": "=",
                "number":1   
            },
            "hot-dog": {
                "health": 20,
                "index_x": 10,
                "index_y": 10,
                "icon": ":",
                "number":1 
            },
            "beer": {
                "health": 50,
                "index_x": 13,
                "index_y": 7,
                "icon": "U",
                "number":1   
            },  
        },
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
        "quest_description": ["quest 2 description here"]
    },    
    "3": {
        "quest_description": ["quest 3 descripton here"]
    },   
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
        "health": 70,
        "position_x": 3,
        "position_y": 6,
        "current_board": "board_1",
        "player_icon": user_icon
    }
    return player


def ask_for_details():
    """
    Asks player for name and icon.
    
    Returns:
    User's details
    """
    possible_names = ["Captain America", "Iron Man", "Hulk", "Thor", "Black Widow", "War Machine", "Captain Marvel", "Spider-Man", "Black Panther", "Star Lord"]
    user_name = input("Choose your name or press 'r' if you want to randomly pick a name from the Avengers team. > ")
    if user_name in ["r", "R"] or len(user_name) < 1:
        user_name = random.choice(possible_names)
    # implement option for user to choose one of the possible names in the list @rr
    
    if user_name in ["s", "S"]:
        user_name = "Spider-Man"
    elif user_name in ["i", "I"]:
        user_name = "Iron-Man"
    elif user_name in ["r", "R"] or len(user_name) < 1:
        user_name = random.choice(["Spider-Man", "Iron-Man"])

    ui.type_writter_effect([questions[1]])
    print("\t\t\t",end="")
    user_icon = input("> ")

    possible_icons = ["@", "&", "#", "%"]
    if user_icon not in possible_icons:
        user_icon = random.choice(possible_icons)

    return user_name, user_icon


def make_opposite_boolean(boolean):
    if boolean == True:
        boolean = False
    else:
        boolean = True
    return boolean

def main():
    util.clear_screen()
    asci_logo = data_menager.read_file("avengers.txt")
    # zakomentujcie sobie poniżej wtedy nie będzie się wam wczytywać logo za każdym razem
    # ui.display_logo(asci_logo)
    # util.clear_screen()
    # pygame.init()
    # mixer.music.load("The Avengers Theme Song.ogg")
    # mixer.music.play(-1) muzyka działa po odkomentowaniu
    player = create_player()
    board = engine.create_board(boards[player["current_board"]])

    util.clear_screen()
    is_running = True
    while is_running:
        board = engine.create_board(boards[player["current_board"]])
        # engine.put_player_on_board(board, player)
        # ui.display_board(board, boards[player["current_board"]]["name"])
        # key = util.key_pressed()
        # engine.remove_player_from_board(board, player)
        # player = engine.move_player(board, player, key, boards)

        engine.put_player_on_board(board, player)
        ui.display_board(board, boards[player["current_board"]]["name"], player, quests)
        key = util.key_pressed()
        engine.remove_player_from_board(board, player)
        if key in ["W", "w", "s", "S", "a", "A", "D", "d"]:
            player = engine.move_player(board, player, key, boards)
        if key in ["q", "Q"]:
            is_running = False
        elif key in ["i", "I"] and "inventory" in player:
            show_inventory = make_opposite_boolean(show_inventory)
        elif key in ["l", "L"]:
            show_legend = make_opposite_boolean(show_legend)
        else:
            pass

        engine.plot_development(player, quests)
        util.clear_screen()


if __name__ == '__main__':
    main()
