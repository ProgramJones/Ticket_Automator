# Copyright (c) <2022>, <Tai Jones>
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

import os
import ticket
import platform


if (platform.system() == "Windows"):
    # If operating system is Windows, clear command prompt with 'clr'
    os.system("clr")
else:
    # If operating system is Unix, clear terminal with 'clear'
    os.system("clear")


def print_main_menu():
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
    # print("----- *  -----")
    # print("|   |  |")
    # print("|   |  -----")

    print("\nTicket Automator\n\n")

    print("Options:")
    print("Create - Create a new ticket")
    print("End - End the program")


print_main_menu()

flag = input(
    "\n\nEnter an option from the above list: "
).lower()

while flag != "end" and flag != "create":
    print("Please enter a valid option.\n")

    flag = input(
        "\nEnter an option from the above list: "
    ).lower()

if flag == "create":

    newTicket = ticket.Ticket()

    newTicket.setup_ticket()
    newTicket.print_ticket_steps_questions_and_options()

elif flag == "end":
    os.sys.exit(0)
