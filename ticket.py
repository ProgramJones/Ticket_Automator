# Copyright (c) <2022>, <Tai Jones>
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.


import os
import re
import time
import itertools
import random
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
        self.toggle_steps = "Recommended Steps"
        self.ticket_content = {}
        self.recommended_troubleshooting_steps = []
        self.troubleshooting_steps = []
        self.diagnostic_questions = []

        # self.ticket_status will update and hint user depending on responses to prompts. Steps are also sometimes recommended based off the ticket_status.
        #
        # Below examples:
        # self.ticket_status = "Ticket Status: Problem not resolved yet.\n" (More specific message based on latest update from a step)
        # self.ticket_status = "Ticket Status: Problem resolved.\n" + (More specific message based on what troubleshooting step resolved issue)
        # self.ticket_status = "Ticket Status: Problem can't be resolved right now.\nEscalating problem to a higher level is required to solve the problem."
        # self.ticket_status = "Ticket Status: Problem can't be resolved right now.\nReferring to a local technician or the product manufacturer is required to solve the problem." (For device issues)
        #
        self.ticket_status = "Ticket Status: Problem not resolved yet."

        # Steps are based off at least these variables
        self.devices_online = None
        self.ont_status = None  # Possible values: "online", "offline", or "n/a"
        self.main_router_status = None  # Possible values: "online", "offline", or "n/a"
        self.indoor_ont_status = None  # Possible values: "online", "offline", or "n/a"
        self.modem_status = None  # Possible values: "online", "offline", or "n/a"
        self.power_cycled = None  # Possible values: "yes", "no", or "n/a"
        self.correct_ports = None  # Possible values: "yes", "no", or "n/a"
        self.good_cable_conditions = None  # Possible values: "yes", "no", or "n/a"

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
            "Check cabling.",
            "Check if cables are in the correct ports.",
            "Check cable conditions.", "Power cycle all network devices.", "Check ONT.",
            "Check ONT's battery backup.", "Check battery backup for power.",
            "Check each network device’s name, model, and lights.",
            "Check network devices for internet.", "Check a device for internet.",  "Run ping tests on a computer."
        ]
        self.dsl_connectivity_steps = [
            "Check account status.",
            "Check landline phone for dial tone.",
            "Check status of all services.",
            "Check each network device’s name, model, and lights.",
            "Check cabling.",
            "Check if cables are in the correct ports.",
            "Check cable conditions.", "Power cycle all network devices.",
            "Check each network device’s name, model, and lights.",
            "Check network devices for internet.", "Check a device for internet.", "Run ping tests on a computer."
        ]
        self.cable_connectivity_steps = [
            "Check account status.",
            "Check status of all services.",
            "Check each network device’s name, model, and lights.",
            "Check cabling.",
            "Check if cables are in the correct ports.",
            "Check cable conditions.", "Power cycle all network devices.",
            "Check each network device’s name, model, and lights.",
            "Check network devices for internet.", "Check a device for internet.", "Run ping tests on a computer."
        ]
        self.fixed_wireless_connectivity_steps = [
            "Check account status.",
            "Check status of all services.",
            "Check each network device’s name, model, and lights.",
            "Check cabling.",
            "Check if cables are in the correct ports.",
            "Check cable conditions.", "Power cycle all network devices.",
            "Check each network device’s name, model, and lights.",
            "Check network devices for internet.", "Check a device for internet.", "Run ping tests on a computer."
        ]
        self.general_connectivity_steps = [
            "Check account status.",
            "Check status of all services.",
            "Check each network device’s name, model, and lights.",
            "Check cabling.",
            "Check if cables are in the correct ports.",
            "Check cable conditions.", "Power cycle all network devices.",
            "Check each network device’s name, model, and lights.",
            "Check network devices for internet.", "Check a device for internet.", "Run ping tests on a computer."
        ]
        self.speed_steps = [
            "Run speed tests on a device.",
            "Check each network device’s name, model, and lights.",
            "Check cabling.", "Check if cables are in the correct ports.",
            "Check cable conditions.",
            "Power cycle all network devices.",
            "Check each network device’s name, model, and lights.",
            "Check network devices for internet.", "Check a device for internet.",
            "Run speed tests on a device.", "Run ping tests on a computer."
        ]
        self.intermittent_connectivity_and_speed_steps = [
            "Check status of all services.", "Run speed tests on a device.", "Run ping tests on a computer.",
            "Check each network device’s name, model, and lights.",
            "Check cabling.", "Check if cables are in the correct ports.",
            "Check cable conditions.",
            "Power cycle all network devices.",
            "Check each network device’s name, model, and lights.",
            "Check network devices for internet.", "Check a device for internet.",
            "Run speed tests on a device.", "Run ping tests on a computer."
        ]
        self.dsl_intermittent_connectivity_and_speed_steps = [
            "Check status of all services.",
            "Check landline phone for dial tone.",
            "Run speed tests on a device.", "Run ping tests on a computer.",
            "Check each network device’s name, model, and lights.",
            "Check cabling.", "Check if cables are in the correct ports.",
            "Check cable conditions.",
            "Power cycle all network devices.",
            "Check each network device’s name, model, and lights.",
            "Check network devices for internet.", "Check a device for internet.",
            "Run speed tests on a device.", "Run ping tests on a computer."
        ]
        self.fiber_intermittent_connectivity_and_speed_steps = [
            "Check status of all services.", "Run speed tests on a device.", "Run ping tests on a computer.",
            "Check each network device’s name, model, and lights.",
            "Check cabling.", "Check if cables are in the correct ports.",
            "Check cable conditions.",
            "Power cycle all network devices.",
            "Check ONT.",
            "Check ONT's battery backup.", "Check battery backup for power.",
            "Check each network device’s name, model, and lights.",
            "Check network devices for internet.", "Check a device for internet.",
            "Run speed tests on a device.", "Run ping tests on a computer."
        ]

        self.internet_general_questions = [
            "How long has this issue been happening for?",
            "Were there any equipment changes or outside disturbances when the issue first started happening?"
        ]
        self.intermittent_questions = [
            "When is the problem typically happening?",
            "Does the problem happen when more or only certain devices are online?",
            "Does power cycling the equipment temporarily resolve the problem?",
            "How long does the problem typically last for?"
        ]
        self.dsl_questions = [
            ""
        ]
        self.wifi_questions = [
            "Is the router in a closed space?",
            "Are there any sources of interference?"
        ]

        self.email_general_questions = [
            "How long has this issue been happening for?"]
        self.email_setup_questions = []
        self.email_configuration_questions = []

        self.tv_general_questions = [
            "How long has this issue been happening for?"]

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

        self.troubleshooting_steps = []

        # Connectivity Steps

        # If current service is DSL and category is Connectivity, assign self.troubleshooting_steps to value of self.dsl_connectivity_steps
        # If category is Intermittent Connectivity/Speed and self.devices_online is no, assign self.troubleshooting_steps to value of self.dsl_connectivity_steps
        if (self.service == "DSL" and self.category == "Connectivity"):
            self.troubleshooting_steps.append(self.dsl_connectivity_steps)

        # If current service is Fiber and category is Connectivity, assign self.troubleshooting_steps to value of self.fiber_connectivity_steps
        # If category is Intermittent Connectivity/Speed and self.devices_online is no, assign self.troubleshooting_steps to value of self.fiber_connectivity_steps
        elif (self.service == "Fiber" and self.category == "Connectivity"):

            if (self.toggle_steps == "All Steps"):
                self.troubleshooting_steps.append(
                    self.fiber_connectivity_steps)

            elif (self.toggle_steps == "Recommended Steps"):

                if (len(self.recommended_troubleshooting_steps) == 0):
                    self.recommended_troubleshooting_steps.append(
                        ["Check account status."])

                elif ((self.ticket_status == "Ticket Status: Problem not resolved yet.\nAccount is active, but internet is offline."
                        or self.ticket_status == "Ticket Status: Problem not resolved yet.\nCannot determine account status.") and len(self.recommended_troubleshooting_steps[0]) == 1):
                    self.recommended_troubleshooting_steps[0].append(
                        "Check status of all services.")

                elif (self.devices_online == True):
                    self.recommended_troubleshooting_steps[0].append(
                        "Check a device for internet.")

                elif (self.ticket_status == "Ticket Status: Problem not resolved yet.\nMultiple and all services are offline." and len(self.recommended_troubleshooting_steps[0]) == 2):
                    self.recommended_troubleshooting_steps[0].append(
                        "Check ONT.")
                    self.recommended_troubleshooting_steps[0].append(
                        "Check ONT's battery backup.")
                    self.recommended_troubleshooting_steps[0].append(
                        "Check battery backup for power.")

                elif ((self.ticket_status == "Ticket Status: Problem not resolved yet.\nONT is online, but there's no internet - Issue may be the router or some other device.")
                        or (self.ticket_status == "Ticket Status: Problem not resolved yet.\nOther services are working fine.")
                        or (self.ticket_status == "Ticket Status: Problem not resolved yet.\n" + self.service + ", the only service is offline.") and len(self.recommended_troubleshooting_steps[0]) == 2):
                    self.recommended_troubleshooting_steps[0].append(
                        "Check each network device’s name, model, and lights.")
                    self.recommended_troubleshooting_steps[0].append(
                        "Check cabling.")
                    self.recommended_troubleshooting_steps[0].append(
                        "Check if cables are in the correct ports.")

                elif ((self.correct_ports == "yes" or self.correct_ports == "n/a") and len(self.recommended_troubleshooting_steps[0]) == 5):
                    self.recommended_troubleshooting_steps[0].append(
                        "Check cable conditions.")

                elif ((self.correct_ports == "yes" or self.correct_ports == "n/a") and len(self.recommended_troubleshooting_steps[0]) == 6):
                    self.recommended_troubleshooting_steps[0].append(
                        "Power cycle all network devices.")

                self.troubleshooting_steps = self.recommended_troubleshooting_steps

        # If current service is Cable and category is Connectivity, assign self.troubleshooting_steps to value of self.cable_connectivity_steps
        # If category is Intermittent Connectivity/Speed and self.devices_online is no, assign self.troubleshooting_steps to value of self.cable_connectivity_steps
        elif (self.service == "Cable" and self.category == "Connectivity"):
            self.troubleshooting_steps.append(self.cable_connectivity_steps)

        # If current service is Fixed Wireless and category is Connectivity, assign self.troubleshooting_steps to value of self.fixed_wireless_connectivity_steps
        # If category is Intermittent Connectivity/Speed and self.devices_online is no, assign self.troubleshooting_steps to value of self.fixed_wireless_connectivity_steps
        elif (self.service == "Fixed Wireless"
              and self.category == "Connectivity"):
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

        # Intermittent Connectivity/Speed Steps

        elif self.service == "Fiber" and self.category == "Intermittent Connectivity/Speed":
            self.troubleshooting_steps.append(
                self.fiber_intermittent_connectivity_and_speed_steps)

        elif self.service == "DSL" and self.category == "Intermittent Connectivity/Speed":
            self.troubleshooting_steps.append(
                self.dsl_intermittent_connectivity_and_speed_steps)

        # If category is Intermittent Connectivity/Speed and are_devices_online is yes, assign self.troubleshooting_steps to value of self.intermittent_connectivity_and_speed_steps
        elif self.category == "Intermittent Connectivity/Speed":
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
        Assign the value of self.diagnostic_questions based off the current service, category, and self.devices_online status.
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

    def toggling_steps(self):

        if (self.toggle_steps == "Recommended Steps"):
            self.toggle_steps = "All Steps"
            self.set_troubleshooting_steps()
            self.print_ticket_steps_and_questions()

        elif (self.toggle_steps == "All Steps"):
            self.toggle_steps = "Recommended Steps"
            self.set_troubleshooting_steps()
            self.print_ticket_steps_and_questions()

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

        if (self.toggle_steps == "All Steps"):
            print(
                "All Troubleshooting Steps:")
        elif (self.toggle_steps == "Recommended Steps"):
            print("Recommended Troubleshooting Steps:")

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
                    "Toggle Steps - Switch between viewing only the recommended steps and viewing all the steps.",
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

        print("Enter 'exit' at any time to exit prompt.\n")

        first_index = 0
        second_index = None
        ticket_content_list = list(self.ticket_content.values())

        # While second_index is not an int and second_index is less than or greater than self.troubleshooting steps list, run the following code
        while (True):
            second_index = input(
                "\nSelect a step by entering the number next to it: ").strip()

            if (second_index.lower() == "exit"):
                self.print_ticket_steps_and_questions()
                return
            try:
                # Convert second_index, entered by user, into a number
                # Subtract 1 from entered number, since list actually counts from 0
                second_index = int(second_index) - 1
            except ValueError:
                print("Invalid response - a number was not entered.")
                continue
            try:
                # Associate first_index and second_index with steps in self.troubleshooting_steps
                step = self.troubleshooting_steps[first_index][second_index]
            except IndexError:
                print(
                    "Invalid response - number entered does not correlate with a step.")
                continue
            if (second_index > len(self.troubleshooting_steps[0])):
                print(
                    "Invalid response - number entered does not correlate with a question.")
                continue
            if (second_index + 1 <= 0):
                print(
                    "Invalid response - number entered does not correlate with a step.")
                continue
            break

        print("\n\n")

        # Find and execute relevant prompts for chosen step

        # self.ticket_status will update depending on responses to prompts. Steps are recommended based off the ticket_status.
        #
        # Below examples:
        # self.ticket_status = "Ticket Status: Problem not resolved yet.\n" (More specific message based on latest update from a step)
        # self.ticket_status = "Ticket Status: Problem resolved.\n" + (More specific message based on what troubleshooting step resolved issue)
        # self.ticket_status = "Ticket Status: Problem can't be resolved right now.\nEscalating problem to a higher level is required to solve the problem."
        # self.ticket_status = "Ticket Status: Problem can't be resolved right now.\nReferring to a local technician or the product manufacturer is required to solve the problem." (For device issues)
        #

        # Decision Tree - check_account_status
        # self.ticket_status = "Ticket Status: Problem not resolved yet.\nAccount is active, but internet is offline.
        # self.ticket_status = "Ticket Status: Problem not resolved yet.\nCannot determine account status."
        # self.ticket_status = "Ticket Status: Problem resolved.\nAccount is disabled. Advised to pay service provider over phone or on website."
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
                    self.ticket_status = "Ticket Status: Problem resolved.\nAccount is disabled. Advised to pay service provider over phone or on website."
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

        def check_landline_phone_for_dial_tone():

            nonlocal step_response_sentence
            nonlocal step_response

            print("Enter 'exit' at any time to exit prompt.\n")

            can_be_checked = input(
                "Can a landline phone be checked for dial tone?\nEnter “yes” or “no” to respond: ").lower().strip()

            if (can_be_checked == "exit"):

                step_response = "exit"
                return

            while (can_be_checked != "yes" and can_be_checked != "no"):
                print("\nInvalid response - 'yes' or 'no' was not entered.")

                can_be_checked = input(
                    "\nCan a landline phone be checked for dial tone?\nEnter “yes” or “no” to respond: ").lower().strip()

                if (can_be_checked == "exit"):

                    step_response = "exit"
                    return

            if (can_be_checked == "yes"):

                has_dial_tone = input(
                    "\nDoes the landline phone have dial tone?\nEnter 'yes' or 'no' to respond: ").lower().strip()

                if (has_dial_tone == "exit"):

                    step_response = "exit"
                    return

                while (has_dial_tone != "yes" and has_dial_tone != "no"):
                    print("\nInvalid response - 'yes' or 'no' was not entered.")

                    has_dial_tone = input(
                        "\nDoes the landline phone have dial tone?\nEnter 'yes' or 'no' to respond: ").lower().strip()

                    if (has_dial_tone == "exit"):

                        step_response = "exit"
                        return

                if (has_dial_tone == "yes"):
                    step_response_sentence = "Landline phone has dial tone."

                elif (has_dial_tone == "no"):
                    step_response_sentence = "Landline phone does not have dial tone."

            elif (can_be_checked == "no"):
                step_response_sentence = "No landline phone can be checked for dial tone."

        # Simplify when to add steps from this method. Possibly 4 branches in add step can form from these four variables.
        # devices_online | True or False | Boolean | Created!
        # all_services_offline | True or False | Boolean
        # some_services_offline | True or False | Boolean
        # only_service_offline | True or False | Boolean

        # Decision Tree - check_status_of_all_services
        # self.ticket_status = "Ticket Status: Problem not resolved yet.\nOnly some devices have internet."
        # - Shows Steps: "Check a device for internet."
        # - Condition: Only some devices have internet

        # self.ticket_status = "Ticket Status: Problem not resolved yet.\nMultiple and all services are offline."
        # - Shows Steps: "Check ONT", "Check ONT's battery backup", "Check battery backup for power."
        # - Condition: Multiple and all services used are offline

        # self.ticket_status = "Ticket Status: Problem not resolved yet.\nONT is online, but there's no internet - Issue may be the router or some other device"
        # - Show Steps: "Check each network device’s name, model, and lights.", "Check cabling.", "Check if cables are in the correct ports."
        # - Condition: Fiber - Multiple servicves used, but only this service, self.service, is offline
        # Note: Results from "Check if cables are in the correct ports." may add "Check cable conditions." which may add "Power cycle all network devices.",
        # "Check each network device’s name, model, and lights.", and "Check network devices for internet."

        # self.ticket_status = "Ticket Status: Problem not resolved yet.\nOther services are working fine."
        # Show Steps: Same as above
        # - Condition: Multiple servicves used, but only this service, self.service, is offline

        # self.ticket_status = "Ticket Status: Problem not resolved yet.\n" + self.service + ", the only service is offline."
        # Show Steps: Same as above
        # - Condition: Only one service used and it's offline.
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
                    self.devices_online = input(
                        "Do any devices have internet? Enter 'yes' or 'no': ").lower().strip()

                    if (self.devices_online == "exit"):
                        step_response = "exit"
                        return

                    # While are_devices_online is not 'yes' and are_devices_online is not 'no', prompt for network status of all devices.
                    while (self.devices_online != "yes" and self.devices_online != "no"):
                        print(
                            "\nInvalid response - 'yes' or 'no' was not entered.")

                        self.devices_online = input(
                            "\nDo any devices have internet? Enter 'yes' or 'no': ").lower().strip()

                        if (self.devices_online == "exit"):

                            step_response = "exit"
                            return

                    # if some devices are online, mention this in step_response_sentence, find out which devices are online, and then set troubleshooting steps.
                    if (self.devices_online == "yes"):
                        self.devices_online = True

                        step_response_sentence += "At least one device is online."

                        # Prompt for which devices are online.
                        devices_online = input(
                            "\nWhat devices are online? Enter a comma seperated list of devices: ").lower().strip()

                        if (self.devices_online == "exit"):

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
                    if (self.devices_online == "no"):

                        self.devices_online = False

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

        # self.ticket_status = "Ticket Status: Problem can't be resolved right now.\nCables can't be switched to the correct ports."
        # - Show Steps: None
        # - Condition: Cabling can't be moved to correct ports
        # self.correct_ports == "yes", or "n/a" and length is 5
        # - Show Steps: "Check cable conditions."
        # - Condition: Cabling can be moved to correct ports, cabling can't be checked, cabling aready in correct ports
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
                self.correct_ports = "n/a"

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
                    self.correct_ports = "yes"

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
                        self.correct_ports = "yes"
                        check_cabling("yes", "yes")
                    elif (can_be_corrected == "no"):
                        step_response_sentence += "\nCables can't be moved to the correct ports."
                        self.ticket_status = "Ticket Status: Problem can't be resolved right now.\nCables can't be switched to the correct ports."

            self.set_troubleshooting_steps()

        # self.ticket_status = "Ticket Status: Problem can't be resolved right now.\nCables can't be fixed or replaced."
        # self.ticket_status = "Ticket Status: Problem can't be resolved right now.\nCables can't be replaced."
        # - Show Steps: None
        # - Condition: Cabling can't be replaced (damaged cables), Cabling can't be fixed or replaced (loose cables)
        # self.good_cable_conditions == "yes", or "n/a" and length is 6
        # - Show Steps: "Power cycle all network devices."
        # - Condition: Cables fixed or replaced, cabling can't be checked, cables aready secure with no damage
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
                self.good_cable_conditions = "n/a"

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
                    self.good_cable_conditions = "yes"
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
                        self.good_cable_conditions = "no"
                        self.ticket_status = "Ticket Status: Problem can't be resolved right now.\nCables can't be replaced."
                        return

                    elif (can_be_replaced == "yes"):
                        step_response_sentence += "\nJust replaced cable."
                        cables_not_loose_or_damaged = "yes"
                        self.good_cable_conditions = "yes"

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
                        self.good_cable_conditions = "no"
                        self.ticket_status = "Ticket Status: Problem can't be resolved right now.\nCables can't be fixed or replaced."
                        return

                    if (can_be_fixed == "yes"):
                        step_response_sentence += "\nJust fixed cabling."
                        cables_not_loose_or_damaged = "yes"
                        self.good_cable_conditions = "yes"

            self.set_troubleshooting_steps()

        # self.ticket_status = "Ticket Status: Problem not resolved yet.\nPower cycled network devices but haven't verified service works."
        #
        # self.power_cycled == "yes", or "no" and length is 7
        # - Show Steps: "Power cycle all network devices."
        # - Condition: Power cycled all network devices, Power cycled network devices, Couldn't power cycle
        # and "no" and ont_online?
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
                self.power_cycled = "yes"
                self.ticket_status = "Ticket Status: Problem not resolved yet.\nPower cycled all network devices but haven't verified service works."

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
                    self.power_cycled = "no"
                else:
                    step_response_sentence = "Was able to power cycle every device except the: " + \
                        ", ".join(could_not_power_cycle_list)
                    self.power_cycled = "yes"
                    self.ticket_status = "Ticket Status: Problem not resolved yet.\nPower cycled network devices but haven't verified service works."

            self.set_troubleshooting_steps()

        def check_network_devices_for_internet():

            nonlocal step_response
            nonlocal step_response_sentence

            print("Enter 'exit' at any time to exit prompt.\n")

            # Can network devices be checked?
            can_be_checked = input(
                "Can network devices be checked?\nEnter 'yes' or 'no' to respond: ").lower().strip()

            if (can_be_checked == "exit"):

                step_response = "exit"
                return

            while (can_be_checked != "yes" and can_be_checked != "no"):
                print("\nInvalid response - 'yes' or 'no' was not entered.")

                can_be_checked = input(
                    "\nCan network devices be checked?\nEnter “yes” or “no” to respond: ").lower().strip()

                if (can_be_checked == "exit"):

                    step_response = "exit"
                    return

            # if yes, network devices can be checked, Do all non-bridged network devices show internet?
            if (can_be_checked == "yes"):
                all_network_devices_show_internet = input(
                    "\nDo all non-bridged network devices show internet?\nEnter 'yes' or 'no' to respond: ").lower().strip()

                if (all_network_devices_show_internet == "exit"):

                    step_response = "exit"
                    return

                while (all_network_devices_show_internet != "yes" and all_network_devices_show_internet != "no"):
                    print("\nInvalid response - 'yes' or 'no' was not entered.")

                    all_network_devices_show_internet = input(
                        "\nCan network devices be checked?\nEnter “yes” or “no” to respond: ").lower().strip()

                    if (all_network_devices_show_internet == "exit"):

                        step_response = "exit"
                        return

                # if yes, all non-bridged network devices show internet, add "All non-bridged network devices show internet." to ticket.
                if (all_network_devices_show_internet == "yes"):
                    step_response_sentence = "All non-bridged network devices show internet."

                # if no, not all non-bridged network devices show internet, is there a main router?
                if (all_network_devices_show_internet == "no"):

                    is_there_a_main_router = input(
                        "\nIs there a main router?\nEnter 'yes' or 'no' to respond: ").lower().strip()

                    if (is_there_a_main_router == "exit"):

                        step_response = "exit"
                        return

                    while (is_there_a_main_router != "yes" and is_there_a_main_router != "no"):
                        print("\nInvalid response - 'yes' or 'no' was not entered.")

                        is_there_a_main_router = input(
                            "\nIs there a main router?\nEnter 'yes' or 'no' to respond: ").lower().strip()

                        if (is_there_a_main_router == "exit"):

                            step_response = "exit"
                            return

                    # if yes, there is a main router, does the main router show internet?
                    if (is_there_a_main_router == "yes"):

                        main_router_shows_internet = input(
                            "\nDoes the main router show internet?\nEnter 'yes' or 'no' to respond: ").lower().strip()

                        if (main_router_shows_internet == "exit"):

                            step_response = "exit"
                            return

                        while (main_router_shows_internet != "yes" and main_router_shows_internet != "no"):
                            print(
                                "\nInvalid response - 'yes' or 'no' was not entered.")

                            main_router_shows_internet = input(
                                "\nDoes the main router show internet?\nEnter 'yes' or 'no' to respond: ").lower().strip()

                            if (main_router_shows_internet == "exit"):

                                step_response = "exit"
                                return

                        # if yes, main router shows internet, add "Main router shows internet." to ticket.
                        if (main_router_shows_internet == "yes"):
                            step_response_sentence = "Main router shows internet."

                        # if no, main router does not show internet, add "Main router does not show internet." to ticket.
                        if (main_router_shows_internet == "no"):
                            step_response_sentence = "Main router does not show internet."

                # if no, not all non-bridged network devices show internet, is there an indoor ONT? (FIBER)
                if (all_network_devices_show_internet == "no" and self.service == "Fiber"):

                    is_there_an_indoor_ont = input(
                        "\nIs there an indoor ONT?\nEnter “yes” or “no” to respond: ").lower().strip()

                    if (is_there_an_indoor_ont == "exit"):

                        step_response = "exit"
                        return

                    while (is_there_an_indoor_ont != "yes" and is_there_an_indoor_ont != "no"):
                        print("\nInvalid response - 'yes' or 'no' was not entered.")

                        is_there_an_indoor_ont = input(
                            "\nIs there an indoor ONT?\nEnter “yes” or “no” to respond: ").lower().strip()

                        if (is_there_an_indoor_ont == "exit"):

                            step_response = "exit"
                            return

                    # if yes, there is an indoor ONT, does the indoor ONT show internet?
                    if (is_there_an_indoor_ont == "yes"):

                        indoor_ont_shows_internet = input(
                            "\nDoes the indoor ONT show internet?\nEnter “yes” or “no” to respond: ").lower().strip()

                        if (indoor_ont_shows_internet == "exit"):

                            step_response = "exit"
                            return

                        while (indoor_ont_shows_internet != "yes" and indoor_ont_shows_internet != "no"):
                            print(
                                "\nInvalid response - 'yes' or 'no' was not entered.")

                            indoor_ont_shows_internet = input(
                                "\nDoes the indoor ONT show internet?\nEnter “yes” or “no” to respond: ").lower().strip()

                            if (indoor_ont_shows_internet == "exit"):

                                step_response = "exit"
                                return

                        # if yes, indoor ONT shows internet, add "Indoor ONT shows internet." to ticket.
                        if (indoor_ont_shows_internet == "yes"):
                            if (step_response_sentence == ""):
                                step_response_sentence = "Indoor ONT shows internet."
                            else:
                                step_response_sentence += "\nIndoor ONT shows internet."

                        # if no, indoor ONT does not show internet, add "Indoor ONT does not show internet." to ticket.
                        if (indoor_ont_shows_internet == "no"):
                            if (step_response_sentence == ""):
                                step_response_sentence = "Indoor ONT does not show internet."
                            else:
                                step_response_sentence += "\nIndoor ONT does not show internet."

                # if no, not all non-bridged network devices show internet, is there a non-bridged modem? (CABLE and DSL) WORK ON BELOW
                if (all_network_devices_show_internet == "no" and (self.service == "Cable" or self.service == "DSL")):

                    is_there_a_modem = input(
                        "\nIs there a non-bridged modem?\nEnter 'yes' or 'no' to respond: ").lower().strip()

                    if (is_there_a_modem == "exit"):

                        step_response = "exit"
                        return

                    while (is_there_a_modem != "yes" and is_there_a_modem != "no"):
                        print("\nInvalid response - 'yes' or 'no' was not entered.")

                        is_there_a_modem = input(
                            "\nIs there a non-bridged modem?\nEnter 'yes' or 'no' to respond: ").lower().strip()

                        if (is_there_a_modem == "exit"):

                            step_response = "exit"
                            return

                    # if yes, there is a modem, does the modem show internet?
                    if (is_there_a_modem == "yes"):

                        modem_shows_internet = input(
                            "\nDoes the modem show internet?\nEnter 'yes' or 'no' to respond: ").lower().strip()

                        if (modem_shows_internet == "exit"):

                            step_response = "exit"
                            return

                        while (modem_shows_internet != "yes" and modem_shows_internet != "no"):
                            print(
                                "\nInvalid response - 'yes' or 'no' was not entered.")

                            modem_shows_internet = input(
                                "\nDoes the modem show internet?\nEnter 'yes' or 'no' to respond: ").lower().strip()

                            if (modem_shows_internet == "exit"):

                                step_response = "exit"
                                return

                        # if yes, modem shows internet, add "Modem shows internet." to ticket.
                        if (modem_shows_internet == "yes"):
                            if (step_response_sentence == ""):
                                step_response_sentence = "Modem shows internet."
                            else:
                                step_response_sentence += "\nModem shows internet."

                        # if no, modem does not show internet, add "Modem does not show internet." to ticket.
                        if (modem_shows_internet == "no"):
                            if (step_response_sentence == ""):
                                step_response_sentence = "Modem does not show internet."
                            else:
                                step_response_sentence += "\nModem does not show internet."

                # if no, not all non-bridged network devices show internet, what other network devices don't show internet?
                if (all_network_devices_show_internet == "no"):
                    other_devices_showing_no_internet = input(
                        "\nWhat other devices are showing no internet?\n").strip()
                    if (step_response_sentence == ""):
                        step_response_sentence = "Misc devices showing no internet: " + \
                            other_devices_showing_no_internet
                    else:
                        step_response_sentence += "\nMisc devices showing no internet: " + \
                            other_devices_showing_no_internet

            # if no, network devices cannot be checked, "Network devices cannot be checked for internet."
            elif (can_be_checked == "no"):
                step_response_sentence = "Network devices cannot be checked for internet."

        def check_devices():
            nonlocal step_response
            nonlocal step_response_sentence

            print("Enter 'exit' at any time to exit prompt.\n")

            # What device is being checked for internet? Enter 'Phone', 'Computer', or 'Other' to respond.
            check_which_device = input(
                "\nWhat device is being checked for internet?\nEnter 'Mobile Device', 'Computer', 'TV', or 'Other' to respond: ").lower().strip()

            if (check_which_device == "exit"):

                step_response = "exit"
                return

            while (check_which_device != "mobile device" and check_which_device != "computer" and check_which_device != "tv" and check_which_device != "other"):
                print(
                    "Invalid response - Neither 'Mobile Device', 'Computer', 'TV', 'Other' were entered.")

                check_which_device = input(
                    "\nWhat device is being checked for internet?\nEnter 'Mobile Device', 'Computer', 'TV', or 'Other' to respond: ").lower().strip()

                if (check_which_device == "exit"):

                    step_response = "exit"
                    return

            # Checking for internet on a mobile device.
            if (check_which_device == "mobile device"):
                step_response_sentence = "Checking for internet on a mobile device."

                name_of_wifi_network = input(
                    "\nWhat WiFi network is the mobile device connected to?\nEnter name of WiFi network to respond: ").strip()
                step_response_sentence += "\nConnected to SSID of: " + name_of_wifi_network

                is_internet_working = input(
                    "\nIs the internet working?\nEnter 'yes' or 'no' to respond: ").lower().strip()

                if (is_internet_working == "exit"):

                    step_response = "exit"
                    return

                while (is_internet_working != "yes" and is_internet_working != "no"):
                    print("\nInvalid response - 'yes' or 'no' was not entered.")

                    is_internet_working = input(
                        "\nIs the internet working?\nEnter 'yes' or 'no' to respond: ").lower().strip()

                    if (is_internet_working == "exit"):

                        step_response = "exit"
                        return

                # if yes, internet is working, add "Internet is working on a mobile device." to ticket.
                if (is_internet_working == "yes"):

                    step_response_sentence += "\nInternet is working on a mobile device."

                # if no, internet is not working, what's the IPv4 address?
                elif (is_internet_working == "no"):
                    mobile_device_ip_address = input(
                        "\nWhat's the mobile device's IPv4 address? ").strip()

                    step_response_sentence += "\nNo internet on mobile device."
                    step_response_sentence += "\nIPv4 address: " + \
                        mobile_device_ip_address

            # Checking for internet on a computer.
            elif (check_which_device == "computer"):
                step_response_sentence = "Checking for internet on a computer"

                # How is the computer connected to the internet?
                how_computer_is_connected = input(
                    "\nIs the computer bypassing the main router, wiring to a network device, or using Wi-Fi?\nEnter 'bypass', 'wire', or 'wifi' to respond: ").lower().strip()

                if (how_computer_is_connected == "exit"):

                    step_response = "exit"
                    return

                while (how_computer_is_connected != "bypass" and how_computer_is_connected != "wire" and how_computer_is_connected != "wifi"):
                    print(
                        "\nInvalid response - Neither 'Bypass', 'Wire', or 'WiFi' were entered.")

                    how_computer_is_connected = input(
                        "\nIs the computer bypassing the main router, wiring to a network device, or using Wi-Fi?\nEnter 'bypass', 'wire', or 'wifi' to respond: ").lower().strip()

                    if (how_computer_is_connected == "exit"):

                        step_response = "exit"
                        return

                if (how_computer_is_connected == "bypass"):
                    step_response_sentence += "\nComputer is bypassing the main router."

                elif (how_computer_is_connected == "wire"):
                    step_response_sentence += "\nComputer is wiring to a network device."

                elif (how_computer_is_connected == "wifi"):
                    name_of_wifi_network = input(
                        "\nWhat WiFi network is the computer connected to?\nEnter name of WiFi network to respond: ").strip()
                    step_response_sentence += "\nConnected to SSID of: " + name_of_wifi_network

                is_internet_working = input(
                    "\nIs the internet working?\nEnter 'yes' or 'no' to respond: ").lower().strip()

                if (is_internet_working == "exit"):

                    step_response = "exit"
                    return

                while (is_internet_working != "yes" and is_internet_working != "no"):
                    print("\nInvalid response - 'yes' or 'no' was not entered.")

                    is_internet_working = input(
                        "\nIs the internet working?\nEnter 'yes' or 'no' to respond: ").lower().strip()

                    if (is_internet_working == "exit"):

                        step_response = "exit"
                        return

                # if yes, internet is working, add "Internet is working on a computer." to ticket.
                if (is_internet_working == "yes"):

                    step_response_sentence += "\nInternet is working on a computer."

                # if no, internet is not working, what's the IPv4 address?
                elif (is_internet_working == "no"):
                    computer_ip_address = input(
                        "\nWhat's the computer's IPv4 address? ").strip()
                    computer_default_gateway = input(
                        "What's the computer's default gateway address? ").strip()

                    step_response_sentence += "\nNo internet on computer."
                    step_response_sentence += "\nIPv4 address: " + \
                        computer_ip_address
                    step_response_sentence += "\nDefault Gateway: " + \
                        computer_default_gateway

            # Checking for internet on a TV.
            elif (check_which_device == "tv"):
                step_response_sentence = "Checking for internet on a TV"

                # How is the tv connected to the internet?
                how_tv_is_connected = input(
                    "\nIs the TV bypassing the main router, wiring to a network device, or using Wi-Fi?\nEnter 'bypass', 'wire', or 'wifi' to respond: ").lower().strip()

                if (how_tv_is_connected == "exit"):

                    step_response = "exit"
                    return

                while (how_tv_is_connected != "bypass" and how_tv_is_connected != "wire" and how_tv_is_connected != "wifi"):
                    print(
                        "\nInvalid response - Neither 'Bypass', 'Wire', or 'WiFi' were entered.")

                    how_tv_is_connected = input(
                        "\nIs the TV bypassing the main router, wiring to a network device, or using Wi-Fi?\nEnter 'bypass', 'wire', or 'wifi' to respond: ").lower().strip()

                    if (how_tv_is_connected == "exit"):

                        step_response = "exit"
                        return

                if (how_tv_is_connected == "bypass"):
                    step_response_sentence += "\nTV is bypassing the main router."

                elif (how_tv_is_connected == "wire"):
                    step_response_sentence += "\nTV is wiring to a network device."

                elif (how_tv_is_connected == "wifi"):
                    name_of_wifi_network = input(
                        "\nWhat WiFi network is the TV connected to?\nEnter name of WiFi network to respond: ").strip()
                    step_response_sentence += "\nConnected to SSID of: " + name_of_wifi_network

                is_internet_working = input(
                    "\nIs the internet working?\nEnter 'yes' or 'no' to respond: ").lower().strip()

                if (is_internet_working == "exit"):

                    step_response = "exit"
                    return

                while (is_internet_working != "yes" and is_internet_working != "no"):
                    print("\nInvalid response - 'yes' or 'no' was not entered.")

                    is_internet_working = input(
                        "\nIs the internet working?\nEnter 'yes' or 'no' to respond: ").lower().strip()

                    if (is_internet_working == "exit"):

                        step_response = "exit"
                        return

                # if yes, internet is working, add "Internet is working on a computer." to ticket.
                if (is_internet_working == "yes"):

                    step_response_sentence += "\nInternet is working on a TV."

                # if no, internet is not working, what's the IPv4 address?
                elif (is_internet_working == "no"):
                    tv_ip_address = input(
                        "\nWhat's the TV's IPv4 address? ").strip()
                    tv_default_gateway = input(
                        "What's the TV's default gateway address? ").strip()

                    step_response_sentence += "\nNo internet on TV."
                    step_response_sentence += "\nIPv4 address: " + \
                        tv_ip_address
                    step_response_sentence += "\nDefault Gateway: " + \
                        tv_default_gateway

            # Checking for internet on some other device.
            elif (check_which_device == "other"):

                name_of_other_device = input(
                    "\nWhat's the name of the device?\nEnter the device name to respond: ")
                step_response_sentence = "Checking for internet on: " + name_of_other_device

                # How is the device connected to the internet?
                how_device_is_connected = input(
                    "\nIs the device bypassing the main router, wiring to a network device, or using Wi-Fi?\nEnter 'bypass', 'wire', or 'wifi' to respond: ").lower().strip()

                if (how_device_is_connected == "exit"):

                    step_response = "exit"
                    return

                while (how_device_is_connected != "bypass" and how_device_is_connected != "wire" and how_device_is_connected != "wifi"):
                    print(
                        "\nInvalid response - Neither 'Bypass', 'Wire', or 'WiFi' were entered.")

                    how_device_is_connected = input(
                        "\nIs the device bypassing the main router, wiring to a network device, or using Wi-Fi?\nEnter 'bypass', 'wire', or 'wifi' to respond: ").lower().strip()

                    if (how_device_is_connected == "exit"):

                        step_response = "exit"
                        return

                if (how_device_is_connected == "bypass"):
                    step_response_sentence += "\nDevice is bypassing the main router."

                elif (how_device_is_connected == "wire"):
                    step_response_sentence += "\nDevice is wiring to a network device."

                elif (how_device_is_connected == "wifi"):
                    name_of_wifi_network = input(
                        "\nWhat WiFi network is the device connected to?\nEnter name of WiFi network to respond: ").strip()
                    step_response_sentence += "\nConnected to SSID of: " + name_of_wifi_network

                is_internet_working = input(
                    "\nIs the internet working?\nEnter 'yes' or 'no' to respond: ").lower().strip()

                if (is_internet_working == "exit"):

                    step_response = "exit"
                    return

                while (is_internet_working != "yes" and is_internet_working != "no"):
                    print("\nInvalid response - 'yes' or 'no' was not entered.")

                    is_internet_working = input(
                        "\nIs the internet working?\nEnter 'yes' or 'no' to respond: ").lower().strip()

                    if (is_internet_working == "exit"):

                        step_response = "exit"
                        return

                # if yes, internet is working, add "Internet is working on the device." to ticket.
                if (is_internet_working == "yes"):

                    step_response_sentence += "\nInternet is working on a device."

                # if no, internet is not working, what's the IPv4 address?
                elif (is_internet_working == "no"):
                    device_ip_address = input(
                        "\nWhat's the device's IPv4 address? ").strip()
                    device_default_gateway = input(
                        "What's the device's default gateway address? ").strip()

                    step_response_sentence += "\nNo internet on device."
                    step_response_sentence += "\nIPv4 address: " + \
                        device_ip_address
                    step_response_sentence += "\nDefault Gateway: " + \
                        device_default_gateway

        def run_ping_tests():
            nonlocal step_response
            nonlocal step_response_sentence

            print("Enter 'exit' at any time to exit prompt.\n")
            print("\nNOTE:\nSpeeds are most accurate when bypassing the main router.\nIf main router can't be bypassed, wiring to a network device is second best.\nIf a device can't be wired at all, it's okay to use 5G WiFi or 2.4G if there's no 5G.\n\n")

            # Can a computer be used?
            can_be_used = input(
                "Can a computer be used?\nEnter 'yes' or 'no' to respond: ").lower().strip()

            if (can_be_used == "exit"):

                step_response = "exit"
                return

            while (can_be_used != "yes" and can_be_used != "no"):
                print("\nInvalid response - 'yes' or 'no' was not entered.")

                can_be_used = input(
                    "\nCan a computer be used?\nEnter “yes” or “no” to respond: ").lower().strip()

                if (can_be_used == "exit"):

                    step_response = "exit"
                    return

            # Find out how computer is connected
            if (can_be_used == "yes"):
                step_response_sentence = "Running ping tests on a computer."

                # How is the computer connected to the internet?
                how_computer_is_connected = input(
                    "\nIs the computer bypassing the main router, wiring to a network device, or using Wi-Fi?\nEnter 'bypass', 'wire', or 'wifi' to respond: ").lower().strip()

                if (how_computer_is_connected == "exit"):

                    step_response = "exit"
                    return

                while (how_computer_is_connected != "bypass" and how_computer_is_connected != "wire" and how_computer_is_connected != "wifi"):
                    print(
                        "\nInvalid response - Neither 'Bypass', 'Wire', or 'WiFi' were entered.")

                    how_computer_is_connected = input(
                        "\nIs the computer bypassing the main router, wiring to a network device, or using Wi-Fi?\nEnter 'bypass', 'wire', or 'wifi' to respond: ").lower().strip()

                    if (how_computer_is_connected == "exit"):

                        step_response = "exit"
                        return

                if (how_computer_is_connected == "bypass"):
                    step_response_sentence += "\nComputer is bypassing the main router."

                elif (how_computer_is_connected == "wire"):
                    step_response_sentence += "\nComputer is wiring to a network device."

                elif (how_computer_is_connected == "wifi"):
                    name_of_wifi_network = input(
                        "\nWhat WiFi network is the computer connected to?\nEnter name of WiFi network to respond: ").strip()
                    step_response_sentence += "\nConnected to SSID of: " + name_of_wifi_network

                # Run ping tests here

                print(
                    "\n\nEnter 'Done' to exit prompt and save ping statistics to ticket.\n")

                while (True):

                    host = input("\nWhat host is being pinged? ").strip()
                    if (host.lower() == "exit"):
                        step_response = "exit"
                        return
                    if (host.lower() == "done"):
                        return
                    step_response_sentence += "\n\nPinging Host: " + host

                    packets_sent = input(
                        "How many packets are being sent? ").strip()
                    if (packets_sent.lower() == "exit"):
                        step_response = "exit"
                        return
                    if (packets_sent.lower() == "done"):
                        return
                    step_response_sentence += "\nSent: " + packets_sent

                    packets_lost = input(
                        "How many packets were lost? ").strip()
                    if (packets_lost.lower() == "exit"):
                        step_response = "exit"
                        return
                    if (packets_lost.lower() == "done"):
                        return
                    step_response_sentence += "\nLost: " + packets_lost

                    min_value = input("What's the min ping speed? ").strip()
                    if (min_value.lower() == "exit"):
                        step_response = "exit"
                        return
                    if (min_value.lower() == "done"):
                        return
                    step_response_sentence += "\nMin: " + min_value

                    max_value = input("What's the max ping speed? ").strip()
                    if (max_value.lower() == "exit"):
                        step_response = "exit"
                        return
                    if (max_value.lower() == "done"):
                        return
                    step_response_sentence += "\nMax: " + min_value

                    avg_value = input("What's the avg ping speed? ").strip()
                    if (avg_value.lower() == "exit"):
                        step_response = "exit"
                        return
                    if (avg_value.lower() == "done"):
                        return
                    step_response_sentence += "\nAvg: " + avg_value

            if (can_be_used == "no"):
                step_response_sentence = "Can't run ping tests - No computer can be used."

        def run_speed_tests():
            nonlocal step_response
            nonlocal step_response_sentence

            print("Enter 'exit' at any time to exit prompt.\n")
            print("\nNOTE:\nSpeeds are most accurate when bypassing the main router.\nIf main router can't be bypassed, wiring to a network device is second best.\nIf a device can't be wired at all, it's okay to use 5G WiFi or 2.4G if there's no 5G.\n\n")

            # Can a computer be used?
            running_test_on_which_device = input(
                "Can a speed test be run on a computer or mobile device?\nEnter 'Computer', 'Mobile Device', or 'No' to respond: ").lower().strip()

            if (running_test_on_which_device == "exit"):

                step_response = "exit"
                return

            while (running_test_on_which_device != "computer" and running_test_on_which_device != "mobile device" and running_test_on_which_device != "no"):
                print(
                    "\nInvalid response - Neither 'Computer', 'Mobile Device', or 'No' were entered.")

                running_test_on_which_device = input(
                    "\nIs the speed test being run on a computer or mobile device?\nEnter 'Computer', 'Mobile Device', or 'No' to respond: ").lower().strip()

                if (running_test_on_which_device == "exit"):

                    step_response = "exit"
                    return

            # Find out how computer is connected
            if (running_test_on_which_device == "computer"):
                step_response_sentence = "Running speed tests on a computer."

                # How is the computer connected to the internet?
                how_computer_is_connected = input(
                    "\nIs the computer bypassing the main router, wiring to a network device, or using Wi-Fi?\nEnter 'bypass', 'wire', or 'wifi' to respond: ").lower().strip()

                if (how_computer_is_connected == "exit"):

                    step_response = "exit"
                    return

                while (how_computer_is_connected != "bypass" and how_computer_is_connected != "wire" and how_computer_is_connected != "wifi"):
                    print(
                        "\nInvalid response - Neither 'Bypass', 'Wire', or 'WiFi' were entered.")

                    how_computer_is_connected = input(
                        "\nIs the computer bypassing the main router, wiring to a network device, or using Wi-Fi?\nEnter 'bypass', 'wire', or 'wifi' to respond: ").lower().strip()

                    if (how_computer_is_connected == "exit"):

                        step_response = "exit"
                        return

                if (how_computer_is_connected == "bypass"):
                    step_response_sentence += "\nComputer is bypassing the main router."

                elif (how_computer_is_connected == "wire"):
                    step_response_sentence += "\nComputer is wiring to a network device."

                elif (how_computer_is_connected == "wifi"):
                    name_of_wifi_network = input(
                        "\nWhat WiFi network is the computer connected to?\nEnter name of WiFi network to respond: ").strip()
                    step_response_sentence += "\nConnected to SSID of: " + name_of_wifi_network

                # Run speed tests here

                print(
                    "\n\nEnter 'Done' to exit prompt and save speed test results to ticket.\n")

                while (True):

                    website = input(
                        "\nWhat website is the speed test being run from? ").strip()
                    if (website.lower() == "exit"):
                        step_response = "exit"
                        return
                    if (website.lower() == "done"):
                        return
                    step_response_sentence += "\n\nSpeed test: " + website

                    download = input(
                        "What's the download speed? ").strip()
                    if (download.lower() == "exit"):
                        step_response = "exit"
                        return
                    if (download.lower() == "done"):
                        return
                    step_response_sentence += "\nDownload: " + download

                    upload = input(
                        "What's the upload speed? ").strip()
                    if (upload.lower() == "exit"):
                        step_response = "exit"
                        return
                    if (upload.lower() == "done"):
                        return
                    step_response_sentence += "\nUpload: " + upload

                    ping = input("What's the ping speed? ").strip()
                    if (ping.lower() == "exit"):
                        step_response = "exit"
                        return
                    if (ping.lower() == "done"):
                        return
                    step_response_sentence += "\nPing: " + ping

                    jitter = input("What's the jitter speed? ").strip()
                    if (jitter.lower() == "exit"):
                        step_response = "exit"
                        return
                    if (jitter.lower() == "done"):
                        return
                    step_response_sentence += "\nJitter: " + jitter

            if (running_test_on_which_device == "mobile device"):
                step_response_sentence = "Running speed tests on a mobile device."

                name_of_wifi_network = input(
                    "\nWhat WiFi network is the mobile device connected to?\nEnter name of WiFi network to respond: ").strip()
                step_response_sentence += "\nConnected to SSID of: " + name_of_wifi_network

                # Run speed tests here

                print(
                    "\n\nEnter 'Done' to exit prompt and save speed test results to ticket.\n")

                while (True):

                    website = input(
                        "\nWhat website is the speed test being run from? ").strip()
                    if (website.lower() == "exit"):
                        step_response = "exit"
                        return
                    if (website.lower() == "done"):
                        return
                    step_response_sentence += "\n\nSpeed test: " + website

                    download = input(
                        "What's the download speed? ").strip()
                    if (download.lower() == "exit"):
                        step_response = "exit"
                        return
                    if (download.lower() == "done"):
                        return
                    step_response_sentence += "\nDownload: " + download

                    upload = input(
                        "What's the upload speed? ").strip()
                    if (upload.lower() == "exit"):
                        step_response = "exit"
                        return
                    if (upload.lower() == "done"):
                        return
                    step_response_sentence += "\nUpload: " + upload

                    ping = input("What's the ping speed? ").strip()
                    if (ping.lower() == "exit"):
                        step_response = "exit"
                        return
                    if (ping.lower() == "done"):
                        return
                    step_response_sentence += "\nPing: " + ping

                    jitter = input("What's the jitter speed? ").strip()
                    if (jitter.lower() == "exit"):
                        step_response = "exit"
                        return
                    if (jitter.lower() == "done"):
                        return
                    step_response_sentence += "\nJitter: " + jitter

            if (running_test_on_which_device == "no"):
                step_response_sentence = "Can't run speed tests - No computer or mobile device can be used."

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

        def check_battery_backup_power():

            nonlocal step_response
            nonlocal step_response_sentence

            print("Enter 'exit' at any time to exit prompt.\n")

            # Initial check of battery backup for power.

            battery_backup_has_power = input(
                "Does the battery backup have power? Enter “yes” or “no” to respond: ").lower().strip()

            if (battery_backup_has_power == "exit"):

                step_response = "exit"
                return

            while (battery_backup_has_power != "yes" and battery_backup_has_power != "no"):
                print("Invalid response - 'yes' or 'no' was not entered.")

                battery_backup_has_power = input(
                    "\nDoes the battery backup have power? Enter “yes” or “no” to respond: ").lower().strip()

                if (battery_backup_has_power == "exit"):

                    step_response = "exit"
                    return

            # If yes, battery backup has power, add "Battery backup has power." to ticket.

            if (battery_backup_has_power == "yes"):
                step_response_sentence = "Battery backup has power."
                self.ticket_status = "Problem not resolved yet.\nBattery backup has power, but internet hasn't worked yet."

            # If no, battery backup has no power, add "Battery backup has no power." to ticket.

            elif (battery_backup_has_power == "no"):
                step_response_sentence = "Battery backup has no power."

                can_plug_other_device_into_outlet = input(
                    "\nCan some device plug into the other port of the outlet used by the battery backup?\nEnter “yes” or “no” to respond: ").lower().strip()

                if (can_plug_other_device_into_outlet == "exit"):

                    step_response = "exit"
                    return

                while (can_plug_other_device_into_outlet != "yes" and can_plug_other_device_into_outlet != "no"):
                    print("\nInvalid response - 'yes' or 'no' was not entered.")

                    can_plug_other_device_into_outlet = input(
                        "\nCan some device plug into the other port of the outlet used by the battery backup?\nEnter “yes” or “no” to respond: ").lower().strip()

                    if (can_plug_other_device_into_outlet == "exit"):

                        step_response = "exit"
                        return

                if (can_plug_other_device_into_outlet == "yes"):

                    # if yes, a device can be plugged into the outlet, does the other device get power in the outlet next to battery backup?

                    other_device_getting_power = input(
                        "\nIs the other device getting power?\nEnter “yes” or “no” to respond: ").lower().strip()

                    if (other_device_getting_power == "exit"):

                        step_response = "exit"
                        return

                    while (other_device_getting_power != "yes" and other_device_getting_power != "no"):
                        print("\nInvalid response - 'yes' or 'no' was not entered.")

                        other_device_getting_power = input(
                            "\nIs the other device getting power?\nEnter “yes” or “no” to respond: ").lower().strip()

                        if (other_device_getting_power == "exit"):

                            step_response = "exit"
                            return

                    if (other_device_getting_power == "yes"):

                        # if yes, some other device is getting power in the outlet, add "Some other device is getting power in the same outlet used by battery backup." to ticket.
                        step_response_sentence += "\nSome other device is getting power in the same outlet used by battery backup."

                        # if yes, some other device is getting power in the outlet, can the battery backup be plugged into the other outlet port?

                        can_battery_backup_plug_into_other_port = input(
                            "\nCan the battery backup plug into the other outlet port?\nEnter “yes” or “no” to respond: ").lower().strip()

                        if (can_battery_backup_plug_into_other_port == "exit"):

                            step_response = "exit"
                            return

                        while (can_battery_backup_plug_into_other_port != "yes" and can_battery_backup_plug_into_other_port != "no"):
                            print(
                                "\nInvalid response - 'yes' or 'no' was not entered.")

                            can_battery_backup_plug_into_other_port = input(
                                "\nCan the battery backup plug into the other outlet port?\nEnter “yes” or “no” to respond: ").lower().strip()

                            if (can_battery_backup_plug_into_other_port == "exit"):

                                step_response = "exit"
                                return

                        # if yes, battery backup can be plugged into other outlet port, does the battery backup get power if it's plugged into the other outlet port?

                        if (can_battery_backup_plug_into_other_port == "yes"):

                            battery_backup_powered_in_other_port = input(
                                "\nIs the battery backup getting power in the outlet's other port?\nEnter “yes” or “no” to respond: ").lower().strip()

                            if (battery_backup_powered_in_other_port == "exit"):

                                step_response = "exit"
                                return

                            while (battery_backup_powered_in_other_port != "yes" and battery_backup_powered_in_other_port != "no"):
                                print(
                                    "\nInvalid response - 'yes' or 'no' was not entered.")

                                battery_backup_powered_in_other_port = input(
                                    "\nIs the battery backup getting power in the outlet's other port?\nEnter “yes” or “no” to respond: ").lower().strip()

                                if (battery_backup_powered_in_other_port == "exit"):

                                    step_response = "exit"
                                    return

                            # if yes, battery backup gets power from other outlet port, add "Battery backup gets power from other outlet port." to ticket
                            if (battery_backup_powered_in_other_port == "yes"):
                                step_response_sentence += "\nBattery backup gets power from outlet's other port."

                            # if no, battery backup does not get power from other outlet port, add "Battery backup does not get power from other outlet port." to ticket
                            elif (battery_backup_powered_in_other_port == "no"):
                                step_response_sentence += "\nBattery backup does not get power from outlet's other port."

                        if (can_battery_backup_plug_into_other_port == "no"):
                            step_response_sentence += "\nBattery backup cannot be plugged into outlet's other port."

                    # if no, some other device is not getting power in the outlet, add "Some other device is not getting power in the same outlet used by battery backup." to ticket.
                    elif (other_device_getting_power == "no"):
                        step_response_sentence += "\nSome other device is not getting power in the same outlet used by battery backup."

                # if no, no other device can be plugged into the outlet, add "No other device can be plugged into outlet"

                elif (can_plug_other_device_into_outlet == "no"):
                    step_response_sentence += "\nNo other device can be plugged into outlet."

                # If no, battery backup has no power, see if a nearby GFCI reset button can be pressed.

                can_nearby_gfci_reset_button_be_pressed = input(
                    "\nCan some nearby GFCI reset button be pressed?\nEnter “yes” or “no” to respond: ").lower().strip()

                if (can_nearby_gfci_reset_button_be_pressed == "exit"):

                    step_response = "exit"
                    return

                while (can_nearby_gfci_reset_button_be_pressed != "yes" and can_nearby_gfci_reset_button_be_pressed != "no"):
                    print("\nInvalid response - 'yes' or 'no' was not entered.")

                    can_nearby_gfci_reset_button_be_pressed = input(
                        "\nCan some nearby GFCI reset button be pressed?\nEnter “yes” or “no” to respond: ").lower().strip()

                    if (can_nearby_gfci_reset_button_be_pressed == "exit"):

                        step_response = "exit"
                        return

                if (can_nearby_gfci_reset_button_be_pressed == "yes"):

                    # If yes, a GFCI reset button can be pressed, does pressing the reset button give the battery backup power?
                    does_pressing_reset_give_power = input(
                        "\nDoes the battery backup have power after pressing the GFCI outlet's reset button?\nEnter “yes” or “no” to respond: ").lower().strip()

                    if (does_pressing_reset_give_power == "exit"):

                        step_response = "exit"
                        return

                    while (does_pressing_reset_give_power != "yes" and does_pressing_reset_give_power != "no"):
                        print("\nInvalid response - 'yes' or 'no' was not entered.")

                        does_pressing_reset_give_power = input(
                            "\nDoes the battery backup have power after pressing the GFCI outlet's reset button?\nEnter “yes” or “no” to respond: ").lower().strip()

                        if (does_pressing_reset_give_power == "exit"):

                            step_response = "exit"
                            return

                    if (does_pressing_reset_give_power == "yes"):

                        # if yes, pressing reset button gives battery backup power, add "Pressed GFCI reset button. > Battery backup has power." to ticket. DONE
                        step_response_sentence += "/nPressed GFCI reset button. > Battery backup has power."

                    elif (does_pressing_reset_give_power == "no"):

                        # if no, pressing reset button does not give battery backup power, add "Pressed GFCI reset button. > Battery backup still has no power." to ticket.
                        step_response_sentence += "\nPressed GFCI reset button. > Battery backup still has no power."

                        # if no, pressing reset button does not give battery backup power, see if battery backup can be wired to a working outlet.

                        can_battery_backup_wire_to_working_outlet = input(
                            "\nCan the battery backup be plugged into a working outlet?\nEnter “yes” or “no” to respond: ").lower().strip()

                        if (can_battery_backup_wire_to_working_outlet == "exit"):

                            step_response = "exit"
                            return

                        while (can_battery_backup_wire_to_working_outlet != "yes" and can_battery_backup_wire_to_working_outlet != "no"):
                            print(
                                "\nInvalid response - 'yes' or 'no' was not entered.")

                            can_battery_backup_wire_to_working_outlet = input(
                                "\nCan the battery backup be plugged into a working outlet?\nEnter “yes” or “no” to respond: ").lower().strip()

                            if (can_battery_backup_wire_to_working_outlet == "exit"):

                                step_response = "exit"
                                return

                        # if yes, does the battery backup have power after being wired to a working outlet?

                        if (can_battery_backup_wire_to_working_outlet == "yes"):

                            power_after_wiring_to_other_outlet = input(
                                "\nDoes the battery backup have power after wiring to a working outlet?\nEnter “yes” or “no” to respond: ").lower().strip()

                            if (power_after_wiring_to_other_outlet == "exit"):

                                step_response = "exit"
                                return

                            while (power_after_wiring_to_other_outlet != "yes" and power_after_wiring_to_other_outlet != "no"):
                                print(
                                    "\nInvalid response - 'yes' or 'no' was not entered.")

                                power_after_wiring_to_other_outlet = input(
                                    "\nDoes the battery backup have power after wiring to a working outlet?\nEnter “yes” or “no” to respond: ").lower().strip()

                                if (power_after_wiring_to_other_outlet == "exit"):

                                    step_response = "exit"
                                    return

                            if (power_after_wiring_to_other_outlet == "yes"):

                                # if yes, battery backup has power after wiring to working outlet, add "Battery backup has power after wiring to a working outlet." to ticket.
                                step_response_sentence += "\nBattery backup has power after wiring to a working outlet."

                            elif (power_after_wiring_to_other_outlet == "no"):

                                # if no, battery backup has no power after wiring to working outlet, add "Battery backup still has no power after wiring to a working outlet." to ticket.
                                step_response_sentence += "\nBattery backup still has no power after wiring to a working outlet."

                        elif (can_battery_backup_wire_to_working_outlet == "no"):

                            # if no, add "Battery backup can't be wired to working outlet." to ticket.
                            step_response_sentence += "\nBattery backup can't be wired to a working outlet."

                elif (can_nearby_gfci_reset_button_be_pressed == "no"):

                    # If no, a GFCI reset button cannot be pressed, add "No GFCI outlet reset button can be pressed." to ticket.
                    step_response_sentence += "\nNo GFCI outlet reset button can be pressed."

                    # if no, reset button can't be pressed, see if battery backup can be wired to a working outlet.

                    can_battery_backup_wire_to_working_outlet = input(
                        "\nCan the battery backup be plugged into a working outlet?\nEnter “yes” or “no” to respond: ").lower().strip()

                    if (can_battery_backup_wire_to_working_outlet == "exit"):

                        step_response = "exit"
                        return

                    while (can_battery_backup_wire_to_working_outlet != "yes" and can_battery_backup_wire_to_working_outlet != "no"):
                        print("\nInvalid response - 'yes' or 'no' was not entered.")

                        can_battery_backup_wire_to_working_outlet = input(
                            "\nCan the battery backup be plugged into a working outlet?\nEnter “yes” or “no” to respond: ").lower().strip()

                        if (can_battery_backup_wire_to_working_outlet == "exit"):

                            step_response = "exit"
                            return

                    # if yes, does the battery backup have power after being wired to a working outlet?

                    if (can_battery_backup_wire_to_working_outlet == "yes"):

                        power_after_wiring_to_other_outlet = input(
                            "\nDoes the battery backup have power after wiring to a working outlet?\nEnter “yes” or “no” to respond: ").lower().strip()

                        if (power_after_wiring_to_other_outlet == "exit"):

                            step_response = "exit"
                            return

                        while (power_after_wiring_to_other_outlet != "yes" and power_after_wiring_to_other_outlet != "no"):
                            print(
                                "\nInvalid response - 'yes' or 'no' was not entered.")

                            power_after_wiring_to_other_outlet = input(
                                "\nDoes the battery backup have power after wiring to a working outlet?\nEnter “yes” or “no” to respond: ").lower().strip()

                            if (power_after_wiring_to_other_outlet == "exit"):

                                step_response = "exit"
                                return

                        if (power_after_wiring_to_other_outlet == "yes"):

                            # if yes, battery backup has power after wiring to working outlet, add "Battery backup has power after wiring to a working outlet." to ticket.
                            step_response_sentence += "\nBattery backup has power after wiring to a working outlet."

                        elif (power_after_wiring_to_other_outlet == "no"):

                            # if no, battery backup has no power after wiring to working outlet, add "Battery backup still has no power after wiring to a working outlet." to ticket.
                            step_response_sentence += "\nBattery backup still has no power after wiring to a working outlet."

                    elif (can_battery_backup_wire_to_working_outlet == "no"):

                        # if no, add "Battery backup can't be wired to working outlet." to ticket.
                        step_response_sentence += "\nBattery backup can't be wired to a working outlet."

        if (step == "Check account status."):
            check_account_status()

        elif (step == "Check landline phone for dial tone."):
            check_landline_phone_for_dial_tone()

        elif (step == "Check status of all services."):
            check_status_of_all_services()

        elif (step == "Check each network device’s name, model, and lights."):
            check_each_network_device()

        elif (step == "Check cabling."):
            check_cabling()

        elif (step == "Check if cables are in the correct ports."):
            check_cable_ports()

        elif (step == "Check cable conditions."):
            check_cable_conditions()

        elif (step == "Power cycle all network devices."):
            power_cycle()

        elif (step == "Check network devices for internet."):
            check_network_devices_for_internet()

        elif (step == "Check a device for internet."):
            check_devices()

        elif (step == "Check ONT."):
            check_ont()

        elif (step == "Check ONT’s battery backup."):
            check_battery_backup()

        elif (step == "Check battery backup for power."):
            check_battery_backup_power()

        elif (step == "Run ping tests on a computer."):
            run_ping_tests()

        elif (step == "Run speed tests on a device."):
            run_speed_tests()

        # If exit is returned from any of the function calls, exit the loop without editing ticket content
        if (step_response == 'exit'):
            self.print_ticket_steps_and_questions()

            return

        # Add step_response_sentence in dictionary into a specific spot of ticket_content that's based off keys in ticket_content

        # Find last key in ticket_content
        for index, key in enumerate(self.ticket_content.keys()):
            # If current index in iteration is the last index in the list(ticket_content.keys()) list, assign last_key to value of key in current iteration
            if index + 1 == len(self.ticket_content.keys()):
                last_key = list(self.ticket_content.keys())[index]

        # If 'user' is not found in ticket_content, insert step after last key in ticket content.
        if (not "user" in list(self.ticket_content)):
            insert_at_index = list(
                self.ticket_content.keys()).index(last_key) + 1
        # If 'user' is found in ticket_content, insert step before 'user' key in ticket content.
        else:
            insert_at_index = list(self.ticket_content.keys()).index('user')

        # Assign ticket_content_items list to the keys and values of ticket_content dictionary
        ticket_content_items = list(self.ticket_content.items())
        # Insert key and step_response_sentence value into ticket_content_items at index of insert_at_index
        ticket_content_items.insert(
            insert_at_index, ("step_" + self.service + "_" + self.category + "_" + str(first_index) + "_" + str(second_index) + "_" + str(random.randrange(10000)) + "_" + step_response_sentence, step_response_sentence))
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

        ticket_content_list = list(self.ticket_content.values())

        print("\n")

        self.print_diagnostic_questions()

        print("\n\n")

        print("Enter 'exit' at any time to exit prompt.\n")

        first_index = 0
        second_index = None

        # While second_index is not an int and second_index is less than or greater than self.troubleshooting steps list, run the following code
        while (True):
            second_index = input(
                "\nSelect a question by entering the number next to it: ").strip()

            if (second_index.lower() == "exit"):
                self.print_ticket_steps_and_questions()
                return
            try:
                # Convert second_index, entered by user, into a number
                # Subtract 1 from entered number, since list actually counts from 0
                second_index = int(second_index) - 1
            except ValueError:
                print("Invalid response - a number was not entered.")
                continue
            try:
                # Associate first_index and second_index with question in self.diagnostic_questions
                question = self.diagnostic_questions[first_index][second_index]
            except IndexError:
                print(
                    "Invalid response - number entered does not correlate with a question.")
                continue
            if (second_index > len(self.diagnostic_questions[0])):
                print(
                    "Invalid response - number entered does not correlate with a question.")
                continue
            if (second_index + 1 <= 0):
                print(
                    "Invalid response - number entered does not correlate with a question.")
                continue
            break

        print("\n\n")

        # Find and execute relevant prompts for chosen question

        # Below are general internet question functions

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

        # Below are WiFi question functions

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

        def check_for_interference():

            nonlocal question_response
            nonlocal question_response_sentence

            print("Enter 'exit' at any time to exit prompt.\n")

            print("Are there any sources of interference like:\n\n")

            print(
                "Radios\nExtenders\nConcrete walls\nMetal ceilings\n\n")

            any_interference = input(
                "Enter 'yes' or 'no' to respond: ").lower().strip()

            if (any_interference == "exit"):

                question_response = "exit"
                return

            while (any_interference != "yes" and any_interference != "no"):

                print("Invalid response - 'yes' or 'no' was not entered.")

                any_interference = input(
                    "\nEnter 'yes' or 'no' to respond: ").lower().strip()

                if (any_interference == "exit"):

                    question_response = "exit"
                    return

            if (any_interference == "no"):

                question_response_sentence = "No sources of interference such as radios, extenders, concrete walls, or metal ceilings."

            elif (any_interference == "yes"):

                cause_of_interference = input(
                    "\nCould the interference be caused by a network device like a radio or extender?\nEnter 'yes' or 'no' to respond: ").lower().strip()

                if (cause_of_interference == "exit"):

                    question_response = "exit"
                    return

                while (cause_of_interference != "yes" and cause_of_interference != "no"):

                    print("\nInvalid response - 'yes' or 'no' was not entered.")

                    cause_of_interference = input(
                        "\nEnter 'yes' or 'no' to respond: ").lower().strip()

                    if (cause_of_interference == "exit"):

                        question_response = "exit"
                        return

                if (cause_of_interference == "no"):

                    interference_caused_by_other = input(
                        "\nWhat could be causing interference? ").strip()

                    if (interference_caused_by_other.lower() == "exit"):

                        question_response = "exit"
                        return

                    question_response_sentence = "Interference possibly caused by: " + \
                        interference_caused_by_other

                elif (cause_of_interference == "yes"):

                    question_response_sentence = "Interference possibly caused by a network device."

                    can_unplug_devices = input(
                        "\nCan the devices be unplugged from power? Enter 'yes' or 'no' to respond: ").lower().strip()

                    if (can_unplug_devices == "exit"):

                        question_response = "exit"
                        return

                    while (can_unplug_devices != "yes" and can_unplug_devices != "no"):

                        print("Invalid response - 'yes' or 'no' was not entered.")

                        can_unplug_devices = input(
                            "\nEnter 'yes' or 'no' to respond: ").lower().strip()

                        if (can_unplug_devices == "exit"):

                            question_response = "exit"
                            return

                    if (can_unplug_devices == "no"):
                        question_response_sentence += "\nNetwork device can't be unplugged from power."

                    if (can_unplug_devices == "yes"):

                        question_response_sentence += "\nUnplugged network device from power."

                        issue_fixed = input(
                            "\nIs the issue still happening? Enter 'yes', 'no', or 'maybe' to respond: ").lower().strip()

                        if (issue_fixed == "exit"):

                            question_response = "exit"
                            return

                        while (issue_fixed != "yes" and issue_fixed != "no" and issue_fixed != "maybe"):

                            print(
                                "Invalid response - Neither 'yes', 'no', or 'maybe' was entered.")

                            issue_fixed = input(
                                "\nEnter 'yes', 'no', or 'maybe' to respond: ").lower().strip()

                            if (issue_fixed == "exit"):

                                question_response = "exit"
                                return

                        if (issue_fixed == 'yes'):
                            question_response_sentence += "\nIssue is still happening."

                        elif (issue_fixed == 'no'):
                            question_response_sentence += "\nIssue is resolved."

                        elif (issue_fixed == 'maybe'):
                            question_response_sentence += "\nCan't determine whether issue is still happening or not."

        # Below are intermittent question functions

        def when_does_problem_happen():
            nonlocal question_response
            nonlocal question_response_sentence

            print("Enter 'exit' at any time to exit prompt.\n")

            when_problem_happens = input(
                "When is the problem typically happening? ").strip()

            if (when_problem_happens.lower() == "exit"):

                question_response = "exit"
                return

            question_response_sentence = "Problem typically happens: " + when_problem_happens

        def does_problem_happen_when_more_devices_online():
            nonlocal question_response
            nonlocal question_response_sentence

            print("Enter 'exit' at any time to exit prompt.\n")

            does_problem_happen_with_more_or_certain_devices = input(
                "Does power cycling the equipment temporarily resolve the problem?\nEnter 'more', 'certain', or 'no' to respond: ").lower().strip()

            if (does_problem_happen_with_more_or_certain_devices == "exit"):

                question_response = "exit"
                return

            while (does_problem_happen_with_more_or_certain_devices != "more" and does_problem_happen_with_more_or_certain_devices != "certain" and does_problem_happen_with_more_or_certain_devices != "no"):
                print(
                    "\nInvalid response - Neither 'yes', 'no', or 'sometimes' were entered.")

                does_problem_happen_with_more_or_certain_devices = input(
                    "\nDoes power cycling the equipment temporarily resolve the problem?\nEnter 'more', 'certain', or 'no' to respond: ").lower().strip()

                if (does_problem_happen_with_more_or_certain_devices == "exit"):

                    question_response = "exit"
                    return

            if (does_problem_happen_with_more_or_certain_devices == "more"):
                question_response_sentence = "Problem typically happens when more devices are online."

            elif (does_problem_happen_with_more_or_certain_devices == "certain"):

                certain_devices = input(
                    "\nWhat devices are online when the problem happens?\n").strip()

                if (certain_devices == "exit"):

                    question_response = "exit"
                    return
                question_response_sentence = "Problem typically happens when these devices are online: " + certain_devices

            elif (does_problem_happen_with_more_or_certain_devices == "no"):
                question_response_sentence = "Problem doesn't typically happen when more or certain devices are online."

        def does_power_cycling_help():
            nonlocal question_response
            nonlocal question_response_sentence

            print("Enter 'exit' at any time to exit prompt.\n")

            does_power_cycling_help = input(
                "Does power cycling the equipment temporarily resolve the problem?\nEnter 'yes', 'no', or 'sometimes' to respond: ").lower().strip()

            if (does_power_cycling_help == "exit"):

                question_response = "exit"
                return

            while (does_power_cycling_help != "yes" and does_power_cycling_help != "no" and does_power_cycling_help != "sometimes"):
                print(
                    "\nInvalid response - Neither 'yes', 'no', or 'sometimes' were entered.")

                does_power_cycling_help = input(
                    "\nDoes power cycling the equipment temporarily resolve the problem?\nEnter 'yes', 'no', or 'sometimes' to respond: ").lower().strip()

                if (does_power_cycling_help == "exit"):

                    question_response = "exit"
                    return

            if (does_power_cycling_help == "yes"):
                question_response_sentence = "Power cycling temporarily fixes the issue."

            elif (does_power_cycling_help == "no"):
                question_response_sentence = "Power cycling does not temporarily fix the issue."

            elif (does_power_cycling_help == "sometimes"):
                question_response_sentence = "Power cycling sometimes temporarily fixes the issue."

        def how_long_problem_lasts():
            nonlocal question_response
            nonlocal question_response_sentence

            print("Enter 'exit' at any time to exit prompt.\n")

            how_long_problem_lasts = input(
                "How long does the problem last? ").strip()

            if (how_long_problem_lasts.lower() == "exit"):

                question_response = "exit"
                return

            question_response_sentence = "Problem typically lasts for: " + how_long_problem_lasts

        # Below are for general internet questions

        if (question == "How long has this issue been happening for?"):
            happening_for()

        elif (question == "Were there any equipment changes or outside disturbances when the issue first started happening?"):
            recent_changes()

        # Below are for WiFi questions

        elif (question == "Is the router in a closed space?"):
            closed_space()

        elif (question == "Are there any sources of interference?"):
            check_for_interference()

        # Below are for intermittent questions

        elif (question == "When is the problem typically happening?"):
            when_does_problem_happen()

        elif (question == "Does the problem happen when more or only certain devices are online?"):
            does_problem_happen_when_more_devices_online()

        elif (question == "Does power cycling the equipment temporarily resolve the problem?"):
            does_power_cycling_help()

        elif (question == "How long does the problem typically last for?"):
            how_long_problem_lasts()

        # Executed anytime user enters 'exit' from within a function
        if (question_response == 'exit'):

            self.print_ticket_steps_and_questions()
            return

        # Add question_response_sentence in dictionary into a specific spot of ticket_content that's based off keys in ticket_content

        # Find last key in ticket_content
        for index, key in enumerate(self.ticket_content.keys()):
            # If current index in iteration is the last index in the list(ticket_content.keys()) list, assign last_key to value of key in current iteration
            if index + 1 == len(self.ticket_content.keys()):
                last_key = list(self.ticket_content.keys())[index]

        # If 'user' is not found in ticket_content, insert question after last key in ticket content.
        if (not "user" in list(self.ticket_content)):
            insert_at_index = list(
                self.ticket_content.keys()).index(last_key) + 1
        # If 'user' is found in ticket_content, insert question before 'user' key in ticket content.
        else:
            insert_at_index = list(self.ticket_content.keys()).index('user')

        # Assign ticket_content_items list to the keys and values of ticket_content dictionary
        ticket_content_items = list(self.ticket_content.items())
        # Insert key and question_response_sentence value into ticket_content_items at index of insert_at_index
        ticket_content_items.insert(
            insert_at_index, ("question_" + self.service + "_" + self.category + "_" + str(random.randrange(10000)) + "_" + question_response_sentence, question_response_sentence))
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

        ticket_content_list = list(self.ticket_content.values())

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

        line_to_insert = None

        # Until no exceptions are found, see if number is a valid number
        while (True):
            line_to_insert = input(
                "\nInsert custom line before which line number: ").strip()

            if (line_to_insert.lower() == "exit"):
                self.print_ticket_steps_and_questions()
                return
            try:
                # Convert whatever was typed in into an int. Subtract value by 1 since line numbers start at 0.
                line_to_insert = int(line_to_insert) - 1
            except ValueError:
                print("Invalid response - a number was not entered.")
                continue
            if (line_to_insert >= len(ticket_content_list)):
                print(
                    "Invalid response - number entered does not correlate with a line.")
                continue
            if (line_to_insert + 1 <= 0):
                print(
                    "Invalid response - number entered does not correlate with a line.")
                continue
            break

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

        system.clear_prompt_or_terminal()

        print("\n")

        # Output ticket with line numbers, so user knows which line to select
        print("Ticket:\n")
        print(self.print_ticket_with_line_numbers())

        print("\n\n")

        # Prompt user to choose which line from ticket to remove.
        print("Enter 'exit' at any time to exit prompt.")

        index_to_remove = None

        # Until no exceptions are found, see if number is a valid number
        while (True):
            index_to_remove = input(
                "\nSelect which line number to remove: ").strip()

            if (index_to_remove.lower() == "exit"):
                self.print_ticket_steps_and_questions()
                return
            try:
                # Convert prompted line number from a string to an int and subtract by 1 to get the correct index.
                index_to_remove = int(index_to_remove) - 1
            except ValueError:
                print("Invalid response - a number was not entered.")
                continue
            try:
                # Define the value from selected line to be removed
                value_to_remove = ticket_content_list[index_to_remove]
            except IndexError:
                print(
                    "Invalid response - number entered does not correlate with a line.")
                continue
            if (index_to_remove + 1 <= 0):
                print(
                    "Invalid response - number entered does not correlate with a line.")
                continue
            break

        # Loop through all keys and values in ticket_content
        for key, value in self.ticket_content.items():
            # if the current value is the same value from selected line number, assign current key to index_to_remove
            if value == value_to_remove:
                index_to_remove = key

        # Delete ticket_content's key_to_remove key
        del self.ticket_content[index_to_remove]

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
            "add step", "add question", "add line", "remove line", "toggle steps", "copy", "help", "main", "end"]

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

        # if user enters 'toggle steps', switch to viewing either recommended steps and all the steps, based off current self.toggle_steps value
        if (ticket_command_choice == 'toggle steps'):

            self.toggling_steps()

            print("\nNow showing " + self.toggle_steps.lower() + "!\n")

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
