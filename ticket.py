# Copyright (c) <2022>, <Tai Jones>
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

import os
import re
import time
import itertools
import random
import ipaddress
import pyperclip
import system
import main_menu


class Ticket():

    def __init__(self):
        # * Variables assigned in 'setup_ticket' method
        self.user = None
        self.name = None
        self.number = None
        self.address = None
        self.custom_issue = None
        self.services = None
        self.category = None

        # * Contains everything printed to ticket
        self.ticket_content = {}

        # * Variables containing troubleshooting steps and questions
        self.recommended_troubleshooting_steps = []
        self.troubleshooting_steps = []
        self.diagnostic_questions = []

        # * Contains all the network devices from check_each_network_device
        self.network_devices = {}

        # Possible values: Recommended Steps | All Steps
        self.toggle_steps = "Recommended Steps"

        # * Provides updates and hints to user depending on responses to prompts. (Only for recommended steps)
        self.ticket_status = "Ticket Status: Problem not resolved yet."

        # * Variables specifying whether methods can be run | Possible values: "yes", "no"
        self.can_check_landline = None
        self.can_check_network_device_lights = None
        self.can_check_cabling = None
        self.can_check_ont = None

        # * Assigned in "check_account_status"
        self.account_status = None  # Possible values: "online", "offline", or "n/a"

        # * Assigned in "Check status of all services." - All additional steps branch off from these attributes
        self.devices_online = None  # Possible values: True or False
        self.devices_offline = None
        self.all_services_offline = None  # Possible values: True or False | Boolean
        self.some_services_offline = None  # Possible values: True or False | Boolean
        self.only_service_offline = None  # Possible values: True or False | Boolean

        # * Assigned in 'check_landline_phone_for_dial_tone'
        self.landline_has_dial_tone = None

        # * Assigned in 'check_cabling'
        self.cables_in_correct_ports = None  # Possible values: True or False
        self.good_cable_conditions = None  # Possible values: "yes", "no", or "n/a"

        # Possible values: "yes", "no"
        self.power_cycled = None

        # * Assigned in 'check_battery_backup'
        # Possible values: 'on', 'off', 'n/a'
        self.battery_backup_status = None
        # Possible values: True or False
        self.battery_backup_fixed = None

        # Possible values: "online", "offline", or "n/a"
        self.ont_status = None

        # * Variables assigned in 'check_network_devices_for_internet' function
        # Atrributes are assigned in this format:
        # - {"device": brand_and_model, "device_type": device_type, "status": online_offline_or_na, "provided_by": device_provided_by, "can_bypass": ""}
        # Possible status values:
        # - "online", "offline", "n/a" | Possible provided_by values: "service provider", "third party" | Possible can_we_bypass values: "yes" or "no"
        self.indoor_ont = {"device": "", "device_type": "",
                           "status": "", "provided_by": "", "can_bypass": ""}
        self.ont_router = {"device": "", "device_type": "",
                           "status": "", "provided_by": "", "can_bypass": ""}
        self.modem = {"device": "", "device_type": "",
                      "status": "", "provided_by": "", "can_bypass": ""}
        self.modem_router = {"device": "", "device_type": "",
                             "status": "", "provided_by": "", "can_bypass": ""}
        self.main_router = {"device": "", "device_type": "",
                            "status": "", "provided_by": "", "can_bypass": ""}
        # Atrributes are appended in this format:
        # - {"device": brand_and_model, "device_type": device_type, "status": online_offline_or_na, "provided_by": device_provided_by, "can_bypass": ""}
        # Possible status values:
        # - "online", "offline", "n/a" | Possible provided_by values: "service provider", "third party" | Possible can_we_bypass values: "yes" or "no"
        self.additional_routers = []
        self.extenders = []
        self.switches = []

        # Possible values: "yes", "no"
        self.can_bypass_or_wire = ""
        # Possible values: True or False
        self.can_bypass_main_router = False
        self.can_wire_to_network_device = False
        self.can_wire_to_wall_jack = False

        # * Assigned in 'check_devices' | Possible values: True or False
        self.last_checked_device_is_online = None
        self.last_checked_device_was_given_ip = None

        # The wall jack or network devices where the internet first comes into
        self.possible_main_network_devices = [
            self.indoor_ont, self.ont_router, self.modem, self.modem_router, self.main_router]
        # The wall jack or network devices that the main network device sends internet to
        self.possible_additional_network_devices = [
            self.main_router, self.additional_routers, self.extenders]

        self.names_of_possible_places_to_wire_devices_for_fiber = [
            "Wall Jack", "Indoor ONT", "ONT/Router", "Main Router", "Additional Router", "Extender", "Switch"]
        self.names_of_possible_places_to_wire_devices_for_non_fiber = [
            "Wall Jack", "Modem", "Modem/Router", "Main Router", "Additional Router", "Extender", "Switch"]

        # # Network devices that can be paired
        # self.pairable_network_devices = [
        #     "main router", "additional router", "extender"]

        # * Variables assigned during 'run_ping_tests"
        self.significant_packet_loss = False
        self.significant_latency = False

        self.internet_services = ["Fiber", "DSL", "Cable", "Fixed Wireless"]
        self.services = [self.internet_services, ["Email"], ["TV"], ["N/A"]]

        self.internet_categories = [
            "General", "Connectivity", "Speed", "Intermittent Connectivity/Speed"]
        self.email_categories = ["General", "Setup", "Configuration"]
        self.tv_categories = ["General"]

        self.fiber_connectivity_steps = [
            "Check account status.",
            "Check landline phone for dial tone.",
            "Check status of all services.",
            "Check each network device's name, model, and lights.",
            "Check cabling.", "Power cycle all network devices.", "Check ONT.",
            "Check ONT's battery backup.",
            "Check each network device's name, model, and lights.",
            "Check network devices for internet.", "Check a device for internet.",  "Run ping tests on a computer."
        ]
        self.dsl_connectivity_steps = [
            "Check account status.",
            "Check landline phone for dial tone.",
            "Check status of all services.",
            "Check each network device's name, model, and lights.",
            "Check cabling.", "Power cycle all network devices.",
            "Check each network device's name, model, and lights.",
            "Check network devices for internet.", "Check a device for internet.", "Run ping tests on a computer."
        ]
        self.cable_connectivity_steps = [
            "Check account status.",
            "Check status of all services.",
            "Check each network device's name, model, and lights.",
            "Check cabling.", "Power cycle all network devices.",
            "Check each network device's name, model, and lights.",
            "Check network devices for internet.", "Check a device for internet.", "Run ping tests on a computer."
        ]
        self.fixed_wireless_connectivity_steps = [
            "Check account status.",
            "Check status of all services.",
            "Check each network device's name, model, and lights.",
            "Check cabling.", "Power cycle all network devices.",
            "Check each network device's name, model, and lights.",
            "Check network devices for internet.", "Check a device for internet.", "Run ping tests on a computer."
        ]
        self.general_connectivity_steps = [
            "Check account status.",
            "Check status of all services.",
            "Check each network device's name, model, and lights.",
            "Check cabling.", "Power cycle all network devices.",
            "Check each network device's name, model, and lights.",
            "Check network devices for internet.", "Check a device for internet.", "Run ping tests on a computer."
        ]
        self.speed_steps = [
            "Run speed tests on a device.",
            "Check each network device's name, model, and lights.",
            "Check cabling.",
            "Power cycle all network devices.",
            "Check each network device's name, model, and lights.",
            "Check network devices for internet.", "Check a device for internet.",
            "Run speed tests on a device.", "Run ping tests on a computer."
        ]
        self.intermittent_connectivity_and_speed_steps = [
            "Check status of all services.", "Run speed tests on a device.", "Run ping tests on a computer.",
            "Check each network device's name, model, and lights.",
            "Check cabling.",
            "Power cycle all network devices.",
            "Check each network device's name, model, and lights.",
            "Check network devices for internet.", "Check a device for internet.",
            "Run speed tests on a device.", "Run ping tests on a computer."
        ]
        self.dsl_intermittent_connectivity_and_speed_steps = [
            "Check status of all services.",
            "Check landline phone for dial tone.",
            "Run speed tests on a device.", "Run ping tests on a computer.",
            "Check each network device's name, model, and lights.",
            "Check cabling.",
            "Power cycle all network devices.",
            "Check each network device's name, model, and lights.",
            "Check network devices for internet.", "Check a device for internet.",
            "Run speed tests on a device.", "Run ping tests on a computer."
        ]
        self.fiber_intermittent_connectivity_and_speed_steps = [
            "Check status of all services.",
            "Check landline phone for dial tone.",
            "Run speed tests on a device.", "Run ping tests on a computer.",
            "Check each network device's name, model, and lights.",
            "Check cabling.",
            "Power cycle all network devices.",
            "Check ONT.",
            "Check ONT's battery backup.",
            "Check each network device's name, model, and lights.",
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

        def print_ticket_preview(**kwargs):
            system.clear_prompt_or_terminal()

            print("\nTicket Preview:\n")

            if (len(kwargs) == 0):
                pass
            else:
                for key, value in kwargs.items():
                    if (key == "number"):
                        print("cb: " + value)
                    elif (key == "name"):
                        print("s/w: " + value)
                    elif (key == "address"):
                        print("address: " + value)
                    elif (key == "user" or key == "custom_issue"):
                        print("\n" + value)

            print("\n----------------------------------\n\n\n")

            if (self.category == None):
                print("Answer the following questions to create the ticket:\n\n\n")

                # if user is about to enter callback number
                if (len(kwargs) == 1):
                    print("Contact Information:")
                # if user already entered the callback number
                if (len(kwargs) == 2):
                    print("Contact Information:")
                    print("What's the best callback number? " + self.number)
                # if user already entered the callback number and name
                if (len(kwargs) == 3):
                    print("Contact Information:")
                    print("What's the best callback number? " + self.number)
                    print("Who is being helped? " + self.name)
            else:
                print("All questions answered!\n\n\n")

        # Clear prompt and show ticket preview
        print_ticket_preview()

        # Prompt the user for their name - Assign user's name to class instance's attributes.
        self.user = self.set_user()

        # Clear prompt, append user to ticket preview, and ask for number
        print_ticket_preview(user=self.user)

        # Prompt the user for contact information - Assign contact information to class instance's attributes.
        self.number = input("What's the best callback number? ").strip()

        print_ticket_preview(number=self.number, user=self.user)

        self.name = input("Who is being helped? ").strip()

        print_ticket_preview(number=self.number,
                             name=self.name, user=self.user)

        self.address = input("What's their address? ").strip()

        print_ticket_preview(number=self.number, name=self.name,
                             address=self.address, user=self.user)

        # Append number, name, and address key and values to ticket_content
        self.ticket_content.update({"number": "cb: " + self.number})
        self.ticket_content.update({"name": "s/w: " + self.name})
        self.ticket_content.update({"address": "address: " + self.address})

        # Prompt user for issue information - Assign issue information to class instance's attributes.
        print("Issue:")
        self.custom_issue = input("What's the Issue? ").strip()

        print_ticket_preview(number=self.number, name=self.name,
                             address=self.address, custom_issue=self.custom_issue, user=self.user)

        # Append custom issue key and value to ticket_content
        self.ticket_content.update({"custom_issue": self.custom_issue})

        self.service = self.set_service()

        print_ticket_preview(number=self.number, name=self.name,
                             address=self.address, custom_issue=self.custom_issue, user=self.user)

        self.category = self.set_category()

        # self.set_are_devices_online()
        self.set_troubleshooting_steps()
        self.set_diagnostic_questions()

        # Append user key and value to end of ticket_content
        self.ticket_content.update({"user": self.user})

        print_ticket_preview(number=self.number, name=self.name,
                             address=self.address, custom_issue=self.custom_issue, user=self.user)

        print("Service: " + self.service + " | Category: " + self.category)
        print("Outputting ticket, ticket status, troubleshooting steps, and diagnostic questions.",
              end="", flush=True)

        time.sleep(.70)
        print(".", end="", flush=True)

        time.sleep(.70)
        print(".", end="", flush=True)

        time.sleep(.70)

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

        # Used to add steps or edit ticket status based off network device status combinations
        def determine_steps_after_checking_network_devices_for_internet():

            # If user can connect over WiFi or ETH | If main router is online
            if (self.can_bypass_or_wire == True or self.main_router["status"] == "online"):

                self.recommended_troubleshooting_steps[0].append(
                    "Check a device for internet.")

        def determine_steps_when_device_ip_is_valid_but_theres_no_internet():
            # END of branch - If checked device has no valid IP - If no other device is online
            if (self.last_checked_device_was_given_ip != False and self.devices_online == False and self.last_checked_device_is_online == False):
                self.ticket_status = "Ticket Status: Problem not resolved yet.\nAt least one device has a valid IP, but there's still no internet."
                self.recommended_troubleshooting_steps[0].append(
                    "Run ping tests on a computer.")

        # Connectivity Steps

        # If current service is DSL and category is Connectivity, assign self.troubleshooting_steps to value of self.dsl_connectivity_steps
        if (self.service == "DSL" and self.category == "Connectivity"):
            self.troubleshooting_steps.append(self.dsl_connectivity_steps)

        # If current service is Fiber and category is Connectivity, assign self.troubleshooting_steps to value of self.fiber_connectivity_steps
        elif (self.service == "Fiber" and self.category == "Connectivity"):

            # If user is viewing all steps ...
            if (self.toggle_steps == "All Steps"):
                self.troubleshooting_steps.append(
                    self.fiber_connectivity_steps)

            # If user is viewing recommended steps ...
            elif (self.toggle_steps == "Recommended Steps"):

                if (len(self.recommended_troubleshooting_steps) == 0):
                    self.recommended_troubleshooting_steps.append(
                        ["Check account status."])

                elif ((self.account_status == "online" or self.account_status == "n/a") and (len(self.recommended_troubleshooting_steps[0]) == 1)):
                    self.recommended_troubleshooting_steps[0].append(
                        "Check status of all services.")

                # If some devices are online and others are offline ...
                # - Branching from the 'check_status_of_all_services' function
                elif (self.devices_online == True and self.devices_offline == True):

                    # END of branch - self.ticket_status assigned in 'check_status_of_all_services'

                    if (len(self.recommended_troubleshooting_steps[0]) == 2):
                        self.recommended_troubleshooting_steps[0].append(
                            "Check a device for internet.")

                # If all services are offline ...
                # - Branching from the 'check_status_of_all_services' function
                # - Could be renamed internet_and_phone_offline
                elif (self.all_services_offline == True):

                    # Add logic:
                    # All services are only offline and internet and landline service are offline, and landline wires to wall jack
                    #
                    # Below conditions for when wall jack > phone

                    # self.ticket_status assigned in 'check_status_of_all_services'

                    # Chech landline for dial tone
                    if (len(self.recommended_troubleshooting_steps[0]) == 2):
                        self.recommended_troubleshooting_steps[0].append(
                            "Check landline phone for dial tone.")

                    # Check ONT and battery backup
                    elif (len(self.recommended_troubleshooting_steps[0]) == 3 and self.can_check_landline != None):
                        self.recommended_troubleshooting_steps[0].append(
                            "Check ONT.")
                        self.recommended_troubleshooting_steps[0].append(
                            "Check ONT's battery backup.")

                    # END of branch - If attempted checking ONT and battery backup wouldn't get power ...
                    elif (self.can_check_ont != None and self.battery_backup_status == "off"):
                        self.ticket_status = "Ticket Status: Problem should be referred to the service provider's main office.\nThe internet, landline, and battery backup are offline."

                    # END of branch - If attempted checking ONT and battery backup couldn't be checked ...
                    elif (self.can_check_ont != None and self.battery_backup_status == "n/a"):
                        self.ticket_status = "Ticket Status: Problem should be referred to the service provider's main office.\nThe internet and landline are offline. Battery backup may be offline."

                    # If attempted checking ONT and turned on battery backup power ...
                    elif (self.can_check_ont != None and self.battery_backup_fixed == True):
                        self.ticket_status = "Ticket Status: Problem not resolved yet.\nBattery backup has power now, but landline hasn't been checked again."

                        if (len(self.recommended_troubleshooting_steps[0]) == 5):
                            self.recommended_troubleshooting_steps[0].append(
                                "Check landline phone for dial tone.")

                        # If landline still has no dial tone ...
                        elif (self.landline_has_dial_tone == "no"):

                            if (len(self.recommended_troubleshooting_steps[0]) == 6):
                                self.ticket_status = "Ticket Status: Problem should be referred to the service provider's main office.\nThe internet and landline are offline, even after giving the battery backup power."

                        # If landline has dial tone ...
                        elif (self.landline_has_dial_tone == "yes"):
                            self.ticket_status = "Ticket Status: Problem not resolved yet.\nLandline has dial tone, but no device has been checked for internet."

                            if (len(self.recommended_troubleshooting_steps[0]) == 6):
                                self.recommended_troubleshooting_steps[0].append(
                                    "Check a device for internet.")

                            # END OF BRANCH - If a device has internet ...
                            elif (self.devices_online == True):
                                self.ticket_status = "Ticket Status: Problem resolved.\nInternet and landline are back online."

                            # If a device has no internet ...
                            elif (self.devices_online == False):

                                if (len(self.recommended_troubleshooting_steps[0]) == 7):
                                    self.ticket_status = "Ticket Status: Problem not resolved yet.\nLandline has dial tone, but internet is still offline. Network devices haven't been checked yet."

                                    self.recommended_troubleshooting_steps[0].append(
                                        "Check each network device's name, model, and lights.")
                                    self.recommended_troubleshooting_steps[0].append(
                                        "Check cabling.")

                                # if cables in wrong ports can't be moved ...
                                elif (self.cables_in_correct_ports == False):
                                    self.ticket_status = "Ticket Status: Problem can't be resolved right now.\nCables can't be switched to the correct ports."

                                # If checked network devices and cabling
                                elif (self.can_check_cabling != None and self.can_check_network_device_lights != None):

                                    if (len(self.recommended_troubleshooting_steps[0]) == 9):
                                        self.ticket_status = "Ticket Status: Problem not resolved yet.\nAttempted to check network devices and cabling, but devices haven't been power cycled yet."

                                        self.recommended_troubleshooting_steps[0].append(
                                            "Power cycle all network devices.")

                                    elif (self.power_cycled == "yes"):

                                        if (len(self.recommended_troubleshooting_steps[0]) == 10):
                                            self.ticket_status = "Ticket Status: Problem not resolved yet.\nPower cycled network devices, but network devices have to be checked again."

                                            self.recommended_troubleshooting_steps[0].append(
                                                "Check each network device's name, model, and lights.")
                                            self.recommended_troubleshooting_steps[0].append(
                                                "Check network devices for internet.")

                                        # END of branch - Condition after step to check network devices is added ...
                                        elif (len(self.recommended_troubleshooting_steps[0]) == 12):

                                            determine_steps_after_checking_network_devices_for_internet()

                                        # END of branch - Condition after step to check devices is added ...
                                        elif (len(self.recommended_troubleshooting_steps[0]) == 13):

                                            determine_steps_when_device_ip_is_valid_but_theres_no_internet()

                                    elif (self.power_cycled == "no"):

                                        if (len(self.recommended_troubleshooting_steps[0]) == 10):
                                            self.ticket_status = "Ticket Status: Problem not resolved yet.\nNetwork devices couldn't be power cycled, but maybe they can be checked for internet."

                                            self.recommended_troubleshooting_steps[0].append(
                                                "Check network devices for internet.")

                                        # END of branch - Condition after step to check network devices is added ...
                                        elif (len(self.recommended_troubleshooting_steps[0]) == 11):

                                            determine_steps_after_checking_network_devices_for_internet()

                                        # END of branch - Condition after step to check devices is added ...
                                        elif (len(self.recommended_troubleshooting_steps[0]) == 12):

                                            determine_steps_when_device_ip_is_valid_but_theres_no_internet()

                # If either some or the only service is offline ...
                # Branching from the 'check_status_of_all_services' function
                elif ((self.some_services_offline == True or self.only_service_offline == True)):

                    # self.ticket_status assigned in 'check_status_of_all_services'

                    if (len(self.recommended_troubleshooting_steps[0]) == 2):
                        self.recommended_troubleshooting_steps[0].append(
                            "Check each network device's name, model, and lights.")
                        self.recommended_troubleshooting_steps[0].append(
                            "Check cabling.")

                    # if cables in wrong ports can't be moved ...
                    elif (self.cables_in_correct_ports == False):
                        self.ticket_status = "Ticket Status: Problem can't be resolved right now.\nCables can't be switched to the correct ports."

                    elif (len(self.recommended_troubleshooting_steps[0]) == 4):

                        # If attempted to check network devices and cabling ...
                        if (self.can_check_cabling != None and self.can_check_network_device_lights != None):
                            self.ticket_status = "Ticket Status: Problem not resolved yet.\nAttempted to check cabling, but network devices haven't been power cycled."

                            self.recommended_troubleshooting_steps[0].append(
                                "Power cycle all network devices.")

                    # If ONT status unknown ...
                    elif (self.only_service_offline == True):

                        # Branching from the 'power_cycle' function - If no equipment could be power cycled ...
                        if (self.power_cycled == "no"):

                            if (len(self.recommended_troubleshooting_steps[0]) == 5):
                                # Might be better to see if we can bypass, and only check the ONT if we can't bypass
                                self.ticket_status = "Ticket Status: Problem not resolved yet.\nNetwork devices couldn't be power cycled, but maybe the ONT and battery backup can be checked."

                                self.recommended_troubleshooting_steps[0].append(
                                    "Check ONT.")
                                self.recommended_troubleshooting_steps[0].append(
                                    "Check ONT's battery backup.")

                            # END of branch - If attempted checking ONT and battery backup wouldn't get power ...
                            elif (self.can_check_ont != None and self.battery_backup_status == "off"):
                                self.ticket_status = "Ticket Status: Problem should be escalated to a higher level.\nThe battery backup box has no power even after troubleshooting it."

                            # If attempted checking ONT and battery backup power status is on/unknown ...
                            elif (self.can_check_ont != None and (self.battery_backup_status == "on" or self.battery_backup_status == "n/a")):

                                if (len(self.recommended_troubleshooting_steps[0]) == 7):
                                    self.ticket_status = "Ticket Status: Problem not resolved yet.\nThe ONT might be working fine, but network devices haven't been checked for internet."

                                    self.recommended_troubleshooting_steps[0].append(
                                        "Check network devices for internet.")

                                # Condition after step to check network devices is added ...
                                elif (len(self.recommended_troubleshooting_steps[0]) == 8):

                                    determine_steps_after_checking_network_devices_for_internet()

                                # Condition after step to check devices is added ...
                                elif (len(self.recommended_troubleshooting_steps[0]) == 9):

                                    determine_steps_when_device_ip_is_valid_but_theres_no_internet()

                        # Branching from the 'power_cycle' function - If equipment could be power cycled ...
                        elif (self.power_cycled == "yes"):

                            if (len(self.recommended_troubleshooting_steps[0]) == 5):
                                self.ticket_status = "Ticket Status: Problem not resolved yet.\nEquipment power cycled, but network devices haven't been checked for internet."

                                self.recommended_troubleshooting_steps[0].append(
                                    "Check each network device's name, model, and lights.")
                                self.recommended_troubleshooting_steps[0].append(
                                    "Check network devices for internet.")

                            # If main router offline ...
                            elif (self.main_router["status"] == "offline"):

                                if (len(self.recommended_troubleshooting_steps[0]) == 7):
                                    self.ticket_status = "Ticket Status: Problem not resolved yet.\nMain network device is offline, so ONT and battery backup should be checked."

                                    self.recommended_troubleshooting_steps[0].append(
                                        "Check ONT.")
                                    self.recommended_troubleshooting_steps[0].append(
                                        "Check ONT's battery backup.")

                                # END of branch - If attempted checking ONT and battery backup wouldn't get power ...
                                elif (self.can_check_ont != None and self.battery_backup_status == "off"):
                                    self.ticket_status = "Ticket Status: Problem should be escalated to a higher level.\nMain router and battery backup are offline."

                                # END of branch - If attempted checking ONT and battery backup couldn't be checked ...
                                elif (self.can_check_ont != None and self.battery_backup_status == "n/a"):
                                    self.ticket_status = "Ticket Status: Problem should be escalated to a higher level.\nMain router and battery backup may be offline."

                                # If attempted checking ONT and turned on battery backup power ...
                                elif (self.can_check_ont != None and self.battery_backup_fixed == True):

                                    if (len(self.recommended_troubleshooting_steps[0]) == 9):
                                        self.ticket_status = "Ticket Status: Problem not resolved yet.\nThe ONT might be working fine, but network devices haven't been checked for internet."

                                        self.recommended_troubleshooting_steps[0].append(
                                            "Check network devices for internet.")

                                    # END of branch - Condition after step to check network devices is added ...
                                    elif (len(self.recommended_troubleshooting_steps[0]) == 10):

                                        determine_steps_after_checking_network_devices_for_internet()

                                    # END of branch - Condition after step to check devices is added ...
                                    elif (len(self.recommended_troubleshooting_steps[0]) == 11):

                                        determine_steps_when_device_ip_is_valid_but_theres_no_internet()

                            elif (self.main_router["status"] == "online"):

                                # Condition after step to check network devices is added ...
                                if (len(self.recommended_troubleshooting_steps[0]) == 7):

                                    determine_steps_after_checking_network_devices_for_internet()

                                # Condition after step to check devices is added ...
                                elif (len(self.recommended_troubleshooting_steps[0]) == 8):

                                    determine_steps_when_device_ip_is_valid_but_theres_no_internet()

                    # If ONT is online ...
                    elif (self.some_services_offline == True):

                        # Branching from the 'power_cycle' function - ONT is online/unknown status | Equipment power cycled
                        if (self.power_cycled == "yes"):

                            if (len(self.recommended_troubleshooting_steps[0]) == 5):
                                self.ticket_status = "Ticket Status: Problem not resolved yet.\nEquipment power cycled, but network devices haven't been checked for internet."

                                self.recommended_troubleshooting_steps[0].append(
                                    "Check each network device's name, model, and lights.")
                                self.recommended_troubleshooting_steps[0].append(
                                    "Check network devices for internet.")

                            # Condition after step to check network devices is added ...
                            elif (len(self.recommended_troubleshooting_steps[0]) == 7):

                                determine_steps_after_checking_network_devices_for_internet()

                            # Condition after step to check devices is added ...
                            elif (len(self.recommended_troubleshooting_steps[0]) == 8):

                                determine_steps_when_device_ip_is_valid_but_theres_no_internet()

                        # Branching from the 'power_cycle' function - ONT is online | No equipment could be powercycled
                        elif (self.power_cycled == "no"):

                            if (len(self.recommended_troubleshooting_steps[0]) == 5):

                                self.ticket_status = "Ticket Status: Problem not resolved yet.\nEquipment could not be power cycled, but network devices can still be checked for internet."
                                self.recommended_troubleshooting_steps[0].append(
                                    "Check network devices for internet.")

                            # Condition after step to check network devices is added ...
                            elif (len(self.recommended_troubleshooting_steps[0]) == 6):

                                determine_steps_after_checking_network_devices_for_internet()

                            # Condition after step to check devices is added ...
                            elif (len(self.recommended_troubleshooting_steps[0]) == 7):

                                determine_steps_when_device_ip_is_valid_but_theres_no_internet()

                self.troubleshooting_steps = self.recommended_troubleshooting_steps

        # If current service is Cable and category is Connectivity, assign self.troubleshooting_steps to value of self.cable_connectivity_steps
        elif (self.service == "Cable" and self.category == "Connectivity"):
            self.troubleshooting_steps.append(self.cable_connectivity_steps)

        # If current service is Fixed Wireless and category is Connectivity, assign self.troubleshooting_steps to value of self.fixed_wireless_connectivity_steps
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

        print("\nTicket:\n")

        print(self.print_ticket())

        print("\n----------------------------------\n\n\n")

        # Possible values for ticket_status:
        # self.ticket_status = "Ticket Status: Problem not resolved yet."
        # self.ticket_status = "Ticket Status: Problem resolved.\n" + (More specific message based on what troubleshooting step resolved issue)
        # self.ticket_status = "Ticket Status: Escalating problem to a higher level is required to solve the problem."

        if (self.toggle_steps == "Recommended Steps"):
            print(self.ticket_status + "\n\n\n")

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

        first_index = 0
        second_index = None

        # Used in steps when checking whether user entered one of two values
        def check_for_a_or_b(question, a, b):

            nonlocal step_response

            variable = input(question).lower().strip()

            if (variable == "exit"):
                step_response = "exit"
                return None

            while (variable != a and variable != b):

                if ("\n" in question):
                    print("\nInvalid response - '" + a +
                          "' or '" + b + "' was not entered.")
                else:
                    print("Invalid response - '" + a +
                          "' or '" + b + "' was not entered.")

                variable = input("\nEnter '" + a + "' or '" +
                                 b + "': ").lower().strip()

                if (variable == "exit"):

                    step_response = "exit"
                    return None

            return variable

        # Used in steps when checking whether user entered one of three values
        def check_for_a_or_b_or_c(question, a, b, c):
            nonlocal step_response

            variable = input(question).lower().strip()

            if (variable == "exit"):
                step_response = "exit"
                return None

            while (variable != a and variable != b and variable != c):

                if ("\n" in question):
                    print("\nInvalid response - Neither '" + a + "', '" +
                          b + "', or '" + c + "' were entered.")
                else:
                    print("Invalid response - Neither '" + a + "', '" +
                          b + "', or '" + c + "' were entered.")

                variable = input("\nEnter '" + a + "', '" +
                                 b + "', or '" + c + "': ").lower().strip()

                if (variable == "exit"):
                    step_response = "exit"
                    return None

            return variable

        # Used in steps when documenting lights and cabling
        def document_lights_or_cabling(light_or_cabling, current_print_responses):

            nonlocal step_response_sentence
            nonlocal step_response

            status = ""

            while (status.lower().strip() != "done"):

                current_print_responses()

                if (light_or_cabling == "lights"):
                    status = input(
                        "Enter light in format of 'Light Name: Color – Status': ").strip()
                elif (light_or_cabling == "cabling"):
                    status = input(
                        "Enter in format of 'beginning device and port > end device and port': ").strip()

                if (status.lower().strip() == "exit"):
                    step_response = "exit"
                    return
                elif (status.lower().strip() == "done"):
                    break

                step_response_sentence += "\n" + status

        # Used in steps when checking if a prompted value is in a list
        def prompt_for_value_in_list(list_compared_to):
            nonlocal step_response
            nonlocal step_response_sentence

            lowercase_list_compared_to = [
                item.lower() for item in list_compared_to]

            variable = input(
                "Enter one of the above choices: ").lower().strip()

            if (variable == "exit"):
                step_response = "exit"
                return None

            while (variable not in lowercase_list_compared_to):

                print(
                    f"Invalid response - '{variable}' is not a valid choice.")

                variable = input(
                    "\nEnter one of the above choices: ").lower().strip()

                if (variable == "exit"):

                    step_response = "exit"
                    return None

            return variable

        # Used when seeing whether all values in first_list_or_set are also in second_list_or_set
        # If comparison shows a problem, return false
        def compare_two_lists_or_sets(first_list_or_set, second_list_or_set, comparing_by):

            if ((type(first_list_or_set) == list) and (type(second_list_or_set) == list)):
                first_set = set(first_list_or_set)
                second_set = set(second_list_or_set)

            if (comparing_by == "union"):
                pass

            elif (comparing_by == "intersection"):
                pass

            elif (comparing_by == "difference"):
                pass

            elif (comparing_by == "symmetric_difference"):
                pass

        # Used when asking for a comma seperated string
        # Returns formatted string, list, and list length
        def manipulate_comma_seperated_string(instructions):

            nonlocal step_response

            # Get comma-seperated string from user
            comma_seperated_string = input(instructions).lower().strip()

            if (comma_seperated_string == "exit"):
                comma_seperated_string = ""
                step_response = "exit"
                return "", "", ""

            # Create a list of all words in comma_seperated_string
            list_from_string = comma_seperated_string.split(",")
            # Format list by stripping all whitespace
            list_from_string = [list_item.strip(
            ) for list_item in list_from_string]

            # Remove duplicate items from the list
            list_from_string = list(set(list_from_string))

            # Create int type variable for the number of items in list_from_string
            list_length = len(list_from_string)

            # Create a formatted string version of comma_seperated_string
            formatted_string = ", ".join(list_from_string)

            return formatted_string, list_from_string, list_length

        system.clear_prompt_or_terminal()

        if (self.toggle_steps == "Recommended Steps"):
            print("\nEnter 'exit' at any time to exit prompt.")
            print("\nAdd steps to get more recommended steps\n\n\n")
        else:
            print("\nEnter 'exit' at any time to exit prompt.\n\n\n")

        self.print_troubleshooting_steps()

        print("")

        # Make sure user selects a valid step
        while (True):
            second_index = input(
                "\n\nSelect a step by entering the number next to it: ").strip()

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
        #
        # self.ticket_status will update depending on responses to the below prompts.
        #
        # Below examples:
        # self.ticket_status = "Ticket Status: Problem not resolved yet.\n" (More specific message based on latest update from a step)
        # self.ticket_status = "Ticket Status: Problem resolved.\n" + (More specific message based on what troubleshooting step resolved issue)
        # self.ticket_status = "Ticket Status: Problem can't be resolved right now.\nEscalating problem to a higher level is required to solve the problem."
        # self.ticket_status = "Ticket Status: Problem can't be resolved right now.\nReferring to a local technician or the product manufacturer is required to solve the problem." (For device issues)

        def check_account_status():

            # self.account_status == "online" or self.account_status == "n/a"
            # - Shows Steps: Check status of all services.
            # - Condition: Account is enabled, Cannot determine account status
            #
            # Decision Tree - check_account_status
            # self.ticket_status = "Ticket Status: Problem not resolved yet.\nAccount is active, but internet is offline.
            # self.ticket_status = "Ticket Status: Problem not resolved yet.\nCannot determine account status."
            # self.ticket_status = "Ticket Status: Problem resolved.\nAccount is disabled. Advised to pay service provider over phone or on website."

            nonlocal step_response
            nonlocal step_response_sentence

            def print_responses(all_questions_answered=False, **kwargs):

                nonlocal step_response_sentence

                system.clear_prompt_or_terminal()

                print("\nEnter 'exit' at any time to exit prompt.\n\n")

                print("\nAdding To Ticket:\n")

                if (step_response_sentence == ""):
                    pass
                else:
                    print(step_response_sentence)

                print("\n----------------------------------\n\n\n")

                print("\nResponses:\n")

                if (len(kwargs) == 0):
                    pass
                else:
                    for key, value in kwargs.items():
                        if (key == "can_determine_account_status"):
                            print("Can determine account status: " + value)
                        if (key == "account_status"):
                            print("Account Status: " + value)

                print("\n----------------------------------\n\n\n")

                if (all_questions_answered == False):
                    print("Answer the following questions to add this step:\n\n\n")
                else:
                    print("All questions answered!\n\n\n")

                    print("Adding step to ticket.",
                          end="", flush=True)

                    time.sleep(.70)
                    print(".", end="", flush=True)

                    time.sleep(.70)
                    print(".", end="", flush=True)

                    time.sleep(.70)

                    print()

            print_responses()

            # See if account status can be determined
            can_determine_account_status = check_for_a_or_b(
                "Can the account status be determined? Enter 'yes' or 'no': ", "yes", "no")
            if (step_response == "exit"):
                return

            # If account status can be determined, what's the account status?
            if (can_determine_account_status == "yes"):
                print_responses(can_determine_account_status="Yes")

                account_status = check_for_a_or_b(
                    "Is the account enabled or disabled? Enter 'enabled' or 'disabled': ", "enabled", "disabled")
                if (step_response == "exit"):
                    return

                # If account is disabled ...
                if (account_status == "disabled"):
                    self.ticket_status = "Ticket Status: Problem resolved.\nAccount is disabled. Advised to pay service provider over phone or on website."
                    step_response_sentence = "Account is disabled. Advised to pay service provider over phone or on website."

                    print_responses(all_questions_answered=True,
                                    can_determine_account_status="No", account_status="Disabled")

                # If account is enabled
                elif (account_status == "enabled"):
                    self.ticket_status = "Ticket Status: Problem not resolved yet.\nAccount is enabled, but internet is offline."
                    self.account_status = "online"
                    # Call this method to add "Check status of all services." to troubleshooting steps
                    step_response_sentence = "Account is enabled."

                    print_responses(all_questions_answered=True,
                                    can_determine_account_status="No", account_status="Enabled")

            # If account status cannot be determined ...
            if (can_determine_account_status == 'no'):
                self.ticket_status = "Ticket Status: Problem not resolved yet.\nCannot determine account status."
                self.account_status = "n/a"
                # Call this method to add "Check status of all services." to troubleshooting steps
                step_response_sentence = "Cannot determine account status."

                print_responses(all_questions_answered=True,
                                can_determine_account_status="No")

            self.set_troubleshooting_steps()

        def check_landline_phone_for_dial_tone():

            nonlocal step_response_sentence
            nonlocal step_response

            def print_responses(all_questions_answered=False, **kwargs):

                nonlocal step_response_sentence

                system.clear_prompt_or_terminal()

                print("\nEnter 'exit' at any time to exit prompt.\n\n")

                print("\nAdding To Ticket:\n")

                if (step_response_sentence == ""):
                    pass
                else:
                    print(step_response_sentence)

                print("\n----------------------------------\n\n\n")

                print("\nResponses:\n")

                if (len(kwargs) == 0):
                    pass
                else:
                    for key, value in kwargs.items():
                        if (key == "can_check_landline"):
                            print(
                                "Can a landline phone be checked for dial tone: " + value)
                        if (key == "landline_has_dial_tone"):
                            print("Landline has dial tone: " + value)

                print("\n----------------------------------\n\n\n")

                if (all_questions_answered == False):
                    print("Answer the following questions to add this step:\n\n\n")
                else:
                    print("All questions answered!\n\n\n")

                    print("Adding step to ticket.",
                          end="", flush=True)

                    time.sleep(.70)
                    print(".", end="", flush=True)

                    time.sleep(.70)
                    print(".", end="", flush=True)

                    time.sleep(.70)

                    print()

            print_responses()

            if (self.can_check_landline == None or self.can_check_landline == "no"):

                # See if a landline phone can be checked
                self.can_check_landline = check_for_a_or_b(
                    "Can a landline phone be checked for dial tone?\nEnter “yes” or “no”: ", "yes", "no")
                if (step_response == "exit"):
                    return

                # If a landline phone cannot be checked ...
                if (self.can_check_landline == "no"):
                    step_response_sentence = "No landline phone can be checked for dial tone."

                    print_responses(can_check_landline=self.can_check_landline,
                                    all_questions_answered=True)

            # If a landline phone can be checked ...
            if (self.can_check_landline == "yes"):
                print_responses(can_check_landline=self.can_check_landline)

                # Check landline phone for dial tone
                self.landline_has_dial_tone = check_for_a_or_b(
                    "Does the landline phone have dial tone?\nEnter 'yes' or 'no': ", "yes", "no")
                if (step_response == "exit"):
                    return

                # If the landline phone has dial tone ...
                if (self.landline_has_dial_tone == "yes"):
                    step_response_sentence = "Landline phone has dial tone."

                    print_responses(
                        can_check_landline=self.can_check_landline, landline_has_dial_tone=self.landline_has_dial_tone, all_questions_answered=True)

                # If the landline phone has no dial tone ...
                elif (self.landline_has_dial_tone == "no"):
                    step_response_sentence = "Landline phone does not have dial tone."

                    print_responses(
                        can_check_landline=self.can_check_landline, landline_has_dial_tone=self.landline_has_dial_tone, all_questions_answered=True)

            self.set_troubleshooting_steps()

        def check_status_of_all_services():

            # Decision Tree - check_status_of_all_services
            # self.ticket_status = "Ticket Status: Problem not resolved yet.\nOnly some devices have internet."
            # - Shows Steps: "Check a device for internet."
            # - Condition: Only some devices have internet

            # self.ticket_status = "Ticket Status: Problem not resolved yet.\nMultiple and all services are offline."
            # - Shows Steps: "Check ONT", "Check ONT's battery backup", "Check battery backup for power."
            # - Condition: Multiple and all services used are offline

            # self.ticket_status = "Ticket Status: Problem not resolved yet.\nONT is online, but there's no internet - Issue may be the router or some other device"
            # - Show Steps: "Check each network device's name, model, and lights.", "Check cabling.", "Check if cables are in the correct ports."
            # - Condition: Fiber - Multiple servicves used, but only this service, self.service, is offline
            # Note: Results from "Check if cables are in the correct ports." may add "Check cable conditions." which may add "Power cycle all network devices.",
            # "Check each network device's name, model, and lights.", and "Check network devices for internet."

            # self.ticket_status = "Ticket Status: Problem not resolved yet.\nOther services are working fine."
            # Show Steps: Same as above
            # - Condition: Multiple servicves used, but only this service, self.service, is offline

            # self.ticket_status = "Ticket Status: Problem not resolved yet.\n" + self.service + ", the only service is offline."
            # Show Steps: Same as above
            # - Condition: Only one service used and it's offline.

            devices_online = ""

            services = ""
            offline_services = ""
            online_services = ""

            # User chooses an option from this list
            service_options = ["internet", "email",
                               "phone", "cable tv", "iptv"]

            # These lists populate based on what user enters
            services_list = []
            offline_services_list = []
            online_services_list = []

            number_of_services = None
            number_of_offline_services = None

            nonlocal step_response_sentence
            nonlocal step_response

            def print_responses(all_questions_answered=False, checking_services=None, **kwargs):

                nonlocal step_response_sentence

                system.clear_prompt_or_terminal()

                print("\nEnter 'exit' at any time to exit prompt.\n\n")

                print("\nAdding To Ticket:\n")

                if (step_response_sentence == ""):
                    pass
                else:
                    print(step_response_sentence)

                print("\n----------------------------------\n\n\n")

                print("\nResponses:\n")

                if (len(kwargs) == 0):
                    pass
                else:
                    for key, value in kwargs.items():
                        if (key == "devices_online"):
                            if (value == ""):
                                pass
                            else:
                                print(
                                    "Devices are online: " + value)
                        if (key == "devices_online_list"):
                            print(
                                "Devices online: " + value)
                        if (key == "devices_offline"):
                            print(
                                "Devices are offline: " + value)
                        if (key == "services"):
                            print(
                                "Services: " + value)
                        if (key == "offline_services"):
                            print(
                                "Offline Services: " + value)
                        if (key == "online_services"):
                            print(
                                "Online Services: " + value)

                print("\n----------------------------------\n\n\n")

                if (all_questions_answered == False):

                    if (checking_services != None):
                        if (checking_services == "services"):
                            print("Which of the following services are used:\n")
                        elif (checking_services == "offline_services"):
                            print("Which of the following services are offline:\n")
                        elif (checking_services == "online_services"):
                            print(
                                "Which of the following services are online:\n")
                        print(
                            "Internet\nEmail\nPhone\nCable TV\nIPTV\n\n\n")
                    elif (checking_services == None):
                        print(
                            "Answer the following questions to add this step:\n\n\n")
                else:
                    print("All questions answered!\n\n\n")

                    print("Adding step to ticket.",
                          end="", flush=True)

                    time.sleep(.70)
                    print(".", end="", flush=True)

                    time.sleep(.70)
                    print(".", end="", flush=True)

                    time.sleep(.70)

                    print()

            print_responses()

            # Determine if any devices are online
            # if service is an internet service and category is connectivity or intermittent connectivity/speed
            if (self.service in self.internet_services and (self.category == "Connectivity" or self.category == "Intermittent Connectivity/Speed")):
                self.devices_online = check_for_a_or_b(
                    "Do any devices have internet? Enter 'yes' or 'no': ", "yes", "no")
                if (step_response == "exit"):
                    return

                # Find out which devices are online, and then set troubleshooting steps.
                # if some devices are online ...
                if (self.devices_online == "yes"):
                    self.devices_online = True
                    step_response_sentence += "At least one device is online."

                    print_responses(
                        devices_online=str(self.devices_online))

                    # Check what devices are online
                    devices_online, devices_online_list, devices_online_list_length = manipulate_comma_seperated_string(
                        "What devices are online? Enter a comma seperated list of devices: ")
                    if (step_response == "exit"):
                        return

                    step_response_sentence += "\nDevices online: " + devices_online

                    print_responses(
                        devices_online=str(self.devices_online), devices_online_list=", ".join(devices_online_list))

                    # Check if any devices are offline
                    self.devices_offline = check_for_a_or_b(
                        "Do any devices NOT have internet? Enter 'yes' or 'no': ", "yes", "no")
                    if (step_response == "exit"):
                        return

                    # If some devices are also offline ...
                    if (self.devices_offline == "yes"):
                        self.devices_offline = True
                        step_response_sentence += "\n\nAt least one other device is offline."

                        print_responses(
                            all_questions_answered=True, devices_online=str(self.devices_online), devices_online_list=", ".join(devices_online_list), devices_offline=str(self.devices_offline))

                    # If no devices are also offline ...
                    if (self.devices_offline == "no"):
                        # # Option to switch to a different category, since internet is online
                        # self.devices_offline = False
                        # step_response_sentence += "\n\nNo device is offline."
                        pass

                    # Will add step to 'Check a device for internet.'
                    self.ticket_status = "Ticket Status: Problem not resolved yet.\nOnly some devices have internet."
                    self.set_troubleshooting_steps()

                    return

                # if no devices are online, mention this in step_response_sentence.
                if (self.devices_online == "no"):

                    self.devices_online = False
                    self.devices_offline = True

                    step_response_sentence += "No devices are online."

            print_responses(
                checking_services="services", devices_online=str(self.devices_online))

            valid_services = False

            while (valid_services == False):

                # Check for services provided by service provider
                services, services_list, number_of_services = manipulate_comma_seperated_string(
                    "Enter a comma seperated list of services: ")
                if (step_response == "exit"):
                    return

                # Check if all services entered are valid options
                valid_services = all(
                    service in service_options for service in services_list)

                if (valid_services == False):
                    print(
                        "\nInvalid response - Not all entered services are valid options.\n")

            if (self.service in self.internet_services and (self.category == "Connectivity" or self.category == "Intermittent Connectivity/Speed")):
                step_response_sentence += "\n\nServices: " + services
            else:
                step_response_sentence += "Services: " + services

            # If more than one service is provided by the service provider ...
            if (number_of_services > 1):

                print_responses(
                    checking_services="offline_services", devices_online=str(self.devices_online), services=services)

                valid_offline_services = False

                while (valid_offline_services == False):

                    # Check for offline services provided by service provider.
                    offline_services, offline_services_list, number_of_offline_services = manipulate_comma_seperated_string(
                        "Enter a comma seperated list of offline services: ")
                    if (step_response == "exit"):
                        return

                    # Check if all services entered are valid options
                    valid_offline_services = all(
                        service in service_options for service in offline_services_list)

                    if (valid_offline_services == False):
                        print(
                            "\nInvalid response - Not all entered services are valid options.\n")

                # # Prompt for offline services repeatedly
                # # If user entered more offline services than services ...
                # while ((number_of_offline_services > number_of_services)):

                #     print(
                #         "There cannot be more offline services than services provided by service provider.")

                #     valid_online_services = False

                #     while (valid_online_services == False):

                #         # Check for offline services provided by service provider.
                #         offline_services, offline_services_list, number_of_offline_services = manipulate_comma_seperated_string(
                #             "Enter a comma seperated list of offline services: ")
                #         if (step_response == "exit"):
                #             return

                #         # Check if all services entered are valid options
                #         valid_online_services = all(
                #             service in service_options for service in online_services_list)

                #         if (valid_online_services == False):
                #             print(
                #                 "\nInvalid response - Not all entered services are valid options.\n")

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

                # If all servies are offline ...

                step_response_sentence += "\nOffline Services: " + offline_services

                if (number_of_offline_services == number_of_services):
                    if (self.service == "Fiber"):
                        self.ont_status = "offline"
                    self.ticket_status = "Ticket Status: Problem not resolved yet.\nMultiple and all services are offline."
                    self.all_services_offline = True

                    print_responses(
                        all_questions_answered="True", devices_online=str(self.devices_online), services=services, offline_services=", ".join(offline_services_list))

                # If only some but not all services are offline ...
                elif (number_of_offline_services < number_of_services):

                    print_responses(
                        checking_services="online_services", devices_online=str(self.devices_online), services=services, offline_services=", ".join(offline_services_list))

                    valid_online_services = False

                    while (valid_online_services == False):

                        # Check for online services provided by service provider.
                        online_services, online_services_list, number_of_online_services = manipulate_comma_seperated_string(
                            "Enter a comma seperated list of working services: ")
                        if (step_response == "exit"):
                            return

                        # Check if all services entered are valid options
                        valid_online_services = all(
                            service in service_options for service in online_services_list)

                        if (valid_online_services == False):
                            print(
                                "\nInvalid response - Not all entered services are valid options.\n")

                    step_response_sentence += "\nOnline Services: " + online_services

                    # # Inform that at least one of the online services is not a service provided by the service provider
                    # # While not all entered online services are provided
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

                    # if service is fiber and 'phone' or 'tv' are online ...
                    if (("phone" in online_services_list or "tv" in online_services_list) and (self.service == "Fiber" and (self.category == "Connectivity" or self.category == "Intermittent Connectivity/Speed"))):
                        self.ticket_status = "Ticket Status: Problem not resolved yet.\nONT is online, but there's no internet - Issue may be the router or some other device."
                        self.some_services_offline = True
                        self.ont_status = "online"

                        print_responses(
                            all_questions_answered="True", devices_online=str(self.devices_online), services=services, offline_services=", ".join(offline_services_list), online_services=", ".join(online_services_list))

                    # if service is not fiber and 'phone' or 'tv' are offline
                    else:
                        self.ticket_status = "Ticket Status: Problem not resolved yet.\nOther services are working fine."
                        self.some_services_offline = True

                        print_responses(
                            all_questions_answered="True", devices_online=str(self.devices_online), services=services, offline_services=", ".join(offline_services_list), online_services=", ".join(online_services_list))

                self.set_troubleshooting_steps()

            # If only one service is provided by the service provider ...
            elif (number_of_services == 1):
                self.ticket_status = "Ticket Status: Problem not resolved yet.\nThe only service is offline."

                if (self.service == "Fiber"):
                    self.ont_status = "n/a"

                self.only_service_offline = True

                print_responses(
                    all_questions_answered=str(self.only_service_offline), devices_online=str(self.devices_online), services=services)

                self.set_troubleshooting_steps()

        def check_each_network_device():

            nonlocal step_response
            nonlocal step_response_sentence

            def print_responses(all_questions_answered=False, checking_network_device_lights=False, **kwargs):

                nonlocal step_response_sentence

                system.clear_prompt_or_terminal()

                print("\nEnter 'exit' at any time to exit prompt.\n\n")

                print("\nAdding To Ticket:\n")

                if (step_response_sentence == ""):
                    pass
                else:
                    print(step_response_sentence)

                print("\n----------------------------------\n\n\n")

                if "can_check_network_device_lights" in kwargs:
                    if kwargs["can_check_network_device_lights"] == "yes":
                        pass
                    else:
                        print("\nResponses:\n")

                        if (len(kwargs) == 0):
                            pass
                        else:
                            for key, value in kwargs.items():
                                if (key == "can_check_network_device_lights"):
                                    print(
                                        "Can check network device lights: " + value)

                        print("\n----------------------------------\n\n\n")

                if (all_questions_answered == False):

                    if checking_network_device_lights == True:
                        print(
                            "Network device information will be displayed in the following example format:\n")
                        print("Brand Name - Model Number\nPower: Green - Solid\nInternet: Green - Flashing\n2.4GHz: Green - Flashing\n5GHz: Green - Flashing" +
                              "\nEthernet: Off\n\n")
                        print("Enter “done” when all lights are documented.\n\n\n")
                    else:
                        print(
                            "\nAnswer the following questions to add this step:\n\n\n")

                else:
                    print("All questions answered!\n\n\n")

                    print("Adding step to ticket.",
                          end="", flush=True)

                    time.sleep(.70)
                    print(".", end="", flush=True)

                    time.sleep(.70)
                    print(".", end="", flush=True)

                    time.sleep(.70)

                    print()

            def add_device(device=None):
                nonlocal step_response
                nonlocal step_response_sentence

                print_responses(
                    can_check_network_device_lights=self.can_check_network_device_lights)

                # Prompt for network device name and model
                # if device isn't reassigned in argument
                if (device == None):
                    print(
                        "What device is being checked? Enter in format of 'Brand Name – Model Number': ")

                    device_brand_and_model = input(
                        "").strip()

                    if (device_brand_and_model.lower() == "exit"):

                        step_response = "exit"
                        return

                    step_response_sentence = device_brand_and_model

                    print_responses(
                        can_check_network_device_lights=self.can_check_network_device_lights)

                    print(
                        "Which of the following device types best decribes this device: ")

                    if (self.service == "Fiber"):
                        print(
                            "\nMain Router\nAdditional Router\nExtender\nSwitch\nIndoor ONT\nONT/Router\n\n\n")

                        device_type = input(
                            "Enter one of the above device types: ").lower().strip()

                        if (device_type.lower() == "exit"):

                            step_response = "exit"
                            return

                        while (device_type.lower() != "main router" and device_type.lower() != "additional router" and device_type.lower() != "extender"
                               and device_type.lower() != "switch" and device_type.lower() != "indoor ont" and device_type.lower() != "ont/router"):
                            print(
                                "Invalid response - A valid device type was not entered.")

                            device_type = input(
                                "\nEnter one of the above device types: ").lower().strip()

                            if (device_type.lower() == "exit"):

                                step_response = "exit"
                                return

                        if (device_type.lower() == "indoor ont"):
                            device_type = "Indoor ONT"
                        elif (device_type.lower() == "ont/router"):
                            device_type = "ONT/Router"
                        else:
                            device_type = device_type.title()

                    elif ((self.service in self.internet_services) and (self.service != "Fiber")):
                        print(
                            "\nMain Router\nAdditional Router\nExtender\nSwitch\nModem\nModem/Router\n\n\n")

                        device_type = input(
                            "Enter one of the above device types: ").lower().strip()

                        if (device_type.lower() == "exit"):

                            step_response = "exit"
                            return

                        while (device_type.lower() != "main router" and device_type.lower() != "additional router" and device_type.lower() != "extender"
                               and device_type.lower() != "switch" and device_type.lower() != "modem" and device_type.lower() != "modem/router"):
                            print(
                                "Invalid response - A valid device type was not entered.")

                            device_type = input(
                                "\nEnter one of the above device types: ").lower().strip()

                            if (device_type.lower() == "exit"):

                                step_response = "exit"
                                return

                        device_type = device_type.title()

                    self.network_devices.update(
                        {device_brand_and_model: device_type})
                # Assign brand and model to device argument's value
                # if device is reassigned in argument
                else:
                    device_brand_and_model = device
                    step_response_sentence = device_brand_and_model

                # Prompt for network device lights
                document_lights_or_cabling(
                    "lights", print_responses)
                if (step_response == "exit"):
                    return

                print_responses(all_questions_answered=True,
                                can_check_network_device_lights=self.can_check_network_device_lights)

                return step_response_sentence

            def select_key(update_or_delete):

                nonlocal step_response
                nonlocal step_response_sentence

                # See if user entered a valid number (selected a valid key)
                while (True):

                    if (update_or_delete == "update"):
                        selected_number = input(
                            "\nEnter the number next to a device to add a new light readout for the device: ").strip()
                    elif (update_or_delete == "delete"):
                        selected_number = input(
                            "\nEnter the number next to a device to delete the device: ").strip()

                    if (selected_number.lower() == "exit"):
                        step_response = "exit"
                        return

                    try:
                        selected_number = int(selected_number)
                    except ValueError:
                        print("Invalid response - a number was not entered.")
                        continue

                    # Assign selected_key to option user selected
                    # If selected key matches a key in the list of network devices
                    selected_key = None

                    for index, (brand_and_model, type_of_device) in enumerate(self.network_devices.items()):
                        if (index + 1 == selected_number):
                            selected_key = brand_and_model

                    if selected_key == None:
                        print(
                            "Invalid response - number entered does not correlate with a line.")
                        continue

                    break

                return selected_key

            # See if network devices can be checked
            # If network devices can't be checked or haven't been checked
            if (self.can_check_network_device_lights == "no" or self.can_check_network_device_lights == None):

                print_responses()

                self.can_check_network_device_lights = check_for_a_or_b(
                    "Can network devices be checked? Enter “yes” or “no” to respond: ", "yes", "no")
                if (step_response == "exit"):
                    return

                if (self.can_check_network_device_lights == "no"):
                    step_response_sentence = "No network devices can be checked."

                    self.set_troubleshooting_steps()

                    print_responses(all_questions_answered="True",
                                    can_check_network_device_lights=self.can_check_network_device_lights)

                    return

            # If network devices can be checked
            if (self.can_check_network_device_lights == "yes"):

                if (len(self.network_devices) == 0):
                    step_response_sentence = add_device()

                    if (step_response == "exit"):
                        return

                else:

                    print_responses(
                        can_check_network_device_lights=self.can_check_network_device_lights)

                    print("\nEnter 'exit' at any time to exit prompt.\n")

                    print("\nThe following devices were saved:")

                    # Print all saved network devices
                    for index, (brand_and_model, type_of_device) in enumerate(self.network_devices.items()):
                        print(str(index + 1) + ". " + brand_and_model +
                              " | " + type_of_device)

                    print("\n\nAvailable commands:")
                    print(
                        "Update - Choose a saved device and document a new light readout for it.")
                    print("Add - Save a new device and document it's lights.")
                    print("Delete - Delete a saved device.\n\n")

                    # Prompt to choose 'update', 'add', or 'delete'
                    device_list_choice = check_for_a_or_b_or_c(
                        "Enter 'add', 'update', or 'delete': ", "add", "update", "delete")
                    if (step_response == "exit"):
                        return

                    if (device_list_choice == "update"):
                        device_lights_to_update = select_key(
                            update_or_delete="update")

                        if (step_response == "exit"):
                            return

                        step_response_sentence = add_device(
                            device_lights_to_update)

                        if (step_response == "exit"):
                            return

                    elif (device_list_choice == "add"):
                        step_response_sentence = add_device()

                        if (step_response == "exit"):
                            return

                    elif (device_list_choice == "delete"):
                        device_to_remove = select_key(
                            update_or_delete="delete")

                        if (step_response == "exit"):
                            return

                        del self.network_devices[device_to_remove]

        def check_cabling():
            nonlocal step_response
            nonlocal step_response_sentence

            checking_cabling = False

            def print_responses(all_questions_answered=False, **kwargs):

                nonlocal step_response_sentence

                system.clear_prompt_or_terminal()

                print("\nEnter 'exit' at any time to exit prompt.\n\n")

                print("\nAdding To Ticket:\n")

                if (step_response_sentence == ""):
                    pass
                else:
                    print(step_response_sentence)

                print("\n----------------------------------\n\n\n")

                if (checking_cabling == False):

                    print("\nResponses:\n")

                    if (len(kwargs) == 0):
                        pass
                    else:
                        for key, value in kwargs.items():
                            if (key == "can_check_cabling"):
                                print(
                                    "Can check cabling: " + value)
                            elif (key == "correct_ports"):
                                print(
                                    "Cables in correct ports: " + value)
                            elif (key == "can_be_corrected"):
                                if (value == ""):
                                    pass
                                else:
                                    print(
                                        "Cables can be put in correct ports: " + value)
                            elif (key == "cables_not_loose_or_damaged"):
                                if (value == "yes"):
                                    print(
                                        "Cables not loose or damaged: " + value)
                                elif (value == "damaged"):
                                    print(
                                        "Damaged cable: Yes")
                                elif (value == "loose"):
                                    print(
                                        "Loose cable: Yes")
                            elif (key == "can_be_replaced"):
                                if (value == "no"):
                                    print(
                                        "Cable can be replaced: " + value)
                                else:
                                    pass
                            elif (key == "can_be_fixed"):
                                if (value == "no"):
                                    print(
                                        "Cable can be fixed: " + value)
                                else:
                                    pass

                    print("\n----------------------------------\n\n\n")

                if (all_questions_answered == False):

                    if (checking_cabling == True):
                        print(
                            "Cabling will be displayed in the following example format:\n")
                        print(
                            "wall jack > Router WAN port\nRouter ETH 2 port > Mesh router WAN port\nRouter ETH 4 port > Computer ETH port\n")
                        print(
                            "\n\nEnter “done” when all cabling is documented.\n\n\n")

                    else:
                        print(
                            "\nAnswer the following questions to add this step:\n\n\n")
                else:
                    print("All questions answered!\n\n\n")

                    print("Adding step to ticket.",
                          end="", flush=True)

                    time.sleep(.70)
                    print(".", end="", flush=True)

                    time.sleep(.70)
                    print(".", end="", flush=True)

                    time.sleep(.70)

                    print()

            def check_cable_connections():

                nonlocal step_response
                nonlocal step_response_sentence

                nonlocal checking_cabling

                checking_cabling = True

                document_lights_or_cabling(
                    "cabling", print_responses)

                checking_cabling = False

            def check_cable_ports():

                nonlocal step_response
                nonlocal step_response_sentence

                nonlocal correct_ports
                nonlocal can_be_corrected

                print_responses(
                    can_check_cabling=self.can_check_cabling)

                # Check if cables are in the correct ports
                correct_ports = check_for_a_or_b(
                    "Are all cables in the correct ports? Enter “yes” or “no” to respond: ", "yes", "no")
                if (step_response == "exit"):
                    return

                # If cables are in the correct ports ...
                if (correct_ports == "yes"):
                    step_response_sentence += "\n\nCables are in the correct ports."
                    self.cables_in_correct_ports = True

                    print_responses(can_check_cabling=self.can_check_cabling,
                                    correct_ports=correct_ports)

                # If cables are not in the correct ports ...
                elif (correct_ports == "no"):

                    step_response_sentence += "\nCables are not in the correct ports."

                    print_responses(can_check_cabling=self.can_check_cabling,
                                    correct_ports=correct_ports)

                    # Check if cables can be moved to the correct ports ...
                    can_be_corrected = check_for_a_or_b(
                        "Can the cables be moved to the correct ports? Enter “yes” or “no” to respond: ", "yes", "no")
                    if (step_response == "exit"):
                        return

                    # If cables can be moved to the correct ports ...
                    if (can_be_corrected == "yes"):
                        step_response_sentence += "\nCables moved to the correct ports.\n\n"
                        self.cables_in_correct_ports = True

                        check_cable_connections()

                    # If cables cannot be moved to the correct ports ...
                    elif (can_be_corrected == "no"):
                        self.cables_in_correct_ports = False
                        step_response_sentence += "\nCables can't be moved to the correct ports."

                        print_responses(
                            all_questions_answered=True, can_check_cabling=self.can_check_cabling,
                            correct_ports=correct_ports, can_be_corrected=can_be_corrected)

            def check_cable_conditions():

                nonlocal step_response
                nonlocal step_response_sentence

                nonlocal correct_ports
                nonlocal can_be_corrected

                nonlocal cables_not_loose_or_damaged
                nonlocal can_be_replaced
                nonlocal can_be_fixed

                while (True):

                    print_responses(
                        can_check_cabling=self.can_check_cabling,
                        correct_ports=correct_ports, can_be_corrected=can_be_corrected)

                    # Check if cabling is good, damaged, or loose
                    cables_not_loose_or_damaged = check_for_a_or_b_or_c(
                        "Are all cables secure and tight on all ends with no visible damage?\nEnter “yes”, “damaged”, or “loose” to respond: ", "yes", "damaged", "loose")
                    if (step_response == "exit"):
                        return

                    # If cabling is good ...
                    if (cables_not_loose_or_damaged == "yes"):
                        step_response_sentence += "\n\nAll cables secure with no visible damage."
                        self.good_cable_conditions = "yes"

                        break

                    # If cabling is damaged ...
                    elif (cables_not_loose_or_damaged == "damaged"):

                        print_responses(
                            can_check_cabling=self.can_check_cabling,
                            correct_ports=correct_ports, can_be_corrected=can_be_corrected,
                            cables_not_loose_or_damaged=cables_not_loose_or_damaged)

                        # See which cables are damaged
                        damaged_cable = input(
                            "Which cable is damaged? Enter in format of 'beginning device and port > end device and port':\n")

                        step_response_sentence += "\n\nDamaged cable: " + damaged_cable

                        print_responses(
                            can_check_cabling=self.can_check_cabling,
                            correct_ports=correct_ports, can_be_corrected=can_be_corrected,
                            cables_not_loose_or_damaged=cables_not_loose_or_damaged)

                        # Check if cabling can be replaced
                        can_be_replaced = check_for_a_or_b(
                            "Can the cable be replaced? Enter “yes” or “no” to respond: ", "yes", "no")
                        if (step_response == "exit"):
                            return

                        if (can_be_replaced == "no"):
                            step_response_sentence += "\nCable cannot be replaced."
                            self.good_cable_conditions = "no"

                            break

                        elif (can_be_replaced == "yes"):
                            step_response_sentence += "\nJust replaced cable."
                            cables_not_loose_or_damaged = "yes"
                            self.good_cable_conditions = "yes"

                    # If cabling is loose ...
                    elif (cables_not_loose_or_damaged == "loose"):

                        print_responses(
                            can_check_cabling=self.can_check_cabling,
                            correct_ports=correct_ports, can_be_corrected=can_be_corrected,
                            cables_not_loose_or_damaged=cables_not_loose_or_damaged)

                        # See which cables are loose
                        loose_cable = input(
                            "Which cable is loose? Enter in format of 'beginning device and port > end device and port':\n")

                        step_response_sentence += "\n\nLoose cable: " + loose_cable

                        print_responses(
                            can_check_cabling=self.can_check_cabling,
                            correct_ports=correct_ports, can_be_corrected=can_be_corrected,
                            cables_not_loose_or_damaged=cables_not_loose_or_damaged)

                        # Check if cabling can be pushed in or replaced
                        can_be_fixed = check_for_a_or_b(
                            "Can the cable be pushed in or replaced? Enter “yes” or “no” to respond: ", "yes", "no")
                        if (step_response == "exit"):
                            return

                        # If cabling cannot be pushed in or replaced ...
                        if (can_be_fixed == "no"):
                            step_response_sentence += "\nCable cannot be pushed in or replaced."
                            self.good_cable_conditions = "no"

                            break

                        # If cabling can be pushed in or replaced ...
                        elif (can_be_fixed == "yes"):
                            step_response_sentence += "\nJust fixed cabling."
                            cables_not_loose_or_damaged = "yes"
                            self.good_cable_conditions = "yes"

            # If function hasn't been run before or previously stated cabling couldn't be checked ...
            if (self.can_check_cabling == "no" or self.can_check_cabling == None):
                print_responses(can_be_checked=self.can_check_cabling)

                # Check if cabling can be checked
                self.can_check_cabling = check_for_a_or_b(
                    "Can cabling be checked? Enter “yes” or “no” to respond: ", "yes", "no")
                if (step_response == "exit"):
                    return

            # if cabling cannot be checked ...
            if (self.can_check_cabling == "no"):
                step_response_sentence = "Cabling cannot be checked."

                self.set_troubleshooting_steps()

                print_responses(
                    all_questions_answered="True", can_check_cabling=self.can_check_cabling)

                return

            # if cabling can be checked ...
            elif (self.can_check_cabling == "yes"):

                correct_ports = ""

                can_be_corrected = ""

                cables_not_loose_or_damaged = ""

                can_be_replaced = ""
                can_be_fixed = ""

                self.cables_in_correct_ports = None
                self.good_cable_conditions = None

                check_cable_connections()

                check_cable_ports()

                if (self.cables_in_correct_ports == False):
                    self.set_troubleshooting_steps()
                    return

                check_cable_conditions()

                print_responses(
                    all_questions_answered=True, can_check_cabling=self.can_check_cabling,
                    correct_ports=correct_ports, can_be_corrected=can_be_corrected,
                    cables_not_loose_or_damaged=cables_not_loose_or_damaged, can_be_replaced=can_be_replaced, can_be_fixed=can_be_fixed)

                self.set_troubleshooting_steps()

        def power_cycle():

            # self.ticket_status = "Ticket Status: Problem not resolved yet.\nPower cycled network devices but haven't verified service works."
            #
            # self.power_cycled == "yes"
            # - Show Steps: "Check each network device's name, model, and lights.", "Check network devices for internet."
            # - Condition: Power cycled all network devices, Power cycled some network devices
            #
            # self.power_cycled == "no" and self.only_service_offline == True
            # - Show Steps: "Check ONT", "Check ONT's battery backup", "Check battery backup for power."
            # - Condition: Couldn't power cycle and the only service is offline
            #
            # self.power_cycled == "no"
            # - Show Steps: "Check network devices for internet."
            # - Condition: Couldn't power cycle

            nonlocal step_response
            nonlocal step_response_sentence

            def print_responses(all_questions_answered=False, **kwargs):

                nonlocal step_response_sentence

                system.clear_prompt_or_terminal()

                print("\nEnter 'exit' at any time to exit prompt.\n\n")

                print("\nAdding To Ticket:\n")

                if (step_response_sentence == ""):
                    pass
                else:
                    print(step_response_sentence)

                print("\n----------------------------------\n\n\n")

                print("\nResponses:\n")

                if (len(kwargs) == 0):
                    pass
                else:
                    for key, value in kwargs.items():
                        if (key == "can_be_power_cycled"):
                            print(
                                "All network devices power cycled: " + value)
                        if (key == "could_not_power_cycle_list"):
                            if (value == ""):
                                pass
                            else:
                                print(
                                    "Could not power cycle: " + value)

                print("\n----------------------------------\n\n\n")

                if (all_questions_answered == False):
                    print(
                        "\nAnswer the following questions to add this step:\n\n\n")
                else:
                    print("All questions answered!\n\n\n")

                    print("Adding step to ticket.",
                          end="", flush=True)

                    time.sleep(.70)
                    print(".", end="", flush=True)

                    time.sleep(.70)
                    print(".", end="", flush=True)

                    time.sleep(.70)

                    print()

            print_responses()

            print("Were all the following devices power cycled:\n")

            # Print all network devices
            for brand_and_model, type_of_device in self.network_devices.items():
                print(brand_and_model + " | " + type_of_device)

            # Check if all network devices could be power cycled
            can_be_power_cycled = check_for_a_or_b(
                "\n\nEnter “yes” or “no” to respond: ", "yes", "no")
            if (step_response == "exit"):
                return

            # If all network devices could be power cycled ...
            if (can_be_power_cycled == "yes"):
                step_response_sentence = "All network devices power cycled for 30 seconds off."
                self.power_cycled = "yes"

                print_responses(all_questions_answered="True",
                                can_be_power_cycled=can_be_power_cycled)

            # If all network devices could not be power cycled ...
            if (can_be_power_cycled == "no"):

                number_of_network_devices = len(self.network_devices)

                could_not_power_cycle_list = ""

                if (number_of_network_devices != 0):

                    print_responses(
                        can_be_power_cycled=can_be_power_cycled)

                    could_not_power_cycle = input(
                        "Enter a comma seperated list of devices that couldn't be power cycled: ").lower().strip()

                    # Create a list of devices that couldn't be power cycled from sentence entered by user, with a new entry in list after every entered comma
                    could_not_power_cycle_list = could_not_power_cycle.split(
                        ",")
                    # Strip any whitespace before and after every device in list
                    could_not_power_cycle_list = [
                        device.strip() for device in could_not_power_cycle_list]

                if ((number_of_network_devices == len(could_not_power_cycle_list)) or number_of_network_devices == 0):
                    step_response_sentence = "Was not able to power cycle any network device."
                    self.power_cycled = "no"

                    print_responses(
                        all_questions_answered="True", can_be_power_cycled="No", could_not_power_cycle_list=", ".join(could_not_power_cycle_list))
                else:
                    step_response_sentence = "Was able to power cycle every device except the: " + \
                        ", ".join(could_not_power_cycle_list)
                    self.power_cycled = "yes"

                    print_responses(
                        all_questions_answered="True", can_be_power_cycled="No", could_not_power_cycle_list=", ".join(could_not_power_cycle_list))

            self.set_troubleshooting_steps()

        def check_network_devices_for_internet():

            # self.ticket_status = "Ticket Status: Problem not resolved yet.\nIndoor ONT has internet but the main router does not - Bypass the main router."
            # self.power_cycled == "yes"
            # - Show Steps: "Check each network device's name, model, and lights.", "Check network devices for internet."
            # - Condition: Power cycled all network devices, Power cycled some network devices

            nonlocal step_response
            nonlocal step_response_sentence

            def print_responses(all_questions_answered=False, **kwargs):

                nonlocal step_response_sentence

                system.clear_prompt_or_terminal()

                print("\nEnter 'exit' at any time to exit prompt.\n\n")

                print("\nAdding To Ticket:\n")

                if (step_response_sentence == ""):
                    pass
                else:
                    print(step_response_sentence)

                print("\n----------------------------------\n\n\n")

                print("\nResponses:\n")

                if (len(kwargs) == 0):
                    pass
                else:
                    for key, value in kwargs.items():
                        if (key == "can_check_network_device_lights"):
                            print(
                                "Can check network device lights: " + value)
                        if (key == "all_network_devices_show_internet"):
                            print(
                                "All network devices show internet: " + value)
                        if (key == "online_offline_or_na"):
                            print(
                                "What's the device status: " + value)

                print("\n----------------------------------\n\n\n")

                if (all_questions_answered == False):
                    print(
                        "\nAnswer the following questions to add this step:\n\n\n")
                else:
                    print("All questions answered!\n\n\n")

                    print("Adding step to ticket.",
                          end="", flush=True)

                    time.sleep(.70)
                    print(".", end="", flush=True)

                    time.sleep(.70)
                    print(".", end="", flush=True)

                    time.sleep(.70)

                    print()

            if (self.can_check_network_device_lights == "no" or self.can_check_network_device_lights == None):

                print_responses()

                # Can network devices be checked?
                self.can_check_network_device_lights = check_for_a_or_b(
                    "Can network devices be checked?\nEnter 'yes' or 'no' to respond: ", "yes", "no")

                # if no, network devices cannot be checked, "Network devices cannot be checked for internet."
                if (self.can_check_network_device_lights == "no"):
                    step_response_sentence = "Network devices cannot be checked for internet."

                    print_responses(
                        all_questions_answered=True, can_check_network_device_lights=self.can_check_network_device_lights)

            # Ask if all of the saved network devices have internet
            if (self.can_check_network_device_lights == "yes"):

                # Set these attributes to empty lists, in case this method is called multiple times
                self.additional_routers = []
                self.extenders = []
                self.switches = []

                # Assigned in 'what_status_and_who_provided' function
                online_offline_or_na = None
                device_provided_by = None

                # Assigned in 'check_if_user_can_bypass_or_wire' function
                self.can_bypass_or_wire = ""
                self.can_bypass_main_router = False
                self.can_wire_to_network_device = False
                self.can_wire_to_wall_jack = False

                # Assigned in 'find_online_network_device' function
                online_main_network_device = ""

                # Function to see if a device is online or offline and whether the device was provided by the service provider or a third party.
                def what_status_and_who_provided(brand_and_model, device_type):

                    nonlocal step_response

                    nonlocal online_offline_or_na
                    nonlocal device_provided_by

                    online_offline_or_na = input(
                        "Is the " + brand_and_model + " status online, offline, or not available?\nEnter 'online', 'offline', or 'n/a': ").lower().strip()

                    if (online_offline_or_na == "exit"):

                        step_response = "exit"
                        return

                    while (online_offline_or_na != "online" and online_offline_or_na != "offline" and online_offline_or_na != "n/a"):
                        print(
                            "\nInvalid response - Neither 'online', 'offline', or 'n/a' were entered.")

                        online_offline_or_na = input(
                            "\nEnter 'online', 'offline', or 'n/a': ").lower().strip()

                        if (online_offline_or_na == "exit"):

                            step_response = "exit"
                            return

                    if (online_offline_or_na == "online"):
                        return {"device": brand_and_model, "device_type": device_type, "status": online_offline_or_na, "provided_by": "", "can_bypass": ""}

                    elif (online_offline_or_na == "offline" or online_offline_or_na == "n/a"):

                        print_responses(
                            can_check_network_device_lights=self.can_check_network_device_lights, all_network_devices_show_internet=all_network_devices_show_internet, online_offline_or_na=online_offline_or_na)

                        device_provided_by = input(
                            "\nWas the " + brand_and_model + " provided by a service provider or third party?\nEnter 'service provider' or 'third party': ").lower().strip()

                        if (device_provided_by == "exit"):

                            step_response = "exit"
                            return

                        while (device_provided_by != "service provider" and device_provided_by != "third party"):
                            print(
                                "\nInvalid response - 'service provider' or 'provided by' was not entered.")

                            device_provided_by = input(
                                "\nWas the " + brand_and_model + " provided by a service provider or third party?\nEnter 'service provider' or 'third party': ").lower().strip()

                            if (device_provided_by == "exit"):

                                step_response = "exit"
                                return

                        if (device_type == "Main Router" or device_type == "Indoor ONT" or device_type == "ONT/Router" or device_type == "Modem" or device_type == "Modem/Router") or (device_type == "Additional Router" or device_type == "Extender" or device_type == "Switch"):
                            return {"device": brand_and_model, "device_type": device_type, "status": online_offline_or_na, "provided_by": device_provided_by, "can_bypass": ""}

                def check_if_user_can_bypass_or_wire(what_is_bypassed_or_wired_to):

                    nonlocal step_response
                    nonlocal step_response_sentence

                    print_responses(
                        can_check_network_device_lights=self.can_check_network_device_lights, all_network_devices_show_internet=all_network_devices_show_internet)

                    if ("main router" in what_is_bypassed_or_wired_to):

                        # Check if main router can be bypassed
                        self.can_bypass_or_wire = check_for_a_or_b(
                            f"Can the main router be bypassed?\nEnter 'yes' or 'no' to respond: ", "yes", "no")

                        if (self.can_bypass_or_wire == "yes"):
                            step_response_sentence += "\nOffline main router can be bypassed."

                            self.can_bypass_main_router = True

                            if (what_is_bypassed_or_wired_to == "main router to wall"):
                                self.can_wire_to_wall_jack = True
                            elif (what_is_bypassed_or_wired_to == "main router to network device"):
                                self.can_wire_to_network_device = True

                        else:
                            step_response_sentence += f"\nCannot bypass main router."

                    elif (what_is_bypassed_or_wired_to == "network device"):

                        # Check if online network device can be wired to

                        self.can_bypass_or_wire = check_for_a_or_b(
                            f"Can the {online_main_network_device} be wired to?\nEnter 'yes' or 'no' to respond: ", "yes", "no")

                        if (self.can_bypass_or_wire == "yes"):
                            self.can_wire_to_network_device = True
                            step_response_sentence += f"\n{online_main_network_device} can be wired to."
                        else:
                            step_response_sentence += f"\nCannot wire to {online_main_network_device}."

                    elif (what_is_bypassed_or_wired_to == "wall jack"):

                        # Check if wall jack can be wired to
                        self.can_bypass_or_wire = check_for_a_or_b(
                            f"Can the wall jack be wired to?\nEnter 'yes' or 'no' to respond: ", "yes", "no")

                        if (self.can_bypass_or_wire == "yes"):
                            self.can_wire_to_wall_jack = True
                            step_response_sentence += f"\nWall jack can be wired to."
                        else:
                            step_response_sentence += "\nCannot wire to wall jack."

                def find_online_network_device():

                    nonlocal online_main_network_device

                    if (self.service == "Fiber"):
                        if (self.indoor_ont["status"] == "online"):
                            online_main_network_device = "indoor ont"
                        else:
                            online_main_network_device = "ont/router"
                    else:
                        if (self.modem["status"] == "online"):
                            online_main_network_device = "modem"
                        else:
                            online_main_network_device = "modem/router"

                def refer_or_escalate():

                    nonlocal step_response_sentence

                    # #   1.1.0. If main router is offline and nothing comes before it, and the main router cannot be bypassed
                    # if (self.main_router["status"] == "offline" and
                    #         (self.indoor_ont["status"] == "" and self.ont_router["status"] == "" and self.modem["status"] == "" and self.modem_router["status"] == "")):

                    #     pass

                    # #   1.1.1. If main router is offline but some indoor ont, ont/router, modem, modem/router is online, and the main router cannot be bypassed
                    # elif (self.main_router["status"] == "offline" and
                    #         (self.indoor_ont["status"] == "online" or self.ont_router["status"] == "online" or self.modem["status"] == "online" or self.modem_router["status"] == "online")):

                    #     pass

                    # #   1.1.2. If some indoor ont, ont/router, modem, modem/router is online and cannot be wired to, when no main router
                    # elif (self.main_router["status"] == "" and
                    #         (self.indoor_ont["status"] == "online" or self.ont_router["status"] == "online" or self.modem["status"] == "online" or self.modem_router["status"] == "online")):

                    #     pass

                    # #   1.1.3. If there's no kind of ont, modem, router, and service is not fixed wireless, and cannot wire directly to the wall jack
                    # elif (self.main_router["status"] == "" and
                    #         (self.indoor_ont["status"] == "" and self.ont_router["status"] == "" and self.modem["status"] == "" and self.modem_router["status"] == "") and
                    #         self.service != "Fixed Wireless"):

                    #     pass

                    # # If a main network device, besides the main router, is offline
                    # elif (self.indoor_ont["status"] == "offline" or self.ont_router["status"] == "offline" or self.modem["status"] == "offline" or
                    #         self.modem_router["status"] == "offline"):

                    #     pass

                    # If we can't check for internet, there's no scenario where we refer to oem - Escalate for all conditions
                    step_response_sentence += "\n\nEscalate for no internet"

                    self.ticket_status = "Ticket Status: Problem resolved.\nEscalated ticket for no internet."

                print_responses(
                    can_check_network_device_lights=self.can_check_network_device_lights)

                print(
                    "Do all of the following network devices show internet:\n")

                # Print the content of self.network_devices
                for brand_and_model, type_of_device in self.network_devices.items():
                    print(brand_and_model +
                          " | " + type_of_device + "\n\n")

                all_network_devices_show_internet = check_for_a_or_b(
                    "Enter 'yes' or 'no' to respond: ", "yes", "no").lower().strip()

                # if yes, all network devices show internet, add "All network devices show internet." to ticket.
                if (all_network_devices_show_internet == "yes"):
                    step_response_sentence = "All network devices show internet."

                    # Call what_status_and_who_provided function for each network device and assign relevant network device attributes to function's return value.
                    for brand_and_model, type_of_device in self.network_devices.items():

                        # what_status_and_who_provided - Working with these possible return values:
                        #
                        # if (device_type == "Main Router" or device_type == "Indoor ONT" or device_type == "ONT/Router" or device_type == "Modem" or device_type == "Modem/Router") or (device_type == "Additional Router" or device_type == "Extender" or device_type == "Switch"):
                        #     return {"device": brand_and_model, "device_type": device_type, "status": online_offline_or_na, "provided_by": device_provided_by, "can_bypass": ""}

                        if (step_response == "exit"):
                            return

                        if (type_of_device == "Main Router"):

                            self.main_router["device"] = brand_and_model
                            self.main_router["device_type"] = type_of_device
                            self.main_router["status"] = "online"

                        elif (type_of_device == "Indoor ONT"):

                            self.indoor_ont["device"] = brand_and_model
                            self.indoor_ont["device_type"] = type_of_device
                            self.indoor_ont["status"] = "online"

                        elif (type_of_device == "ONT/Router"):

                            self.ont_router["device"] = brand_and_model
                            self.ont_router["device_type"] = type_of_device
                            self.ont_router["status"] = "online"

                        elif (type_of_device == "Modem"):

                            self.modem["device"] = brand_and_model
                            self.modem["device_type"] = type_of_device
                            self.modem["status"] = "online"

                        elif (type_of_device == "Modem/Router"):

                            self.modem_router["device"] = brand_and_model
                            self.modem_router["device_type"] = type_of_device
                            self.modem_router["status"] = "online"

                        elif (type_of_device == "Additional Router"):

                            self.additional_routers.append(
                                {"device": brand_and_model, "device_type": type_of_device, "status": "online", "provided_by": "", "can_bypass": ""})

                        elif (type_of_device == "Extender"):

                            self.extenders.append(
                                {"device": brand_and_model, "device_type": type_of_device, "status": "online", "provided_by": "", "can_bypass": ""})

                        elif (type_of_device == "Switch"):

                            self.switches.append({"device": brand_and_model, "device_type": type_of_device,
                                                 "status": "online", "provided_by": "", "can_bypass": ""})

                # if no, not all network devices show internet, what device don't have internet?
                if (all_network_devices_show_internet == "no"):

                    # Call what_status_and_who_provided function for each network device and assign relevant network device attributes to function's return value.
                    for brand_and_model, type_of_device in self.network_devices.items():

                        # what_status_and_who_provided - Working with these possible return values:
                        #
                        # if (device_type == "Main Router" or device_type == "Indoor ONT" or device_type == "ONT/Router" or device_type == "Modem" or device_type == "Modem/Router") or (device_type == "Additional Router" or device_type == "Extender" or device_type == "Switch"):
                        #     return {"device": brand_and_model, "device_type": device_type, "status": online_offline_or_na, "provided_by": device_provided_by, "can_bypass": ""}

                        print_responses(
                            can_check_network_device_lights=self.can_check_network_device_lights, all_network_devices_show_internet=all_network_devices_show_internet)

                        device = what_status_and_who_provided(
                            brand_and_model, type_of_device)

                        if (step_response == "exit"):
                            return

                        if (type_of_device == "Main Router"):

                            self.main_router = device

                        elif (type_of_device == "Indoor ONT"):

                            self.indoor_ont = device

                        elif (type_of_device == "ONT/Router"):

                            self.ont_router = device

                        elif (type_of_device == "Modem"):

                            self.modem = device

                        elif (type_of_device == "Modem/Router"):

                            self.modem_router = device

                        elif (type_of_device == "Additional Router"):

                            self.additional_routers.append(device)

                        elif (type_of_device == "Extender"):

                            self.extenders.append(device)

                        elif (type_of_device == "Switch"):

                            self.switches.append(device)

                # * Numbering steps after this line

                # * 1.1.  Figure out whether to bypass the main router, wire to some ont or modem, or wire to the wall jack
                #   NOTE: If any of the following conditions are true, assign self.can_bypass_or_wire to True
                #   NOTE: If no network devices saved, further functions might say "Wiring to wall jack" instead of "bypassing main router"
                #
                #   1.1.0. If main router is offline and nothing comes before it, and the main router can be bypassed
                if (self.main_router["status"] == "offline" and
                        (self.indoor_ont["status"] == "" and self.ont_router["status"] == "" and self.modem["status"] == "" and self.modem_router["status"] == "")):
                    step_response_sentence += "\n\nMain router is offline."
                    check_if_user_can_bypass_or_wire("main router to wall")

                #   1.1.1. If main router is offline but some indoor ont, ont/router, modem, modem/router is online, and the main router can be bypassed
                elif (self.main_router["status"] == "offline" and
                        (self.indoor_ont["status"] == "online" or self.ont_router["status"] == "online" or self.modem["status"] == "online" or self.modem_router["status"] == "online")):
                    find_online_network_device()

                    step_response_sentence += f"\n\nMain router is offline, but the {online_main_network_device} is online"
                    check_if_user_can_bypass_or_wire(
                        "main router to network device")

                #   1.1.2. If some indoor ont, ont/router, modem, modem/router is online and can be wired to, when no main router
                elif (self.main_router["status"] == "" and
                        (self.indoor_ont["status"] == "online" or self.ont_router["status"] == "online" or self.modem["status"] == "online" or self.modem_router["status"] == "online")):
                    find_online_network_device()

                    step_response_sentence += f"\n\n{online_main_network_device} is online."
                    check_if_user_can_bypass_or_wire("network device")

                #   1.1.3. If there's no kind of ont, modem, router, and service is not fixed wireless, can we wire directly to the wall jack
                elif (self.main_router["status"] == "" and
                        (self.indoor_ont["status"] == "" and self.ont_router["status"] == "" and self.modem["status"] == "" and self.modem_router["status"] == "") and
                        self.service != "Fixed Wireless"):
                    step_response_sentence += "\n\nThere's no network devices."
                    check_if_user_can_bypass_or_wire("wall jack")

                #   1.1.4. If the main network device, besides the main router, is offline
                elif (self.indoor_ont["status"] == "offline" or self.ont_router["status"] == "offline" or self.modem["status"] == "offline" or
                      self.modem_router["status"] == "offline"):
                    find_online_network_device()

                    step_response_sentence += f"\n\n{online_main_network_device} is offline."

                #   1.1.5. If main router is online
                elif (self.main_router["status"] == "online"):
                    step_response_sentence += "\n\nMain router is online."

                # * 1.2   Possibly run 'refer_or_escalate' function - Possible END of branch
                #   1.2.0. Determine whether to run 'refer_or_escalate' function
                #   NOTE: If self.can_bypass_or_wire is false, no device can be checked for internet
                #   NOTE: 'refer_or_escalate' is run here whenever we can't check a device internet

                # If (cannot bypass main router, wire to working network device, or wire to wall jack,
                #     the main network device, besides the main router, is offline

                if (self.can_bypass_or_wire == "no" or
                    (self.indoor_ont["status"] == "offline" or self.ont_router["status"] == "offline" or self.modem["status"] == "offline" or
                             self.modem_router["status"] == "offline")
                    ):
                    refer_or_escalate()

                    print_responses(
                        all_questions_answered=True, can_check_network_device_lights=self.can_check_network_device_lights, all_network_devices_show_internet=all_network_devices_show_internet)
                    return

                print_responses(
                    all_questions_answered=True, can_check_network_device_lights=self.can_check_network_device_lights, all_network_devices_show_internet=all_network_devices_show_internet)

            self.set_troubleshooting_steps()

        def check_devices():
            nonlocal step_response
            nonlocal step_response_sentence

            def print_responses(all_questions_answered=False, **kwargs):

                nonlocal step_response_sentence

                system.clear_prompt_or_terminal()

                print("\nEnter 'exit' at any time to exit prompt.\n\n")

                print("\nAdding To Ticket:\n")

                if (step_response_sentence == ""):
                    pass
                else:
                    print(step_response_sentence)

                print("\n----------------------------------\n\n\n")

                print("\nResponses:\n")

                if (len(kwargs) == 0):
                    pass
                else:
                    for key, value in kwargs.items():
                        if (key == "device"):
                            print(
                                "Device: " + value)
                        elif (key == "type_of_computer"):
                            if (value == ""):
                                pass
                            else:
                                print(
                                    "Type of computer: " + value)
                        elif (key == "name_of_device"):
                            if ("computer" not in value and value != "mobile device" and value != "TV"):
                                print(
                                    "Name of device: " + value)
                            else:
                                pass
                        elif (key == "how_device_is_connected"):
                            if (value == "bypass"):
                                print("Connected by: bypassing the main router")
                            elif (value == "wire"):
                                print("Connected by: wiring to a network device")
                            elif (value == "wifi"):
                                print("Connected by: wifi")
                        elif (key == "name_of_wifi_network"):
                            if (value == ""):
                                pass
                            else:
                                print("WiFi network: " + value)
                        elif (key == "is_internet_working"):
                            print("Internet is working: " + value)
                        elif (key == "ipv4_address"):
                            print("IPv4 Address: " + value)
                        elif (key == "default_gateway"):
                            print("Default Gateway: " + value)
                        elif (key == "device_has_internet_after_power_cycling"):
                            if (value == ""):
                                pass
                            else:
                                print("Internet after power cycling: " + value)

                print("\n----------------------------------\n\n\n")

                if (all_questions_answered == False):
                    print(
                        "\nAnswer the following questions to add this step:\n\n\n")
                else:
                    print("All questions answered!\n\n\n")

                    print("Adding step to ticket.",
                          end="", flush=True)

                    time.sleep(.70)
                    print(".", end="", flush=True)

                    time.sleep(.70)
                    print(".", end="", flush=True)

                    time.sleep(.70)

                    print()

            def check_computer_tv_mobile_or_other_device(device):

                nonlocal step_response
                nonlocal step_response_sentence

                # The wall jack or network devices where the internet first comes into
                self.possible_main_network_devices = [
                    self.indoor_ont, self.ont_router, self.modem, self.modem_router, self.main_router]
                # The wall jack or network devices that the main network device sends internet to
                self.possible_additional_network_devices = [
                    self.main_router, self.additional_routers, self.extenders]

                # * Assign below variables based on ethernet status
                self.can_bypass_or_wire = ""
                self.can_bypass_main_router = False
                self.can_wire_to_network_device = False
                self.can_wire_to_wall_jack = False

                # * Possible values: 'ethernet' or 'wifi'
                how_device_is_connected = ""

                # * Variable for when device connects over ethernet | Possbile values: 'wall jack', 'indoor ont', 'main router', etc
                what_device_is_wired_to = ""

                # * Variable for when device connects over WiFi
                name_of_wifi_network = ""

                # * Set to none when checking a device since this value should be reset when checking a new device
                self.last_checked_device_was_given_ip = None
                self.last_checked_device_is_online = None

                def refer_or_escalate():
                    nonlocal step_response_sentence

                    # NOTE: self.possible_main_network_devices = [self.indoor_ont, self.ont_router, self.modem, self.modem_router, self.main_router]
                    #
                    # NOTE: self.possible_additional_network_devices = [self.main_router, self.additional_routers, self.extenders]
                    #
                    # NOTE: self.names_of_possible_places_to_wire_devices_for_fiber = [
                    #            "Wall Jack", "Indoor ONT", "ONT/Router", "Main Router", "Additional Router", "Extender", "Switch"]
                    #
                    # NOTE: self.names_of_possible_places_to_wire_devices_for_non_fiber = [
                    #    "Wall Jack", "Modem", "Modem/Router", "Main Router", "Additional Router", "Extender", "Switch"]

                    # If last checked device is offline AND other devices are online (device issue) ...
                    if (self.last_checked_device_is_online == False and self.devices_online == True):
                        step_response_sentence += "\n\nDevice is offline even though other devices are online."
                        step_response_sentence += "\nRefer to oem/LT for device issue"

                        self.ticket_status = "Ticket Status: Problem resolved.\nReferred to oem/LT for device issue."

                    # If device is offline ...
                    elif (self.last_checked_device_is_online == False and self.last_checked_device_was_given_ip == False):

                        # * Confirm if there's an ONT or modem
                        ont_or_modem_is_saved = False

                        for network_device in self.possible_main_network_devices[:-1]:
                            if (network_device["status"] != ""):
                                ont_or_modem_is_saved = True
                                break

                        # * Lowercase the list of possible places to wire, for comparing
                        lowercase_names_of_possible_places_to_wire_devices = ""

                        if (self.service == "Fiber"):
                            lowercase_names_of_possible_places_to_wire_devices = [
                                name.lower() for name in self.names_of_possible_places_to_wire_devices_for_fiber]
                        else:
                            lowercase_names_of_possible_places_to_wire_devices = [name.lower(
                            ) for name in self.names_of_possible_places_to_wire_devices_for_non_fiber]

                        # * Below conditions for when device is connected over ethernet

                        # if wired to the wall jack ...
                        # if wired to some ONT or modem ...
                        # if wired to main router, there's no ont or modem, and the main router can't be bypassed ...
                        if ((self.can_wire_to_wall_jack == True) or
                            (what_device_is_wired_to in lowercase_names_of_possible_places_to_wire_devices[1:3]) or
                                (what_device_is_wired_to == "main router" and ont_or_modem_is_saved == False and (
                                    self.can_bypass_or_wire != "" and self.can_bypass_main_router == False))
                            ):
                            step_response_sentence += f"\n\nEscalate for no internet from {what_device_is_wired_to}"

                            self.ticket_status = f"Ticket Status: Problem resolved.\nEscalated for no internet coming from {what_device_is_wired_to}."

                    # If device is online ...
                    elif (self.last_checked_device_is_online == True):

                        first_offline_network_device = ""

                        # * Find the first offline main network device
                        for network_device in self.possible_main_network_devices:
                            if network_device["status"] == "offline":
                                first_offline_network_device = network_device
                                break

                        # * Find the first offline additional network device, if no offline main network device
                        if (first_offline_network_device == ""):

                            # Loop through self.additional_routers and self.extenders
                            for network_device_list in self.possible_additional_network_devices[1:]:
                                # If there's no saved device in network_device_list ...
                                if len(network_device_list) == 0:
                                    continue
                                # If there's at lease one saved device in network_device_list ...
                                else:
                                    # Check each network_device status in network_device_list
                                    for network_device in network_device_list:
                                        if network_device["status"] == "offline":
                                            first_offline_network_device = network_device
                                            break

                        if (first_offline_network_device != ""):
                            first_offline_network_device_name = first_offline_network_device[
                                "device"]
                            first_offline_network_device_type = first_offline_network_device[
                                "device_type"]
                            first_offline_network_device_provider = first_offline_network_device[
                                "provided_by"]

                        # * Below conditions for when device is connected over ethernet or WiFi

                        # If there's no offline main network device ...
                        if (first_offline_network_device == ""):
                            pass

                        # If the main network device is offline ...
                        else:

                            if (first_offline_network_device_provider == "service provider"):
                                step_response_sentence += f"\n\nEscalate for offline {first_offline_network_device_name} {first_offline_network_device_type}"
                                self.ticket_status = f"Ticket Status: Problem resolved.\nEscalated for offline {first_offline_network_device_name} {first_offline_network_device_type}."

                            elif (first_offline_network_device_provider == "third party"):
                                step_response_sentence += f"\n\nRefer to oem for offline {first_offline_network_device_name} {first_offline_network_device_type}"
                                self.ticket_status = f"Ticket Status: Problem resolved.\Referred to oem for offline {first_offline_network_device_name} {first_offline_network_device_type}."

                # * Function to prompt for IPv4 or default gateway address
                def prompt_for_address(type_of_address):

                    nonlocal step_response
                    nonlocal step_response_sentence

                    while (True):

                        # Change prompt depending on if checking for IPv4 or DG
                        if (type_of_address == "IPv4"):
                            address = input(
                                "What's the device's " + type_of_address + " address?\nEnter IPv4 address (or 'n/a' if can't find address): ").strip()
                        elif (type_of_address == "default gateway" or type_of_address == "router"):
                            address = input(
                                "What's the " + type_of_address + " IPv4 address?\nEnter IPv4 address (or 'n/a' if can't find address): ").strip()

                        if (address.lower() == "exit"):
                            step_response = "exit"
                            return
                        elif (address.lower() == "n/a"):
                            return address.lower()

                        try:
                            ipaddress.IPv4Address(address)
                        except ValueError:
                            print("\n" + address +
                                  " is not a valid IPv4 address.\n")
                            continue

                        break

                    return address

                if (device != "mobile device" and device != "tv"):
                    print_responses(device=device)

                # if device is a computer ...
                type_of_computer = ""

                if (device == "computer"):

                    # Check what type of computer is being checked
                    type_of_computer = check_for_a_or_b_or_c(
                        "What kind of computer is being checked?\nEnter “Windows”, “Mac”, or “Linux” to respond: ", "windows", "mac", "linux")
                    if (step_response == "exit"):
                        return

                # Display device being checked
                if (device == "other"):
                    name_of_device = input(
                        "What's the name of the device?\nEnter the device name to respond: ")
                    step_response_sentence = "Checking for internet on: " + name_of_device + " >\n"
                else:
                    if (device == "tv"):
                        name_of_device = device.upper()
                    elif (device == "computer"):
                        name_of_device = type_of_computer + " " + device
                    else:
                        name_of_device = device
                    step_response_sentence = "Checking for internet on a " + name_of_device + " >\n"

                print_responses(
                    device=device, type_of_computer=type_of_computer, name_of_device=name_of_device)

                # Check for how device connects to internet
                how_device_is_connected = check_for_a_or_b(
                    "Is the device connected over ethernet or WiFi?\nEnter 'ethernet' or 'wifi' to respond: ", "ethernet", "wifi")
                if (step_response == "exit"):
                    return

                # If device connects over ethernet ...

                print_responses(device=device, type_of_computer=type_of_computer,
                                name_of_device=name_of_device, how_device_is_connected=how_device_is_connected)

                if (how_device_is_connected == "ethernet"):

                    # NOTE: self.names_of_possible_places_to_wire_devices_for_fiber = ["Indoor ONT", "ONT/Router", "Main Router", "Additional Router", "Extender", "Switch"]
                    # NOTE: self.names_of_possible_places_to_wire_devices_for_non_fiber = ["Modem", "Modem/Router", "Main Router", "Additional Router", "Extender", "Switch"]

                    self.can_bypass_or_wire = True

                    print("Which of the following is the device connected to:\n")

                    # If service is Fiber ...
                    if (self.service == "Fiber"):

                        # Print all possible network devices user can wire to | Print wall jack as an option too
                        print(
                            "Wall Jack\nIndoor ONT\nONT/Router\nMain Router\nAdditional Router\nExtender\nSwitch\n\n\n")

                        # Prompt user to enter a value from the above list
                        what_device_is_wired_to = prompt_for_value_in_list(
                            self.names_of_possible_places_to_wire_devices_for_fiber)
                        if (step_response == "exit"):
                            what_device_is_wired_to = ""
                            return

                    # If service is not Fiber ...
                    else:

                        # Print all possible network devices user can wire to | Print wall jack as an option too
                        print(
                            "Wall Jack\nModem\nModem/Router\nMain Router\nAdditional Router\nExtender\nSwitch\n\n\n")

                        # Prompt user to enter a value from the above list
                        what_device_is_wired_to = prompt_for_value_in_list(
                            self.names_of_possible_places_to_wire_devices_for_non_fiber)
                        if (step_response == "exit"):
                            what_device_is_wired_to = ""
                            return

                    # If user is wiring to wall jack ...
                    if (what_device_is_wired_to == "wall jack"):
                        self.can_wire_to_wall_jack = True
                    # If user is wiring to some network device besides the main router ...
                    else:
                        self.can_wire_to_network_device = True

                    # If a main router was saved ...
                    if (self.main_router["status"] != ""):
                        # Declare that user is bypassing it ...
                        self.can_bypass_main_router = True

                # If device connects over WiFi ...
                elif (how_device_is_connected == "wifi"):
                    how_device_is_connected = "wifi"

                    # Check what WiFi network device connects to
                    name_of_wifi_network = input(
                        "What WiFi network is the device connected to?\nEnter name of WiFi network to respond: ").strip()

                print_responses(device=device, type_of_computer=type_of_computer,
                                name_of_device=name_of_device, how_device_is_connected=how_device_is_connected, name_of_wifi_network=name_of_wifi_network)

                # Check if internet is working
                is_internet_working = check_for_a_or_b(
                    "Is the internet working?\nEnter 'yes' or 'no' to respond: ", "yes", "no")
                if (step_response == "exit"):
                    return

                # if internet is working ...
                if (is_internet_working == "yes"):

                    if (how_device_is_connected == "ethernet"):
                        step_response_sentence += f"\nInternet is working when wired to the {what_device_is_wired_to}"

                    elif (how_device_is_connected == "wifi" or device == "mobile device"):
                        step_response_sentence += f"\nInternet is working when connected to SSID of: {name_of_wifi_network}"

                    self.last_checked_device_is_online = True
                    self.devices_online = True

                    refer_or_escalate()

                    print_responses(all_questions_answered=True, device=device, type_of_computer=type_of_computer,
                                    name_of_device=name_of_device, how_device_is_connected=how_device_is_connected, name_of_wifi_network=name_of_wifi_network, is_internet_working=is_internet_working)

                # if internet is not working ...
                elif (is_internet_working == "no"):

                    self.last_checked_device_is_online = False
                    self.last_checked_device_was_given_ip = None

                    device_has_self_assigned_ip = None

                    if (how_device_is_connected == "ethernet"):
                        step_response_sentence += f"\nNo internet when wired to the {what_device_is_wired_to}"

                    elif (how_device_is_connected == "wifi" or device == "mobile device"):
                        step_response_sentence += f"\nNo internet when connected to SSID of: {name_of_wifi_network}"

                    print_responses(device=device, type_of_computer=type_of_computer,
                                    name_of_device=name_of_device, how_device_is_connected=how_device_is_connected,
                                    name_of_wifi_network=name_of_wifi_network, is_internet_working=is_internet_working)

                    # Prompt for IPv4 address
                    ipv4_address = prompt_for_address("IPv4")
                    if (step_response == "exit"):
                        return

                    step_response_sentence += "\nIPv4 address: " + \
                        ipv4_address

                    print_responses(device=device, type_of_computer=type_of_computer,
                                    name_of_device=name_of_device, how_device_is_connected=how_device_is_connected,
                                    name_of_wifi_network=name_of_wifi_network, is_internet_working=is_internet_working,
                                    ipv4_address=ipv4_address)

                    # Prompt for router/default gateway address
                    if (device == "computer" and type_of_computer == "mac"):
                        default_gateway = prompt_for_address("router")
                    else:
                        default_gateway = prompt_for_address("default gateway")

                    if (step_response == "exit"):
                        return

                    # Specify whether device was given a valid IP address
                    if (ipv4_address == "n/a" and default_gateway == "n/a"):
                        self.last_checked_device_was_given_ip = None
                    elif (ipv4_address.startswith("169.254.")):
                        self.last_checked_device_was_given_ip = False
                    else:
                        self.last_checked_device_was_given_ip = True

                    step_response_sentence += "\nDefault Gateway: " + \
                        default_gateway

                    print_responses(device=device, type_of_computer=type_of_computer,
                                    name_of_device=name_of_device, how_device_is_connected=how_device_is_connected,
                                    name_of_wifi_network=name_of_wifi_network, is_internet_working=is_internet_working,
                                    ipv4_address=ipv4_address, default_gateway=default_gateway)

                    # If device's IPv4 address is self-assigned ...
                    if (ipv4_address.startswith("169.254.")):
                        self.last_checked_device_is_online = False

                        device_has_self_assigned_ip = True

                        if (device == "mobile device"):
                            pass
                        elif (device == "computer"):
                            # Advise to renew IP address
                            print(
                                "Device's self assigned IPv4 address will not work\nFollow these instructions to renew the IP address:\n")

                            if (type_of_computer == "windows"):
                                # Show instructions for renewing IP on Windows
                                print("On Windows: \n1. Open Command Prompt")
                                print(
                                    "2. Run 'ipconfig /release' to release the current IP \n3. Run 'ipconfig /renew' to renew the IP\n\n")

                            elif (type_of_computer == "mac"):
                                # Show instructions for renewing IP on Mac
                                print("On macOS: \n1. Open System Preferences")
                                print(
                                    "2. Select 'Network' \n3. Select current interface \n4. Select 'Details' \n5. Select 'TCP/IP' \n6. Select 'Renew DHCP Lease'\n\n")

                                # Show instructions for renewing IP on older versions of Mac
                                print(
                                    "\nOn older versions of macOS: \n1. Open System Preferences")
                                print(
                                    "2. Select 'Network' \n3. Select current interface \n4. Select 'Advanced' \n5. Select 'TCP/IP' \n6. Select 'Renew DHCP Lease'\n\n")

                            elif (type_of_computer == "linux"):
                                # Show instructions for renewing IP on Linux
                                print(
                                    "On Linux: \n1. Press CTRL+ALT+T to launch Terminal")
                                print(
                                    "2. Run 'sudo dhclient – r' to release the current IP \n3. Run 'sudo dhclient' to renew the IP\n\n")

                            print()

                            ipv4_address = ""
                            default_gateway = ""

                            # Prompt for IPv4 address
                            ipv4_address = prompt_for_address("IPv4")

                            if (step_response == "exit"):
                                return

                            step_response_sentence += "\n\nReleased and renewed IP addresses"
                            step_response_sentence += "\nIPv4 address: " + ipv4_address

                            print_responses(device=device, type_of_computer=type_of_computer,
                                            name_of_device=name_of_device, how_device_is_connected=how_device_is_connected,
                                            name_of_wifi_network=name_of_wifi_network, is_internet_working=is_internet_working,
                                            ipv4_address=ipv4_address)

                            # Prompt for router/default gateway address
                            if (type_of_computer == "mac"):
                                default_gateway = prompt_for_address("router")
                            else:
                                default_gateway = prompt_for_address(
                                    "default gateway")

                            if (step_response == "exit"):
                                return

                            # Specify whether device was given a valid IP address
                            if (ipv4_address == "n/a" and default_gateway == "n/a"):
                                self.last_checked_device_was_given_ip = None
                            elif (ipv4_address.startswith("169.254.")):
                                self.last_checked_device_was_given_ip = False
                            else:
                                self.last_checked_device_was_given_ip = True

                            step_response_sentence += "\nDefault Gateway: " + default_gateway

                            # if there's still a self-assigned IPv4 address ...
                            if (ipv4_address.startswith("169.254.")):
                                self.last_checked_device_is_online = False

                                device_has_self_assigned_ip = True

                                step_response_sentence += "\n\nDevice is still getting a self assigned IPv4 address."

                                print_responses(device=device, type_of_computer=type_of_computer,
                                                name_of_device=name_of_device, how_device_is_connected=how_device_is_connected,
                                                name_of_wifi_network=name_of_wifi_network, is_internet_working=is_internet_working,
                                                ipv4_address=ipv4_address, default_gateway=default_gateway)

                            # if there's a non-self-assigned IPv4 address ...
                            elif (not (ipv4_address.startswith("169.254."))):
                                self.last_checked_device_is_online = False

                                device_has_self_assigned_ip = False

                                print_responses(device=device, type_of_computer=type_of_computer,
                                                name_of_device=name_of_device, how_device_is_connected=how_device_is_connected,
                                                name_of_wifi_network=name_of_wifi_network, is_internet_working=is_internet_working,
                                                ipv4_address=ipv4_address, default_gateway=default_gateway)

                                # Check if internet is working
                                is_internet_working = check_for_a_or_b(
                                    "Is the internet working?\nEnter 'yes' or 'no' to respond: ", "yes", "no")
                                if (step_response == "exit"):
                                    return

                                # if internet is working ...
                                if (is_internet_working == "yes"):
                                    step_response_sentence += "\n\nInternet working now."

                                    self.devices_online = True

                                    self.last_checked_device_is_online = True
                                    device_has_self_assigned_ip = False

                                    print_responses(all_questions_answered=True, device=device, type_of_computer=type_of_computer,
                                                    name_of_device=name_of_device, how_device_is_connected=how_device_is_connected,
                                                    name_of_wifi_network=name_of_wifi_network,
                                                    ipv4_address=ipv4_address, default_gateway=default_gateway, is_internet_working=is_internet_working)

                                    return

                                # if internet is not working ...
                                if (is_internet_working == "no"):

                                    self.last_checked_device_is_online = False

                                    device_has_self_assigned_ip = False

                                    step_response_sentence += "\n\nInternet still not working even with non-self-assigned IP address."

                                    print_responses(device=device, type_of_computer=type_of_computer,
                                                    name_of_device=name_of_device, how_device_is_connected=how_device_is_connected,
                                                    name_of_wifi_network=name_of_wifi_network,
                                                    ipv4_address=ipv4_address, default_gateway=default_gateway, is_internet_working=is_internet_working)

                    device_has_internet_after_power_cycling = ""

                    # if devices are online but device being checked is offline ...
                    if (self.devices_online == True and self.last_checked_device_is_online == False):

                        # Power cycle device
                        device_has_internet_after_power_cycling = check_for_a_or_b(
                            "Is the internet working after power cycling the devive?\nEnter 'yes' or 'no': ", "yes", "no")
                        if (step_response == "exit"):
                            return

                        if (device_has_internet_after_power_cycling == "yes"):

                            self.devices_online = True

                            self.last_checked_device_is_online = True

                            step_response_sentence += "\n\nInternet working after power cycling device."

                        elif (device_has_internet_after_power_cycling == "no"):

                            self.last_checked_device_is_online = False

                            step_response_sentence += "\n\nInternet still not working even after power cycling device."

                    # * Numbering steps after this line

                    # * 1.1    Determine whether to run 'refer_or_escalate' function
                    #          NOTE: Function is used when problem is a device or network device.
                    #
                    #   1.1.0. If last checked device is offline AND other devices are online (device issue),
                    #              all devices are offline AND device has invalid IP (network device or ISP issue)

                    # Possible END of branch
                    refer_or_escalate()

                    print_responses(all_questions_answered=True, device=device, type_of_computer=type_of_computer,
                                    name_of_device=name_of_device, how_device_is_connected=how_device_is_connected,
                                    name_of_wifi_network=name_of_wifi_network,
                                    ipv4_address=ipv4_address, default_gateway=default_gateway, is_internet_working=is_internet_working,
                                    device_has_internet_after_power_cycling=device_has_internet_after_power_cycling)

            print_responses()

            # Ask if checking for internet on a phone, computer, TV or other device.
            check_which_device = input(
                "What device is being checked for internet?\nEnter 'Mobile Device', 'Computer', 'TV', or 'Other' to respond: ").lower().strip()

            if (check_which_device == "exit"):

                step_response = "exit"
                return

            while (check_which_device != "mobile device" and check_which_device != "computer" and check_which_device != "tv" and check_which_device != "other"):
                print(
                    "\nInvalid response - Neither 'Mobile Device', 'Computer', 'TV', 'Other' were entered.")

                check_which_device = input(
                    "\nEnter 'Mobile Device', 'Computer', 'TV', or 'Other' to respond: ").lower().strip()

                if (check_which_device == "exit"):

                    step_response = "exit"
                    return

            # Checking for internet on a mobile device.
            if (check_which_device == "mobile device"):
                check_computer_tv_mobile_or_other_device(
                    check_which_device)

                if (step_response == "exit"):
                    return

            # Checking for internet on a computer.
            elif (check_which_device == "computer"):
                check_computer_tv_mobile_or_other_device(
                    check_which_device)

                if (step_response == "exit"):
                    return

            # Checking for internet on a TV.
            elif (check_which_device == "tv"):
                check_computer_tv_mobile_or_other_device(
                    check_which_device)

                if (step_response == "exit"):
                    return

            # Checking for internet on some other device.
            elif (check_which_device == "other"):
                check_computer_tv_mobile_or_other_device(
                    check_which_device)

                if (step_response == "exit"):
                    return

            self.set_troubleshooting_steps()

        def run_ping_tests():
            nonlocal step_response
            nonlocal step_response_sentence

            def print_responses(all_questions_answered=False, running_pings=False):

                nonlocal step_response_sentence

                system.clear_prompt_or_terminal()

                print("\nEnter 'exit' at any time to exit prompt.\n\n")
                print("\nNOTE:\nSpeeds are most accurate when bypassing the main router.\nIf main router can't be bypassed, wiring to a network device is second best.\nIf a device can't be wired at all, it's okay to use 5G WiFi or 2.4G if there's no 5G.\n\n")

                print("\nAdding To Ticket:\n")

                if (step_response_sentence == ""):
                    pass
                else:
                    print(step_response_sentence)

                print("\n----------------------------------\n\n\n")

                if (all_questions_answered == False):
                    if (running_pings == True):
                        print(
                            "Enter 'Done' to exit prompt and save ping statistics to ticket.\n")
                    else:
                        print(
                            "\nAnswer the following questions to add this step:\n\n\n")

                else:
                    print("All questions answered!\n\n\n")

                    print("Adding step to ticket.",
                          end="", flush=True)

                    time.sleep(.70)
                    print(".", end="", flush=True)

                    time.sleep(.70)
                    print(".", end="", flush=True)

                    time.sleep(.70)

                    print()

            print_responses()

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

            # if a computer can be used, run ping tests on it
            if (can_be_used == "yes"):

                print_responses()

                # How is the computer connected to the internet?
                how_computer_is_connected = input(
                    "Is the computer bypassing the main router, wiring to a network device, or using Wi-Fi?\nEnter 'bypass', 'wire', or 'wifi' to respond: ").lower().strip()

                if (how_computer_is_connected == "exit"):

                    step_response = "exit"
                    return

                while (how_computer_is_connected != "bypass" and how_computer_is_connected != "wire" and how_computer_is_connected != "wifi"):
                    print(
                        "\nInvalid response - Neither 'Bypass', 'Wire', or 'WiFi' were entered.")

                    how_computer_is_connected = input(
                        "\nEnter 'bypass', 'wire', or 'wifi' to respond: ").lower().strip()

                    if (how_computer_is_connected == "exit"):

                        step_response = "exit"
                        return

                if (how_computer_is_connected == "bypass"):
                    step_response_sentence = "Pings on computer bypassing the main router >"

                elif (how_computer_is_connected == "wire"):
                    step_response_sentence = "Pings on computer wired to a network device >"

                elif (how_computer_is_connected == "wifi"):
                    name_of_wifi_network = input(
                        "\nWhat WiFi network is the computer connected to?\nEnter name of WiFi network to respond: ").strip()
                    step_response_sentence = "Pings on computer connected to SSID of: " + name_of_wifi_network

                # Issue when at least 2.5% of packets are lost
                packets_sent = None
                packets_lost = None

                min_value = None
                max_value = None

                # Issue when avg is at least 100
                avg_value = None

                # Holds lost values from all ping tests
                packets_lost_list = []

                # Holds avg values from all ping tests
                avg_value_list = []

                def check_for_valid_number(number):
                    # Returns a number that can be converted and that's not less than 0
                    # Used for: sent, lost, min, max, avg

                    try:
                        # Check if user entered a number
                        number = int(number)
                    except ValueError:
                        print("\nInvalid response - a number was not entered.\n")
                        return number

                    if (number < 0):
                        print(
                            "\nInvalid response - number must be greater than or equal to 0.\n")

                    return number

                def set_ping_statistics(statistic):
                    # Function called when prompted for min, max, avg, and lost

                    nonlocal packets_sent
                    nonlocal packets_lost
                    nonlocal min_value
                    nonlocal max_value
                    nonlocal avg_value

                    nonlocal how_computer_is_connected

                    nonlocal packets_lost_list

                    nonlocal step_response
                    step_response = None

                    nonlocal step_response_sentence

                    print_responses(running_pings=True)

                    if (statistic == "host"):
                        host = input("What host is being pinged? ").strip()

                        if (host.lower() == "exit"):
                            step_response = "exit"
                            return
                        elif (host.lower() == "done"):
                            step_response = "done"
                            return
                        elif (host.lower() == "n/a"):
                            step_response = "n/a"
                            return

                        step_response_sentence += "\n\nPinging Host: " + host

                    if (statistic == "sent"):

                        packets_sent = ""

                        while (type(packets_sent) != int or packets_sent < 0):

                            packets_sent = input(
                                "How many packets are being sent?\nEnter either a number or 'n/a': ").strip()

                            if (packets_sent.lower() == "exit"):
                                step_response = "exit"
                                return
                            elif (packets_sent.lower() == "done"):
                                step_response = "done"
                                return
                            elif (packets_sent.lower() == "n/a"):
                                step_response = "n/a"
                                step_response_sentence += "\nSent: " + \
                                    packets_sent
                                return

                            packets_sent = check_for_valid_number(packets_sent)

                        step_response_sentence += "\nSent: " + \
                            str(packets_sent)

                    if (statistic == "lost"):

                        packets_lost = ""

                        while (type(packets_lost) != int or packets_lost < 0):

                            packets_lost = input(
                                "How many packets were lost?\nEnter either a number or 'n/a': ").strip()

                            if (packets_lost.lower() == "exit"):
                                step_response = "exit"
                                return
                            elif (packets_lost.lower() == "done"):
                                step_response = "done"
                                return
                            elif (packets_lost.lower() == "n/a"):
                                step_response = "n/a"
                                step_response_sentence += "\nLost: " + packets_lost
                                return

                            packets_lost = check_for_valid_number(packets_lost)

                            if (type(packets_lost) == int):
                                if (packets_lost > packets_sent):
                                    print(
                                        "\nInvalid response - Cannot be more lost packets than packets sent.\n")
                                    packets_lost = ""

                        packets_lost_list.append(packets_lost)

                        step_response_sentence += "\nLost: " + \
                            str(packets_lost)

                    if (statistic == "min"):

                        min_value = ""

                        while (type(min_value) != int or min_value < 0):

                            min_value = input(
                                "What's the min ping speed?\nEnter either a number or 'n/a': ").strip()

                            if (min_value.lower() == "exit"):
                                step_response = "exit"
                                return
                            elif (min_value.lower() == "done"):
                                step_response = "done"
                                return
                            elif (min_value.lower() == "n/a"):
                                step_response = "n/a"
                                step_response_sentence += "\nMin: " + min_value
                                return

                            min_value = check_for_valid_number(min_value)

                        step_response_sentence += "\nMin: " + \
                            str(min_value) + "ms"

                    if (statistic == "max"):

                        max_value = ""

                        while (type(max_value) != int or max_value < 0):

                            max_value = input(
                                "What's the max ping speed?\nEnter either a number or 'n/a': ").strip()

                            if (max_value.lower() == "exit"):
                                step_response = "exit"
                                return
                            elif (max_value.lower() == "done"):
                                step_response = "done"
                                return
                            elif (max_value.lower() == "n/a"):
                                step_response = "n/a"
                                step_response_sentence += "\nMax: " + max_value
                                return

                            max_value = check_for_valid_number(max_value)

                        step_response_sentence += "\nMax: " + \
                            str(max_value) + "ms"

                    if (statistic == "avg"):

                        avg_value = ""

                        while (type(avg_value) != int or avg_value < 0):

                            avg_value = input(
                                "What's the avg ping speed?\nEnter either a number or 'n/a': ").strip()

                            if (avg_value.lower() == "exit"):
                                step_response = "exit"
                                return
                            elif (avg_value.lower() == "done"):
                                step_response = "done"
                                return
                            elif (avg_value.lower() == "n/a"):
                                step_response = "n/a"
                                step_response_sentence += "\nAvg: " + avg_value
                                return

                            avg_value = check_for_valid_number(avg_value)

                        avg_value_list.append(avg_value)

                        step_response_sentence += "\nAvg: " + \
                            str(avg_value) + "ms"

                # Run ping tests:

                while (True):

                    set_ping_statistics("host")
                    if (step_response == "exit"):
                        return
                    elif (step_response == "done"):
                        break
                    elif (step_response == "n/a"):
                        pass

                    set_ping_statistics("sent")
                    if (step_response == "exit"):
                        return
                    elif (step_response == "done"):
                        break
                    elif (step_response == "n/a"):
                        pass

                    set_ping_statistics("lost")
                    if (step_response == "exit"):
                        return
                    elif (step_response == "done"):
                        break
                    elif (step_response == "n/a"):
                        pass

                    set_ping_statistics("min")
                    if (step_response == "exit"):
                        return
                    elif (step_response == "done"):
                        break
                    elif (step_response == "n/a"):
                        pass

                    set_ping_statistics("max")
                    if (step_response == "exit"):
                        return
                    elif (step_response == "done"):
                        break
                    elif (step_response == "n/a"):
                        pass

                    set_ping_statistics("avg")
                    if (step_response == "exit"):
                        return
                    elif (step_response == "done"):
                        break
                    elif (step_response == "n/a"):
                        pass

                # Inform if more than 2% of sent packets were lost or avg values are bad

                for packet in packets_lost_list:
                    if (packet >= (packets_sent * .025)):
                        self.significant_packet_loss = True
                        step_response_sentence += "\n\nSignificant packet loss while pinging."

                        break

                for value in avg_value_list:
                    if (value >= 100):
                        self.significant_latency = True
                        step_response_sentence += "\n\nSignificant latency while pinging."

                        break

                print_responses(all_questions_answered=True)

            # if a computer cannot be used, mention that and do nothing else
            if (can_be_used == "no"):
                step_response_sentence = "Can't run ping tests - No computer can be used."

                print_responses(all_questions_answered=True)

        def run_speed_tests():
            nonlocal step_response
            nonlocal step_response_sentence

            def run_speed_test_on_computer():

                nonlocal step_response
                nonlocal step_response_sentence

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

            def run_speed_test_on_mobile_device():

                nonlocal step_response
                nonlocal step_response_sentence

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

            print("\nEnter 'exit' at any time to exit prompt.\n\n")
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

            # If user is running a speed test on a computer
            if (running_test_on_which_device == "computer"):
                run_speed_test_on_computer()

                if (step_response == "exit"):
                    return

            # If user is running a speed test on a mobile device
            if (running_test_on_which_device == "mobile device"):
                run_speed_test_on_mobile_device()

                if (step_response == "exit"):
                    return

        def check_ont():
            nonlocal step_response
            nonlocal step_response_sentence

            def print_responses(all_questions_answered=False, checking_ont_lights=False, **kwargs):

                nonlocal step_response_sentence

                system.clear_prompt_or_terminal()

                print("\nEnter 'exit' at any time to exit prompt.\n\n")

                print("\nAdding To Ticket:\n")

                if (step_response_sentence == ""):
                    pass
                else:
                    print(step_response_sentence)

                print("\n----------------------------------\n\n\n")

                print("\nResponses:\n")

                if (len(kwargs) == 0):
                    pass
                else:
                    for key, value in kwargs.items():
                        if (key == "can_check_ont"):
                            print("Can check ONT: " + value)

                print("\n----------------------------------\n\n\n")

                if (all_questions_answered == False):
                    if (checking_ont_lights == True):
                        print(
                            "\nONT information will be displayed in the following example format:\n")

                        print(
                            "ONT:\nPower: Amber - Solid\nWAN: Amber - Flashing")

                        print(
                            "\n\nEnter “done” when all lights are documented.\n\n\n")
                    else:
                        print(
                            "\nAnswer the following questions to add this step:\n\n\n")
                else:
                    print("All questions answered!\n\n\n")

                    print("Adding step to ticket.",
                          end="", flush=True)

                    time.sleep(.70)
                    print(".", end="", flush=True)

                    time.sleep(.70)
                    print(".", end="", flush=True)

                    time.sleep(.70)

                    print()

            print_responses()

            if (self.can_check_ont == None or self.can_check_ont == "no"):
                self.can_check_ont = check_for_a_or_b(
                    "Can the ONT be checked? Enter “yes” or “no” to respond: ", "yes", "no")

                # if the ONT cannot be checked, mention that and do nothing else
                if (self.can_check_ont == "no"):
                    step_response_sentence = "ONT cannot be checked."

                    print_responses(all_questions_answered=True,
                                    can_check_ont=self.can_check_ont)

            # if ONT can be checked, check the ONT lights
            if (self.can_check_ont == "yes"):

                step_response_sentence = "ONT"

                document_lights_or_cabling("lights", print_responses)

                print_responses(all_questions_answered=True,
                                can_check_ont=self.can_check_ont)

            self.set_troubleshooting_steps()

        def check_battery_backup():

            nonlocal step_response
            nonlocal step_response_sentence

            # Variable from function: check_battery_backup
            battery_backup_can_be_checked = ""

            # Variable from function: check_battery_backup > check_battery_backup_power
            battery_backup_has_power = ""

            # Variables from function: check_battery_backup > check_battery_backup_power > check_battery_backup_outlet
            can_other_device_plug_into_other_outlet_port = ""
            is_other_device_getting_power = ""
            can_battery_backup_plug_into_other_port = ""
            does_battery_backup_have_power_in_other_port = ""

            # Variables from function: check_battery_backup > check_battery_backup_power > check_gcfi_reset_button
            can_nearby_gfci_reset_button_be_pressed = ""
            does_pressing_reset_give_power = ""

            # Variables from function: check_battery_backup > check_battery_backup_power > check_working_outlet
            can_battery_backup_wire_to_working_outlet = ""
            is_there_power_after_wiring_to_other_outlet = ""

            # Variables from function: check_battery_backup > check_breaker_box
            can_breaker_box_be_checked = ""
            are_any_breakers_tripped_or_off = ""
            does_resetting_breakers_give_battery_backup_power = ""

            def print_responses(all_questions_answered=False, checking_battery_backup_lights=False, **kwargs):

                nonlocal step_response_sentence

                system.clear_prompt_or_terminal()

                print("\nEnter 'exit' at any time to exit prompt.\n\n")

                print("\nAdding To Ticket:\n")

                if (step_response_sentence == ""):
                    pass
                else:
                    print(step_response_sentence)

                print("\n----------------------------------\n\n\n")

                if (checking_battery_backup_lights == False):
                    print("\nResponses:\n")

                    if (len(kwargs) == 0):
                        pass
                    else:
                        for key, value in kwargs.items():

                            # Variable from function: check_battery_backup
                            if (key == "battery_backup_can_be_checked"):
                                print("Can check battery backup: " + value)

                            # Variable from function: check_battery_backup > check_battery_backup_power
                            elif (key == "battery_backup_has_power"):
                                if (value == ""):
                                    pass
                                else:
                                    print("Battery backup has power: " + value)

                            # Variables from function: check_battery_backup > check_battery_backup_power > check_battery_backup_outlet
                            elif (key == "can_other_device_plug_into_other_outlet_port"):
                                if (value == ""):
                                    pass
                                else:
                                    print(
                                        "Other device can plug into other outlet port: " + value)
                            elif (key == "is_other_device_getting_power"):
                                if (value == ""):
                                    pass
                                else:
                                    print(
                                        "Other device is getting power: " + value)
                            elif (key == "can_battery_backup_plug_into_other_port"):
                                if (value == ""):
                                    pass
                                else:
                                    print(
                                        "Can battery backup plug into outlet's other port: " + value)
                            elif (key == "does_battery_backup_have_power_in_other_port"):
                                if (value == ""):
                                    pass
                                else:
                                    print(
                                        "Battery backup has power in other port: " + value)

                            # Variables from function: check_battery_backup > check_battery_backup_power > check_gcfi_reset_button
                            elif (key == "can_nearby_gfci_reset_button_be_pressed"):
                                if (value == ""):
                                    pass
                                else:
                                    print(
                                        "Nearby GCFI button can be pressed: " + value)
                            elif (key == "does_pressing_reset_give_power"):
                                if (value == ""):
                                    pass
                                else:
                                    print(
                                        "Pressing reset button gives battery backup power: " + value)

                            # Variables from function: check_battery_backup > check_battery_backup_power > check_working_outlet
                            elif (key == "can_battery_backup_wire_to_working_outlet"):
                                if (value == ""):
                                    pass
                                else:
                                    print(
                                        "Can battery backup wire to working outlet: " + value)
                            elif (key == "is_there_power_after_wiring_to_other_outlet"):
                                if (value == ""):
                                    pass
                                else:
                                    print(
                                        "Battery backup has power after wiring to working outlet: " + value)

                            # Variables from function: check_battery_backup > check_breaker_box
                            elif (key == "can_breaker_box_be_checked"):
                                if (value == ""):
                                    pass
                                else:
                                    print("Can breaker box be checked " + value)
                            elif (key == "are_any_breakers_tripped_or_off"):
                                if (value == ""):
                                    pass
                                else:
                                    print(
                                        "Are any breakers tripped or off: " + value)
                            elif (key == "does_resetting_breakers_give_battery_backup_power"):
                                if (value == ""):
                                    pass
                                else:
                                    print(
                                        "Does resetting breakers give battery backup power: " + value)

                            # Variable assigned in every function
                            elif (key == "battery_backup_status"):
                                if (value == ""):
                                    pass
                                else:
                                    print("Battery backup status " + value)

                    print("\n----------------------------------\n\n\n")
                else:
                    pass

                if (all_questions_answered == False):
                    if (checking_battery_backup_lights == True):
                        print(
                            "\nBattery backup information will be displayed in the following example format:\n")

                        print(
                            "Battery Backup:\nAC: Amber - Solid\nDC: Green - Solid")

                        print(
                            "\n\nEnter “done” when all lights are documented.\n\n\n")
                    else:
                        print(
                            "\nAnswer the following questions to add this step:\n\n\n")
                else:
                    print("All questions answered!\n\n\n")

                    print("Adding step to ticket.",
                          end="", flush=True)

                    time.sleep(.70)
                    print(".", end="", flush=True)

                    time.sleep(.70)
                    print(".", end="", flush=True)

                    time.sleep(.70)

                    print()

            # Check battery backup power
            def check_battery_backup_power():

                nonlocal step_response
                nonlocal step_response_sentence

                # Variable from function: check_battery_backup > check_battery_backup_power
                nonlocal battery_backup_has_power

                # Variables from function: check_battery_backup > check_battery_backup_power > check_battery_backup_outlet
                nonlocal can_other_device_plug_into_other_outlet_port
                nonlocal is_other_device_getting_power
                nonlocal can_battery_backup_plug_into_other_port
                nonlocal does_battery_backup_have_power_in_other_port

                # Variables from function: check_battery_backup > check_battery_backup_power > check_gcfi_reset_button
                nonlocal can_nearby_gfci_reset_button_be_pressed
                nonlocal does_pressing_reset_give_power

                # Variables from function: check_battery_backup > check_battery_backup_power > check_working_outlet
                nonlocal can_battery_backup_wire_to_working_outlet
                nonlocal is_there_power_after_wiring_to_other_outlet

                # Check if the other port of battery backup's outlet can be tested
                def check_battery_backup_outlet():

                    nonlocal step_response
                    nonlocal step_response_sentence

                    # Variables from function: check_battery_backup_outlet
                    nonlocal can_other_device_plug_into_other_outlet_port
                    nonlocal is_other_device_getting_power
                    nonlocal can_battery_backup_plug_into_other_port
                    nonlocal does_battery_backup_have_power_in_other_port

                    print_responses(battery_backup_can_be_checked=battery_backup_can_be_checked,
                                    battery_backup_has_power=battery_backup_has_power)

                    # Check if the other port of battery backup's outlet can be tested
                    can_other_device_plug_into_other_outlet_port = check_for_a_or_b(
                        "Can some other device plug into the other port of the outlet used by the battery backup?\nEnter “yes” or “no”: ", "yes", "no")
                    if (step_response == "exit"):
                        return

                    # If no other device can be plugged into other outlet port ...
                    if (can_other_device_plug_into_other_outlet_port == "no"):
                        step_response_sentence += "\nNo other device can be plugged into outlet."

                    # If some other device can be plugged into other outlet port ...
                    elif (can_other_device_plug_into_other_outlet_port == "yes"):

                        print_responses(battery_backup_can_be_checked=battery_backup_can_be_checked,
                                        battery_backup_has_power=battery_backup_has_power,
                                        can_other_device_plug_into_other_outlet_port=can_other_device_plug_into_other_outlet_port)

                        # Check device for power
                        is_other_device_getting_power = check_for_a_or_b(
                            "Is the other device getting power?\nEnter “yes” or “no”: ", "yes", "no")
                        if (step_response == "exit"):
                            return

                        # if some other device does not get power from other outlet port ...
                        if (is_other_device_getting_power == "no"):
                            step_response_sentence += "\nSome other device is not getting power in the same outlet used by battery backup."

                        # if some other device gets power from other outlet port ...
                        elif (is_other_device_getting_power == "yes"):
                            step_response_sentence += "\nSome other device is getting power in the same outlet used by battery backup."

                            print_responses(battery_backup_can_be_checked=battery_backup_can_be_checked,
                                            battery_backup_has_power=battery_backup_has_power,
                                            can_other_device_plug_into_other_outlet_port=can_other_device_plug_into_other_outlet_port,
                                            is_other_device_getting_power=is_other_device_getting_power)

                            # Check if battery backup gets power from other port
                            can_battery_backup_plug_into_other_port = check_for_a_or_b(
                                "Can the battery backup plug into the other outlet port?\nEnter “yes” or “no” to respond: ", "yes", "no")
                            if (step_response == "exit"):
                                return

                            # If battery backup cannot be plugged into other port ...
                            if (can_battery_backup_plug_into_other_port == "no"):
                                step_response_sentence += "\nBattery backup cannot be plugged into outlet's other port."

                            # If battery backup can be plugged into other port ...
                            elif (can_battery_backup_plug_into_other_port == "yes"):

                                print_responses(battery_backup_can_be_checked=battery_backup_can_be_checked,
                                                battery_backup_has_power=battery_backup_has_power,
                                                can_other_device_plug_into_other_outlet_port=can_other_device_plug_into_other_outlet_port,
                                                is_other_device_getting_power=is_other_device_getting_power,
                                                can_battery_backup_plug_into_other_port=can_battery_backup_plug_into_other_port)

                                # Check if battery backup gets power in other port
                                does_battery_backup_have_power_in_other_port = check_for_a_or_b(
                                    "Is the battery backup getting power in the outlet's other port?\nEnter “yes” or “no” to respond: ", "yes", "no")
                                if (step_response == "exit"):
                                    return

                                # If battery backup does not get power from other port ...
                                if (does_battery_backup_have_power_in_other_port == "no"):
                                    step_response_sentence += "\nBattery backup does not get power from outlet's other port."

                                # If battery backup gets power from other port ...
                                elif (does_battery_backup_have_power_in_other_port == "yes"):
                                    step_response_sentence += "\nBattery backup gets power from outlet's other port."

                                    self.battery_backup_status = "on"
                                    self.battery_backup_fixed = True
                                    return

                # Check if a nearby GCF reset button can be pressed
                def check_gcfi_reset_button():

                    nonlocal step_response
                    nonlocal step_response_sentence

                    # Variables from function: check_gcfi_reset_button
                    nonlocal can_nearby_gfci_reset_button_be_pressed
                    nonlocal does_pressing_reset_give_power

                    print_responses(battery_backup_can_be_checked=battery_backup_can_be_checked,
                                    battery_backup_has_power=battery_backup_has_power,
                                    can_other_device_plug_into_other_outlet_port=can_other_device_plug_into_other_outlet_port,
                                    is_other_device_getting_power=is_other_device_getting_power,
                                    can_battery_backup_plug_into_other_port=can_battery_backup_plug_into_other_port,
                                    does_battery_backup_have_power_in_other_port=does_battery_backup_have_power_in_other_port)

                    # Check if a nearby GCF reset button can be pressed
                    can_nearby_gfci_reset_button_be_pressed = check_for_a_or_b(
                        "Can some nearby GFCI reset button be pressed?\nEnter “yes” or “no” to respond: ", "yes", "no")
                    if (step_response == "exit"):
                        return

                    # If no GCFI reset button can be pressed ...
                    if (can_nearby_gfci_reset_button_be_pressed == "no"):
                        step_response_sentence += "\n\nNo GCFI reset button can be pressed."

                    # If a GCFI reset button can be pressed ...
                    elif (can_nearby_gfci_reset_button_be_pressed == "yes"):

                        print_responses(battery_backup_can_be_checked=battery_backup_can_be_checked,
                                        battery_backup_has_power=battery_backup_has_power,
                                        can_other_device_plug_into_other_outlet_port=can_other_device_plug_into_other_outlet_port,
                                        is_other_device_getting_power=is_other_device_getting_power,
                                        can_battery_backup_plug_into_other_port=can_battery_backup_plug_into_other_port,
                                        does_battery_backup_have_power_in_other_port=does_battery_backup_have_power_in_other_port,
                                        can_nearby_gfci_reset_button_be_pressed=can_nearby_gfci_reset_button_be_pressed)

                        # Check if pressing reset button gives power
                        does_pressing_reset_give_power = check_for_a_or_b(
                            "Does the battery backup have power after pressing the GFCI outlet's reset button?\nEnter “yes” or “no” to respond: ", "yes", "no")
                        if (step_response == "exit"):
                            return

                        # If battery backup does not have power after pressing reset button ...
                        if (does_pressing_reset_give_power == "no"):
                            step_response_sentence += "\n\nPressed GFCI reset button. > Battery backup still has no power."

                        # If battery backup has power after pressing reset button ...
                        elif (does_pressing_reset_give_power == "yes"):
                            step_response_sentence += "\n\nPressed GFCI reset button. > Battery backup has power."

                            self.battery_backup_status = "on"
                            self.battery_backup_fixed = True
                            return

                # Check if battery backup can be plugged into a different, working outlet
                def check_working_outlet():

                    nonlocal step_response
                    nonlocal step_response_sentence

                    # Variables from function: check_working_outlet
                    nonlocal can_battery_backup_wire_to_working_outlet
                    nonlocal is_there_power_after_wiring_to_other_outlet

                    print_responses(battery_backup_can_be_checked=battery_backup_can_be_checked,
                                    battery_backup_has_power=battery_backup_has_power,
                                    can_other_device_plug_into_other_outlet_port=can_other_device_plug_into_other_outlet_port,
                                    is_other_device_getting_power=is_other_device_getting_power,
                                    can_battery_backup_plug_into_other_port=can_battery_backup_plug_into_other_port,
                                    does_battery_backup_have_power_in_other_port=does_battery_backup_have_power_in_other_port,
                                    can_nearby_gfci_reset_button_be_pressed=can_nearby_gfci_reset_button_be_pressed,
                                    does_pressing_reset_give_power=does_pressing_reset_give_power)

                    # Check if battery backup can be plugged into a different, working outlet
                    can_battery_backup_wire_to_working_outlet = check_for_a_or_b(
                        "Can the battery backup be plugged into a working outlet?\nEnter “yes” or “no”: ", "yes", "no")
                    if (step_response == "exit"):
                        return

                    # If battery backup cannot be plugged into a different, working outlet ...
                    if (can_battery_backup_wire_to_working_outlet == "no"):
                        step_response_sentence += "\n\nBattery backup can't be wired to a working outlet."

                    # If battery backup can be plugged into a different, working outlet ...
                    elif (can_battery_backup_wire_to_working_outlet == "yes"):

                        print_responses(battery_backup_can_be_checked=battery_backup_can_be_checked,
                                        battery_backup_has_power=battery_backup_has_power,
                                        can_other_device_plug_into_other_outlet_port=can_other_device_plug_into_other_outlet_port,
                                        is_other_device_getting_power=is_other_device_getting_power,
                                        can_battery_backup_plug_into_other_port=can_battery_backup_plug_into_other_port,
                                        does_battery_backup_have_power_in_other_port=does_battery_backup_have_power_in_other_port,
                                        can_nearby_gfci_reset_button_be_pressed=can_nearby_gfci_reset_button_be_pressed,
                                        does_pressing_reset_give_power=does_pressing_reset_give_power,
                                        can_battery_backup_wire_to_working_outlet=can_battery_backup_wire_to_working_outlet)

                        # Check if battery backup has power in the different, working outlet
                        is_there_power_after_wiring_to_other_outlet = check_for_a_or_b(
                            "Does the battery backup have power after wiring to a working outlet?\nEnter “yes” or “no” to respond: ", "yes", "no")
                        if (step_response == "exit"):
                            return

                        # If battery backup does not have power in the different, working outlet
                        if (is_there_power_after_wiring_to_other_outlet == "no"):
                            step_response_sentence += "\n\nBattery backup still has no power after wiring to a working outlet."

                        # If battery backup has power in the different, working outlet
                        elif (is_there_power_after_wiring_to_other_outlet == "yes"):
                            step_response_sentence += "\n\nBattery backup has power after wiring to a working outlet."

                            self.battery_backup_status = "on"
                            self.battery_backup_fixed = True
                            return

                print_responses(
                    battery_backup_can_be_checked=battery_backup_can_be_checked)

                # Check if battery backup has power
                battery_backup_has_power = check_for_a_or_b(
                    "Does the battery backup have power? Enter “yes” or “no”: ", "yes", "no")
                if (step_response == "exit"):
                    return

                # If yes, battery backup has power ...
                if (battery_backup_has_power == "yes"):
                    step_response_sentence += "\n\nBattery backup has power."
                    self.battery_backup_status = "on"

                # If no, battery backup has no power ...
                elif (battery_backup_has_power == "no"):
                    step_response_sentence += "\n\nBattery backup has no power."
                    self.battery_backup_status = "off"

                    check_battery_backup_outlet()
                    if (step_response == "exit" or self.battery_backup_status == "on"):
                        return

                    check_gcfi_reset_button()
                    if (step_response == "exit" or self.battery_backup_status == "on"):
                        return

                    check_working_outlet()
                    if (step_response == "exit" or self.battery_backup_status == "on"):
                        return

            # Check whether all breakers are on or not
            def check_breaker_box():

                nonlocal step_response
                nonlocal step_response_sentence

                # Variables from function: check_breaker_box
                nonlocal can_breaker_box_be_checked
                nonlocal are_any_breakers_tripped_or_off
                nonlocal does_resetting_breakers_give_battery_backup_power

                print_responses(battery_backup_can_be_checked=battery_backup_can_be_checked,
                                battery_backup_has_power=battery_backup_has_power,
                                can_other_device_plug_into_other_outlet_port=can_other_device_plug_into_other_outlet_port,
                                is_other_device_getting_power=is_other_device_getting_power,
                                can_battery_backup_plug_into_other_port=can_battery_backup_plug_into_other_port,
                                does_battery_backup_have_power_in_other_port=does_battery_backup_have_power_in_other_port,
                                can_nearby_gfci_reset_button_be_pressed=can_nearby_gfci_reset_button_be_pressed,
                                does_pressing_reset_give_power=does_pressing_reset_give_power,
                                can_battery_backup_wire_to_working_outlet=can_battery_backup_wire_to_working_outlet,
                                is_there_power_after_wiring_to_other_outlet=is_there_power_after_wiring_to_other_outlet)

                # Check if the breaker box can be checked
                can_breaker_box_be_checked = check_for_a_or_b(
                    "Can the breaker box be checked?\nEnter “yes” or “no” to respond: ", "yes", "no")
                if (step_response == "exit"):
                    return

                # If the breaker box cannot be checked ...
                if (can_breaker_box_be_checked == "no"):
                    step_response_sentence += "\n\nNo breaker box can be checked."

                # If the breaker box can be checked ...
                elif (can_breaker_box_be_checked == "yes"):

                    print_responses(battery_backup_can_be_checked=battery_backup_can_be_checked,
                                    battery_backup_has_power=battery_backup_has_power,
                                    can_other_device_plug_into_other_outlet_port=can_other_device_plug_into_other_outlet_port,
                                    is_other_device_getting_power=is_other_device_getting_power,
                                    can_battery_backup_plug_into_other_port=can_battery_backup_plug_into_other_port,
                                    does_battery_backup_have_power_in_other_port=does_battery_backup_have_power_in_other_port,
                                    can_nearby_gfci_reset_button_be_pressed=can_nearby_gfci_reset_button_be_pressed,
                                    does_pressing_reset_give_power=does_pressing_reset_give_power,
                                    can_battery_backup_wire_to_working_outlet=can_battery_backup_wire_to_working_outlet,
                                    is_there_power_after_wiring_to_other_outlet=is_there_power_after_wiring_to_other_outlet,
                                    can_breaker_box_be_checked=can_breaker_box_be_checked)

                    # Check if any breakers are tripped or off
                    are_any_breakers_tripped_or_off = check_for_a_or_b(
                        "Are any breakers tripped or off?\nEnter “yes” or “no” to respond: ", "yes", "no")
                    if (step_response == "exit"):
                        return

                    # If no breakers are tripped or off ...
                    if (are_any_breakers_tripped_or_off == "no"):
                        step_response_sentence += "\n\nChecked breaker box > All breakers are on."

                    # If breakers are tripped or off ...
                    elif (are_any_breakers_tripped_or_off == "yes"):
                        step_response_sentence += "\n\nChecked breaker box > Tripped/Off breakers found."

                        print_responses(battery_backup_can_be_checked=battery_backup_can_be_checked,
                                        battery_backup_has_power=battery_backup_has_power,
                                        can_other_device_plug_into_other_outlet_port=can_other_device_plug_into_other_outlet_port,
                                        is_other_device_getting_power=is_other_device_getting_power,
                                        can_battery_backup_plug_into_other_port=can_battery_backup_plug_into_other_port,
                                        does_battery_backup_have_power_in_other_port=does_battery_backup_have_power_in_other_port,
                                        can_nearby_gfci_reset_button_be_pressed=can_nearby_gfci_reset_button_be_pressed,
                                        does_pressing_reset_give_power=does_pressing_reset_give_power,
                                        can_battery_backup_wire_to_working_outlet=can_battery_backup_wire_to_working_outlet,
                                        is_there_power_after_wiring_to_other_outlet=is_there_power_after_wiring_to_other_outlet,
                                        can_breaker_box_be_checked=can_breaker_box_be_checked,
                                        are_any_breakers_tripped_or_off=are_any_breakers_tripped_or_off)

                        # Check if resetting breakers gives the battery backup power
                        if (self.battery_backup_status == "off"):
                            does_resetting_breakers_give_battery_backup_power = check_for_a_or_b(
                                "Does resetting the breakers give the battery backup power?\nEnter “yes” or “no” to respond: ", "yes", "no")
                            if (step_response == "exit"):
                                return
                        elif (self.battery_backup_status == "n/a"):
                            does_resetting_breakers_give_battery_backup_power = check_for_a_or_b(
                                "Does resetting the breakers turn the internet back on?\nEnter “yes” or “no” to respond: ", "yes", "no")
                            if (step_response == "exit"):
                                return

                        # If battery backup still has no power ...
                        if (does_resetting_breakers_give_battery_backup_power == "no"):

                            if (self.battery_backup_status == "off"):
                                step_response_sentence += "\nReset breakers > Battery backup still has no power."
                            elif (self.battery_backup_status == "n/a"):
                                step_response_sentence += "\nReset breakers > Internet is still offline."

                        # If battery backup has power ...
                        elif (does_resetting_breakers_give_battery_backup_power == "yes"):

                            if (self.battery_backup_status == "off"):
                                step_response_sentence += "\nReset breakers > Battery backup has power."
                            elif (self.battery_backup_status == "n/a"):
                                step_response_sentence += "\nReset breakers > Internet is back online."

                            self.battery_backup_status = "on"
                            self.battery_backup_fixed = True

            print_responses()

            # See if battery backup can be checked
            battery_backup_can_be_checked = check_for_a_or_b(
                "Can the ONT's battery backup be checked? Enter “yes” or “no”: ", "yes", "no")
            if (step_response == "exit"):
                return

            # if the battery backup cannot be checked ...
            if (battery_backup_can_be_checked == "no"):
                step_response_sentence = "ONT's battery backup cannot be checked."
                self.battery_backup_status = "n/a"

            # if battery backup can be checked
            # Check the battery backup lights and power
            elif (battery_backup_can_be_checked == "yes"):

                # Check battery backup lights
                step_response_sentence = "Battery Backup"

                document_lights_or_cabling("lights", print_responses)
                if (step_response == "exit"):
                    return

                # Check battery backup power
                check_battery_backup_power()
                if (step_response == "exit"):
                    return

            # If battery backup couldn't be checked or battery backup was checked but there's still no internet ...
            if (self.battery_backup_status == "off" or self.battery_backup_status == "n/a"):

                # Check the breaker box
                check_breaker_box()
                if (step_response == "exit"):
                    return

            print_responses(all_questions_answered=True, battery_backup_can_be_checked=battery_backup_can_be_checked,
                            battery_backup_has_power=battery_backup_has_power,
                            can_other_device_plug_into_other_outlet_port=can_other_device_plug_into_other_outlet_port,
                            is_other_device_getting_power=is_other_device_getting_power,
                            can_battery_backup_plug_into_other_port=can_battery_backup_plug_into_other_port,
                            does_battery_backup_have_power_in_other_port=does_battery_backup_have_power_in_other_port,
                            can_nearby_gfci_reset_button_be_pressed=can_nearby_gfci_reset_button_be_pressed,
                            does_pressing_reset_give_power=does_pressing_reset_give_power,
                            can_battery_backup_wire_to_working_outlet=can_battery_backup_wire_to_working_outlet,
                            is_there_power_after_wiring_to_other_outlet=is_there_power_after_wiring_to_other_outlet,
                            can_breaker_box_be_checked=can_breaker_box_be_checked,
                            are_any_breakers_tripped_or_off=are_any_breakers_tripped_or_off,
                            does_resetting_breakers_give_battery_backup_power=does_resetting_breakers_give_battery_backup_power,
                            battery_backup_status=self.battery_backup_status)

            self.set_troubleshooting_steps()

        if (step == "Check account status."):
            system.clear_prompt_or_terminal()
            check_account_status()

        elif (step == "Check landline phone for dial tone."):
            system.clear_prompt_or_terminal()
            check_landline_phone_for_dial_tone()

        elif (step == "Check status of all services."):
            system.clear_prompt_or_terminal()
            check_status_of_all_services()

        elif (step == "Check each network device's name, model, and lights."):
            system.clear_prompt_or_terminal()
            check_each_network_device()

        elif (step == "Check cabling."):
            system.clear_prompt_or_terminal()
            check_cabling()

        elif (step == "Power cycle all network devices."):
            system.clear_prompt_or_terminal()
            power_cycle()

        elif (step == "Check network devices for internet."):
            system.clear_prompt_or_terminal()
            check_network_devices_for_internet()

        elif (step == "Check a device for internet."):
            system.clear_prompt_or_terminal()
            check_devices()

        elif (step == "Check ONT."):
            system.clear_prompt_or_terminal()
            check_ont()

        elif (step == "Check ONT's battery backup."):
            system.clear_prompt_or_terminal()
            check_battery_backup()

        elif (step == "Run ping tests on a computer."):
            system.clear_prompt_or_terminal()
            run_ping_tests()

        elif (step == "Run speed tests on a device."):
            system.clear_prompt_or_terminal()
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

        # ticket_content_list = list(self.ticket_content.values())

        system.clear_prompt_or_terminal()

        print("\nEnter 'exit' at any time to exit prompt.\n\n")

        self.print_diagnostic_questions()

        print("")

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

            system.clear_prompt_or_terminal()

            print("\nEnter 'exit' at any time to exit prompt.\n\n")

            happening_for_how_long = input(
                "How long has the issue been happening since? Enter in example format of '3 weeks ago': ").strip()

            if (happening_for_how_long.lower() == "exit"):

                question_response = "exit"
                return

            question_response_sentence = "Issue happening since: " + happening_for_how_long

        def recent_changes():

            nonlocal question_response
            nonlocal question_response_sentence

            system.clear_prompt_or_terminal()

            print("\nEnter 'exit' at any time to exit prompt.\n\n")

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

            system.clear_prompt_or_terminal()

            print("\nEnter 'exit' at any time to exit prompt.\n\n")

            print("Is the router in any of the following closed spaces for example:\n\n")

            print(
                "Closet\nCabinet\nEntertainment Center\nKitchen\nLaundry room\nBesides a phone's base\n\n")

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
                question_response_sentence = "Router is not in a closed space like a closet, cabinet, entertainment center, kitchen/laundry room, or besides a phone's base."

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

            system.clear_prompt_or_terminal()

            print("\nEnter 'exit' at any time to exit prompt.\n\n")

            print("Are there any sources of interference like:\n")

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

            system.clear_prompt_or_terminal()

            print("\nEnter 'exit' at any time to exit prompt.\n\n")

            when_problem_happens = input(
                "When is the problem typically happening? ").strip()

            if (when_problem_happens.lower() == "exit"):

                question_response = "exit"
                return

            question_response_sentence = "Problem typically happens: " + when_problem_happens

        def does_problem_happen_when_more_devices_online():
            nonlocal question_response
            nonlocal question_response_sentence

            system.clear_prompt_or_terminal()

            print("\nEnter 'exit' at any time to exit prompt.\n\n")

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

            system.clear_prompt_or_terminal()

            print("\nEnter 'exit' at any time to exit prompt.\n\n")

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

            system.clear_prompt_or_terminal()

            print("\nEnter 'exit' at any time to exit prompt.\n\n")

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

        print("\nEnter 'exit' at any time to exit prompt.\n\n")

        ticket_content_list = list(self.ticket_content.values())

        # Output ticket with line numbers, so user knows which line to select
        print("Ticket:\n")
        print(self.print_ticket_with_line_numbers())

        print("")

        # Prompt user for a custom line of text, and save that text into 'custom_line'

        print("\nPress enter key to input multiple lines.\nEnter “done” when all lines are entered.")

        print("\nEnter lines below:")

        custom_line = input("").strip()

        if (custom_line.lower() == "exit"):
            self.print_ticket_steps_and_questions()
            return

        while ("done" not in custom_line.lower().strip()):

            custom_line += "\n" + input("").strip()

            if ("exit" in custom_line.lower().strip()):
                return

        if (len(custom_line) >= 4):
            custom_line = custom_line.rstrip(
                custom_line[-4:]).rstrip()

        print("")

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

        print("\nEnter 'exit' at any time to exit prompt.\n\n")

        # Output ticket with line numbers, so user knows which line to select
        print("Ticket:\n")
        print(self.print_ticket_with_line_numbers())

        print("")

        # Prompt user to choose which line from ticket to remove.
        print("\nEnter 'exit' at any time to exit prompt.\n")

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
            system.clear_prompt_or_terminal()
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
