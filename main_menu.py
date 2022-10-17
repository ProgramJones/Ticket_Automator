import os
import ticket


def print_main_menu_information():
    """
    Name: 
    print_main_menu

    Parameters:
    None

    When code is run: 
    At start of application.

    Purpose: 
    Prints the main menu for the application. 

    Offers options to: 
    Create a ticket.
    End the program.
    """

    print("\nTicket Automator\n\n")

    print("Options:")
    print("Create - Create a new ticket")
    print("End - End the program")


def choose_menu_command():
    menu_commands = ["end", "create"]

    menu_choice = input(
        "\n\nEnter an option from the above list: "
    ).lower()

    while menu_choice not in menu_commands:
        print("Please enter a valid option.\n")

        menu_choice = input(
            "\nEnter an option from the above list: "
        ).lower()

    return menu_choice


def execute_menu_command(menu_choice):
    if menu_choice == "create":

        newTicket = ticket.Ticket()
        newTicket.create_ticket()

    elif menu_choice == "end":
        os.sys.exit(0)


def open_main_menu():

    print_main_menu_information()

    execute_menu_command(choose_menu_command())
