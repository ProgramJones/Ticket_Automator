# Copyright (c) <2022>, <Tai Jones>
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

# TASKS

# - Ability to add steps and diagnostic questions to ticket
# Print steps and diagnostic questions
# ...

# Make print_options add all lines to a dictionary and then print those lines

# Compartmentalize print_troubleshooting_steps and print_diagnostic_questions

import re


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
            "How long has issue been happening for? ",
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
            "Are there any splitters on the wall jack? ",
            "Does the landline phone have dial tone? "
        ]
        self.wifi_questions = [
            "Is the router in a closed space like a closet, cabinet, entertainment center, kitchen/laundry room, or besides a phone’s base? ",
            "Are there sources of interference like radios, extenders, metal doors, or metal ceilings? "
        ]

    def setup_ticket(self):
        """
        Name: 
        setup_ticket

        Parameters:
        None

        When code is run: 
        After choosing to create a ticket.

        Purpose: 
        Prompt the user for their name, the contact information, and the issue information.
        Assigns what's entered into class isntance's respective attributes.

        Result: 
        number, name, address, custom_issue, service, and category attributes are overwritten.
        """

        print("\n\n-------------------------------------------\n\n")
        print("More information needed to create the ticket.\nPlease answer the following questions:")

        print("\n\n")

        # Prompt the user for their name - Assign user's name to class instance's attributes.
        self.user = self.get_user()

        print("\n\n")

        # Prompt the user for contact information - Assign contact information to class instance's attributes.
        print("Contact Information:")
        self.number = input("What's the best callback number? ")
        self.name = input("Who is being helped? ")
        self.address = input("What's their address? ")

        print("\n\n")

        # Prompt user for issue information - Assign issue information to class instance's attributes.
        print("Issue:")
        self.custom_issue = input("What's the Issue? ")

        print("\n\n")

        self.service = self.get_service()

        print("\n\n")

        self.category = self.get_category()

        print("\n\n")

        print("No further questions!")

    def get_user(self):
        """
        Name: 
        get_user

        Parameters:
        None

        When code is run: 
        When setup_ticket function is called.

        Purpose: 
        Prompts the user for their first and last name.

        Result: 
        Returns the user's name in format of first_name_initial + last_name.
        """

        user = input("Who's creating this ticket? Enter first and last name. ")

        # Find out if user entered at least two words.
        two_words = re.search(" {1}.+", user)

        # While user has not entered at least two words, prompt user to enter at least two words.
        while two_words == None:
            print("Enter a first and last name.\n")

            user = input(
                "Who's creating this ticket? Enter first and last name. ")
            two_words = re.search(" {1}.+", user)

        # Sepearte words entered by user, and assign them as names in an array called 'all_names'.
        all_names = re.split("\s", user)

        # Format names from all_names in format of first_name_initial + last_name + any_other_last_names
        signature = ""
        for index, name in enumerate(all_names):

            if index == 0:
                signature += name[0].lower()
            else:
                signature += name.title()
        return signature

    def get_service(self):
        """
        Name: 
        get_service

        Parameters:
        None

        When code is run: 
        When setup_ticket function is called.

        Purpose: 
        Prompts the user for what service they're having issues with.
        While entered service is not in the program's 'service' list, prompt user for service.

        Result: 
        Returns service entered by user.
        """

        print("Service:")
        print("Which of the following services is being worked on? \n")

        # Print all services.
        for item in self.services:
            for innerValue in item:
                print(innerValue)

        # Prompts the user for what service they're having issues with.
        service = input(
            "\nEnter a service from the above list, with correct casing: "
        )

        # While entered service is not in the program's 'service' list, prompt user for service.
        while (not any(service in x for x in self.services)):
            print("Please enter a valid service\n")
            service = input(
                "\nEnter a service from the above list, with correct casing: "
            )

        # Return service enetered by user.
        return service

    def get_category(self):
        """
        Name: 
        get_category

        Parameters:
        None

        When code is run: 
        When setup_ticket function is called.

        Purpose: 
        Prompts the user for what service category they're having issues with.
        While entered service category does not match a predefined service from program, prompt user for service.

        Result: 
        Returns service category entered by user.
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
            "\nEnter a category from the above list, with correct casing: "
        )

        # While entered service category does not match a predefined service from program, prompt user for service.
        while (category not in current_categories):
            print("Please enter a valid category\n")
            category = input(
                "\nEnter a category from the above list, with correct casing: "
            )

        # Return service category entered by user.
        return category

    def is_online_or_not(self):
        """
        Name: 
        is_online_or_not

        Parameters:
        None

        When code is run: 
        When generate_ticket_automator method is called.

        Purpose: 
        When category is Intermittent Connectivity/Speed, determine if internet is online or not.

        Result: 
        Re-assigns isOnline variable to 'yes' or 'no', when category is intermittent connectivity/speed.
        """

        # If category is intermittent connectivity/speed and if method hasn't been run before, run the following code...
        if (self.category == "Intermittent Connectivity/Speed") and (self.isOnline == None):

            # Prompt the user for network status.
            print("Is the internet online? \n")
            self.isOnline = input("Enter yes or no to respond. ").lower()

            # While response is not 'yes' or 'no', prompt user for network status.
            while (self.isOnline.lower() != "yes") and (self.isOnline.lower()
                                                        != "no"):
                print("Please enter a valid response.\n")
                self.isOnline = input("Enter yes or no to respond. ").lower()

    def print_ticket(self):
        """
        Print the most current ticket. 
        """
        print("cb: " + self.number)
        print("s/w: " + self.name)
        print("address: " + self.address)
        print("")

        print("Issue: " + self.custom_issue)
        print(self.service + " - " + self.category)

        print()

        print(self.user)

    def print_troubleshooting_steps(self):
        """
        Print all troubleshooting steps relevant to the service and category. 
        """

        print("Troubleshooting Steps:")

        # Connectivity Steps
        if (self.service == "DSL" and self.category == "Connectivity") or (
                self.service == "DSL"
                and self.category == "Intermittent Connectivity/Speed"
                and self.isOnline == "no"):
            for index, item in enumerate(self.dsl_connectivity_steps):
                print(str(index + 1) + ". " + item)

        elif (self.service == "Fiber" and self.category == "Connectivity") or (
                self.service == "Fiber"
                and self.category == "Intermittent Connectivity/Speed"
                and self.isOnline == "no"):
            for index, item in enumerate(self.fiber_connectivity_steps):
                print(str(index + 1) + ". " + item)

        elif (self.service == "Cable" and self.category == "Connectivity") or (
                self.service == "Cable"
                and self.category == "Intermittent Connectivity/Speed"
                and self.isOnline == "no"):
            for index, item in enumerate(self.cable_connectivity_steps):
                print(str(index + 1) + ". " + item)

        elif (self.service == "Fixed Wireless"
              and self.category == "Connectivity") or (
                  self.service == "Fixed Wireless"
                  and self.category == "Intermittent Connectivity/Speed"
                  and self.isOnline == "no"):
            for index, item in enumerate(self.fixed_wireless_connectivity_steps):
                print(str(index + 1) + ". " + item)

        # General Connectivity Steps
        elif self.service == "N/A" and self.category == "Connectivity":
            for index, item in enumerate(self.general_connectivity_steps):
                print(str(index + 1) + ". " + item)

        # General Speed Steps
        elif self.category == "Speed":
            for index, item in enumerate(self.speed_steps):
                print(str(index + 1) + ". " + item)

        # General Intermittent Connectivity/Speed Steps
        elif self.category == "Intermittent Connectivity/Speed" and self.isOnline == "yes":
            for index, item in enumerate(self.intermittent_connectivity_and_speed_steps):
                print(str(index + 1) + ". " + item)

    def print_diagnostic_questions(self, service, category):
        """
        Print all diagnostic questions relevant to the service and category. 
        """

        ticket_questions = []

        print("Diagnostic Questions:")

        if (service == "Fiber") or (service == "DSL") or (
                service == "Cable") or (service == "Fixed wireless"):
            ticket_questions.append(self.internet_general_questions)
            ticket_questions.append(self.wifi_questions)
        if (service == "DSL"):
            ticket_questions.append(self.dsl_questions)
        if (category == "Intermittent Connectivity/Speed"):
            ticket_questions.append(self.intermittent_questions)

        count = 1
        for list in ticket_questions:
            for item in list:
                print(str(count) + ". " + item)
                count += 1

    def print_options(self):
        """
        Print all options available for editing the ticket.
        """

        options = [
            "Add Question - Add a diagnostic question to the ticket.",
            "Add Step - Add a troubleshooting step to the ticket.",
            "Add Line - Add a custom line of text and choose where to insert it.",
            "Add Category - Add a new service and/or category to the ticket.",
            "Remove Question - Remove a diagnostic question from the ticket.",
            "Remove Step - Remove a troubleshooting step from the ticket.",
            "Remove Line - Remove a custom line from the ticket.",
            "Remove Category - Remove a service and/or category from the ticket.",
            "Main - Return to the main menu.", "End - End the program."
        ]

        print("Options:")

        for option in options:
            print("• " + option)

    def print_ticket_steps_questions_and_options(self):

        self.is_online_or_not()

        print("\n\n----------------------------------\n\n")

        print("Ticket:\n")

        self.print_ticket()

        print("\n\n")

        self.print_troubleshooting_steps()

        print("\n\n")

        self.print_diagnostic_questions(self.service, self.category)

        # print("\n")

        # self.print_options()
