import copy
import main
import collections
import random
import pygame
from pygame import mixer
import ui
from time import sleep


def create_rows(board, horizontal_brick, vertical_brick, floor_char):
    '''
    Creates default rows to build the board with.
    Args: board (dictionary from main.py) and three strings: characters with which the board will be built.
    Returns: two lists: horizontal_wall and middle row 
    '''

    horizontal_wall = [horizontal_brick for i in range(board["width"])]
    middle_row = [vertical_brick]
    middle_row.extend([floor_char for i in range(board["width"]-2)])
    middle_row.extend([vertical_brick])

    return horizontal_wall, middle_row


def add_static_elements(board, board_list):
    """
    Adds repeatable objects to the board (stones, trees etc.). Objects can't be collected by player.
    Args: current board in form of dictionary (board) and list of lists (board_list).
    Returns: list of lists (board_list) with extra elements added.
    """

    for key in board["static_elements"]:
        for cor in board["static_elements"][key]["coor"]:
            x = cor[0]
            y = cor[1]
            board_list[y][x] = board["static_elements"][key]["icon"]
    
    return board_list


def add_to_board(board, board_list, items_to_add):
    """
    Adds any elements to board_list.
    Args: Current board as dictionary (board) and list of lists (board_list) as well as all items to add (list).
    Returns: list of lists (board_list)
    """
    
    for to_add in items_to_add:
        if to_add in board:
            for element in board[to_add]:
                x = board[to_add][element]["index_x"]
                y = board[to_add][element]["index_y"]
                board_list[y][x] = board[to_add][element]["icon"]
    
    return board_list


def add_boss(board, board_list):
    """
    Adds a boss that consists of more than one character.
    Args: Current board as dictionary (board) and list of lists (board_list).
    Returns: list of lists (board_list)
    """

    if "boss" in board:
        icons_nested_list = board["boss"]["icons"]
        for i in range(len(icons_nested_list)):
            for j in range(len(icons_nested_list[i])):
                board_list[i + board["boss"]["position_x"]][j + board["boss"]["position_y"]] = icons_nested_list[i][j]

    return board_list


def put_player_on_board(board, player):
    '''
    Modifies the game board by placing the player icon at its coordinates.
    Args: list of lists (the game board) and dictionary (the player information containing icon and coordinates)
    Returns: modified list of lists
    '''

    y = player["position_y"]-1
    x = player["position_x"]-1
    board[y][x] = player["player_icon"]

    return board


def add_all_additions_to_board(board, board_list, player):
    '''
    Coordinates adding all other elements to board (player, static elements, characters and collectables).
    Args: dictionaries (board and player) and list of lists (board_list).
    Returns: list of lists.
    '''

    board_list = add_to_board(board, board_list, ["exits", "items", "characters", "food"])
    board_list = add_boss(board, board_list)
    board_list = add_static_elements(board, board_list)
    board_list = put_player_on_board(board_list, player)
    
    return board_list


def create_board(board, player):
    '''
    Creates a new game board based on input parameters.
    Args: dictionaries with details of the board and the player.
    Returns: list - game board
    '''

    horizontal_brick, vertical_brick, floor_char = "-", "|", " "
    board_list = []
    
    horizontal_wall, middle_row = create_rows(board, horizontal_brick, vertical_brick, floor_char)
    north_wall = copy.deepcopy(horizontal_wall)
    south_wall = copy.deepcopy(horizontal_wall)

    board_list.append(north_wall)
    for row in range(board["height"]-2):
        board_list.append(copy.deepcopy(middle_row))
    board_list.append(south_wall)

    board_list = add_all_additions_to_board(board, board_list, player)
    
    return board_list


def remove_player_from_board(board, player):
    '''
    Modifies the player position  by removing the player icon at its coordinates.
    Args: list of lists (the game board) and dictionary (player information containing icon and coordinates)
    Returns: list of lists (the game board)
    '''

    y = player["position_y"]-1
    x = player["position_x"]-1
    board[y][x] = " "

    return board


def correct_coordinates(player, boards, direction_from, next_board):
    '''
    Corrects user's coordinates after entering to another room. Correction was needed due to some bug in user's movement mechanism.
    Args: player (list of lists), boards (dictinary), direction_from and next_board (strings)
    Returns: player (dictionary)
    '''

    directions = ["south", "north", "east", "west"]
    correction_numbers = [[1, 0], [1, 2], [0, 1], [2, 1]]

    for direction in directions:
        if direction_from == direction:
            index = directions.index(direction)
            player["position_x"] = boards[next_board]["exits"][direction_from]["index_x"] + correction_numbers[index][0]
            player["position_y"] = boards[next_board]["exits"][direction_from]["index_y"] + correction_numbers[index][1]
    
    return player


def change_board(player, boards, direction_from, direction_to):
    '''
    Function responsible for printing another board while player walks through the door.
    Args: player (list of lists), boards (dictionary), direction_from and direction_to (strings)
    Returns: player (dictionary)
    '''

    next_board = boards[player["current_board"]]["exits"][direction_to]["leads_to"]
    player["current_board"] = next_board
    player = correct_coordinates(player, boards, direction_from, next_board)
    player = change_quest(player)
    
    return player


def update_inventory(boards, player, to_add, what_we_update): 
    '''
    Adds an item to player's inventory.
    Args: boards, player and to_add (dictionaries), what_we_update (string).
    Returns: boards.
    '''

    if to_add in player["inventory"]:
        player["inventory"][to_add] += boards[player["current_board"]][what_we_update][to_add]["number"]
    else:
        player["inventory"][to_add] = boards[player["current_board"]][what_we_update][to_add]["number"]
    
    return boards


def remove_object_from_board(board, player, to_remove, boards, what_we_update):
    '''
    Removes the item from the "boards" dictionary.
    Args: board (list of lists), player, to_remove, boards (all dictionaries) and what_we_update (string)
    Returns: boards (list of lists)
    '''

    board_name = player["current_board"]
    del boards[board_name][what_we_update][to_remove]
    
    return boards


def update_player_health(player, value):
    '''
    Adds hp value of consumed item to player's health.
    Args: player (dictionary), value (integer).
    Returns: player (dictionary)
    '''
    player["health"] += value
    
    return player


def get_item(player, current_board, boards):
    '''
    Collects items (adds them to inventory and removes from the board).
    Args: player, current_board, boards (all dictionaries).
    Returns: boards (dictionary).
    '''

    items_on_board = current_board["items"]
    for item in items_on_board:
        if items_on_board[item]["index_x"]+1 == player["position_x"]:
            boards = update_inventory(boards, player, item, "items")
            boards = remove_object_from_board(current_board, player, item, boards, "items")
            break

    return boards


def eat_food(player, current_board, boards):
    '''
    Collects food (removes it from the board and updates player's health by its value).
    Args: player, current_board, boards (all dictionaries).
    Returns: boards and player (both dictionaries).
    '''
    
    food_on_board = current_board["food"]
    for food in food_on_board:
        if food_on_board[food]["index_x"] + 1 == player["position_x"]:
            player = update_player_health(player, food_on_board[food]["health"])
            boards = remove_object_from_board(current_board, player, food, boards, "food")
            break
    
    return boards, player


    #################################################################


def move_player(board, player, key, boards):
    '''
    Modifies the player's coordinates according to the pressed key.
    Prevents from walking into walls and loads another board if a player go into gate.

    Args:
    list: The game board
    dictionary: The player information containing the icon and coordinates
    string: The key pressed by the player ("w", "s", "a" or "d")

    Returns:
    "Player" dictionary with modified player's coordinates
    '''
    height = len(board)-1
    width = len(board[0]) - 1
    index_x = player["position_x"] - 1
    index_y = player["position_y"] - 1
    current_board = boards[player["current_board"]]

    key_pairs = [["a", "A"], ["d", "D"], ["s", "S"], ["w", "W"]]
    condition_if_not_wall = [[eval("index_x > 1")], [eval("index_x < (width - 1)")], [eval("index_y < (height - 1)")], [eval("index_y > 1")]]
    desired_place_coordinates = [board[index_y][index_x - 1], board[index_y][index_x + 1], board[index_y + 1][index_x], board[index_y - 1][index_x]]
    movement_axis = [["position_x", -1, "-"], ["position_x", 1, "+"], ["position_y", 1, "+"], ["position_y", -1, "-"]]
    movement_directions = [["east", "west"], ["west", "east"], ["north", "south"], ["south", "north"]]

    for pair in key_pairs:
        if key in pair:
            move_index = key_pairs.index(pair)

    if condition_if_not_wall[move_index] and desired_place_coordinates[move_index] in [" "]:
        player[movement_axis[move_index][0]] += movement_axis[move_index][1]
    elif desired_place_coordinates[move_index] == "+":
        player = change_board(player, boards, movement_directions[move_index][0], movement_directions[move_index][1])
    elif desired_place_coordinates[move_index] in ["$", "D", "1", "?", "B", "*","K", "R"]:
        player[movement_axis[move_index][0]] += movement_axis[move_index][1]
        boards = get_item(player, current_board, boards)
    elif desired_place_coordinates[move_index] in [":", "=", "U"]:
        player[movement_axis[move_index][0]] += movement_axis[move_index][1]
        boards, player = eat_food(player, current_board, boards)
    elif desired_place_coordinates[move_index] == "L":
        fight_with_Loki(player, current_board)
        
        if is_enemy_dead(current_board["characters"]["Loki"]) == True:
            remove_enemy_from_board(current_board["characters"], "Loki")
            player[movement_axis[move_index][0]] += movement_axis[move_index][1]
    
    elif desired_place_coordinates[move_index] == "E":
        answer = input("You Can beat easy:) Do you know a cheat[yes/now]? >  ")
        if answer in ["yes", "Yes", "Yes", "y", "Y"]:
            cheat = input("Type a cheat > ")
            if (cheat in ["Avengers", "AVENGERS","avengers"]):
                ui.won()
        
        print("You have to find other way.Hint: Look up the current board")
        sleep(3)
        
    elif desired_place_coordinates[move_index] in ["\\", "/", "[", "]"]:
        fight_with_boss(boards, player)
            

    return player


def plot_development(player, quests, boards, board_list):
    '''
    description
    '''
    message, message_type, name = "", "no_type", ""
        
    # elif check_health_is_zero_or_below(boards["board_4"]["Boss"]) == False:
    #     ui.won()
        
    if player["current_board"] == "board_1":
        if "Loki" in boards["board_1"]["characters"]:
            character_movement(boards, "board_1", board_list, "Loki")
        else:  # kamienie pokazują się po zniknięciu Lokiego:
            if "mind stone" not in player["inventory"]:
                add_infinity_stones(boards, "board_1", "mind stone", 9, 3)
            if "time stone" not in player["inventory"]:
                add_infinity_stones(boards, "board_1", "time stone", 5, 5)
            if "mind stone" in player["inventory"] and "time stone" in player["inventory"]:
                boards[player["current_board"]]["exits"]["north"]["icon"] = "+"
                boards["board_2"]["exits"]["south"]["icon"] = "+"
    

    elif player["current_board"] == "board_2":
        if "reality stone" in player["inventory"] and "space stone" in player["inventory"]:
                boards[player["current_board"]]["exits"]["north"]["icon"] = "+"
                boards["board_3"]["exits"]["south"]["icon"]="+"

    elif player["current_board"] == "board_3":
        characters = boards[player["current_board"]]["characters"] # map Characters dict into local var
        for character_name in characters:
            if player_next_to_character(player,
                                        character_name,
                                        boards[player["current_board"]]):
                message, message_type, name = characters[character_name]["riddle"], "input", character_name
        if "power stone" in player["inventory"] and "soul stone" in player["inventory"]:
                boards[player["current_board"]]["exits"]["north"]["icon"] = "+"
                boards["board_4"]["exits"]["south"]["icon"]="+"
    
    elif player["current_board"] == "board_4":
        # put_boss_on_board(boards)
        pass
        # character_movement(boards, "board_4", board_list, "boss")
    
    return message, message_type, name

def validate_answer(character_name, player, boards, message_type):
    if message_type == "input":  
        riddle_solved = False
        while not riddle_solved and player["riddle_counter"] < 3:
            answer = input("What's Your answer? ")
            if answer in boards[player["current_board"]]["characters"][character_name]["answer"]:
                riddle_solved = True
                player["riddle_counter"] = 0 # reset riddle counter
                print("You are right")
                stone_name = boards["board_3"]["characters"][character_name]["stone"]
                stone_x = boards["board_3"]["characters"][character_name]["index_x"]
                stone_y = boards["board_3"]["characters"][character_name]["index_y"]
                add_infinity_stones(boards, "board_3", stone_name, stone_x, stone_y)
                remove_enemy_from_board(boards["board_3"]["characters"], character_name)
                
            else:
                player["riddle_counter"] += 1

        if player["riddle_counter"] >= 3:
            print("Your are dead")
                # remove_player_from_board(player, boards[player["board"]])
                
            #NAPRAWIĆ - nie działa umieranie po 3 złych odpowiedziach


def character_movement(boards, board, board_list, name):
    black_character = boards[board]["characters"][name]
    numbers = random.choices(["0", "1", "-1"], k=2)
    print(numbers)
    print(black_character["index_x"], black_character["index_y"])
    if check_free_space(numbers, board_list, black_character):
        black_character["index_y"] += int(numbers[0])
        black_character["index_x"] += int(numbers[1])


def get_neighbor_fields(field_coor: tuple) -> list:
    neighboring_fields = [
                          [field_coor[0] - 1, field_coor[1]],
                          [field_coor[0] + 1, field_coor[1]],
                          [field_coor[0], field_coor[1] - 1],
                          [field_coor[0], field_coor[1] + 1]
                          ]
    return neighboring_fields

def player_next_to_character(player: dict,
                             character_name: str,
                             board: dict) -> bool:
    try:
        character_coor = (board["characters"][character_name]["index_x"] + 1,
                          board["characters"][character_name]["index_y"] + 1)
        neighboring_fields = get_neighbor_fields(character_coor)

        player_coor = [player["position_x"], player["position_y"]]
        if player_coor in neighboring_fields:
            return True
        else:
            return False
    except KeyError:
        return False


def player_is_close_to_Loki(player):
    if "Loki" in main.boards["board_1"]["characters"]:
        if (player['position_x'] + 1) == main.boards['board_1']['characters']['Loki']['index_x']:
            return True
        elif (player['position_y'] + 1) == main.boards['board_1']['characters']['Loki']['index_y']:
            return True
        else:
            return False
    else:
        return True


def player_is_next_to_Loki(player):
    if "Loki" in main.boards["board_1"]["characters"]:
        if player['position_x'] == main.boards['board_1']['characters']['Loki']['index_x']:
            return True
        elif player['position_y'] == main.boards['board_1']['characters']['Loki']['index_y']:
            return True
        else:
            return False
    else:
        return False
    


def remove_enemy_from_board(board,enemy):
    del board[enemy]


def add_infinity_stones(boards, board, stone_name, x, y):
    boards[board]["items"][stone_name] = {
        "number": 1,
        "index_x": x,
        "index_y": y,
        "icon":"*",
    }


def check_free_space(move, board_list, character):
    field_y = character["index_y"] + int(move[0])
    field_x=character["index_x"]+int(move[1])
    if board_list[field_y][field_x] == " ":
        return True
    return False


def check_health_is_zero_or_below(character, is_running):
    if character["health"] < 0:
        ui.player_has_lost()
        return False
    else:
        return is_running


def is_enemy_dead(enemy):
    if enemy["health"] < 0:
        ui.player_has_won()
        return True
    else:
        return False



def fight_with_Loki(player, current_board):
    if "thor's hammer" and "captain's america' shield" in player["inventory"]:
            current_board["characters"]["Loki"]["health"] -= 50
            #play fight music
    elif "thor's hammer" in player["inventory"]:
        current_board["characters"]["Loki"]["health"] -= 10
        player["health"] -= 40
        #play fight music
    elif "thor's hammer" not in player["inventory"] and "captain's america' shield" not in player["inventory"]:
        player["health"] -= 50
        print(player)
        #playe fight music

def change_quest(player):
    if player["current_board"] == "board_1":
        player["quest"] = 1
    elif player["current_board"] == "board_2":
        player["quest"] = 2
    elif player["current_board"] == "board_3":
        player["quest"] = 3
    elif player["current_board"] == "board_4":
        player["quest"] = 4

    return player

def fight_with_boss(boards,player):
    weapon = input("Look in your inventory. What do you want to use? > ")
    if (weapon in ["ak", "AK-47", "AK-47","Racket-Luncher","Racket"]):
        print("Good choice for you. I am weaker now")
        sleep(2)
        boards["board_4"]["boss"]["health"] -= 300
    #walka nie działa - hp nie schodzi Thanosowi i możemy go bić AK jak nie mamy go w inventory
        
    else:
        print("Bad choice. You are weaker now")
        sleep(2)
        player["health"]-=40