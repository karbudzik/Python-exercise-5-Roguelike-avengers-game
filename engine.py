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
    
    horizontal_wall = [horizontal_brick for i in range(board["width"])]
    middle_row = [vertical_brick]
    middle_row.extend([floor_char for i in range(board["width"]-2)])
    middle_row.extend([vertical_brick])

    board_list = []
    board_list.append(horizontal_wall)
    for row in range(board["height"]-2):
       board_list.append(middle_row)
    board_list.append(horizontal_wall)

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
    pass

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
    print(board, player, key)
    # for i in range(len(board)):
    #     for j in range(len(board[i])):
    if player["player_position_x"] < len(board) and player["player_position_x"] > 0:
        
        if key == "a":
            player["player_position_x"] -= 1
        elif key == "d":
            player["player_position_x"] += 1

    return player               
  