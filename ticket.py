# Copyright (c) <2022>, <Tai Jones>
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

# TASKS

# For add question, add step, add line: Figure out how to add keys and values before or after existing keys and values in ticket_content

# Just remove certain keys values in ticket_content when remove question, remove step, and remove line commands are run
# What about just having one remove command that can remove question, line, and step?

# Add troubleshooting steps for:
# Email - Setup
# Email - Configuration

# Add code for all commands

# Edit README.md


# ** Add below with user auth enabled:

# Add user auth with flask so different users can have different options when creating a ticket
# options: login, logout | if logged out, create from general ticket
# options: filtering information based on ISP, saving tickets, opening tickets

# if login is chosen, admin_ticket and isp_ticket are possible subclasses depending on credentials
# ticket, admin_ticket, isp_ticket

# main_menu.py: Add 'Open' comand - Open an existing ticket. (For superusers)
# ticket.py: Add 'Save' command - Save ticket as a .txt file. (For superusers)

# Ask user if service was provided by an ISP
# option to print ISPs, in case user isn't sure what ISPs are available
# When user enters ISP name, troubleshooting steps and diagnostic questions are filtered


import os
import re
import time
import pyperclip
import system
import main_menu


class Ticket():

    def __init__(self):
        self.user = None
        self.name = None
        self.number = None
        self.address = None
        self.custom_issue = None
        self.service = None
        self.category = None
        self.isOnline = None
        self.ticket_content = {}

        self.internet_services = ["Fiber", "DSL", "Cable", "Fixed Wireless"]
        self.services = [self.internet_services, ["Email"], ["TV"], ["N/A"]]

        self.internet_categories = [
            "General", "Connectivity", "Speed", "Intermittent Connectivity/Speed"]
        self.email_categories = ["General", "Setup", "Configuration"]
        self.tv_categories = ["General"]

        self.fiber_connectivity_steps = [
            "Check each network device’s name, model, and lights.",
            "Check a router for Wi-Fi.", "Check cabling.",
            "Check if cables are in the correct ports.",
            "Check cable conditions.", "Power cycle all network devices.",
            "Check each network device’s name, model, and lights.",
            "Check a device for internet.", "Check ONT",
            "Check ONT's battery backup", "Run ping tests on a computer."
        ]
        self.dsl_connectivity_steps = [
            "Check if there’s a landline phone with dial tone.",
            "Check each network device’s name, model, and lights.",
            "Check a router for Wi-Fi.", "Check cabling.",
            "Check if cables are in the correct ports.",
            "Check cable conditions.", "Power cycle all network devices.",
            "Check each network device’s name, model, and lights.",
            "Check a device for internet.", "Run ping tests on a computer."
        ]
        self.cable_connectivity_steps = [
            "Check each network device’s name, model, and lights.",
            "Check a router for Wi-Fi.", "Check cabling.",
            "Check if cables are in the correct ports.",
            "Check cable conditions.", "Power cycle all network devices.",
            "Check each network device’s name, model, and lights.",
            "Check a device for internet.", "Run ping tests on a computer."
        ]
        self.fixed_wireless_connectivity_steps = [
            "Check each network device’s name, model, and lights.",
            "Check a router for Wi-Fi.", "Check cabling.",
            "Check if cables are in the correct ports.",
            "Check cable conditions.", "Power cycle all network devices.",
            "Check each network device’s name, model, and lights.",
            "Check a device for internet.", "Run ping tests on a computer."
        ]
        self.general_connectivity_steps = [
            "Check each network device’s name, model, and lights.",
            "Check a router for Wi-Fi.", "Check cabling.",
            "Check if cables are in the correct ports.",
            "Check cable conditions.", "Power cycle all network devices.",
            "Check each network device’s name, model, and lights.",
            "Check a device for internet.", "Run ping tests on a computer."
        ]
        self.speed_steps = [
            "Run speed tests on a device.",
            "Check each network device’s name, model, and lights.",
            "Check cabling.", "Check cable conditions.",
            "Power cycle all network devices.",
            "Check each network device’s name, model, and lights.",
            "Run speed tests on a device.", "Run ping tests on a computer."
        ]
        self.intermittent_connectivity_and_speed_steps = [
            "Run speed tests on a device.", "Run ping tests on a computer.",
            "Check each network device’s name, model, and lights.",
            "Check cabling.", "Check cable conditions.",
            "Power cycle all network devices.",
            "Check each network device’s name, model, and lights.",
            "Run speed tests on a device.", "Run ping tests on a computer."
        ]

        self.internet_general_questions = [
            "Are any services still working? ",
            "Are all devices effected? If not, what is affected? ",
            "How long has this issue been happening for? ",
            "Where there any equipment changes or outside disturbances like weather or maintenance when issue first started happening? "
        ]
        self.intermittent_questions = [
            "Is issue only happening during a certain time frame? If so, during what time(s)? ",
            "Is issue only happening when a certain device is online? If so, which device? ",
            "Is issue only happening when a lot of devices are online? ",
            "How long is internet affected for? ",
            "Does the equipment typically have to be powercycled to temporarily resolve the issue? ",
            "Do lights on the router look the same when internet disconnects? "
        ]
        self.dsl_questions = [
            "Does the landline phone have dial tone? ",
            "Are there any splitters on the wall jack? "
        ]
        self.wifi_questions = [
            "Is the router in a closed space like a closet, cabinet, entertainment center, kitchen/laundry room, or besides a phone’s base? ",
            "Are there sources of interference like radios, extenders, metal doors, or metal ceilings? "
        ]

        self.email_general_questions = [
            "How long has this issue been happening for? "]
        self.email_setup_questions = []
        self.email_configuration_questions = []

        self.tv_general_questions = [
            "How long has this issue been happening for? "]

    def setup_ticket(self):
        """
        Name:
        setup_ticket

        Parameters:
        None

        When code is run:
        When create_ticket is called.

        Purpose:
        Prompt for number, name, address, custom_issue, service, and category and assign inputted information to relevant attributes.
        Append number, name, address, custom_issue, service, and category attributes to ticket_content dictionary.
        """

        print("\n\n-------------------------------------------\n\n")
        print("More information needed to create the ticket.\nPlease answer the following questions:")

        print("\n\n")

        # Prompt the user for their name - Assign user's name to class instance's attributes.
        self.user = self.set_user()

        print("\n\n")

        # Prompt the user for contact information - Assign contact information to class instance's attributes.
        print("Contact Information:")
        self.number = input("What's the best callback number? ").strip()
        self.name = input("Who is being helped? ").strip()
        self.address = input("What's their address? ").strip()

        # Append number, name, and address key and values to ticket_content
        self.ticket_content.update({"number": "cb: " + self.number})
        self.ticket_content.update({"name": "s/w: " + self.name})
        self.ticket_content.update({"address": "address: " + self.address})

        print("\n\n")

        # Prompt user for issue information - Assign issue information to class instance's attributes.
        print("Issue:")
        self.custom_issue = input("What's the Issue? ").strip()

        # Append custom issue key and value to ticket_content
        self.ticket_content.update({"custom_issue": self.custom_issue})

        print("\n\n")

        self.service = self.set_service()

        print("\n\n")

        self.category = self.set_category()

        # Append user key and value to end of ticket_content
        self.ticket_content.update({"user": self.user})

        print("\n\n")

        self.is_online_or_not()

        print("All questions answered!\n")

        print("Service: " + self.service + " | Category: " + self.category)
        print("Outputting ticket, troubleshooting steps, and diagnostic questions.",
              end="", flush=True)

        time.sleep(.75)
        print(".", end="", flush=True)

        time.sleep(.75)
        print(".", end="", flush=True)

        time.sleep(.75)

    def set_user(self):
        """
        Name:
        set_user

        Parameters:
        None

        When code is run:
        When setup_ticket function is called.

        Purpose:
        Prompt the user for their first and last name.
        Return a formatted version of user's first and last name. ( Format is first_name_initial + last_name(s) ) 
        """

        user = input(
            "Who's creating this ticket? Enter first and last name. ").strip()

        # Find out if user entered at least two words.
        two_words = re.search(" {1}.+", user)

        # While user has not entered at least two words, prompt user to enter at least two words.
        while two_words == None:
            print("Enter a first and last name.\n")

            user = input(
                "Who's creating this ticket? Enter first and last name. ").strip()
            two_words = re.search(" {1}.+", user)

        # Sepearte words entered by user, and assign them as names in an array called 'all_names'.
        all_names = re.split("\s", user)

        # Format names from all_names in format of first_name_initial + last_name + any_other_last_names
        signature = ""

        for index, name in enumerate(all_names):
            if index == 0:
                signature += name[0].lower()
            else:
                signature += name.lower()

        return signature

    def set_service(self):
        """
        Name:
        set_service

        Parameters:
        None

        When code is run:
        When setup_ticket function is called.

        Purpose:
        Prompt the user for what service they're having issues with.
        Return service entered by user.    
        """

        print("Service:")
        print("Which of the following services is being worked on? \n")

        # Make a temporarily list that's the lowercase version of self.services
        lowercase_services = [[service.lower() for service in list]
                              for list in self.services]

        # Print all services.
        for item in self.services:
            for innerValue in item:
                print(innerValue)

        # Prompts the user for what service they're having issues with.
        service = input(
            "\nEnter a service from the above list: "
        ).strip()

        # While entered service is not in the lowercase_services list, prompt user for service.
        while (not any(service.lower() in x for x in lowercase_services)):
            print("Please enter a valid service\n")
            service = input(
                "\nEnter a service from the above list: "
            ).strip()

        # Reassign and return service enetered by user.
        # if service is DSL or TV, catapitalize all letters of service
        if (service.lower() == "dsl" or service.lower() == "tv"):
            service = service.upper()
            return service
        else:
            # if service is anything besides DSL or TV, uppercase the first letter of each word in service variable
            service = service.title()
            return service

    def set_category(self):
        """
        Name:
        set_category

        Parameters:
        None

        When code is run:
        When setup_ticket function is called.

        Purpose:
        Prompt the user for what category they're having issues with.
        Return category entered by user.
        """

        print("Category:")
        print("Which of the following categories is being worked on? \n")

        # Current categories is an array that will contain categories relevent to the selected service
        current_categories = []

        # if service is also in internet_services list, assign current_categories to the value of internet_categories
        if (self.service in self.internet_services):
            current_categories = self.internet_categories

        # if service is 'Email', assign current_categories to the value of email_categories
        elif (self.service == "Email"):
            current_categories = self.email_categories

        # if service is 'TV', assign current_categories to the value of tv_categories
        elif (self.service == "TV"):
            current_categories = self.tv_categories

        # if service is 'N/A', just append "general" to current_categories
        elif (self.service == 'N/A'):
            current_categories.append("General")

        # Print the categories to choose from
        for item in current_categories:
            print(item)

        # Prompts the user for what service category they're having issues with.
        category = input(
            "\nEnter a category from the above list: "
        ).strip()

        # Make a temporarily list that's the lowercase version of current_categories
        lowercase_categories = [category.lower()
                                for category in current_categories]

        # While entered category is not in lowercase_categories list, prompt user for category.
        while (category.lower() not in lowercase_categories):
            print("Please enter a valid category\n")
            category = input(
                "\nEnter a category from the above list: "
            ).strip()

        category = category.title()
        return category

    def is_online_or_not(self):
        """
        Name:
        is_online_or_not

        Parameters:
        None

        When code is run:
        When setup_ticket method is called.

        Purpose:
        Re-assign isOnline variable to 'yes' or 'no' when category is intermittent connectivity/speed.
        """

        # If category is intermittent connectivity/speed and if method hasn't been run before, run the following code...
        if (self.category == "Intermittent Connectivity/Speed") and (self.isOnline == None):

            # Prompt the user for network status.
            print("Is the internet online? \n")
            self.isOnline = input(
                "Enter yes or no to respond. ").lower().strip()

            # While response is not 'yes' or 'no', prompt user for network status.
            while (self.isOnline.lower() != "yes") and (self.isOnline.lower()
                                                        != "no"):
                print("Please enter a valid response.\n")
                self.isOnline = input(
                    "Enter yes or no to respond. ").lower().strip()

            print("\n\n")

    def print_ticket(self):
        """
        Name:
        print_ticket

        Parameters:
        None

        When code is run:
        When print_ticket_steps_and_questions method is called.
        In wait_for_command method, when 'copy' is enetered.

        Purpose:
        Assign all values from ticket_content to ticket_content_string.
        Return ticket_content_string.
        """

        ticket_content_string = ""

        # iterate through ticket_content dictionary
        for key, value in self.ticket_content.items():
            # if current key is custom_issue or user, print current value following two new lines.
            if (key == "custom_issue" or key == "user"):
                ticket_content_string += "\n\n" + value
            # if current key is number, print current value.
            elif (key == "number"):
                ticket_content_string += value
            # print current value following one new line.
            else:
                ticket_content_string += "\n" + value

        return ticket_content_string

    def print_troubleshooting_steps(self):
        """
        Name:
        print_troubleshooting_steps

        Parameters:
        None

        When code is run:
        When print_ticket_steps_and_questions method is called.

        Result:
        Print certain troubleshooting steps, depending on current service, category, and isOnline status.
        """

        print("Troubleshooting Steps:")

        # Connectivity Steps

        # If current service is DSL and category is Connectivity, print troubleshooting steps from dsl_connectivity_steps list
        # If category is Intermittent Connectivity/Speed and isOnline is no, print troubleshooting steps from dsl_connectivity_steps list
        if (self.service == "DSL" and self.category == "Connectivity") or (
                self.service == "DSL"
                and self.category == "Intermittent Connectivity/Speed"
                and self.isOnline == "no"):
            for index, item in enumerate(self.dsl_connectivity_steps):
                print(str(index + 1) + ". " + item)

        # If current service is Fiber and category is Connectivity, print troubleshooting steps from fiber_connectivity_steps list
        # If category is Intermittent Connectivity/Speed and isOnline is no, print troubleshooting steps from fiber_connectivity_steps list
        elif (self.service == "Fiber" and self.category == "Connectivity") or (
                self.service == "Fiber"
                and self.category == "Intermittent Connectivity/Speed"
                and self.isOnline == "no"):
            for index, item in enumerate(self.fiber_connectivity_steps):
                print(str(index + 1) + ". " + item)

        # If current service is Cable and category is Connectivity, print troubleshooting steps from cable_connectivity_steps list
        # If category is Intermittent Connectivity/Speed and isOnline is no, print troubleshooting steps from cable_connectivity_steps list
        elif (self.service == "Cable" and self.category == "Connectivity") or (
                self.service == "Cable"
                and self.category == "Intermittent Connectivity/Speed"
                and self.isOnline == "no"):
            for index, item in enumerate(self.cable_connectivity_steps):
                print(str(index + 1) + ". " + item)

        # If current service is Fixed Wireless and category is Connectivity, print troubleshooting steps from fixed_wireless_connectivity_steps list
        # If category is Intermittent Connectivity/Speed and isOnline is no, print troubleshooting steps from fixed_wireless_connectivity_steps list
        elif (self.service == "Fixed Wireless"
              and self.category == "Connectivity") or (
                  self.service == "Fixed Wireless"
                  and self.category == "Intermittent Connectivity/Speed"
                  and self.isOnline == "no"):
            for index, item in enumerate(self.fixed_wireless_connectivity_steps):
                print(str(index + 1) + ". " + item)

        # General Connectivity Steps

        # If current service is N/A and category is Connectivity, print troubleshooting steps from general_connectivity_steps list
        elif self.service == "N/A" and self.category == "Connectivity":
            for index, item in enumerate(self.general_connectivity_steps):
                print(str(index + 1) + ". " + item)

        # General Speed Steps

        # If category is Speed, print troubleshooting steps from speed_steps list
        elif self.category == "Speed":
            for index, item in enumerate(self.speed_steps):
                print(str(index + 1) + ". " + item)

        # General Intermittent Connectivity/Speed Steps

        # If category is Intermittent Connectivity/Speed and isOnline is yes, print troubleshooting steps from intermittent_connectivity_and_speed_steps list
        elif self.category == "Intermittent Connectivity/Speed" and self.isOnline == "yes":
            for index, item in enumerate(self.intermittent_connectivity_and_speed_steps):
                print(str(index + 1) + ". " + item)

        # Email

        # if service is Email and category is Setup, print "No steps defined yet."
        elif self.service == "Email" and self.category == "Setup":
            print("No steps defined yet.")

        # if service is Email and category is Configuration, print "No steps defined yet."
        elif self.service == "Email" and self.category == "Configuration":
            print("No steps defined yet.")

        # General

        # if category is General, print "No troubleshooting steps defined for general categories"
        elif (self.category == "General"):
            print("No troubleshooting steps defined for general categories")

    def print_diagnostic_questions(self):
        """
        Name:
        print_diagnostic_questions

        Parameters:
        service, category

        When code is run:
        When print_ticket_steps_and_questions method is called.

        Purpose:
        Print certain diagnostic questions, depending on current service, category, and isOnline status.
        """

        # Initialize an empty list called ticket_questions.
        # The content will later depend on the current service and category
        ticket_questions = []

        print("Diagnostic Questions:")

        # if service is in internet_services list, run the following code
        if (self.service in self.internet_services):
            # append internet_general_questions and wifi_questions to ticket_questions.
            ticket_questions.append(self.internet_general_questions)
            ticket_questions.append(self.wifi_questions)
            # if service is DSL, append dsl_questions to ticket_questions
            if (self.service == "DSL"):
                ticket_questions.append(self.dsl_questions)
            # if category is Intermittent Connectivity/Speed, append intermittent_questions to ticket_questions.
            if (self.category == "Intermittent Connectivity/Speed"):
                ticket_questions.append(self.intermittent_questions)

        # if service is Email, run the following code
        elif (self.service == "Email"):
            # append email_general_questions to ticket_questions
            ticket_questions.append(self.email_general_questions)
            # if category is Setup, append email_setup_questions to ticket_questions
            if (self.category == "Setup"):
                ticket_questions.append(self.email_setup_questions)
            # if category is Configuration, append email_configuration_questions to ticket_questions
            if (self.category == "Configuration"):
                ticket_questions.append(self.email_configuration_questions)

        # if service is TV, run the following code
        elif (self.service == "TV"):
            # append tv_general_questions to ticket_questions
            ticket_questions.append(self.tv_general_questions)

        # Print all items in ticket_questions list.
        # Format: some_number. question_example | 1. "What devices are affected?"
        count = 1
        for list in ticket_questions:
            for item in list:
                print(str(count) + ". " + item)
                count += 1

    def print_commands(self):
        """
        Name:
        print_commands

        Parameters:
        None

        When code is run:
        When wait_for_command() is called.

        Purpose:
        Print all commands.
        """

        # # All commands - Uncomment when code written for all commands
        # print("Commands:")
        # command = [
        #     "Add Step - Add a troubleshooting step to the ticket.",
        #     "Add Question - Add a diagnostic question to the ticket.",
        #     "Add Line - Add a custom line of text and choose where to insert it.",
        #     "Add Category - Add a new service and/or category to the ticket.",
        #     "Remove Step - Remove a troubleshooting step from the ticket.",
        #     "Remove Question - Remove a diagnostic question from the ticket.",
        #     "Remove Line - Remove a custom line from the ticket.",
        #     "Remove Category - Remove a service and/or category from the ticket.",
        #     "Copy - Copy current ticket to the clipboard.",
        #     "Help - Show all available options.",
        #     "Main - Return to the main menu.",
        #     "End - End the program."
        # ]

        print("Commands:")
        commands = ["Help - Show all available options.", "Main - Return to the main menu.",
                    "End - End the program."
                    ]

        # In a certain format, print all items in commands.
        # Format: • Add Question - Add a diagnostic question to the ticket.
        for command in commands:
            print("• " + command)

    def print_ticket_steps_and_questions(self):
        """
        Name:
        print_ticket_steps_and_questions

        Parameters:
        None

        When code is run:
        At the end of the setup_ticket() method.
        When create_ticket() is called.

        Purpose:
        Prints the ticket, troubleshooting steps, and diagnostic questions.
        """

        print("\n\n----------------------------------\n\n")

        print("Ticket:\n")

        print(self.print_ticket())

        print("\n\n")

        self.print_troubleshooting_steps()

        print("\n\n")

        self.print_diagnostic_questions()

        print("\n\n")

    def wait_for_command(self):
        """
        Name:
        wait_for_command

        Parameters:
        None

        When code is run:
        At the end of create_ticket().
        When wait_for_command() is being run and user enters 'help'.

        Purpose:
        Allow the user to choose a command from a list of commands.
        Program will do something depending on which command is entered.
        Ex. typing 'help' shows all available commands. | Ex. typing 'main' will send user back to main menu.
        """

        # # Full list of commands - Uncomment when code written for all commands
        # ticket_command_choices = ["add step", "add question", "add line", "add category",
        #  "remove step", "remove question", "remove line", "remove category", "copy", "help", "main", "end"]

        # Commands not added yet
        # ticket_command_choices = ["add step", "add question", "add line", "add category",
        #  "remove step", "remove question", "remove line", "remove category"]

        print("Enter 'Help' to view available commands.\n")

        ticket_command_choices = ["copy", "help", "main", "end"]

        ticket_command_choice = input("Enter a command: ").lower().strip()

        # while user has not entered a command that's also in ticket_command_choices list, prompt user for a command.
        while ticket_command_choice not in ticket_command_choices:
            print("Please enter a valid option.\n")

            ticket_command_choice = input("Enter a command: ").lower().strip()

        # if user enters 'copy', copy contents of ticket into the clipboard
        if (ticket_command_choice == 'copy'):

            # copied_ticket contains the value of print_ticket()
            copied_ticket = self.print_ticket()

            # copied_ticket is passed to pyperclip.copy() since methods can't be passed to pyperclip.copy()
            pyperclip.copy(copied_ticket)

            print("\nTicket copied to clipboard!\n")

            self.wait_for_command()

        # if user enters 'help', print all available commands.
        # run wait_for_command after doing this, which will prompt user for a command again.
        elif (ticket_command_choice == "help"):
            print()

            self.print_commands()

            print()

            self.wait_for_command()

        # if user enters 'main', go back to the program's main menu
        elif (ticket_command_choice == "main"):
            system.clear_prompt_or_terminal()

            main_menu.open_main_menu()

        # if user enters 'end', end the program
        elif (ticket_command_choice == "end"):
            os.sys.exit(0)

    def create_ticket(self):
        """
        Name:
        create_ticket

        Parameters:
        None

        When code is run:
        From main_menu.py's execute_menu_command method, when user enters 'create'.

        Purpose:
        Call the setup_ticket, print_ticket_steps_and_questions, and wait_for_command methods.
        """

        self.setup_ticket()

        self.print_ticket_steps_and_questions()

        self.wait_for_command()
