# Copyright (c) <2022>, <Tai Jones>
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.


import os
import re
import time
import itertools
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
        self.services = None
        self.category = None
        self.are_devices_online = None
        self.ont_status = None
        self.ticket_content = {}
        self.ticket_status = "Ticket Status: Problem not resolved yet."
        self.troubleshooting_steps = []
        self.diagnostic_questions = []

        self.internet_services = ["Fiber", "DSL", "Cable", "Fixed Wireless"]
        self.services = [self.internet_services, ["Email"], ["TV"], ["N/A"]]

        self.internet_categories = [
            "General", "Connectivity", "Speed", "Intermittent Connectivity/Speed"]
        self.email_categories = ["General", "Setup", "Configuration"]
        self.tv_categories = ["General"]

        self.fiber_connectivity_steps = [
            "Check account status.",
            "Check status of all services.",
            "Check each network device’s name, model, and lights.",
            "Check a router for Wi-Fi.", "Check cabling.",
            "Check if cables are in the correct ports.",
            "Check cable conditions.", "Power cycle all network devices.",
            "Check each network device’s name, model, and lights.",
            "Check a device for internet.", "Check ONT.",
            "Check ONT's battery backup.", "Run ping tests on a computer."
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
            "How long has this issue been happening for?",
            "Were there any equipment changes or outside disturbances when the issue first started happening?"
        ]
        self.intermittent_questions = [
            "Is issue only happening during a certain time frame? If so, during what time(s)?",
            "Is issue only happening when a certain device is online? If so, which device?",
            "Is issue only happening when a lot of devices are online?",
            "How long is internet affected for?",
            "Does the equipment typically have to be powercycled to temporarily resolve the issue?",
            "Do lights on the router look the same when internet disconnects?"
        ]
        self.dsl_questions = [
            ""
        ]
        self.wifi_questions = [
            "Is the router in a closed space?",
            "Are there sources of interference like radios, extenders, metal doors, or metal ceilings?"
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

        # self.set_are_devices_online()
        self.set_troubleshooting_steps()
        self.set_diagnostic_questions()

        # Append user key and value to end of ticket_content
        self.ticket_content.update({"user": self.user})

        print("\n\n")

        print("All questions answered!\n")

        print("Service: " + self.service + " | Category: " + self.category)
        print("Outputting ticket, ticket status, troubleshooting steps, and diagnostic questions.",
              end="", flush=True)

        time.sleep(.75)
        print(".", end="", flush=True)

        time.sleep(.75)
        print(".", end="", flush=True)

        time.sleep(.75)

        print()

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

    def set_troubleshooting_steps(self):
        """
        Name:
        set_troubleshooting_steps

        Parameters:
        None

        When code is run:
        When setup_ticket method is called.

        Result:
        Append troubleshooting step lists to self.troubleshooting_steps based off the current service, category, and are_devices_online status.
        """

        # Connectivity Steps

        # If current service is DSL and category is Connectivity, assign self.troubleshooting_steps to value of self.dsl_connectivity_steps
        # If category is Intermittent Connectivity/Speed and self.are_devices_online is no, assign self.troubleshooting_steps to value of self.dsl_connectivity_steps
        if (self.service == "DSL" and self.category == "Connectivity") or (
                self.service == "DSL"
                and self.category == "Intermittent Connectivity/Speed"
                and self.are_devices_online == "no"):
            self.troubleshooting_steps.append(self.dsl_connectivity_steps)

        # If current service is Fiber and category is Connectivity, assign self.troubleshooting_steps to value of self.fiber_connectivity_steps
        # If category is Intermittent Connectivity/Speed and self.are_devices_online is no, assign self.troubleshooting_steps to value of self.fiber_connectivity_steps
        elif (self.service == "Fiber" and self.category == "Connectivity") or (
                self.service == "Fiber"
                and self.category == "Intermittent Connectivity/Speed"
                and self.are_devices_online == "no"):

            if (len(self.troubleshooting_steps) == 0):
                self.troubleshooting_steps.append(["Check account status."])

            elif ((self.ticket_status == "Ticket Status: Problem not resolved yet.\nAccount is active, but internet is offline.")
                  or (self.ticket_status == "Ticket Status: Problem not resolved yet.\nCannot determine account status.")):
                self.troubleshooting_steps[0].append(
                    "Check status of all services.")

            elif (self.ticket_status == "Ticket Status: Problem not resolved yet.\nOnly some devices have internet."):
                self.troubleshooting_steps[0].append(
                    "Check a device for internet.")

            elif (self.ticket_status == "Ticket Status: Problem not resolved yet.\nMultiple and all services are offline."):
                self.troubleshooting_steps[0].append("Check ONT")
                self.troubleshooting_steps[0].append(
                    "Check ONT's battery backup")

            elif ((self.ticket_status == "Ticket Status: Problem not resolved yet.\nONT is online, but there's no internet - Issue may be the router or some other device.")
                  or (self.ticket_status == "Ticket Status: Problem not resolved yet.\nOther services are working fine.")
                  or (self.ticket_status == "Ticket Status: Problem not resolved yet.\n" + self.service + ", the only service is offline.")):
                self.troubleshooting_steps[0].append(
                    "Check each network device’s name, model, and lights.")
                self.troubleshooting_steps[0].append("Check cabling.")
                self.troubleshooting_steps[0].append(
                    "Check if cables are in the correct ports.")
                self.troubleshooting_steps[0].append("Check cable conditions.")
                self.troubleshooting_steps[0].append(
                    "Power cycle all network devices.")
                self.troubleshooting_steps[0].append(
                    "Check each network device’s name, model, and lights.")
                self.troubleshooting_steps[0].append(
                    "Check a device for internet.")

                # Temporary: The steps below should not be hardcoded here if steps are based off decisions
                self.troubleshooting_steps[0].append(
                    "Run ping tests on a computer.")
                self.troubleshooting_steps[0].append(
                    "Check ONT.")
                self.troubleshooting_steps[0].append(
                    "Check ONT’s battery backup.")

        # If current service is Cable and category is Connectivity, assign self.troubleshooting_steps to value of self.cable_connectivity_steps
        # If category is Intermittent Connectivity/Speed and self.are_devices_online is no, assign self.troubleshooting_steps to value of self.cable_connectivity_steps
        elif (self.service == "Cable" and self.category == "Connectivity") or (
                self.service == "Cable"
                and self.category == "Intermittent Connectivity/Speed"
                and self.are_devices_online == "no"):
            self.troubleshooting_steps.append(self.cable_connectivity_steps)

        # If current service is Fixed Wireless and category is Connectivity, assign self.troubleshooting_steps to value of self.fixed_wireless_connectivity_steps
        # If category is Intermittent Connectivity/Speed and self.are_devices_online is no, assign self.troubleshooting_steps to value of self.fixed_wireless_connectivity_steps
        elif (self.service == "Fixed Wireless"
              and self.category == "Connectivity") or (
                  self.service == "Fixed Wireless"
                  and self.category == "Intermittent Connectivity/Speed"
                  and self.are_devices_online == "no"):
            self.troubleshooting_steps.append(
                self.fixed_wireless_connectivity_steps)

        # General Connectivity Steps

        # If current service is N/A and category is Connectivity, assign self.troubleshooting_steps to value of self.general_connectivity_steps
        elif self.service == "N/A" and self.category == "Connectivity":
            self.troubleshooting_steps.append(self.general_connectivity_steps)

        # General Speed Steps

        # If category is Speed, assign self.troubleshooting_steps to value of self.speed_steps
        elif self.category == "Speed":
            self.troubleshooting_steps.append(self.speed_steps)

        # General Intermittent Connectivity/Speed Steps

        # If category is Intermittent Connectivity/Speed and are_devices_online is yes, assign self.troubleshooting_steps to value of self.intermittent_connectivity_and_speed_steps
        elif self.category == "Intermittent Connectivity/Speed" and self.are_devices_online == "yes":
            self.troubleshooting_steps.append(
                self.intermittent_connectivity_and_speed_steps)

    def set_diagnostic_questions(self):
        """
        Name:
        set_diagnostic_questions

        Parameters:
        None

        When code is run:
        When setup_ticket method is called.

        Purpose:
        Assign the value of self.diagnostic_questions based off the current service, category, and self.are_devices_online status.
        """

        current_questions = []

        # if service is in internet_services list, run the following code:
        if (self.service in self.internet_services):
            # append internet_general_questions and wifi_questions to current_questions.
            current_questions.append(self.internet_general_questions)
            current_questions.append(self.wifi_questions)
            # # if service is DSL, append dsl_questions to current_questions.
            # if (self.service == "DSL"):
            #     current_questions.append(self.dsl_questions)
            # if category is Intermittent Connectivity/Speed, append intermittent_questions to current_questions.
            if (self.category == "Intermittent Connectivity/Speed"):
                current_questions.append(self.intermittent_questions)

        # if service is Email, run the following code:
        elif (self.service == "Email"):
            # append email_general_questions to current_questions.
            current_questions.append(self.email_general_questions)
            # if category is Setup, append email_setup_questions to current_questions.
            if (self.category == "Setup"):
                current_questions.append(self.email_setup_questions)
            # if category is Configuration, append email_configuration_questions to current_questions.
            if (self.category == "Configuration"):
                current_questions.append(
                    self.email_configuration_questions)

        # if service is TV, run the following code:
        elif (self.service == "TV"):
            # append tv_general_questions to current_questions.
            current_questions.append(self.tv_general_questions)

        # Combine the nested current_questions list into one list. Append the combined list to current_questions
        self.diagnostic_questions.append(list(itertools.chain.from_iterable(
            current_questions)))

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
        Assign all values from ticket_content dictionary to ticket_content_string.
        Return ticket_content_string.
        """

        ticket_content_string = ""

        # iterate through ticket_content dictionary
        for key, value in self.ticket_content.items():
            # if current key is user, starts with 'question_', or starts with 'step_', print current value following two new lines.
            if (key == "user" or key.startswith("question_") or key.startswith("step_")):
                ticket_content_string += "\n\n" + value
            # if current key is address or starts with 'current_line_', print a new line, value, and another new line.
            elif (key == "address") or (key.startswith("custom_line_")):
                ticket_content_string += "\n" + value + "\n"
            # if current key is number, print current value.
            elif (key == "number"):
                ticket_content_string += value
            # print current value following one new line.
            else:
                ticket_content_string += "\n" + value

        return ticket_content_string

    def print_ticket_with_line_numbers(self):
        """
        Name:
        print_ticket_with_line_numbers

        Parameters:
        None

        When code is run:
        When 'add line' is called.
        When 'remove line' is called.

        Purpose:
        Returns the order of lines in the ticket.
        """

        ticket_content_string = ""
        index = 1

        # iterate through ticket_content dictionary
        for key, value in self.ticket_content.items():
            # if current key is user, starts with 'question_', or starts with 'step_', print current value following two new lines.
            if (key == "user" or key.startswith("question_") or key.startswith("step_")):
                ticket_content_string += "\n\n" + str(index) + ". " + value
                index += 1
            # if current key is address or starts with 'current_line_', print a new line, value, and another new line.
            elif (key == "address") or (key.startswith("custom_line_")):
                ticket_content_string += "\n" + \
                    str(index) + ". " + value + "\n"
                index += 1
            # if current key is number, print current value.
            elif (key == "number"):
                ticket_content_string += str(index) + ". " + value
                index += 1
            # print current value following one new line.
            else:
                ticket_content_string += "\n" + str(index) + ". " + value
                index += 1

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
        Print troubleshooting steps from the ticket's troubleshooting_steps list, self.troubleshooting_steps.
        """

        print("Troubleshooting Steps:")

        # if service is Email and category is Setup, print "No steps defined yet."
        # if service is Email and category is Configuration, print "No steps defined yet."
        if (self.service == "Email" and self.category == "Setup") or (self.service == "Email" and self.category == "Configuration"):
            print("No steps defined yet.")

        # General

        # if category is General, print "No troubleshooting steps defined for general categories"
        elif (self.category == "General"):
            print("No troubleshooting steps defined for general categories")

        # Print all items in self.troubleshooting_steps list.
        # Format: some_number. troubleshooting_step_example | 1. "Run Speed tests on a devivce."
        count = 1
        for list in self.troubleshooting_steps:
            for item in list:
                print(str(count) + ". " + item)
                count += 1

    def print_diagnostic_questions(self):
        """
        Name:
        print_diagnostic_questions

        Parameters:
        None

        When code is run:
        When print_ticket_steps_and_questions method is called.

        Purpose:
        Print all questions in self.diagnostic_questions.
        """

        print("Diagnostic Questions:")

        # Print all items in self.diagnostic_questions list.
        # Format: some_number. question_example | 1. "What devices are affected?"
        count = 1
        for list in self.diagnostic_questions:
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
        #     "Remove Line - Remove a step, question, or custom line from the ticket.",
        #     "Remove Category - Remove a service and/or category from the ticket.",
        #     "Copy - Copy current ticket to the clipboard.",
        #     "Help - Show all available commands.",
        #     "Main - Return to the main menu.",
        #     "End - End the program."
        # ]

    # # Commands not coded for yet
        # print("Commands:")
        # command = [
        #     "Add Category - Add a new service and/or category to the ticket.",
        #     "Remove Category - Remove a service and/or category from the ticket."
        # ]

        print("Commands:")
        commands = ["Add Step - Add a troubleshooting step to the ticket.",
                    "Add Question - Add a diagnostic question to the ticket.",
                    "Add Line - Add one or more custom lines to the ticket.",
                    "Remove Line - Remove a step, question, or custom line from the ticket.",
                    "Copy - Copy current ticket to the clipboard.",
                    "Help - Show all available commands.",
                    "Main - Return to the main menu.",
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
        When create_ticket() is called.
        At the end of the setup_ticket() method.
        At the end of the add_step() method.
        At the end of the add_question() method.

        Purpose:
        Prints the ticket, troubleshooting steps, and diagnostic questions.
        """

        system.clear_prompt_or_terminal()

        print("\n\n----------------------------------\n\n")

        print("Ticket:\n")

        print(self.print_ticket())

        print("\n\n")

        # Possible values for ticket_status:
        # self.ticket_status = "Ticket Status: Problem not resolved yet."
        # self.ticket_status = "Ticket Status: Problem resolved.\n" + (More specific message based on what troubleshooting step resolved issue)
        # self.ticket_status = "Ticket Status: Escalating problem to a higher level is required to solve the problem."
        print(self.ticket_status)

        print("\n\n")

        self.print_troubleshooting_steps()

        print("\n\n")

        self.print_diagnostic_questions()

        print("\n\n")

    def add_step(self):
        """
        Name:
        add_step

        Parameters:
        None

        When code is run:
        In wait_for_command, when 'add_step' is entered.

        Purpose:
        Prompt the user for a troubleshooting step, have user answer steps's prompts, and then add the step to the ticket.
        """

        step_response_sentence = ""
        step_response = ""
        step = ""

        # def while_not_a_or_b_or_exit(a, b, variable, question):

        #     nonlocal step_response

        #     while (variable != a and variable != b):
        #         print("Invalid response - '" + a +
        #             "' or '" + b + "' was not entered.")

        #         variable = input("\n" + question).lower().strip()

        #         if (variable == "exit"):

        #             step_response = "exit"
        #             return

        system.clear_prompt_or_terminal()

        print("\n")

        self.print_troubleshooting_steps()

        print("\n\n")

        print("Select a troubleshooting step by entering in the position of a list and the corresponding number next to the list's item: \nExample. 1 2 | selects first list's second item.\n")

        # Prompt user for position of list and its step. Assign number to step_index

        step_index = input(
            "Enter position of list and its step: ").strip()

        # Assign first_index and second_index based off two numbers entered by user

        first_index = int(step_index.split()[0]) - 1
        second_index = int(step_index.split()[1]) - 1

        # Associate first_index and second_index with questions in self.troubleshooting_steps

        step = self.troubleshooting_steps[first_index][second_index]

        print("\n\n")

        # Find and execute relevant prompts for chosen step

        def check_account_status():

            nonlocal step_response
            nonlocal step_response_sentence

            print("Enter 'exit' at any time to exit prompt.\n")

            can_determine_account_status = input(
                "Can the account status be determined? Enter 'yes' or 'no': ").lower().strip()

            if (can_determine_account_status == "exit"):

                step_response = "exit"
                return

            while (can_determine_account_status != "yes" and can_determine_account_status != "no"):
                print("Invalid response - 'yes' or 'no' was not entered.")

                can_determine_account_status = input(
                    "\nCan the account status be determined? Enter 'yes' or 'no': ").lower().strip()

                if (can_determine_account_status == "exit"):

                    step_response = "exit"
                    return

            if (can_determine_account_status == "yes"):

                account_status = input(
                    "\nIs the account enabled or disabled? Enter 'enabled' or 'disabled': ").lower().strip()

                if (account_status == "exit"):

                    step_response = "exit"
                    return

                while (account_status != "enabled" and account_status != "disabled"):
                    print(
                        "Invalid response - 'enabled' or 'disabled' was not entered.")

                    account_status = input(
                        "\nIs the account enabled or disabled? Enter 'enabled' or 'disabled': ").lower().strip()

                    if (account_status == "exit"):

                        step_response = "exit"
                        return

                if (account_status == "disabled"):
                    self.ticket_status = "Ticket Status: Problem resolved in this ticket.\nAccount is disabled. Advised to pay service provider over phone or on website."
                    step_response_sentence = "Account is disabled. Advised to pay service provider over phone or on website."
                elif (account_status == "enabled"):
                    self.ticket_status = "Ticket Status: Problem not resolved yet.\nAccount is enabled, but internet is offline."
                    # Call this method to add "Check status of all services." to troubleshooting steps
                    self.set_troubleshooting_steps()
                    step_response_sentence = "Account is enabled."

            if (can_determine_account_status == 'no'):
                self.ticket_status = "Ticket Status: Problem not resolved yet.\nCannot determine account status."
                # Call this method to add "Check status of all services." to troubleshooting steps
                self.set_troubleshooting_steps()
                step_response_sentence = "Cannot determine account status."

        def check_status_of_all_services():

            if (step == "Check status of all services."):

                devices_online = ""

                services = ""
                offline_services = ""
                online_services = ""

                services_list = []
                offline_services_list = []
                online_services_list = []

                number_of_services = None
                number_of_offline_services = None

                nonlocal step_response_sentence
                nonlocal step_response

                print("Enter 'exit' at any time to exit prompt.\n")

                # Prompt for network status of all devices, if service is an internet service and category is connectivity or intermittent connectivity/speed.

                if (self.service in self.internet_services and (self.category == "Connectivity" or self.category == "Intermittent Connectivity/Speed")):
                    self.are_devices_online = input(
                        "Do any devices have internet? Enter 'yes' or 'no': ").lower().strip()

                    if (self.are_devices_online == "exit"):
                        step_response = "exit"
                        return

                    # While are_devices_online is not 'yes' and are_devices_online is not 'no', prompt for network status of all devices.
                    while (self.are_devices_online != "yes" and self.are_devices_online != "no"):
                        print("\nInvalid response - 'yes' or 'no' was not entered.")

                        self.are_devices_online = input(
                            "\nDo any devices have internet? Enter 'yes' or 'no': ").lower().strip()

                        if (self.are_devices_online == "exit"):

                            step_response = "exit"
                            return

                    # if some devices are online, mention this in step_response_sentence, find out which devices are online, and then set troubleshooting steps.
                    if (self.are_devices_online == 'yes'):
                        step_response_sentence += "At least one device is online."

                        # Prompt for which devices are online.
                        devices_online = input(
                            "\nWhat devices are online? Enter a comma seperated list of devices: ").lower().strip()

                        if (self.are_devices_online == "exit"):

                            step_response = "exit"
                            return

                        # Create a list of devices_online from sentence entered by user, with a new entry in list after every entered comma
                        devices_online_list = devices_online.split(",")
                        # Strip any whitespace before and after every service in list
                        devices_online_list = [device_online.strip(
                        ) for device_online in devices_online_list]

                        step_response_sentence += "\n\nDevices online: " + \
                            ", ".join(devices_online_list)

                        # Will add step to 'Check a device for internet.'
                        self.ticket_status = "Ticket Status: Problem not resolved yet.\nOnly some devices have internet."
                        self.set_troubleshooting_steps()

                        return

                    # if no devices are online, mention this in step_response_sentence.
                    if (self.are_devices_online == 'no'):
                        step_response_sentence += "No devices are online."

                        print("\n\n")

                # Prompt for services provided by service provider.

                services = input(
                    "Enter a comma seperated list of services provided by the service provider (Ex. Internet, Email, Phone, TV): ").lower().strip()

                if (services == "exit"):

                    step_response = "exit"
                    return

                # Create a list of services from sentence entered by user, with a new entry in list after every entered comma
                services_list = services.split(",")
                # Strip any whitespace before and after every service in list
                services_list = [service.strip() for service in services_list]

                # Parse through services variable to find number of entered services. Save this number into variable called number_of_services.
                number_of_services = len(services_list)

                if (self.service in self.internet_services and (self.category == "Connectivity" or self.category == "Intermittent Connectivity/Speed")):
                    step_response_sentence += "\n\nServices: " + \
                        ", ".join(services_list)
                else:
                    step_response_sentence += "Services: " + \
                        ", ".join(services_list)

                # If more than one service is provided by the service provider.
                if (number_of_services > 1):

                    # Prompt for offline services provided by service provider and save prompted information into offline_services variable.
                    offline_services = input(
                        "\nEnter a comma seperated list of offline services provided by the service provider (Ex. Internet, Email, Phone, TV): ").lower().strip()
                    if (offline_services == "exit"):

                        step_response = "exit"
                        return

                    # Create a list of offline services from sentence entered by user, with a new entry in list after every entered comma
                    offline_services_list = offline_services.split(",")
                    # Strip any whitespace before and after every offline service in list
                    offline_services_list = [offline_service.strip(
                    ) for offline_service in offline_services_list]

                    # Parse through services variable to find number of entered services. Save this number into variable called number_of_services.
                    number_of_offline_services = len(offline_services_list)

                    # User entered more offline services than services provided by service provider
                    while ((number_of_offline_services > number_of_services)):

                        print(
                            "There cannot be more offline services than services provided by service provider.")

                        # Prompt for offline services provided by service provider and save prompted information into offline_services variable.
                        offline_services = input(
                            "\nEnter a comma seperated list of offline services provided by the service provider (Ex. Internet, Email, Phone, TV): ").lower().strip()

                        # Exit questioning if user types "exit"
                        if (offline_services == "exit"):

                            step_response = "exit"
                            return

                        # Create a list of offline services from sentence entered by user, with a new entry in list after every entered comma
                        offline_services_list = offline_services.split(",")
                        # Strip any whitespace before and after every offline service in list
                        offline_services_list = [offline_service.strip(
                        ) for offline_service in offline_services_list]

                        # Parse through services variable to find number of entered services. Save this number into variable called number_of_services.
                        number_of_offline_services = len(offline_services_list)

                    # # While not offline services are provided by the service provider
                    # while (not all(offline_service in offline_services_list for service in service_list)):
                    #     print(
                    #         "At least one of the offline services is not a service provided by the service provider.")

                    #     # Prompt for offline services provided by service provider and save prompted information into offline_services variable.
                    #     offline_services = input(
                    #         "Enter 'exit' to exit prompt.\nEnter a comma seperated list of offline services provided by the service provider (Ex. Internet, Email, Phone, TV): ").lower().strip()

                    #     # Exit questioning if user types "exit"
                    #     if (offline_services == "exit"):
                    #         break

                    #     # Create a list of offline services from sentence entered by user, with a new entry in list after every entered comma
                    #     offline_services_list = offline_services.split(",")
                    #     # Strip any whitespace before and after every offline service in list
                    #     offline_services_list = [offline_service.strip(
                    #     ) for offline_service in offline_services_list]

                    #     # Parse through services variable to find number of entered services. Save this number into variable called number_of_services.
                    #     number_of_offline_services = len(offline_services_list)

                    step_response_sentence += "\nOffline Services: " + \
                        ", ".join(offline_services_list)

                    if (number_of_offline_services == number_of_services):
                        # if self.servivce == "fiber": Add the "Check ONT's Battery Backup" and "Check ONT" steps from set_troubleshooting_steps()
                        # if self.service == "dsl": Add "Check landline phone for dial tone" steps from set_troubleshooting_steps()
                        self.ticket_status = "Ticket Status: Problem not resolved yet.\nMultiple and all services are offline."
                        self.set_troubleshooting_steps()

                    elif (number_of_offline_services < number_of_services):

                        # Prompt for working services and save prompted information into online_services variable.
                        online_services = input(
                            "\nEnter a comma seperated list of working services. (Ex. Internet, Email, Phone, TV): ").lower().strip()

                        if (online_services == "exit"):

                            step_response = "exit"
                            return

                        # Create a list of online services from sentence entered by user, with a new entry in list after every entered comma
                        online_services_list = online_services.split(",")
                        # Strip any whitespace before and after every online service in list
                        online_services_list = [online_service.strip(
                        ) for online_service in online_services_list]

                        # # While not all entered online services are provided, inform that at least one of the online services is not a service provided by the service provider
                        # while (not all(online_service in online_services_list for service in service_list)):
                        #     print(
                        #         "At least one of the online services is not a service provided by the service provider.")

                        #     # Prompt for working services and save prompted information into online_services variable.
                        #     online_services = input(
                        #         "Enter 'exit' to exit prompt.\nEnter a comma seperated list of working services. (Ex. Internet, Email, Phone, TV): ").lower().strip()

                        #     # Exit questioning if user types "exit"
                        #     if (online_services == "exit"):
                        #         break

                        #     # Create a list of online services from sentence entered by user, with a new entry in list after every entered comma
                        #     online_services_list = online_services.split(",")
                        #     # Strip any whitespace before and after every online service in list
                        #     online_services_list = [online_service.strip(
                        #     ) for online_service in online_services_list]

                        step_response_sentence += "\nOnline Services: " + \
                            ", ".join(online_services_list)

                        # if online_services_list contains "phone" or online_services_list contains "TV" and self.service == "fiber", assign ont_status variable to online.
                        if (("phone" in online_services_list or "tv" in online_services_list) and (self.service == "Fiber" and (self.category == "Connectivity" or self.category == "Intermittent Connectivity/Speed"))):
                            step_response_sentence += (
                                "\n\nONT is online, but there's no internet - Issue may be the router or some other device.")
                            self.ticket_status = "Ticket Status: Problem not resolved yet.\nONT is online, but there's no internet - Issue may be the router or some other device."
                            self.set_troubleshooting_steps()
                        else:
                            self.ticket_status = "Ticket Status: Problem not resolved yet.\nOther services are working fine."
                            self.set_troubleshooting_steps()

                # If only one service is provided by the service provider.
                elif (number_of_services == 1):
                    self.ticket_status = "Ticket Status: Problem not resolved yet.\n" + \
                        self.service + ", the only service is offline."
                    self.set_troubleshooting_steps()

        def check_each_network_device():

            nonlocal step_response
            nonlocal step_response_sentence

            print("Enter 'exit' at any time to exit prompt.\n")

            can_be_checked = input(
                "Can network devices be checked? Enter “yes” or “no” to respond: ").lower().strip()

            if (can_be_checked == "exit"):

                step_response = "exit"
                return

            while (can_be_checked != "yes" and can_be_checked != "no"):
                print("\nInvalid response - 'yes' or 'no' was not entered.")

                can_be_checked = input(
                    "\nCan network devices be checked? Enter “yes” or “no” to respond: ").lower().strip()

                if (can_be_checked == "exit"):

                    step_response = "exit"
                    return

            if (can_be_checked == "no"):

                step_response_sentence = "No network devices can be checked."
                return

            elif (can_be_checked == "yes"):

                print(
                    "\n\nNetwork device information will be displayed in the following example format:\n")
                print("Brand Name - Model Number\nPower: Green - Solid\nInternet: Green - Flashing\n2.4GHz: Green - Flashing\n5GHz: Green - Flashing" +
                      "\nEthernet 1: Off\nEthernet 2: Green - Flashing\nEthernet 3: Off\nEthernet 4: Green - Solid\nUSB: Off\nWPS: Green - Solid")

                print(
                    "\n\nWhat device is being checked? Enter in format of 'Brand Name – Model Number': ")

                device_brand_and_model = input(
                    "").strip()

                if (device_brand_and_model.lower() == "exit"):

                    step_response = "exit"
                    return

                print("\n\nEnter “done” when all lights are documented.")

                print(
                    "\nWhat’s the status of the lights? Enter status in format of 'Light Name: Color – Status': ")

                device_lights = input("").strip()

                if (device_lights.lower() == "exit"):

                    step_response = "exit"
                    return

                while ("done" not in device_lights.lower().strip()):

                    device_lights += "\n" + input("").strip()

                    if ("exit" in device_lights.lower().strip()):

                        step_response = "exit"
                        return

                # Remove "done" and last new line from device_lights, only if device_lights length is greater than or equal to 4
                # If this is removed, no possiblity of only have a brand and model with no lights
                if (len(device_lights) >= 4):
                    device_lights = device_lights.rstrip(
                        device_lights[-4:]).rstrip()

                # Don't display a new line if device_lights is an empty string
                if (len(device_lights) == 0):
                    step_response_sentence = device_brand_and_model
                else:
                    step_response_sentence = device_brand_and_model + \
                        "\n" + device_lights.rstrip()

        def check_cabling(can_be_checked="yes", checking_again="no"):
            nonlocal step_response
            nonlocal step_response_sentence

            if (checking_again == "no"):
                print("Enter 'exit' at any time to exit prompt.\n")

                can_be_checked = input(
                    "Can cabling be checked? Enter “yes” or “no” to respond: ").lower().strip()

                if (can_be_checked == "exit"):

                    step_response = "exit"
                    return

                while (can_be_checked != "yes" and can_be_checked != "no"):
                    print("Invalid response - 'yes' or 'no' was not entered.")

                    can_be_checked = input(
                        "\nCan cabling be checked? Enter “yes” or “no” to respond: ").lower().strip()

                    if (can_be_checked == "exit"):

                        step_response = "exit"
                        return

            if ((can_be_checked == "no")):
                step_response_sentence = "Cabling cannot be checked."
                return

            elif ((can_be_checked == "yes") or (checking_again == "yes")):

                print(
                    "\n\nCabling will be displayed in the following example format:\n")
                print(
                    "wall jack > Router WAN port\nRouter ETH 2 port > Mesh router WAN port\nRouter ETH 4 port > Computer ETH port")

                print("\n\nEnter “done” when all cabling is documented.")

                print(
                    "\nWhat's the cabling? Enter in format of 'beginning device and port > end device and port': ")

                cabling = input("").strip()

                if (cabling.lower() == "exit"):

                    step_response = "exit"
                    return

                while ("done" not in cabling.lower().strip()):

                    cabling += "\n" + input("").strip()

                    if ("exit" in cabling.lower().strip()):

                        step_response = "exit"
                        return

                if (len(cabling) >= 4):
                    cabling = cabling.rstrip(
                        cabling[-4:]).rstrip()

                    step_response_sentence += cabling.rstrip()

        def check_cable_ports():
            nonlocal step_response
            nonlocal step_response_sentence

            print("Enter 'exit' at any time to exit prompt.\n")

            can_be_checked = input(
                "Can cable ports be checked? Enter “yes” or “no” to respond: ").lower().strip()

            if (can_be_checked == "exit"):

                step_response = "exit"
                return

            while (can_be_checked != "yes" and can_be_checked != "no"):
                print("Invalid response - 'yes' or 'no' was not entered.")

                can_be_checked = input(
                    "\nCan cabling be checked? Enter “yes” or “no” to respond: ").lower().strip()

                if (can_be_checked == "exit"):

                    step_response = "exit"
                    return

            if (can_be_checked == "no"):
                step_response_sentence = "Cable ports cannot be checked."
                return

            elif (can_be_checked == "yes"):

                correct_ports = input(
                    "Are all cables in the correct ports? Enter “yes” or “no” to respond: ").lower().strip()

                while (correct_ports != "yes" and correct_ports != "no"):
                    print("Invalid response - 'yes' or 'no' was not entered.")

                    correct_ports = input(
                        "\nAre all cables in the correct ports? Enter “yes” or “no” to respond: ").lower().strip()

                    if (correct_ports == "exit"):

                        step_response = "exit"
                        return

                if (correct_ports == "yes"):
                    step_response_sentence = "Cables are in the correct ports."

                elif (correct_ports == "no"):
                    step_response_sentence = "Cables are not in the correct ports."

                    can_be_corrected = input(
                        "Can the cables be moved to the correct ports? Enter “yes” or “no” to respond: ").lower().strip()

                    while (can_be_corrected != "yes" and can_be_corrected != "no"):
                        print("Invalid response - 'yes' or 'no' was not entered.")

                        can_be_corrected = input(
                            "\nCan the cables be moved to the correct ports? Enter “yes” or “no” to respond: ").lower().strip()

                        if (can_be_corrected == "exit"):

                            step_response = "exit"
                            return

                    if (can_be_corrected == "yes"):
                        step_response_sentence += "\nCables moved to the correct ports.\n\n"
                        check_cabling("yes", "yes")
                    elif (can_be_corrected == "no"):
                        step_response_sentence += "\nCables can't be moved to the correct ports."
                        self.ticket_status = "Ticket Status: Problem can't be resolved until cables are in the correct ports."

        def check_cable_conditions():
            nonlocal step_response
            nonlocal step_response_sentence

            print("Enter 'exit' at any time to exit prompt.\n")

            can_be_checked = input(
                "Can cable conditions be checked? Enter “yes” or “no” to respond: ").lower().strip()

            if (can_be_checked == "exit"):

                step_response = "exit"
                return

            while (can_be_checked != "yes" and can_be_checked != "no"):
                print("Invalid response - 'yes' or 'no' was not entered.")

                can_be_checked = input(
                    "\nCan cable conditions be checked? Enter “yes” or “no” to respond: ").lower().strip()

                if (can_be_checked == "exit"):

                    step_response = "exit"
                    return

            if (can_be_checked == "no"):
                step_response_sentence = "Cable conditions cannot be checked."

            elif (can_be_checked == "yes"):

                cables_not_loose_or_damaged = input(
                    "\nAre all cables secure and tight on all ends with no visible damage?\nEnter “yes”, “damaged”, or “loose” to respond: ").lower().strip()

                if (cables_not_loose_or_damaged == "exit"):

                    step_response = "exit"
                    return

                while (cables_not_loose_or_damaged != "yes" and cables_not_loose_or_damaged != "damaged" and cables_not_loose_or_damaged != "loose"):
                    print(
                        "Invalid response - Neither 'yes', 'damaged', or 'loose' were entered.")

                    cables_not_loose_or_damaged = input(
                        "\nAre all cables secure and tight on all ends with no visible damage?\nEnter “yes”, “damaged”, or “loose” to respond: ").lower().strip()

                    if (cables_not_loose_or_damaged == "exit"):

                        step_response = "exit"
                        return

                if (cables_not_loose_or_damaged == "yes"):
                    step_response_sentence = "All cables secure with no visible damage."
                    return

                elif (cables_not_loose_or_damaged == "damaged"):
                    damaged_cable = input(
                        "\nWhich cable is damaged? Enter in format of 'beginning device and port > end device and port':\n")

                    step_response_sentence = "Damaged cable: " + damaged_cable

                    can_be_replaced = input(
                        "\nCan the cable be replaced? Enter “yes” or “no” to respond: ").lower().strip()

                    if (can_be_replaced == "exit"):

                        step_response = "exit"
                        return

                    while (can_be_replaced != "yes" and can_be_replaced != "no"):
                        print(
                            "Invalid response - 'yes' or 'no' was not entered.")

                        can_be_replaced = input(
                            "\nCan the cable be replaced? Enter “yes” or “no” to respond: ").lower().strip()

                        if (can_be_replaced == "exit"):

                            step_response = "exit"
                            return

                    if (can_be_replaced == "no"):
                        step_response_sentence += "\nCable cannot be replaced."
                        return

                    elif (can_be_replaced == "yes"):
                        step_response_sentence += "\nJust replaced cable."
                        cables_not_loose_or_damaged = "yes"

                elif (cables_not_loose_or_damaged == "loose"):
                    loose_cable = input(
                        "\nWhich cable is loose? Enter in format of 'beginning device and port > end device and port':\n")

                    step_response_sentence = "Loose cable: " + loose_cable

                    can_be_fixed = input(
                        "\nCan the cable be pushed in or replaced? Enter “yes” or “no” to respond: ").lower().strip()

                    if (can_be_fixed == "exit"):

                        step_response = "exit"
                        return

                    while (can_be_fixed != "yes" and can_be_fixed != "no"):
                        print(
                            "Invalid response - 'yes' or 'no' was not entered.")

                        can_be_fixed = input(
                            "\nCan the cable be pushed in or replaced? Enter “yes” or “no” to respond: ").lower().strip()

                        if (can_be_fixed == "exit"):

                            step_response = "exit"
                            return

                    if (can_be_fixed == "no"):
                        step_response_sentence += "\nCable cannot be pushed in or replaced."
                        return

                    if (can_be_fixed == "yes"):
                        step_response_sentence += "\nJust fixed cabling."
                        cables_not_loose_or_damaged = "yes"

        def power_cycle():

            nonlocal step_response
            nonlocal step_response_sentence

            print("Enter 'exit' at any time to exit prompt.\n")

            can_be_power_cycled = input(
                "Can all network devices be power cycled? Enter “yes” or “no” to respond: ").lower().strip()

            if (can_be_power_cycled == "exit"):

                step_response = "exit"
                return

            while (can_be_power_cycled != "yes" and can_be_power_cycled != "no"):
                print("Invalid response - 'yes' or 'no' was not entered.")

                can_be_power_cycled = input(
                    "\nCan all network devices be power cycled? Enter “yes” or “no” to respond: ").lower().strip()

                if (can_be_power_cycled == "exit"):

                    step_response = "exit"
                    return

            if (can_be_power_cycled == "yes"):
                step_response_sentence = "All network devices power cycled for 30 seconds off."

            if (can_be_power_cycled == "no"):

                number_of_network_devices = input(
                    "\nEnter number of network devices: ").lower().strip()

                number_of_network_devices = int(number_of_network_devices)

                could_not_power_cycle = input(
                    "\nEnter a comma seperated list of devices that couldn't be power cycled: ").lower().strip()

                # Create a list of devices that couldn't be power cycled from sentence entered by user, with a new entry in list after every entered comma
                could_not_power_cycle_list = could_not_power_cycle.split(",")
                # Strip any whitespace before and after every device in list
                could_not_power_cycle_list = [
                    device.strip() for device in could_not_power_cycle_list]

                if (number_of_network_devices == len(could_not_power_cycle_list)):
                    step_response_sentence = "Was not able to power cycle any network device."
                else:
                    step_response_sentence = "Was able to power cycle every device except the: " + \
                        ", ".join(could_not_power_cycle_list)

        def check_ont():
            nonlocal step_response
            nonlocal step_response_sentence

            print("Enter 'exit' at any time to exit prompt.\n")

            can_be_checked = input(
                "Can the ONT be checked? Enter “yes” or “no” to respond: ").lower().strip()

            if (can_be_checked == "exit"):

                step_response = "exit"
                return

            while (can_be_checked != "yes" and can_be_checked != "no"):
                print("\nInvalid response - 'yes' or 'no' was not entered.")

                can_be_checked = input(
                    "\nCan the ONT be checked? Enter “yes” or “no” to respond: ").lower().strip()

                if (can_be_checked == "exit"):

                    step_response = "exit"
                    return

            if (can_be_checked == "no"):
                step_response_sentence = "ONT cannot be checked."

            elif (can_be_checked == "yes"):
                print(
                    "\n\nONT information will be displayed in the following example format:\n")

                print(
                    "ONT:\nPower: Amber - Solid\nWAN: Amber - Flashing")

                print("\n\nEnter “done” when all lights are documented.")

                print(
                    "\nWhat’s the status of the lights? Enter status in format of 'Light Name: Color – Status': ")

                ont_lights = input("").strip()

                if (ont_lights.lower() == "exit"):

                    step_response = "exit"
                    return

                while ("done" not in ont_lights.lower().strip()):

                    ont_lights += "\n" + input("").strip()

                    if ("exit" in ont_lights.lower().strip()):

                        step_response = "exit"
                        return

                if (len(ont_lights) >= 4):
                    ont_lights = ont_lights.rstrip(
                        ont_lights[-4:]).rstrip()

                    step_response_sentence += "ONT:\n" + ont_lights.rstrip()

        def check_battery_backup():

            nonlocal step_response
            nonlocal step_response_sentence

            print("Enter 'exit' at any time to exit prompt.\n")

            can_be_checked = input(
                "Can the ONT's battery backup be checked? Enter “yes” or “no” to respond: ").lower().strip()

            if (can_be_checked == "exit"):

                step_response = "exit"
                return

            while (can_be_checked != "yes" and can_be_checked != "no"):
                print("\nInvalid response - 'yes' or 'no' was not entered.")

                can_be_checked = input(
                    "\nCan the ONT's battery backup be checked? Enter “yes” or “no” to respond: ").lower().strip()

                if (can_be_checked == "exit"):

                    step_response = "exit"
                    return

            if (can_be_checked == "no"):
                step_response_sentence = "ONT's battery backup cannot be checked."

            elif (can_be_checked == "yes"):

                print(
                    "\n\nBattery backup information will be displayed in the following example format:\n")

                print(
                    "Battery Backup:\nAC: Amber - Solid\nDC: Green - Solid")

                print("\n\nEnter “done” when all lights are documented.")

                print(
                    "\nWhat’s the status of the lights? Enter status in format of 'Light Name: Color – Status': ")

                battery_backup_lights = input("").strip()

                if (battery_backup_lights.lower() == "exit"):

                    step_response = "exit"
                    return

                while ("done" not in battery_backup_lights.lower().strip()):

                    battery_backup_lights += "\n" + input("").strip()

                    if ("exit" in battery_backup_lights.lower().strip()):

                        step_response = "exit"
                        return

                if (len(battery_backup_lights) >= 4):
                    battery_backup_lights = battery_backup_lights.rstrip(
                        battery_backup_lights[-4:]).rstrip()

                    step_response_sentence += "Battery Backup:\n" + battery_backup_lights.rstrip()

        if (step == "Check account status."):
            check_account_status()

        if (step == "Check status of all services."):
            check_status_of_all_services()

        if (step == "Check each network device’s name, model, and lights."):
            check_each_network_device()

        if (step == "Check cabling."):
            check_cabling()

        if (step == "Check if cables are in the correct ports."):
            check_cable_ports()

        if (step == "Check cable conditions."):
            check_cable_conditions()

        if (step == "Power cycle all network devices."):
            power_cycle()

        if (step == "Check ONT."):
            check_ont()

        if (step == "Check ONT’s battery backup."):
            check_battery_backup()

        if (step == "Check if there’s a landline phone with dial tone."):
            step_response = input(
                "Can a landline phone be checked?\nEnter 'yes' or 'no' to respond | Enter 'exit' to not add question: ").lower()
            if step_response == "yes":
                print("\n\n")
                step_response = input(
                    "Does the landline phone have dial tone?\nEnter 'yes' or 'no' to respond | Enter 'exit' to not add question: ").lower()
                if step_response == "yes":
                    step_response_sentence = "Landline phone has dial tone."
                elif step_response == "no":
                    step_response_sentence = "Landline phone does not have dial tone."
            elif step_response == "no":
                step_response_sentence = "No landline phone can be checked."
            elif step_response == "exit":
                return

        # If exit is returned from any of the function calls, exit the loop without editing ticket content
        if (step_response == 'exit'):
            self.print_ticket_steps_and_questions()

            return

        # Add step_response_sentence in dictionary into a specific spot of ticket_content that's based off keys in ticket_content

        #   Insert step before 'user' key in ticket content.
        insert_at_index = list(
            self.ticket_content.keys()).index('user')
        # Assign ticket_content_items list to the keys and values of ticket_content dictionary
        ticket_content_items = list(self.ticket_content.items())
        # Insert key and step_response_sentence value into ticket_content_items at index of insert_at_index
        ticket_content_items.insert(
            insert_at_index, ("step_" + self.service + "_" + self.category + "_" + str(first_index) + "_" + str(second_index) + "_" + step_response_sentence, step_response_sentence))
        # Convert the ticket_content_items list to a dictionary
        self.ticket_content = dict(ticket_content_items)

        # Once a step is added to ticket_content, print ticket, steps, and questions

        self.print_ticket_steps_and_questions()

    def add_question(self):
        """
        Name:
        add_question

        Parameters:
        None

        When code is run:
        In wait_for_command, when 'add_question' is entered.

        Purpose:
        Prompt the user for a diagnostic question, have user answer question's prompts, and then add the question to the ticket.
        """

        question_response_sentence = ""
        question_response = ""
        question = ""

        system.clear_prompt_or_terminal()

        print("\n")

        self.print_diagnostic_questions()

        print("\n\n")

        print("Select a question by entering in the position of a list and the corresponding number next to the list's item: \nExample. 1 2 | selects first list's second item.\n")

        # Prompt user for position of list and its question. Assign number to question_index

        question_index = input(
            "Enter position of list and its question: ").strip()

        # Assign first_index and second_index based off two numbers entered by user

        first_index = int(question_index.split()[0]) - 1
        second_index = int(question_index.split()[1]) - 1

        # Associate first_index and second_index with questions in self.diagnostic_questions

        question = self.diagnostic_questions[first_index][second_index]

        print("\n\n")

        # Find and execute relevant prompts for chosen question

        def happening_for():

            nonlocal question_response
            nonlocal question_response_sentence

            print("Enter 'exit' at any time to exit prompt.\n")

            happening_for_how_long = input(
                "How long has the issue been happening since? Enter in example format of '3 weeks ago': ").strip()

            if (happening_for_how_long.lower() == "exit"):

                question_response = "exit"
                return

            question_response_sentence = "Issue happening since: " + happening_for_how_long

        def recent_changes():

            nonlocal question_response
            nonlocal question_response_sentence

            print("Enter 'exit' at any time to exit prompt.\n")

            if_recent_changes = input(
                "Were there any equipment changes or outside disturbances like weather or maintenance when the issue first started happening?\nEnter 'yes' or 'no' to respond: ").strip()

            if (if_recent_changes.lower() == "exit"):

                question_response = "exit"
                return

            while (if_recent_changes.lower() != "yes" and if_recent_changes.lower() != "no"):
                print("\nInvalid response - 'yes' or 'no' was not entered.")

                if_recent_changes = input(
                    "\nWere there any equipment changes or outside disturbances like weather or maintenance when the issue first started happening?\nEnter 'yes' or 'no' to respond: ").strip()

                if (if_recent_changes.lower() == "exit"):

                    question_response = "exit"
                    return

            if (if_recent_changes == "no"):
                question_response_sentence = "No equipment changes or outside disturbances like weather or maintenance when issue first started happening."

            if (if_recent_changes == "yes"):

                were_recent_changes = input(
                    "\nWhat happened when the issue first started happening?\n").strip()

                if (were_recent_changes.lower() == "exit"):

                    question_response = "exit"
                    return

                question_response_sentence = "Changes when the issue first started: " + were_recent_changes

        def closed_space():

            nonlocal question_response
            nonlocal question_response_sentence

            print("Enter 'exit' at any time to exit prompt.\n")

            print("Is the router in any of the following closed spaces for example:\n\n")

            print(
                "Closet\nCabinet\nEntertainment Center\nKitchen\nLaundry room\nBesides a phone’s base\n\n")

            if_closed_space = input(
                "Enter 'yes' or 'no' to respond: ").lower().strip()

            if (if_closed_space == "exit"):

                question_response = "exit"
                return

            while (if_closed_space != "yes" and if_closed_space != "no"):
                print("Invalid response - 'yes' or 'no' was not entered.")

                if_closed_space = input(
                    "\nEnter 'yes' or 'no' to respond: ").lower().strip()

                if (if_closed_space == "exit"):

                    question_response = "exit"
                    return

            if (if_closed_space == "no"):
                question_response_sentence = "Router is not in a closed space like a closet, cabinet, entertainment center, kitchen/laundry room, or besides a phone’s base."

            elif (if_closed_space == "yes"):

                what_closed_space = input(
                    "\nWhere exactly is the router? ").strip()

                if (what_closed_space.lower() == "exit"):

                    question_response = "exit"
                    return

                question_response_sentence = "Router is in: " + what_closed_space

        if (question == "How long has this issue been happening for?"):
            happening_for()

        if (question == "Were there any equipment changes or outside disturbances when the issue first started happening?"):
            recent_changes()

        if (question == "Is the router in a closed space?"):
            closed_space()

        if (question_response == 'exit'):

            self.print_ticket_steps_and_questions()
            return

        # Add question_response_sentence in dictionary into a specific spot of ticket_content that's based off keys in ticket_content

        #   Insert question before 'user' key in ticket content.
        insert_at_index = list(
            self.ticket_content.keys()).index('user')
        # Assign ticket_content_items list to the keys and values of ticket_content dictionary
        ticket_content_items = list(self.ticket_content.items())
        # Insert key and question_response_sentence value into ticket_content_items at index of insert_at_index
        ticket_content_items.insert(
            insert_at_index, ("question_" + self.service + "_" + self.category + "_" + question_response_sentence, question_response_sentence))
        # Convert the ticket_content_items list to a dictionary
        self.ticket_content = dict(ticket_content_items)

        # Once a question is added to ticket_content, print ticket, steps, and questions

        self.print_ticket_steps_and_questions()

    def add_line(self):
        """
        Name:
        add_line

        Parameters:
        None

        When code is run:
        In wait_for_command, when 'add_line' is entered.

        Purpose:
        Prompt user for one or more lines of text, have user select which line of ticket to insert it to, and then add the text to the ticket.
        """

        system.clear_prompt_or_terminal()

        print("\n")

        # Output ticket with line numbers, so user knows which line to select
        print("Ticket:\n")
        print(self.print_ticket_with_line_numbers())

        print("\n\n")

        print("Add Line - Add one or more custom lines to the ticket.\nEnter 'exit' at any time to exit prompt.\n")

        # Prompt user for a custom line of text, and save that text into 'custom_line'

        print("\nPress enter key to input multiple lines.\nEnter “done” when all lines are entered.")

        print("\nEnter lines below:")

        custom_line = input("").strip()

        if (custom_line.lower() == "exit"):
            return

        while ("done" not in custom_line.lower().strip()):

            custom_line += "\n" + input("").strip()

            if ("exit" in custom_line.lower().strip()):
                return

        if (len(custom_line) >= 4):
            custom_line = custom_line.rstrip(
                custom_line[-4:]).rstrip()

        print("\n\n")

        line_to_insert = input(
            "Insert custom line before which line number: ").strip()

        if line_to_insert == "exit":
            return

        # Convert whatever was typed in into an int. Subtract value by 1 since line numbers start at 0.
        line_to_insert = int(line_to_insert) - 1

        # Add custom_text into a specific spot of ticket_content that's based off line_to_insert

        # Assign ticket_content_items list to the keys and values of ticket_content dictionary
        ticket_content_items = list(self.ticket_content.items())
        # Insert key and custom_line value into ticket_content_items at index of line_to_insert
        ticket_content_items.insert(
            line_to_insert, ("custom_line_" + custom_line, custom_line))
        # Convert the ticket_content_items list to a dictionary
        self.ticket_content = dict(ticket_content_items)

        # Once a question is added to ticket_content, print ticket, steps, and questions

        self.print_ticket_steps_and_questions()

    def remove_line(self):
        """
        Name:
        remove_line

        Parameters:
        None

        When code is run:
        In wait_for_command, when 'remove_line' is entered.

        Purpose:
        Prompt user for a number corresponding to a line in the ticket and then remove the line from the ticket.
        """

        ticket_content_list = list(self.ticket_content.values())

        # Print ticket with corresponding line numbers.
        print(self.print_ticket_with_line_numbers())

        print("\n")

        # Prompt user to choose which line from ticket to remove.
        index_to_remove = input(
            "Enter 'exit' at any time to exit prompt.\nSelect which line number to remove: ").strip()

        # Convert prompted line number from a string to an int and subtract by 1 to get the correct index.
        index_to_remove = int(index_to_remove) - 1

        # Define the value from selected line to be removed
        value_to_remove = ticket_content_list[index_to_remove]

        # Loop through all keys and values in ticket_content
        for key, value in self.ticket_content.items():
            # if the current value is the same value from selected line number, assign current key to key_to_remove
            if value == value_to_remove:
                key_to_remove = key

        # Delete ticket_content's key_to_remove key
        del self.ticket_content[key_to_remove]

        self.print_ticket_steps_and_questions()

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
        #  "remove line", "remove category", "copy", "help", "main", "end"]

        # Commands not added yet
        # ticket_command_choices = ["add category",
        #  "remove category"]

        print("Enter 'Help' to view available commands.\n")

        ticket_command_choices = [
            "add step", "add question", "add line", "remove line", "copy", "help", "main", "end"]

        ticket_command_choice = input("Enter a command: ").lower().strip()

        # while user has not entered a command that's also in ticket_command_choices list, prompt user for a command.
        while ticket_command_choice not in ticket_command_choices:
            print("Please enter a valid option.\n")

            ticket_command_choice = input("Enter a command: ").lower().strip()

        # if user enters 'add step', prompt user for troubleshooting step prompts and then add the step to the ticket.
        if (ticket_command_choice == 'add step'):

            print("\n\n----------------------------------\n\n")

            self.add_step()

            self.wait_for_command()

        # if user enters 'add question', prompt user for question prompts and then add the question to the ticket.
        if (ticket_command_choice == 'add question'):

            print("\n\n----------------------------------\n\n")

            self.add_question()

            self.wait_for_command()

        # if user enters 'add line', prompt user for a custom line of text and then add the text to the ticket.
        if (ticket_command_choice == 'add line'):

            print("\n\n----------------------------------\n\n")

            self.add_line()

            self.wait_for_command()

        # if user enters 'remove line', prompt user for a number corresponding to a line in the ticket and then remove the line from the ticket.
        if (ticket_command_choice == 'remove line'):

            print("\n\n----------------------------------\n\n")

            self.remove_line()

            self.wait_for_command()

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

    # def set_are_devices_online(self):
    #     """
    #     Name:
    #     set_are_devices_online

    #     Parameters:
    #     None

    #     When code is run:
    #     When setup_ticket method is called.

    #     Purpose:
    #     Re-assign self.are_devices_online variable to 'yes' or 'no' when category is intermittent connectivity/speed.
    #     """

    #     # If category is intermittent connectivity/speed and if method hasn't been run before, run the following code...
    #     if (self.category == "Intermittent Connectivity/Speed") and (self.are_devices_online == None):

    #         # Prompt the user for network status.
    #         print("Is the internet online? \n")
    #         self.are_devices_online = input(
    #             "Enter yes or no to respond. ").lower().strip()

    #         # While response is not 'yes' or 'no', prompt user for network status.
    #         while (self.are_devices_online.lower() != "yes") and (self.are_devices_online.lower()
    #                                                               != "no"):
    #             print("Please enter a valid response.\n")
    #             self.are_devices_online = input(
    #                 "Enter yes or no to respond. ").lower().strip()

    #         print("\n\n")
