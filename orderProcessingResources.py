from datetime import datetime, timedelta
from os import system
from platform import system as platform
from time import sleep

welcome = """
|==============================|
|Welcome to Wilmort's Groceries|
|==============================|
"""

menu_options = """Choose an option:
[s] to shop
[c] to checkout
"""


class Item:
    """class for items in inventory & cart"""
    def __init__(self, name, value, in_stock):
        self.__name = name
        self.__value = float(value)
        self.__in_stock = int(in_stock)

    def __str__(self) -> str:
        return self.__name.title()

    def __repr__(self) -> str:
        return self.__name.title()

    def get_name(self) -> str:
        """returns capitalized name"""
        return self.__name.title()

    def get_info(self) -> list[str]:
        """returns all item properties in a list"""
        return [self.__name, self.__value, self.__in_stock]

    def add_stock(self, quantity) -> None:
        """adds to item stock"""
        self.__in_stock += quantity

    def remove_stock(self, quantity) -> None:
        """removes from item stock"""
        self.__in_stock -= quantity

    def add_to_cart(self, cart) -> None:
        """allows user to add user-defined quantity of item
           to cart, DOES NOT remove from inventory stock"""
        name, value, in_stock = self.get_info()
        print("================")
        print(f"{name.title()}\nPrice: ${value}\nLeft in Stock:"
              f"{in_stock}")
        print("================\n")
        while True:
            print(f"Please enter the number you'd like to purchase!")
            number = input()
            if not number.isdigit():
                print("Please enter a number!")
                continue
            number = int(number)
            if number > in_stock:
                print(f"We only have {in_stock} available!")
                continue
            break
        cart.append([self, number])
        self.remove_stock(number)



def clear_screen():
    """clears terminal, regardless of platform"""
    plat = platform()
    match plat:
        case "Linux" | "Darwin":
            system("clear")
        case "Windows":
            system("cls")


def inventory_display(inventory):
    """displays items and their info from inventory"""
    for index, item in enumerate(inventory):
        name, value, in_stock = item.get_info()
        print(f"Item #{index + 1}:")
        print("================")
        print(f"{name.title()}\nPrice: ${value}\nLeft in Stock:"
              f"{in_stock}")
        print("================\n")
        sleep(.5)


def cart_display(cart) -> float:
    """displays items in cart, calculates and returns total price"""
    total = 0
    print("=================")
    for i in cart:
        item, number = i
        name, value, in_stock = item.get_info()
        item_total = number * value
        total += item_total
        print(f"{number} {name}")
    print("=================")
    print(f"Cart Total: ${round(total, 2)}")
    return total


def menu() -> str:
    """defines and presents valid choices, error-handles user input
    and returns user choice"""
    valid_options = ["s", "c"]
    while True:
        clear_screen()
        print(welcome)
        print(menu_options)
        choice = input()
        try:
            choice = choice.strip().lower()[0]
        except IndexError:
            print("Please choose either 's' or 'c'")
            continue
        if choice not in valid_options:
            print("Please choose either 's' or 'c'")
            continue
        break
    return choice


def shop(cart, inventory) -> None:
    """a loop allowing users to select an item and add
    it to their cart using the add_to_cart method for
    that item"""
    valid_options = ["y", "n"]
    while True:
        clear_screen()
        inventory_display(inventory)
        print("Please enter the item # for the item you'd like to purchase")
        choice = input()
        if not choice.isdigit():
            print("Please enter the corresponding item #")
            continue
        choice = int(choice)
        try:
            choice = inventory[choice - 1]
        except IndexError:
            print("Please enter the corresponding item #")
            continue
        choice.add_to_cart(cart)
        cart_display(cart)
        while True:
            clear_screen()
            print("Would you like to continue shopping? [y/n]")
            restart = input()
            try:
                restart = restart.strip().lower()[0]
            except IndexError:
                print("Please enter either 'y' or 'n'")
                continue
            if restart not in valid_options:
                print("Please enter either 'y' or 'n'")
                continue
            break
        if restart == "n":
            break





def get_order_details(cart, total) -> list:
    """takes user info and organizes cart info"""
    items_dict = {}
    print("Please enter your first and last name:")
    customer_name = input()
    print("Please enter your shipping address:")
    shipping_address = input()
    for item in cart:
        items_dict[item[0]] = item[1]
    print(items_dict)
    order_total = total
    order_details = [customer_name, shipping_address, items_dict, order_total]
    return order_details


def finalize_order(cart, inventory) -> list:
    """confirms checkout, calls get_order_details for details list,
    and updates inventory file, returns order_details list"""
    valid_options = ["y", "n"]
    while True:
        total = cart_display(cart)
        while True:
            print("Continue Checkout? [y/n]")
            finalize = input()
            try:
                finalize = finalize.strip().lower()[0]
            except IndexError:
                print("Please enter either 'y' or 'n'")
                continue
            if finalize not in valid_options:
                print("Please enter either 'y' or 'n'")
                continue
            break
        with open("inventory", "w") as file:
            for item in inventory:
                line = item.get_info()
                new_line = [str(i) for i in line]
                new_line = "|".join(new_line)
                file.write(f"{new_line}\n")
        order_details = get_order_details(cart, total)
        return order_details


def order_processing(order_details) -> dict:
    """processes order_details list and current date, prints and returns
    a dictionary of the details"""
    customer_name, shipping_address, items_dict, order_total = order_details
    current_date = datetime.now()
    deliver_date = current_date + timedelta(days=3)
    order_dict = {"Order Date": current_date.date(),
                  "Customer Name": customer_name,
                  "Shipping Address": shipping_address,
                  "Items Purchased": items_dict,
                  "Order Total": order_total,
                  "Estimated Delivery": deliver_date.date()
                  }
    print("Thank you for your purchase!")
    for detail, value in order_dict.items():
        if detail == "Items Purchased":
            print("Items Purchased")
            print("===============")
            for k, v, in value.items():
                name = k.get_name()
                print(f"{name}: {v}")
            print("===============")
        elif detail == "Order Total":
            print(f"{detail}: ${value}")
        else:
            print(f"{detail}: {value}")
    return order_dict