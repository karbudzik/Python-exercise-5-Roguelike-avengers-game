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
                "icon": "x"
            }
        },
        "static_elements": {
            "trees": {
                "obstacle_name": "tree",
                "icon": "T",
                "coor": [[2, 2], [1, 4], [13, 9], [13, 8], [13, 10]]
            },
        },
        "items": {
            "gold": {
                "number": 2,
                "index_x": 4,
                "index_y": 8,
                "icon": "$"
            },
            "thor's hammer": {
                "number": 1,
                "index_x": 14,
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
                "health": 100,
                "inventory": {
                    "inventory": "sword"
                },

            },
        },
        "food": {
            "hamburger": {
                "health": 20,
                "index_x": 14,
                "index_y": 5,
                "icon": "=",
                "number": 1
            },
            "hot-dog": {
                "health": 20,
                "index_x": 10,
                "index_y": 10,
                "icon": ":",
                "number": 1
            },
            "beer": {
                "health": 50,
                "index_x": 13,
                "index_y": 7,
                "icon": "U",
                "number": 1
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
                "icon": "x"
            },
            "north": {
                "index_x": 5,
                "index_y": 0,
                "leads_to": "board_3",
                "icon": "x"
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
                "coor": [[7, 1], [13, 1], [12, 2], [3, 3],
                         [6, 3], [6, 3], [6, 3], [2, 4],
                         [4, 4], [11, 4], [5, 5], [4, 5], [11, 5],
                         [12, 5], [2, 6], [4, 6], [7, 6], [12, 6],
                         [3, 7], [6, 7], [8, 7], [12, 7], [9, 8],
                         [9, 9]]
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
                "index_y": 4,
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
            }
        },
        "food": {
            "hamburger": {
                "health": 20,
                "index_x": 14,
                "index_y": 5,
                "icon": "=",
                "number": 1
            },
            "hot-dog": {
                "health": 20,
                "index_x": 10,
                "index_y": 10,
                "icon": ":",
                "number": 1
            },
            "beer": {
                "health": 50,
                "index_x": 13,
                "index_y": 7,
                "icon": "U",
                "number": 1
            },
        },
        "characters": {
            "Collector": {
                "index_x": 13,
                "index_y": 4,
                "icon": "C",
                "health": 30,
                "riddle": """What animal walks with 4 legs, then with 2,
                                       and at end with 3?""",
                "answer": ("human", "human being", "man", "person"),
                "stone": "power_stone"
            },
            "Skull": {
                "index_x": 7,
                "index_y": 8,
                "icon": "S",
                "health": 30,
                "riddle": """Everyone has it, but some don't like it. It makes
                             a kid lough, saddens old man, pleases young girl.
                             When You laugh it laughswith You, when You weep
                             it weeps as well.""",
                "answer": ("reflection", "mirror reflection"),
                "stone": "soul_stone"
            }
        },
        "static_elements": {
            "trees": {
                "obstacle_name": "tree",
                "icon": "T",
                "coor": [[8, 1], [6, 4], [5, 8], [11, 8]]
            },
        },
    }
}

quests = {
    "1": {
        "quest_description": ["You are an Avenger, fighting Thanos and his troops."
                              "Your task is to find infinity stones located on 3 worlds, starting from Earth.",
                              "To find the stones placed here, you'll need to beat the sneakiest of them all - Loki.",
                              "Only then you'll be able to get to other worlds.",
                              "But be careful, you need to prepare for this meeting..."]
    },
    "2": {
        "quest_description": ["""The space and reality stones are hidden on the
                                 board. To get them You need to move pass 2
                                 labyrinths. After collecting both stones
                                 gates to Vormir will open."""]
    },
    "3": {
        "quest_description": ["""Infinity stones are in possession by two
                                 characters: the Collector (Power Stone),
                                 and the Skull (Soul Stone). The characters
                                 will give You the stones
                                 if You will answer their riddles.
                                 Beware off the traps."""]
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
    names = "Avalible heroes: You or Spider-Man/Iron-Man"
    questions = ["Type your name or chosse between Spider-Man [type 'S'] and Iron-Man [type 'I'], or press 'r' if you want to randomly pick",
                 "Choose the icon you want to be your character. You can choose between '@', '&', '#' and '%' or press 'r' if you want to pick randomly."]
    questions = ["Type your name or choose between Spider-Man [type 'S'] and Iron-Man [type 'I'], or press 'r' to pick randomly",
                 "Choose the icon you want to be. Pick between '@', '&', '#' and '%' or press 'r' to choose randomly."]
    ui.type_writter_effect([names, questions[0]])
    print("\t\t\t", end="")
    user_name = input("> ")

    if user_name in ["s", "S"]:
        user_name = "Spider-Man"
    elif user_name in ["i", "I"]:
        user_name = "Iron-Man"
    elif user_name in ["r", "R"] or len(user_name) < 1:
        user_name = random.choice(["Spider-Man", "Iron-Man"])

    ui.type_writter_effect([questions[1]])
    print("\t\t\t", end="")
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
    # asci_logo = data_menager.read_file("avengers.txt")
    # ui.display_logo(asci_logo)
    # util.clear_screen()
    # pygame.init()
    # mixer.music.load("The Avengers Theme Song.ogg")
    # mixer.music.play(-1)
    #  - muzyka działa po odkomentowaniu
    player = create_player()
    show_inventory = False
    show_legend = True
    util.clear_screen()
    is_running = True
    while is_running:
        # if engine.check_health_is_zero_or_below(player) == False:
        #     engine.player_has_lost()
        #     is_running=False
        board = engine.create_board(boards[player["current_board"]])
        engine.put_player_on_board(board, player)
        ui.display_board(board, boards[player["current_board"]]["name"],
                         player, quests, show_inventory, show_legend, legend)
        key = util.key_pressed()
        engine.remove_player_from_board(board, player)

        if key in ["W", "w", "s", "S", "a", "A", "D", "d"]:
            player = engine.move_player(board, player, key, boards)
        if key in ["q", "Q"]:
            is_running = False
            break
        elif key in ["i", "I"] and "inventory" in player:
            show_inventory = make_opposite_boolean(show_inventory)
        elif key in ["l", "L"]:
            show_legend = make_opposite_boolean(show_legend)
        else:
            pass
        engine.plot_development(player, quests, boards, board)
        util.clear_screen()
        if engine.check_health_is_zero_or_below(player) == False:
            engine.player_has_lost()
            is_running = False
        # is_running = engine.check_health_is_zero_or_below(player)


if __name__ == '__main__':
    main()
