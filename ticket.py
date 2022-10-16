# Copyright (c) <2022>, <Tai Jones>
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

import re


def setup_ticket():
    """
    Name: 
    setup_ticket

    When code is run: 
    After choosing to create a ticket.

    Purpose: 
    Prompt the user for contact and issue information.
    Add prompted information to an array.
    Repeat this process until all prompts are answered.

    Result: 
    An array containing all prompted contact and issue information is returned.
    """

    # Create an empty array, that will contain all prompted information
    base_ticket = []
    print("\nCreating a new ticket...\n")

    # Prompt the user for their name - Add user's name to array
    base_ticket.append(get_user())

    # Prompt the user for contact information - Add contact information to array
    print("Contact Information:")
    number = input("What's their callback number? ")
    name = input("Who is being helped? ")
    address = input("What's their address? ")
    print("")

    base_ticket.append(number)
    base_ticket.append(name)
    base_ticket.append(address)

    # Prompt user for issue information - Add issue information to array.
    print("Issue:")
    custom_issue = input("What do they need help with? ")
    print("")
    base_ticket.append(custom_issue)

    base_ticket.append(get_service())
    base_ticket.append(get_category())

    # Return array containing all contact and issue information.
    return base_ticket


def get_user():
    """
    Name: 
    get_user

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

        user = input("Who's creating this ticket? Enter first and last name. ")
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


def get_service():
    """
    Name: 
    get_service

    When code is run: 
    When setup_ticket function is called.

    Purpose: 
    Prompts the user for what service they're having issues with.
    While entered service does not match a predefined service from program, prompt user for service.

    Result: 
    Returns service enetered by user.
    """

    print("Service:")
    print("What service is being worked on?\n")

    # Prompts the user for what service they're having issues with.
    service = input(
        "Enter \"Fiber\", \"DSL\", \"Cable\", \"Fixed Wireless\", or \"N/A\". "
    ).lower()

    # While entered service does not match a predefined service from program, prompt user for service.
    while (service != "fiber") and (service != "dsl") and (
            service != "cable") and (service !=
                                     "fixed wireless") and (service != "n/a"):
        print("Please enter a valid service\n")
        service = input(
            "Enter \"Fiber\", \"DSL\", \"Cable\", \"Fixed Wireless\", or \"N/A\". "
        ).lower()

    # Return service enetered by user.
    print("")
    return service


def get_category():
    print("Category:")
    print("What category is being worked on?\n")

    category = input(
        "Enter \"General\", \"Connectivity\", \"Speed\", \"Intermittent Connectivity/Speed\", or \"N/A\". "
    ).lower()

    while (category != "general") and (category != "connectivity") and (
            category != "speed") and (
                category != "intermittent connectivity/speed") and (category !=
                                                                    "n/a"):
        print("Please enter a valid category\n")
        category = input(
            "Enter \"General\", \"Connectivity\", \"Speed\", \"Intermittent Connectivity/Speed\", or \"N/A\". "
        ).lower()

    return category


class Ticket():

    def __init__(self, user, number, name, address, custom_issue, service,
                 category):
        self.user = user
        self.name = name
        self.number = number
        self.address = address
        self.custom_issue = custom_issue
        self.service = service
        self.category = category
        self.isOnline = None

    def is_online_or_not(self):
        if (self.category == "intermittent connectivity/speed"):
            print("Is the internet online? \n")
            self.isOnline = input("Enter yes or no to respond. ").lower()
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
        if (self.service == "dsl"):
            print(self.service.upper() + " - " + self.category.title())
        else:
            print(self.service.title() + " - " + self.category.title())
        print("\n\n")

        print(self.user)

    def print_troubleshooting_steps(self):
        """
        Print all troubleshooting steps relevant to the service and category. 
        """

        print("Troubleshooting Steps:")

        fiber_connectivity = [
            "Check each network device’s name, model, and lights.",
            "Check a router for Wi-Fi.", "Check cabling.",
            "Check if cables are in the correct ports.",
            "Check cable conditions.", "Power cycle all network devices.",
            "Check each network device’s name, model, and lights.",
            "Check a device for internet.", "Check ONT",
            "Check ONT's battery backup", "Run ping tests on a computer."
        ]

        dsl_connectivity = [
            "Check if there’s a landline phone with dial tone.",
            "Check each network device’s name, model, and lights.",
            "Check a router for Wi-Fi.", "Check cabling.",
            "Check if cables are in the correct ports.",
            "Check cable conditions.", "Power cycle all network devices.",
            "Check each network device’s name, model, and lights.",
            "Check a device for internet.", "Run ping tests on a computer."
        ]

        cable_connectivity = [
            "Check each network device’s name, model, and lights.",
            "Check a router for Wi-Fi.", "Check cabling.",
            "Check if cables are in the correct ports.",
            "Check cable conditions.", "Power cycle all network devices.",
            "Check each network device’s name, model, and lights.",
            "Check a device for internet.", "Run ping tests on a computer."
        ]

        fixed_wireless_connectivity = [
            "Check each network device’s name, model, and lights.",
            "Check a router for Wi-Fi.", "Check cabling.",
            "Check if cables are in the correct ports.",
            "Check cable conditions.", "Power cycle all network devices.",
            "Check each network device’s name, model, and lights.",
            "Check a device for internet.", "Run ping tests on a computer."
        ]

        general_connectivity = [
            "Check each network device’s name, model, and lights.",
            "Check a router for Wi-Fi.", "Check cabling.",
            "Check if cables are in the correct ports.",
            "Check cable conditions.", "Power cycle all network devices.",
            "Check each network device’s name, model, and lights.",
            "Check a device for internet.", "Run ping tests on a computer."
        ]

        speed = [
            "Run speed tests on a device.",
            "Check each network device’s name, model, and lights.",
            "Check cabling.", "Check cable conditions.",
            "Power cycle all network devices.",
            "Check each network device’s name, model, and lights.",
            "Run speed tests on a device.", "Run ping tests on a computer."
        ]

        intermittent_connectivity_and_speed = [
            "Run speed tests on a device.", "Run ping tests on a computer.",
            "Check each network device’s name, model, and lights.",
            "Check cabling.", "Check cable conditions.",
            "Power cycle all network devices.",
            "Check each network device’s name, model, and lights.",
            "Run speed tests on a device.", "Run ping tests on a computer."
        ]

        # Connectivity Steps
        if (self.service == "dsl" and self.category == "connectivity") or (
                self.service == "dsl"
                and self.category == "intermittent connectivity/speed"
                and self.isOnline == "no"):
            for index, item in enumerate(dsl_connectivity):
                print(str(index + 1) + ". " + item)

        elif (self.service == "fiber" and self.category == "connectivity") or (
                self.service == "fiber"
                and self.category == "intermittent connectivity/speed"
                and self.isOnline == "no"):
            for index, item in enumerate(fiber_connectivity):
                print(str(index + 1) + ". " + item)

        elif (self.service == "cable" and self.category == "connectivity") or (
                self.service == "cable"
                and self.category == "intermittent connectivity/speed"
                and self.isOnline == "no"):
            for index, item in enumerate(cable_connectivity):
                print(str(index + 1) + ". " + item)

        elif (self.service == "fixed wireless"
              and self.category == "connectivity") or (
                  self.service == "fixed wireless"
                  and self.category == "intermittent connectivity/speed"
                  and self.isOnline == "no"):
            for index, item in enumerate(fixed_wireless_connectivity):
                print(str(index + 1) + ". " + item)

        # General Connectivity
        elif self.service == "n/a" and self.category == "connectivity":
            for index, item in enumerate(general_connectivity):
                print(str(index + 1) + ". " + item)

        # General Speed
        elif self.category == "speed":
            for index, item in enumerate(speed):
                print(str(index + 1) + ". " + item)

        # General Intermittent Connectivity/Speed
        elif self.category == "intermittent connectivity/speed" and self.isOnline == "yes":
            for index, item in enumerate(intermittent_connectivity_and_speed):
                print(str(index + 1) + ". " + item)

    def print_diagnostic_questions(self, service, category):
        """
        Print all diagnostic questions relevant to the service and category. 
        """

        internet_general_questions = [
            "Are any services still working? ",
            "Are all devices effected? If not, what is affected? ",
            "How long has issue been happening for? ",
            "Where there any equipment changes or outside disturbances like weather or maintenance when issue first started happening? "
        ]

        intermittent_questions = [
            "Is issue only happening during a certain time frame? If so, during what time(s)? ",
            "Is issue only happening when a certain device is online? If so, which device? ",
            "Is issue only happening when a lot of devices are online? ",
            "How long is internet affected for? ",
            "Does the equipment typically have to be powercycled to temporarily resolve the issue? ",
            "Do lights on the router look the same when internet disconnects? "
        ]

        dsl_questions = [
            "Are there any splitters on the wall jack? ",
            "Does the landline phone have dial tone? "
        ]

        wifi_questions = [
            "Is the router in a closed space like a closet, cabinet, entertainment center, kitchen/laundry room, or besides a phone’s base? ",
            "Are there sources of interference like radios, extenders, metal doors, or metal ceilings? "
        ]

        ticket_questions = []

        print("Diagnostic Questions:")

        if (service == "fiber") or (service == "dsl") or (
                service == "cable") or (service == "fixed wireless"):
            ticket_questions.append(internet_general_questions)
            ticket_questions.append(wifi_questions)
        if (service == "dsl"):
            ticket_questions.append(dsl_questions)
        if (category == "intermittent connectivity/speed"):
            ticket_questions.append(intermittent_questions)

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
            "Add Question – Add a diagnostic question to the ticket.",
            "Add Step – Add a troubleshooting step to the ticket.",
            "Add Line – Add a custom line of text and choose where to insert it.",
            "Add Category - Add a new service and/or category to the ticket.",
            "Remove Question – Remove a diagnostic question from the ticket.",
            "Remove Step – Remove a troubleshooting step from the ticket.",
            "Remove Line – Remove a custom line from the ticket.",
            "Remove Category - Remove a service and/or category from the ticket.",
            "Main - Return to the main menu.", "End – End the program."
        ]

        print("Options:")

        for option in options:
            print("• " + option)

    def generate_ticket_automator(self):
        print("\n\nGenerating Ticket Automator...\n\n")
        print("----------------------------------\n")

        self.print_ticket()

        print("\n----------------------------------\n\n")

        self.print_troubleshooting_steps()

        print("\n")

        self.print_diagnostic_questions(self.service, self.category)

        # print("\n")

        # self.print_options()
