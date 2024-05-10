from os import system
from platform import system as platform
from time import sleep


def integer_validation(user_input):
    if not user_input.isdigit():
        return False
    return True


def yes_or_no_validation(user_input):
    valid_options = ["y", "n"]
    try:
        converted = user_input.strip().lower()[0]
    except IndexError:
        return "Invalid"
    if converted not in valid_options:
        return "Invalid"
    if converted == "n":
        return False
    return True


def clear_screen() -> None:
    """clears terminal screen regardless of platform"""
    plat = platform()
    match plat:
        case "Linux" | "Darwin":
            system("clear")
        case "Windows":
            system("cls")


def load_list(list_file):
    with open(list_file, "r") as fh:
        new_list = [line.rstrip().split("|") for line in fh]
    return new_list


def update_list_file(grocery_list, list_file):
    with open(list_file) as fh:
        for item in grocery_list:
            name, quantity = item
            fh.write(f"{name}|{quantity}")


def menu(start_with_clear=True, **options):
    if start_with_clear:
        clear_screen()
    valid_choices = list(options.values())
    while True:
        print("Choose an option:")
        for action, key in options.items():
            print(f"[{key}] to {action}")
        choice = input()
        try:
            choice = choice.strip().lower()[0]
        except IndexError:
            print("Invalid input")
            sleep(1)
            continue
        if choice not in valid_choices:
            print("Invalid input")
            sleep(1)
            continue
        break
    return choice


def view(grocery_list):
    clear_screen()
    print("================")
    sleep(.1)
    for index, item in enumerate(grocery_list):
        item_number = index + 1
        item_name = item[0].title()
        quantity = item[1]
        print(f"{item_number}: {quantity} {item_name}")
        sleep(.1)
    print("================")


def edit_menu(grocery_list, list_file):
    """adds user-inputted items to the grocery list
       (both run-time list and list file)"""
    menu_options = {"add new item to list": "a",
                    "update existing item": "u",
                    "go back to menu": "b"}
    while True:
        view(grocery_list)
        choice = menu(False, **menu_options)
        match choice:
            case "a":
                new_item(grocery_list)
            case "u":
                update_item(grocery_list)
            case "b":
                with open(list_file, "w") as fh:
                    for item in grocery_list:
                        name = item[0]
                        quantity = item[1]
                        fh.write(f"{name}|{quantity}\n")
                break






def new_item(grocery_list):
    while True:
        clear_screen()
        restart = False
        print("What would you like to add?")
        new = input()
        for item in grocery_list:
            name = item[0]
            if name == new:
                restart = True
                print(f"{new} is already on the list")
                print(f"You can update {new} from the previous menu")
                break
        if restart:
            continue
        while True:
            print("How much to add?")
            quantity = input()
            if not integer_validation(quantity):
                print("Invalid input")
                continue
            quantity = int(quantity)
            break
        item_info = [new, quantity]
        grocery_list.append(item_info)
        while True:
            print("Would you like to add another item? [y/n]")
            user_input = input()
            choice = yes_or_no_validation(user_input)
            if choice == "Invalid":
                print("Invalid input")
                continue
            break
        if not choice:
            break


def update_item(grocery_list):
    menu_options = {"remove item": "r",
                    "edit quantity": "q",
                    "go back to previous menu": "b"}
    while True:
        clear_screen()
        view(grocery_list)
        print("Enter the number of the item would you like to edit")
        print("Or enter 'b' to go back")
        user_input = input()
        if user_input.strip().lower()[0] == 'b':
            break
        if not integer_validation(user_input):
            print("Invalid input")
            sleep(1)
            continue
        index = int(user_input) - 1
        if index < 0 or index > len(grocery_list) - 1:
            print("Invalid input")
            sleep(1)
            continue
        item = grocery_list[index]
        name = item[0].title()
        quantity = item[1]
        print(f"You currently have {quantity} {name} on your list")
        choice = menu(False, **menu_options)
        match choice:
            case "r":
                grocery_list.remove(item)
                print("Item Removed!")
            case "q":
                while True:
                    print("Type a number to add to quantity")
                    print("Or type a negative number (using '-') to subtract")
                    user_input = input()
                    choice = user_input.strip()
                    if choice.startswith("-"):
                        number = user_input.strip("-")
                        if not integer_validation(number):
                            print("Invalid input")
                            continue
                        quantity -= int(number)
                        item[1] = quantity
                        break
                    number = user_input
                    if not integer_validation(number):
                        print("Invalid input")
                        continue
                    quantity += int(number)
                    item[1] = quantity
                    break
            case "b":
                print("Returning...")
                sleep(1)
                break


def clear(grocery_list, list_file):
    print("Type 'CLEAR' to confirm")
    confirmation = input()
    if confirmation == "CLEAR":
        print("Clearing...")
        sleep(1)
        grocery_list.clear()
        with open(list_file, "w"):
            ...
