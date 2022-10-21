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
        self.is_online = None
        self.troubleshooting_steps = []
        self.diagnostic_questions = []
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

        self.set_is_online()
        self.set_troubleshooting_steps()
        self.set_diagnostic_questions()

        # Append user key and value to end of ticket_content
        self.ticket_content.update({"user": self.user})

        print("\n\n")

        print("All questions answered!\n")

        print("Service: " + self.service + " | Category: " + self.category)
        print("Outputting ticket, troubleshooting steps, and diagnostic questions.",
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
        Append troubleshooting step lists to self.troubleshooting_steps based off the current service, category, and is_online status.
        """

        # Connectivity Steps

        # If current service is DSL and category is Connectivity, assign self.troubleshooting_steps to value of self.dsl_connectivity_steps
        # If category is Intermittent Connectivity/Speed and self.is_online is no, assign self.troubleshooting_steps to value of self.dsl_connectivity_steps
        if (self.service == "DSL" and self.category == "Connectivity") or (
                self.service == "DSL"
                and self.category == "Intermittent Connectivity/Speed"
                and self.is_online == "no"):
            self.troubleshooting_steps.append(self.dsl_connectivity_steps)

        # If current service is Fiber and category is Connectivity, assign self.troubleshooting_steps to value of self.fiber_connectivity_steps
        # If category is Intermittent Connectivity/Speed and self.is_online is no, assign self.troubleshooting_steps to value of self.fiber_connectivity_steps
        elif (self.service == "Fiber" and self.category == "Connectivity") or (
                self.service == "Fiber"
                and self.category == "Intermittent Connectivity/Speed"
                and self.is_online == "no"):
            self.troubleshooting_steps.append(self.fiber_connectivity_steps)

        # If current service is Cable and category is Connectivity, assign self.troubleshooting_steps to value of self.cable_connectivity_steps
        # If category is Intermittent Connectivity/Speed and self.is_online is no, assign self.troubleshooting_steps to value of self.cable_connectivity_steps
        elif (self.service == "Cable" and self.category == "Connectivity") or (
                self.service == "Cable"
                and self.category == "Intermittent Connectivity/Speed"
                and self.is_online == "no"):
            self.troubleshooting_steps.append(self.cable_connectivity_steps)

        # If current service is Fixed Wireless and category is Connectivity, assign self.troubleshooting_steps to value of self.fixed_wireless_connectivity_steps
        # If category is Intermittent Connectivity/Speed and self.is_online is no, assign self.troubleshooting_steps to value of self.fixed_wireless_connectivity_steps
        elif (self.service == "Fixed Wireless"
              and self.category == "Connectivity") or (
                  self.service == "Fixed Wireless"
                  and self.category == "Intermittent Connectivity/Speed"
                  and self.is_online == "no"):
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

        # If category is Intermittent Connectivity/Speed and is_online is yes, assign self.troubleshooting_steps to value of self.intermittent_connectivity_and_speed_steps
        elif self.category == "Intermittent Connectivity/Speed" and self.is_online == "yes":
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
        Assign the value of self.diagnostic_questions based off the current service, category, and self.is_online status.
        """

        current_questions = []

        # if service is in internet_services list, run the following code:
        if (self.service in self.internet_services):
            # append internet_general_questions and wifi_questions to current_questions.
            current_questions.append(self.internet_general_questions)
            current_questions.append(self.wifi_questions)
            # if service is DSL, append dsl_questions to current_questions.
            if (self.service == "DSL"):
                current_questions.append(self.dsl_questions)
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

    def set_is_online(self):
        """
        Name:
        set_is_online

        Parameters:
        None

        When code is run:
        When setup_ticket method is called.

        Purpose:
        Re-assign self.is_online variable to 'yes' or 'no' when category is intermittent connectivity/speed.
        """

        # If category is intermittent connectivity/speed and if method hasn't been run before, run the following code...
        if (self.category == "Intermittent Connectivity/Speed") and (self.is_online == None):

            # Prompt the user for network status.
            print("Is the internet online? \n")
            self.is_online = input(
                "Enter yes or no to respond. ").lower().strip()

            # While response is not 'yes' or 'no', prompt user for network status.
            while (self.is_online.lower() != "yes") and (self.is_online.lower()
                                                         != "no"):
                print("Please enter a valid response.\n")
                self.is_online = input(
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
        Print the order of lines in the ticket.
        """

        ticket_content_list = self.ticket_content.values()

        for index, value in enumerate(ticket_content_list):
            print(str(index + 1) + ". " + value)

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
                    "Add Line - Add a custom line of text and choose where to insert it.",
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

        print("\n\n----------------------------------\n\n")

        print("Ticket:\n")

        print(self.print_ticket())

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

        # Add step_response_sentence in dictionary into a specific spot of ticket_content that's based off keys in ticket_content

        #   Insert step before 'user' key in ticket content.
        insert_at_index = list(
            self.ticket_content.keys()).index('user')
        # Assign ticket_content_items list to the keys and values of ticket_content dictionary
        ticket_content_items = list(self.ticket_content.items())
        # Insert key and step_response_sentence value into ticket_content_items at index of insert_at_index
        ticket_content_items.insert(
            insert_at_index, ("step_" + self.service + "_" + self.category + "_" + step_response_sentence, step_response_sentence))
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

        if (question == "Are any services still working? "):
            question_response = input(
                "Are any services still working?\nEnter 'yes' or 'no' to respond | Enter 'exit' to not add question: ").lower()
            if question_response == "yes":
                print("\n\n")
                question_response = input(
                    "What services are still working?\nEnter exact service name(s) to respond | Enter 'exit' to not add question: ")
                question_response_sentence = "Still working: " + question_response
            elif question_response == "no":
                question_response_sentence = "No services are working"
            elif question_response == "exit":
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
        Prompt user for a custom line of text, have user select which line of ticket to insert it to, and then add the text to the ticket.
        """

        # Prompt user for a custom line of text, and save that text into 'custom_line'

        custom_line = input(
            "Enter 'exit' at any time to exit prompt.\nEnter a custom line of text: ").strip()

        if custom_line == "exit":
            return

        print("\n\n")

        # Output ticket with line numbers, so user knows which line to select
        self.print_ticket_with_line_numbers()

        print("\n\n")

        line_to_insert = input(
            "Enter 'exit' at any time to exit prompt.\nInsert custom line before line number: ").strip()

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

        pass

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
