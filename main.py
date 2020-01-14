import util
import engine
import ui

boards = {
    "board_1": {
        "width": 15,
        "height": 7,
        "exits": {
            "north": {
                "index_x": 5,
                "index_y": 0,
                "leads_to": "board_2"
            },
            "east": {
                "index_x": 14,
                "index_y": 4,
                "leads_to": "board_3"
            }
        }
    },
    "board_2": {
        "width": 20,
        "height": 30,
        "exits": {
            "south": {
                "index_x": 15,
                "index_y": 29,
                "leads_to": "board_1"
            }
        }
    },
    "board_3": {
        "width": 10,
        "height": 30,
        "exits": {
            "west": {
                "index_x": 0,
                "index_y": 20,
                "leads_to": "board_1"
            }
        }
    }
}
player_info = {
    "player_information": {
        "player_position_x": 5,
        "player_position_y": 5,
        "player_icon": "$"
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
        engine.put_player_on_board(board, player)
        ui.display_board(board)

        key = util.key_pressed()
        player_positions = engine.move_player(board, player_info["player_information"], key)
        
        print(player_positions)
        if key == 'q':
            is_running = False
        else:
            pass
        util.clear_screen()


if __name__ == '__main__':
    main()
