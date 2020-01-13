import util
import engine
import ui

boards = {
    "board_1": {
        "width": 15,
        "height": 7
    },
    "board_2": {
        "width": 30,
        "height": 40
    },
    "board_3": {
        "width": 10,
        "height": 30
    }
}

PLAYER_ICON = '@'
PLAYER_START_X = 3
PLAYER_START_Y = 3

INITIAL_BOARD = boards["board_1"]


def create_player():
    '''
    Creates a 'player' dictionary for storing all player related informations - i.e. player icon, player position.
    Fell free to extend this dictionary!

    Returns:
    dictionary
    '''
    pass


def main():
    player = create_player()
    board = engine.create_board(INITIAL_BOARD)
    # tu jakiś dialog początkowy z userem?
    util.clear_screen()
    is_running = True
    while is_running:
        # engine.put_player_on_board(board, player)
        ui.display_board(board)

        key = util.key_pressed()
        if key == 'q':
            is_running = False
        else:
            pass
        util.clear_screen()


if __name__ == '__main__':
    main()
