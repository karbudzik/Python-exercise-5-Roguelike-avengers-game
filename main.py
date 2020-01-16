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
player= {
    "position": {
        "x": 5,
        "y": 5,
    },
    "icon": "@"
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
    # nie wiem czy dobrze zrobiłem ale chwilowo zakomentowałem, bo poki co funckja nie tworzy jeszcze gracza a pewnie bedzie, ja na potrzeby mojej funkcji musiałem stworzyć obiekt player, zeby zmieniac mu korydnanty, może mam to zrobić innaczej dajcie znać to lekko zmienie dane w mojej funkcji move_player()
    # player = create_player()
    board = engine.create_board(INITIAL_BOARD)
    # tu jakiś dialog początkowy z userem?
    util.clear_screen()
    is_running = True
    while is_running:
        engine.put_player_on_board(board, player)
        ui.display_board(board)
    
        key = util.key_pressed()
        engine.put_player_on_board(board, player, action="remove")
        engine.move_player(board, player["position"], key)
        if key == 'q':
            is_running = False
        else:
            pass
        #wylaczylem na chwile zeby nie znikaly printy
        # util.clear_screen()


if __name__ == '__main__':
    main()
