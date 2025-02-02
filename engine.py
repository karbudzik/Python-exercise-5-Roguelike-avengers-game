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


def change_quest(player):
    """
    Changes "quest" value in player's dictionary to match the board he's currently in.
    Args: player (dictionary)
    Returns: player (dictionary)
    """

    board_names = ["board_1", "board_2", "board_3", "board_4"]
    board_index = board_names.index(player["current_board"])
    player["quest"] = board_index + 1

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


def move_player(board, player, key, boards):
    '''
    Modifies the player's coordinates to match the pressed key.
    Prevents from walking into walls and loads another board if a player go into gate.
    Args: board (list of lists), player (dictionary), key (string) and boards (dictionary).
    Returns: "Player" dictionary with modified player's coordinates
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
    move_index = [key_pairs.index(pair) for pair in key_pairs if key in pair][0]

    if condition_if_not_wall[move_index] and desired_place_coordinates[move_index] in [" "]:
        player[movement_axis[move_index][0]] += movement_axis[move_index][1]
    elif desired_place_coordinates[move_index] == "+":
        player = change_board(player, boards, movement_directions[move_index][0], movement_directions[move_index][1])
    elif desired_place_coordinates[move_index] in ["$", "?", "*"]:
        player[movement_axis[move_index][0]] += movement_axis[move_index][1]
        boards = get_item(player, current_board, boards)
    elif desired_place_coordinates[move_index] in [":", "=", "U"]:
        player[movement_axis[move_index][0]] += movement_axis[move_index][1]
        boards, player = eat_food(player, current_board, boards)
    elif desired_place_coordinates[move_index] == "L":
        fight_with_Loki(player, current_board)
    elif desired_place_coordinates[move_index] == "E":
        ask_for_cheat_code()
    elif desired_place_coordinates[move_index] in ["\\", "/", "[", "]"]:
        fight_with_boss(boards, player)
            
    return player


def plot_development(player, boards, board_list):
    '''
    Function in charge of changing boards' elements to the current plot of the game.
    Args: player (dictionary), boards (dictinary) and board_list (list of lists).
    Returns: message, message_type and name (all strings).
    '''

    message, message_type, name = "", "no_type", ""
        
    if player["current_board"] == "board_1":
        if "Loki" in boards["board_1"]["characters"]:
            boards = character_movement(boards, "board_1", board_list, "Loki")
        else: 
            boards = update_board_if_loki_dead(player, boards)
            boards = open_gates_if_stones_collected(["time stone", "mind stone"], player, boards)

    elif player["current_board"] == "board_2":
        boards = open_gates_if_stones_collected(["reality stone", "space stone"], player, boards)

    elif player["current_board"] == "board_3":
        message, message_type, name = get_riddle_from_characters(boards, player)
        boards = open_gates_if_stones_collected(["power stone", "soul stone"], player, boards)
    
    return message, message_type, name


def ask_for_cheat_code():
    """
    Asks player for a cheat code that allows user to win the game without fighting the main boss.
    Args: none.
    Returns: nothing.
    """

    answer = input("You can win easily if you know a secret code. Do you know it? [yes/no] >  ")
    if answer in ["yes", "Yes", "Yes", "y", "Y"]:
        cheat = input("Type a cheat code: > ")
        if (cheat in ["Avengers", "AVENGERS", "avengers"]):
            ui.player_has_won()
    
    print("You have to find other way.Hint: Look up the current board")
    sleep(3)


def update_board_if_loki_dead(player, boards):
    """
    Adds infinity stones to the board when Loki is killed.
    Args: player and boards (both dictionaries)
    Returns: boards (dictionary)
    """

    if "mind stone" not in player["inventory"]:
        boards = add_infinity_stone(boards, "board_1", "mind stone", 9, 3)
    if "time stone" not in player["inventory"]:
        boards = add_infinity_stone(boards, "board_1", "time stone", 5, 5)
    
    return boards


def open_gates_if_stones_collected(stones, player, boards):
    """
    Opens gates to another board if two required stones are collected.
    Args: stones (list with two strings), player and boards (both dictionaries).
    Returns boards (dictionary).
    """

    if stones[0] in player["inventory"] and stones[1] in player["inventory"]:
        board_names = ["board_1", "board_2", "board_3", "board_4"]
        current_index = board_names.index(player["current_board"])
        boards[player["current_board"]]["exits"]["north"]["icon"] = "+"
        boards[board_names[current_index + 1]]["exits"]["south"]["icon"] = "+"
    
    return boards


def get_riddle_from_characters(boards, player):
    """
    Gets riddle of the character if player stands next to him.
    Args: boards and player (both dictionaries).
    Returns: message, message_type, name (all strings)
    """

    characters = boards[player["current_board"]]["characters"]
    message, message_type, name = "", "no_type", ""
    for character_name in characters:
        if player_next_to_character(player, character_name, boards[player["current_board"]]):
            message, message_type, name = characters[character_name]["riddle"], "input", character_name
    
    return message, message_type, name


def validate_answer(character_name, player, boards, message_type):
    """
    Validates user's answer to the riddle. User has 3 chances to guess and then dies.
    Args: character_name (string), player and boards (dictionaries) and message_type (string)
    Returns: Nothing.
    """

    if message_type == "input":  
        riddle_solved = False
        while not riddle_solved and player["riddle_counter"] < 3:
            answer = input("What's Your answer? ")
            if answer in boards[player["current_board"]]["characters"][character_name]["answer"]:
                riddle_solved = True
                player["riddle_counter"] = 0
                print("You are right. The stone is yours!")
                boards = change_character_into_infinity_stone(character_name, boards)
            else:
                player["riddle_counter"] += 1
        if player["riddle_counter"] >= 3:
            ui.player_has_lost()   


def change_character_into_infinity_stone(character_name, boards):
    """
    After player guesses the riddle, character changes into the infinity stone.
    Args: character_name (string), boards (dictionary).
    Returns: boards (dictionary)
    """

    stone_name = boards["board_3"]["characters"][character_name]["stone"]
    stone_x = boards["board_3"]["characters"][character_name]["index_x"]
    stone_y = boards["board_3"]["characters"][character_name]["index_y"]
    boards = add_infinity_stone(boards, "board_3", stone_name, stone_x, stone_y)
    remove_enemy_from_board(boards["board_3"]["characters"], character_name)

    return boards


def character_movement(boards, board, board_list, name):
    """
    Randomly moves the character on the board.
    Args: boards (dictionary), board (string), board_list (list of lists) and name (string).
    Returns: boards (dictionary)
    """

    bad_character = boards[board]["characters"][name]
    numbers = random.choices(["0", "1", "-1"], k=2)
    if check_free_space(numbers, board_list, bad_character):
        bad_character["index_y"] += int(numbers[0])
        bad_character["index_x"] += int(numbers[1])
    
    return boards


def get_neighbor_fields(field_coor):
    """
    Gets the list of coordinates of all fields next to the given coordinates.
    Args: fields_coor (tuple).
    Returns: neighboring_fields (list)
    """
    
    neighboring_fields = [[field_coor[0] - 1, field_coor[1]],
                          [field_coor[0] + 1, field_coor[1]],
                          [field_coor[0], field_coor[1] - 1],
                          [field_coor[0], field_coor[1] + 1]]

    return neighboring_fields


def player_next_to_character(player, character_name, board):
    """
    Checks if a player stands on a field right next to the given character.
    Args: player (dictionary), character_name (string), board (dictionary).
    Returns: boolean.
    """

    character_coor = (board["characters"][character_name]["index_x"] + 1,
                        board["characters"][character_name]["index_y"] + 1)
    neighboring_fields = get_neighbor_fields(character_coor)

    player_coor = [player["position_x"], player["position_y"]]
    if player_coor in neighboring_fields:
        return True
    else:
        return False


def remove_enemy_from_board(board,enemy):
    """
    Removes an enemy from the given board.
    Args: board (dictionary) and enemy's name (string).    
    Returns: Nothing.
    """

    del board[enemy]


def add_infinity_stone(boards, board, stone_name, x, y):
    """
    Adds a new infinity stone to the dictionary.
    Args: boards (dictionary), board (string), stone_name (string) and x and y (integers).
    Returns: boards (dictionary)
    """

    boards[board]["items"][stone_name] = {
        "number": 1,
        "index_x": x,
        "index_y": y,
        "icon":"*",
    }
    return boards


def check_free_space(move, board_list, character):
    """
    Checks if a place where character is "planning" to move is empty.
    Args: move (tuple of move coordinates), board_list (list of lists) and character (dictionary).
    Returns: boolean
    """

    field_y = character["index_y"] + int(move[0])
    field_x=character["index_x"]+int(move[1])
    if board_list[field_y][field_x] == " ":
        return True
    return False


def check_health_is_zero_or_below(player, is_running):
    """
    Checks if player's health is above 0. If not, ends the game.
    Args: player (dictionary) and is_running (boolean).
    Returns: is_running (boolean)
    """

    if player["health"] < 0:
        ui.player_has_lost()
        return False
    else:
        return is_running


def is_enemy_dead(enemy):
    """
    Checks if character's health dropped below 0.
    Args: character's dictionary.
    Returns: boolean.
    """

    if enemy["health"] < 0:
        return True
    else:
        return False


def fight_with_Loki(player, current_board):
    """
    Conducts fight with Loki, effecting player's and Loki's HP according to the acquired armor.
    Args: player (dictionary) and current_board (dictionary).
    Returns: Nothing.
    """

    if "thor's hammer" in player["inventory"] and "captain's america' shield" in player["inventory"]:
        current_board["characters"]["Loki"]["health"] -= 50
    elif "captain's america' shield" in player["inventory"]:
        current_board["characters"]["Loki"]["health"] -= 10
        player["health"] -= 20
    elif "thor's hammer" in player["inventory"]:
        current_board["characters"]["Loki"]["health"] -= 40
        player["health"] -= 40
    elif "thor's hammer" not in player["inventory"] and "captain's america' shield" not in player["inventory"]:
        player["health"] -= 50
    if is_enemy_dead(current_board["characters"]["Loki"]) == True:
        remove_enemy_from_board(current_board["characters"], "Loki")


def fight_with_boss(boards, player):
    """
    Conducts dialog fight with Thanos, effecting player's and Thanos's HP according to the used equipment.
    Args: board and player (both dictionaries).
    Returns: Nothing.
    """
    
    weapon = input("Look in your inventory. What do you want to use? > ")
    if weapon in ["ak", "AK", "AK-47", "AK-47", "ak-47"]:
        if "AK-47" in player["inventory"]:
            print("Thanos: 'Oh nooo... It hurts...'")
            sleep(3)
            boards["board_4"]["boss"]["health"] -= 300
            del player["inventory"]["AK-47"]
        else:
            print("Thanos: 'Ooops, you don't have that weapon, looser!'")
            sleep(3)
            player["health"] -= 40
    elif weapon in ["Rocket-Launcher","Rocket", "rocket"]:
        if "Rocket-Launcher" in player["inventory"]:
            print("Thanos: 'What a terrifying weapon... Where did you get that???'")
            sleep(3)
            boards["board_4"]["boss"]["health"] -= 300
            del player["inventory"]["Rocket-Launcher"]
        else:
            print("Thanos: 'Ooops, you don't have that weapon, looser!'")
            sleep(3)
            player["health"] -= 40
    else:
        print("Bad choice. You are weaker now")
        sleep(3)
        player["health"] -= 40

    if is_enemy_dead(boards[player["current_board"]]["boss"]) == True:
        remove_enemy_from_board(boards[player["current_board"]], "boss")
        ui.player_has_won()