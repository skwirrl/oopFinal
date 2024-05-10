from groceryListResources import *
from sys import exit

list_file = "grocery_list.txt"

groceries = load_list(list_file)

menu_options = {"edit list": "e",
                "view list": "v",
                "clear list": "c",
                "quit": "q"}

while True:
    choice = menu(**menu_options)

    match choice:
        case "e":
            edit_menu(groceries, list_file)
        case "v":
            view(groceries)
            input("[Enter to Continue]")
        case "c":
            clear(groceries, list_file)
        case "q":
            print("See you next time!")
            exit()