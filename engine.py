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

    Args:
    dictionary: The details of a board in a form of dictionary, with "width" and "height" among them.
    strings: horizontal_brick, vertical_brick and floor_char are characters with which the board will be built.

    Returns:
    list: horizontal_wall - the list that would be added at the beginning and end of each board
    list: middle_row - the list that will be between the horizontal walls
    '''
    horizontal_wall = [horizontal_brick for i in range(board["width"])]
    middle_row = [vertical_brick]
    middle_row.extend([floor_char for i in range(board["width"]-2)])
    middle_row.extend([vertical_brick])

    return horizontal_wall, middle_row


def add_static_elements(board, board_list):
    for key in board["static_elements"]:
        for cor in board["static_elements"][key]["coor"]:
            x = cor[0]
            y = cor[1]
            board_list[y][x] = board["static_elements"][key]["icon"]
    return board_list


def add_const_elements(board, board_list, to_add=""):
    """
    Add exits signs and items to the board_list.

    Args:
    dictionary: The details of a board in a form of dictionary, with "exits", "nature" and "items" among them.
    list: The list of lists in which the characters will be changed
    string: The type of added element

    Returns:
    list: Game board
    """
    if to_add in board:
        for element in board[to_add]:
            x = board[to_add][element]["index_x"]
            y = board[to_add][element]["index_y"]
            board_list[y][x] = board[to_add][element]["icon"]
    return board_list

def add_boos(board, board_list, to_add=""):
    if to_add == "Boss":
        icons_nested_list=board[to_add]["icons"]
        for i in range(len(icons_nested_list)):
            for j in range(len(icons_nested_list[i])):
                board_list[i+3][j+4]=icons_nested_list[i][j]

            
        # if to_add == "Boss":
        #     x = [0:len(board[to_add][element]["width"])]
        #     y = [0:len(board[to_add][element]["height"])]
    else:
        if to_add in board:
            for element in board[to_add]:
                x = board[to_add][element]["index_x"]
                y = board[to_add][element]["index_y"]
                board_list[y][x] = board[to_add][element]["icon"]
    return board_list



def create_board(board):
    '''
    Creates a new game board based on input parameters.

    Args:
    dictionary: The details of a board in a form of dictionary, with "width" and "height" among them.

    Returns:
    list: Game board
    '''
    horizontal_brick = "-"
    vertical_brick = "|"
    floor_char = " "
    exit_char = "x"

    horizontal_wall, middle_row = create_rows(board, horizontal_brick, vertical_brick, floor_char)

    board_list = []
    north_wall = copy.deepcopy(horizontal_wall)
    south_wall = copy.deepcopy(horizontal_wall)

    board_list.append(north_wall)
    for row in range(board["height"]-2):
        middle_row_copy = copy.deepcopy(middle_row)
        board_list.append(middle_row_copy)
    board_list.append(south_wall)

    for category in ["exits", "items", "characters", "food"]:
        board_list = add_const_elements(board, board_list, category)
    
    if "Boss" in board:
        for category in ["exits", "items", "characters", "food", "Boss"]:
            board_list=add_boos(board, board_list, category)
        

    board_list = add_static_elements(board, board_list)

    return board_list


def put_player_on_board(board, player):
    '''
    Modifies the game board by placing the player icon at its coordinates.

    Args:
    list: The game board
    dictionary: The player information containing the icon and coordinates

    Returns:
    Nothing
    '''
    y = player["position_y"]-1
    x = player["position_x"]-1
    board[y][x] = player["player_icon"]


def remove_player_from_board(board, player):
    '''
    Modifies the player position  by removing the player icon at its coordinates.

    Args:
    list: The game board
    dictionary: The player information containing the icon and coordinates

    Returns:
    Nothing
    '''
    y = player["position_y"]-1
    x = player["position_x"]-1
    board[y][x] = " "


def change_board(player, boards, direction_from, direction_to):

    next_board = boards[player["current_board"]]["exits"][direction_to]["leads_to"]
    player["current_board"] = next_board

    directions = ["south", "north", "east", "west"]
    correction_numbers = [[1, 0], [1, 2], [0, 1], [2, 1]] #numbers to correct user's position on the board

    for direction in directions:
        if direction_from == direction:
            index = directions.index(direction)
            player["position_x"] = boards[next_board]["exits"][direction_from]["index_x"] + correction_numbers[index][0]
            player["position_y"] = boards[next_board]["exits"][direction_from]["index_y"] + correction_numbers[index][1]


def update_inventory(boards, player, to_add, what_we_update): #player, stone, items
    if "inventory" not in player:
        player["inventory"] = {}

    if to_add in player["inventory"]:
        player["inventory"][to_add] += boards[player["current_board"]][what_we_update][to_add]["number"]
    else:
        player["inventory"][to_add] = boards[player["current_board"]][what_we_update][to_add]["number"]
    return boards


def remove_object_from_board(board, player, to_remove, boards, what_we_update):
    '''
    Removes the item from the "boards" dictionary.

    Args:
    list: The game board
    dictionary: The player information
    dictionary: Information about the item
    dictionary: Boards available in the game

    Returns:
    Nothing. Only modifies "boards" dictionary.
    '''
    board_name = player["current_board"]
    del boards[board_name][what_we_update][to_remove]
    print("usun")


def update_player_health(player, key):
    player["health"] += key


def get_item(player, axis, current_board, sign, boards, what_we_update):
    '''
    Walks into items, adds them to the inventory and removes from the board

    Args:
    dictionary: player's dictionary with all the information about player
    string: "position_x" or "position_x" - tells us in which direction player's moving
    dictionary: the details of the board on which the player currently is
    string: "-" or "+" sign tells us whether the movement index is increasing or decreasing

    Returns:
    Nothing. The current board and player's inventory are modified.

    '''
    if sign == "-":
        player[axis] -= 1
    else:
        player[axis] += 1

    items_on_board = current_board[what_we_update]
    if what_we_update == "items":
        for item in items_on_board:
            if items_on_board[item]["index_x"]+1 == player["position_x"]:
                boards = update_inventory(boards, player, item, what_we_update)
                remove_object_from_board(current_board, player, item, boards, what_we_update)
                break
    elif what_we_update == "food":
        for item in items_on_board:
            if items_on_board[item]["index_x"] + 1 == player["position_x"]:
                update_player_health(player, items_on_board[item]["health"])
                remove_object_from_board(current_board, player, item, boards, what_we_update)
                break
    return boards


def interact_with_character(boards, icon, player):
    if icon == "L":
        board_name = player["current_board"]
        print("interact")
        del boards[board_name]["characters"]["Loki"]
        # RICARDO:
        # Here you could add a condition that if a player has "thor's hammer" and the "captain's america's shield"
        # in the inventory, then he wins this fight (Loki is deleted from the board - as above). If not, the game is ended
        # - the player looses and game quits


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
    elif desired_place_coordinates[move_index] == "Q":
        change_board(player, boards, movement_directions[move_index][0], movement_directions[move_index][1])
        change_description(player)
    elif desired_place_coordinates[move_index] in ["$", "D", "1", "?", "B", "*","K", "R"]:
        boards = get_item(player, movement_axis[move_index][0], current_board, movement_axis[move_index][2], boards, "items")
    elif desired_place_coordinates[move_index] in [":", "=", "U"]:
        get_item(player, movement_axis[move_index][0], current_board, movement_axis[move_index][2], boards, "food")
    elif desired_place_coordinates[move_index] == "L":
        fight_with_Loki(player, current_board)
        # kick = mixer.Sound("kick.wav")
        # mixer.music.stop()
        # kick.play()
        # mixer.music.play()
        
        if check_health_is_zero_or_below(current_board["characters"]["Loki"])==False:
 
            print(current_board["characters"]["Loki"]["health"])
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
        # fight_with_Boss()
    elif desired_place_coordinates[move_index] == "+":
        fight_with_Boss(boards, player)
            

    return player


def plot_development(player, quests, boards, board_list):
    '''
    description
    '''
    message, message_type, name = "", "no_type", ""
    if player["current_board"] == "board_1":
        if "Loki" in boards["board_1"]["characters"]:
            character_movement(boards, "board_1", board_list, "Loki")
        else:  # kamienie pokazują się po zniknięciu Lokiego:
            if "mind stone" not in player["inventory"]:
                add_infinity_stones(boards, "board_1", "mind stone", 9, 3)
            if "time stone" not in player["inventory"]:
                add_infinity_stones(boards, "board_1", "time stone", 5, 5)
            if "mind stone" in player["inventory"] and "time stone" in player["inventory"]:
                boards[player["current_board"]]["exits"]["north"]["icon"] = "Q"
                boards["board_2"]["exits"]["south"]["icon"] = "Q"
    

    elif player["current_board"] == "board_2":
        if "reality stone" in player["inventory"] and "space stone" in player["inventory"]:
                boards[player["current_board"]]["exits"]["north"]["icon"] = "Q"
                boards["board_3"]["exits"]["south"]["icon"]="Q"

    elif player["current_board"] == "board_3":
        characters = boards[player["current_board"]]["characters"] # map Characters dict into local var
        for character_name in characters:
            if player_next_to_character(player,
                                        character_name,
                                        boards[player["current_board"]]):
                message, message_type, name = characters[character_name]["riddle"], "input", character_name
        if "power stone" in player["inventory"] and "soul stone" in player["inventory"]:
                boards[player["current_board"]]["exits"]["north"]["icon"] = "Q"
                boards["board_4"]["exits"]["south"]["icon"]="Q"
    
    elif player["current_board"] == "board_4":
        # put_boss_on_board(boards)
        pass
        # character_movement(boards, "board_4", board_list, "Boss")
    
    return message, message_type, name

def validate_answer(character_name, player, boards):
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


def check_health_is_zero_or_below(character):
    if character["health"] < 0:
        return False
    else:
        return True


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

def change_description(player):
    if player["current_board"] == "board_1":
        player["quest"] = 1
    elif player["current_board"] == "board_2":
        player["quest"] = 2
    elif player["current_board"] == "board_3":
        player["quest"] = 3
    elif player["current_board"] == "board_4":
        player["quest"] = 4

def fight_with_Boss(boards,player):
    weapon = input("Look in your inventory. What do you want to use? > ")
    if (weapon in ["ak", "AK-47", "AK-47","Racket-Luncher","Racket"]):
        print("Good choice for you. I am weaker now")
        sleep(2)
        boards["board_4"]["Boss"]["health"] -= 300
    
        
    else:
        print("Bad choice. You are weaker now")
        sleep(2)
        player["health"]-=40