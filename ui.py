import os

def display_board(board_list, board_name):
    '''
    Displays complete game board on the screen

    Returns:
    Nothing
    '''
    console_width = os.get_terminal_size().columns
    
    display_title(board_list, board_name)

    for row in board_list:
        row = "".join(row)
        print(row.center(console_width))

def display_title(board_list, board_name):
    '''
    Displays board's name over the printed board.

    Returns:
    Nothing
    '''
    caption = "*** " + board_name + " ***"
    console_width = os.get_terminal_size().columns

    print("")
    print(caption.center(console_width))
    print("")
