# Copyright (c) <2022>, <Tai Jones>
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

import os
import platform
import main_menu

# Clear the command line or terminal
if (platform.system() == "Windows"):
    # If operating system is Windows, clear command prompt with 'cls'
    os.system("cls")
else:
    # If operating system is Unix, clear terminal with 'clear'
    os.system("clear")

main_menu.open_main_menu()
