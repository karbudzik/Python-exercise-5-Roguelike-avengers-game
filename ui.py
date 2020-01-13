def display_board(board_list):
    '''
    Displays complete game board on the screen

    Returns:
    Nothing
    '''
    for row in board_list:
        row = "".join(row)
        print(row)