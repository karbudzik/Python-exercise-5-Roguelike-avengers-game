import os

def display_board(board_list, board_name, player):
    '''
    Displays complete game board on the screen

    Returns:
    Nothing
    '''
    console_width = os.get_terminal_size().columns
    
    display_title(board_list, board_name, console_width)

    for row in board_list:
        row = "".join(row)
        print(row.center(console_width))

    display_stats(player, console_width)


def display_title(board_list, board_name, console_width):
    '''
    Displays board's name over the printed board.

    Returns:
    Nothing
    '''
    caption = "*** " + board_name + " ***"

    print("")
    print(caption.center(console_width))
    print("")


def display_stats(player, console_width):
    '''
    Displays player's statistics under the printed board.

    Returns:
    Nothing
    '''
    #dodać liczenie infinity stones
    keys_to_display = ["name", "quest", "infinity_stones", "health"]
    stats_to_display = []
    for key in keys_to_display:
        if key in player:
            pair_of_stats = [key, player[key]]
            stats_to_display.append(pair_of_stats)

    if "inventory" in player.keys():
        number_of_items = 0
        for key in player["inventory"]:
            number_of_items += player["inventory"][key]
        pair_of_stats = ["inventory items (press 'i' for more)", number_of_items]
        stats_to_display.append(pair_of_stats)

    for pair in stats_to_display:
        stats_to_display[stats_to_display.index(pair)] = str(pair[0]).upper() + ": " + str(pair[1])
        
    string_to_display = (" | ").join(stats_to_display)

    print("")
    print(string_to_display.center(console_width))