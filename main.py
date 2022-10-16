# Copyright (c) <2022>, <Tai Jones>
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

import os
import ticket


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

    print("Ticket Automator\n")
    print("\nEnter \"Create\" to create a new ticket")
    print("Enter \"End\" at any time to end the program")
    print("")


print_main_menu()

flag = input().lower()

while flag != "end" and flag != "create":
    print("Please enter a valid option.\n")

    print("\nEnter \"Create\" to create a new ticket")
    print("Enter \"End\" at any time to end the program\n")

    flag = input().lower()

if flag == "create":
    newTicket = ticket.Ticket()

    newTicket.setup_ticket()

    print("\n")

    newTicket.generate_ticket_automator()

elif flag == "end":
    os.sys.exit(0)
