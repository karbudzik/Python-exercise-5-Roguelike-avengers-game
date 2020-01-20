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
      

def update_inventory(player, to_add):
    if "inventory" not in player:
        player["inventory"] = {}
        
    if to_add in player["inventory"]:
        player["inventory"][to_add] += main.boards[player["current_board"]]["items"][to_add]["number"]
    else:
        player["inventory"][to_add] = main.boards[player["current_board"]]["items"][to_add]["number"]


def remove_object_from_board(board, player, to_remove, boards):
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
    del boards[board_name]["items"][to_remove]
    

def get_item(player, axis, current_board, sign, boards):
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
        
    items_on_board = current_board["items"]
    for item in items_on_board:
        if items_on_board[item]["index_x"]+1 == player["position_x"]: #makes sure only one item is taken by user, not all items from the board
            update_inventory(player, item)
            remove_object_from_board(current_board, player, item, boards)
            break


def interact_with_character(boards, icon, player):
    
    if icon == "L":
        board_name = player["current_board"]
        del boards[board_name]["characters"]["Loki"]
        # RICARDO: Here you can add a condition that if a player has "thor's hammer" and the "captain's america's shield"
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
    # At the end this function will have to be refactored (too many repeatable lines)

    if key in ["a", "A"]:
        if index_x > 1 and board[index_y][index_x - 1] in [" "]:
            player["position_x"] -= 1
        elif board[index_y][index_x - 1] == "x":     
            change_board(player, boards, "west", "east")
        elif board[index_y][index_x - 1] in ["$", "D", "1", "?"]:
            get_item(player, "position_x", current_board, "-", boards)
        elif board[index_y][index_x - 1] == "L":
            interact_with_character(boards, "L", player)
            player["position_x"] -= 1
                
    elif key in ["d", "D"]:
        if index_x < (width - 1) and board[index_y][index_x + 1] in [" "]:
            player["position_x"] += 1
        elif board[index_y][index_x + 1] == "x":
            change_board(player, boards, "east", "west")
        elif board[index_y][index_x + 1] in ["$", "D", "1", "?"]:
            get_item(player, "position_x", current_board, "+", boards)
        elif board[index_y][index_x + 1] == "L":
            interact_with_character(boards, "L", player)
            player["position_x"] += 1
                    
    elif key in ["s", "S"]:
        if index_y < (height - 1) and board[index_y + 1][index_x] in [" "]:
            player["position_y"] += 1
        elif board[index_y + 1][index_x] == "x": 
            change_board(player, boards, "south", "north")
        elif board[index_y + 1][index_x] in ["$", "D", "1", "?"]:
            get_item(player, "position_y", current_board, "+", boards)
        elif board[index_y + 1][index_x] == "L":
            interact_with_character(boards, "L", player)
            player["position_y"] += 1

    elif key in ["w", "W"]:
        if index_y > 1 and board[index_y - 1][index_x] in [" "]:
            player["position_y"] -= 1
        elif board[index_y - 1][index_x] == "x":
            change_board(player, boards, "north", "south")
        elif board[index_y - 1][index_x] in ["$", "D", "1", "?"]:
            get_item(player, "position_y", current_board, "-", boards)
        elif board[index_y - 1][index_x] == "L":
            interact_with_character(boards, "L", player)
            player["position_y"] -= 1
            
    return player


def plot_development(player, quests):
    '''
    description
    '''
    if player["quest"] == 1:
        pass
        #if a player just won 

    # jeśli loki koło nas to tracimy 20hp co ruch
    # jak ma sword to może bić lokiego
    # jak zabijemy lokiego to dodają się do inventory kamienie
    # jak ma armor to może tracić hp wolniej
    # jeśli 


'''
        #spr hp czy żyje
'''