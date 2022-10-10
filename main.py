# Copyright (c) <2022>, <Tai Jones>
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

import os
import Ticket


def print_main_menu():
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
    newTicketValues = Ticket.setup_ticket()

    newTicket = Ticket.Ticket(newTicketValues[0], newTicketValues[1],
                              newTicketValues[2], newTicketValues[3],
                              newTicketValues[4], newTicketValues[5],
                              newTicketValues[6])

    print("\n")
    newTicket.is_online_or_not()
    newTicket.generate_ticket_automator()
elif flag == "end":
    os.sys.exit(0)
