from orderProcessingResources import *


def main():
    with open("inventory.txt") as file:
        inventory_list = [Item(*(line.rstrip().split("|"))) for line in file]

    cart = []
    while True:
        choice = menu()
        match choice:
            case "s":
                shop(cart, inventory_list)
            case "c":
                order_details = finalize_order(cart, inventory_list)
                order_processing(order_details)
                break
    print("Thanks for shopping at Wilmort's!")



if __name__ == "__main__":
    main()









