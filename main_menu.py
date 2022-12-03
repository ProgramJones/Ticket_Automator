# Copyright (c) <2022>, <Tai Jones>
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.


import os
import system
import ticket


def print_main_menu_information():
    """
    Name: 
    print_main_menu

    Parameters:
    None

    When code is run: 
    When open_main_menu is called.

    Purpose: 
    Prints the main menu for the application, which includes the title and available commands.

    Offers options to: 
    Create a ticket.
    End the program.
    """

    print("\nTicket Automator\n\n")

    print("Options:")
    print("Create - Create a new ticket")
    print("End - End the program")


def choose_menu_command():
    """
    Name: 
    choose_menu_command

    Parameters:
    None

    When code is run: 
    When called by execute_menu_command.

    Purpose: 
    Prompt for a command. Return prompted command.
    """

    menu_commands = ["end", "create"]

    # prompt user for a command.
    # save prompted command in menu_choice variable.
    menu_choice = input(
        "\n\nEnter an option from the above list: "
    ).lower().strip()

    # while prompted command is not in menu_commands list, prompt user for a command.
    while menu_choice not in menu_commands:
        print("Please enter a valid option.\n")

        menu_choice = input(
            "\nEnter an option from the above list: "
        ).lower().strip()

    return menu_choice


def execute_menu_command(menu_choice):
    """
    Name: 
    execute_menu_command

    Parameters:
    menu_choice

    When code is run: 
    When open_main_menu is called.

    Purpose: 
    Execute certain steps that depend on which command user chose.
    """

    # if user enters 'create', create an instance of the Ticket class and create a ticket from that instance.
    if menu_choice == "create":

        newTicket = ticket.Ticket()

        newTicket.create_ticket()

    # if user enters 'end', end the program.
    elif menu_choice == "end":
        system.clear_prompt_or_terminal()
        os.sys.exit(0)


def open_main_menu():
    """
    Name: 
    open_main_menu

    Parameters:
    None

    When code is run: 
    At the start of main.py. / When the program starts.

    Purpose: 
    Print the menu for the program and provide user options for how to interact with the program.
    """

    print_main_menu_information()

    execute_menu_command(choose_menu_command())
