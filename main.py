import util
import engine
import ui
import random
import sys

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
# player= {
#     "position": {
#         "x": 5,
#         "y": 5,
#     },

#     "icon": "@"
# }

def create_player():
    '''
    Creates a 'player' dictionary for storing all player related informations - i.e. player icon, player position.
    Fell free to extend this dictionary!
    
    Returns:
    dictionary
    '''

    user_name, user_icon = ask_for_details()
    player = {
        "name": user_name,
        "position_x": 3,
        "position_y": 3,
        "current_board": "board_1",
        "player_icon": user_icon
    }
    print(player)
    return player

def ask_for_details():
    """
    Asks player for name and icon.
    
    Returns:
    User's details
    """
    possible_names = ["Captain America", "Iron Man", "Hulk", "Thor", "Black Widow", "War Machine", "Captain Marvel", "Spider-Man", "Black Panther", "Star Lord"]
    user_name = input("Choose your name or press 'r' if you want to randomly pick a name from the Avengers team. > ")
    if user_name in ["r", "R"] or len(user_name) < 1:
        user_name = random.choice(possible_names)
    
    possible_icons = ["@", "&", "#", "%"]
    user_icon = input("Choose the icon you want to be your character. You can choose between '@', '&', '#' and '%' or press 'r' if you want to pick randomly. > ")
    if user_icon in ["r", "R"] or len(user_icon) < 1:
        user_icon = random.choice(possible_icons)
    while user_icon not in possible_icons:
        user_icon = input("You can't pick this character. You can choose between '@', '&', '#' and '%' or press 'r' to pick randomly. > ")

    return user_name, user_icon

def main():
    # nie wiem czy dobrze zrobiłem ale chwilowo zakomentowałem, bo poki co funckja nie tworzy jeszcze gracza a pewnie bedzie, 
    # ja na potrzeby mojej funkcji musiałem stworzyć obiekt player, zeby zmieniac mu korydnanty, 
    # może mam to zrobić innaczej dajcie znać to lekko zmienie dane w mojej funkcji move_player()
    player = create_player()
    board = engine.create_board(boards[player["current_board"]])
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
        util.clear_screen()


if __name__ == '__main__':
    main()
