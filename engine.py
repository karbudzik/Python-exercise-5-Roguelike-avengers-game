import copy
import main
import collections

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


def add_const_elements(board, board_list, to_add=""):
    """
    Add exits signs, nature elements and items to the board_list.

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

    board_list = add_const_elements(board, board_list, "exits")
    board_list = add_const_elements(board, board_list, "nature")
    board_list = add_const_elements(board, board_list, "items")
    board_list = add_const_elements(board, board_list, "characters")
    board_list = add_const_elements(board, board_list, "food")

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

    next_board = boards[player["current_board"]]["exits"][direction_from]["leads_to"]
    player["current_board"] = next_board
    player["position_x"] = boards[next_board]["exits"][direction_to]["index_x"] + 1
    player["position_y"] = boards[next_board]["exits"][direction_to]["index_y"] + 1
      

def update_inventory(player, to_add,what_we_update):
    if "inventory" not in player:
        player["inventory"] = {}
        
    if to_add in player["inventory"]:
        player["inventory"][to_add] += main.boards[player["current_board"]][what_we_update][to_add]["number"]
    else:
        player["inventory"][to_add] = main.boards[player["current_board"]][what_we_update][to_add]["number"]


def remove_object_from_board(board, player, to_remove, boards,what_we_update):
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
    
def update_player_health(player, key):
    player["health"]+=key

def get_item(player, axis, current_board, sign, boards,what_we_update):
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
    if what_we_update=="items":
        for item in items_on_board:
            if items_on_board[item]["index_x"]+1 == player["position_x"]: 
                update_inventory(player, item,what_we_update)
                remove_object_from_board(current_board, player, item, boards,what_we_update)
                break
    elif what_we_update == "food":
        for item in items_on_board:
            if items_on_board[item]["index_x"] + 1 == player["position_x"]:
                update_player_health(player, items_on_board[item]["health"])
                remove_object_from_board(current_board, player, item, boards, what_we_update)
                break
        


def interact_with_character(boards, icon, player):
    if icon == "L":
        board_name = player["current_board"]
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
    movement_directions = [["west", "east"], ["east", "west"], ["south", "north"], ["north", "south"]]

    for pair in key_pairs:
        if key in pair:
            move_index = key_pairs.index(pair)

    if condition_if_not_wall[move_index] and desired_place_coordinates[move_index] in [" "]:
        player[movement_axis[move_index][0]] += movement_axis[move_index][1]
    elif desired_place_coordinates[move_index] == "x":     
        change_board(player, boards, movement_directions[move_index][0], movement_directions[move_index][1])
    elif desired_place_coordinates[move_index] in ["$", "D", "1", "?", "B"]:
        get_item(player, movement_axis[move_index][0], current_board, movement_axis[move_index][2], boards, "items")
    elif desired_place_coordinates[move_index] in [":", "=", "U"]:
        get_item(player, movement_axis[move_index][0], current_board, movement_axis[move_index][2], boards, "food")
    elif desired_place_coordinates[move_index] == "L":
        interact_with_character(boards, "L", player)
        player[movement_axis[move_index][0]] += movement_axis[move_index][1]

    return player


def plot_development(player, quests):
    '''
    description
    '''
    if player["quest"] == 1: #it's only for the plot happening on Earth (board_1)
        # pass
        #RICARDO - here you can add some conditions:

        # 1. First, if you didn't collect 2 infinity stones from the first board, the gates (x) should be locked
        # You can do that e.g. by adding "gates_unlocked":False to the board's dictionary and then change it to True 
        # (in this function here) when the stones are collected. You'll also have to add some "if board[gates_unlocked] == True"
        # condition to the change_board() function

        # 2. Loki should be at least a little dangerous, so you might add a trick - if user stands close to Loki (their 
        # coordinates are close e.g. player has [4][5] and Loki has [3][5], user's health might decrease -20)

        # 3. if a player just won battle with Loki (Loki is no longer in board["characters"]) - two infinity stones 
        # are added to board["items"] and, therefore, displayed on the board. Or, if you prefer, they might already be
        # in the board's dictionary, but they can have some "invisible":true key which would prevent it from being displayed 
        # (add_const_elements() would have to be slightly modified then)

        # The details of the stones (like names) you can find in story.txt file

        # If a person collects all 2 infinity stones, two things happen:
        # a) in player's dictionary "quest" is changed to "2"
        # b) the gates are visible, as described in 1.
        print("1")
    elif player["quest"] == 2:
        pass
    elif player["quest"] == 3:
        pass
    # at the end of this function we might add condition checking if player didn't loose too much hp - if hp is equal/lower 
    # than 0, then the person died and game ended


