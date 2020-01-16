import copy
import main

def create_rows(board, horizontal_brick, vertical_brick, floor_char):
    '''
    Creates default rows for the board to build the board with.

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

def add_exits(board, board_list, exit_char):
    """
    Add exits signs to the board_list.

    Args:
    dictionary: The details of a board in a form of dictionary, with "exits" among them.
    list: The list of lists in which the characters will be changed
    string: The character which will be a symbol of exit

    Returns:
    list: Game board
    """

    # print(board["exits"])
    # print(board["exits"]["north"]["index_x"])
    
    for element in board["exits"]:
        x = board["exits"][element]["index_x"]
        y = board["exits"][element]["index_y"]
        board_list[y][x] = exit_char

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

    board_list = add_exits(board, board_list, exit_char)

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


# def is_exit(board, player):
#     if board[player["x"]][player["y"]] != "|" or board[player["x"]][player["y"]] != "-":
#         return True
#     return False


# def check_wall(player):
#     if player == 1:
#         return True
#     else:
#         return False


def remove_player_from_board(board, player):
    y = player["position_y"]-1
    x = player["position_x"]-1
    board[y][x] = " "


# def check_next_object(player, board):
#     if board[player["position_y"]][player["position_x"]] != " ":
#         return board[player["position_y"]][player["position_x"]]


# def change_board(board, player):
#     print(boards)

def move_player(board, player, key):
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

    if key in ["a", "A"]: 
        if index_x > 1: # dzięki index_x > 1 nie musimy już sprawdzać czy next object == "|"
            player["position_x"] -= 1
        elif board[index_y][index_x - 1] == "x":
            print("exit") #jeszcze nie wiem co z tym zrobić ale wymyślimy
        
    elif key in ["d", "D"]:
        if index_x < (width - 1):
            player["position_x"] += 1
        elif board[index_y][index_x + 1] == "x":
            print("exit")  #jeszcze nie wiem co z tym zrobić ale wymyślimy
            next_board = main.boards[player["current_board"]]["exits"]["east"]["leads_to"]
            player["current_board"] = next_board
            player["position_x"] = main.boards[next_board]["exits"]["west"]["index_x"]+1
            player["position_y"] = main.boards[next_board]["exits"]["west"]["index_y"]+1
            print(player["position_x"], player["position_y"])
            print("ok")
            
    
    elif key in ["s", "S"]:
        if index_y < (height - 1):
            player["position_y"] += 1
        elif board[index_y + 1][index_x] == "x":
            print("exit") #jeszcze nie wiem co z tym zrobić ale wymyślimy

    elif key in ["w", "W"]:
        if index_y > 1:
            player["position_y"] -= 1
        elif board[index_y - 1][index_x] == "x":
            print("exit") #jeszcze nie wiem co z tym zrobić ale wymyślimy
         
  