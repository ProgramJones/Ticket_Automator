# Copyright (c) <2022>, <Tai Jones>
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.


import os
import platform


def clear_prompt_or_terminal():
    """
    Name:
    clear_prompt_or_terminal

    Parameters:
    None

    When code is run:
    At the start of main.py.
    In ticket.py's wait_for_command method, when 'main' is entered.

    Purpose:
    Clear the command line or terminal
    """

    # If operating system is Windows, clear command prompt with 'cls'
    if (platform.system() == "Windows"):
        os.system("cls")
    # If operating system is Unix, clear terminal with 'clear'
    else:
        os.system("clear")
