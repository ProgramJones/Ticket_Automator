# Ticket Automator

## Description
---

**Overview**

This program assists help desk technicians by autoformatting tickets with:
* Relevant troubleshooting steps.
* Relevant diagnostic questions.
* Responses from steps and questions.
* The current ticket status, which gives hints on what to do next.

**Creating the Ticket**

After choosing 'create' at the main menu, user responds to the following prompts for:
* Number
* Name
* Address
* Custom Issue
* Service
* Category
* User's First and Last Name

The base ticket, diagnostic questions, and troubleshooting steps are based off what was just entered.

**Navigating the Ticket**

User navigates the program by choosing one of the following commands:

* Add Step - Add a troubleshooting step to the ticket.
* Add Question - Add a diagnostic question to the ticket.
* Add Line - Add one or more custom lines to the ticket.
* Remove Line - Remove a step, question, or custom line from the ticket.
* Toggle Steps - Switch between viewing only the recommended steps and viewing all the steps.
* Copy - Copy current ticket to the clipboard.
* Help - Show all available commands.
* Main - Return to the main menu.
* End - End the program.

## Installation
---

**Install Python**
1. [Download Python version 3.7.9 or higher](https://www.python.org/downloads/) for your operating system.
2. Run the Python installer.
3. Verify Python is installed - Run this command in cmd/terminal: `python --version`
4. [More information on Python](https://www.python.org)

**Install pip**
1. Run this command in cmd: `py -m ensurepip --upgrade`
2. Run this command in terminal: `python -m ensurepip --upgrade`
3. [More information on pip.](https://pip.pypa.io/en/stable/installation/)


**Install pyperclip**
1. Run this command in cmd: `pip install pyperclip`
2. Run this command in terminal: `pip3 install pyperclip`
3. [More information on pyperclip.](https://pypi.org/project/pyperclip/)

**Run Project's Code**
1. Download the projects code through git or the [project's page](https://github.com/ProgramJones/Ticket_Automator) on github.
2. Navigate to the project's directory in cmd/terminal and enter `python main.py`

Note:
Try the other operating system's command if your operating system's command isn't working.

## Contributing
---

**Optional: Install Git**
1. If downloading on Linux, run this command: `sudo apt install git-all`
2. If downloading on Mac, run this command: `git --version`
3. If downloading on Windows, [go to this website.](https://git-scm.com/download/win)
3. [More information on git](https://git-scm.com)

**Add Steps**

1. Create a function, which will run after the user selects a step, to the `add_step` method.
2. Add the question to the relevant troubleshooting list in the `ticket` class's `__init__` method.
3. Append the question to the relevant troubleshooting steps list in `set_troubleshooting_steps`.
4. Add code, which allows the function to run after a step is selected, to  `add_step` in the below example format of:
```
elif (step == "step_user_sees_at_prompt"):
    function_just_created_by_contributer()
```

**Add Questions**

1. Create a function, which will run after the user selects a question, to the `add_question` method.
2. Add the question to the relevant diagnostic questions list in the `ticket` class's `__init__` method.
3. Append the question to the relevant diagnostic questions list in `set_diagnostic_questions`.
4. Add code, which allows the function to run after a question is selected, to `add_question` in the below example format of:
```
elif (question == "question_user_sees_at_prompt"):
    function_just_created_by_contributer()
```

**Add Commands**
1. Add a function, which will run after the user selects a command, to the `wait_for_command` method.
2. Edit the lowercase list in `wait_for_command` to include the command.
3. Edit the list in `print_commands` to include the command and description.
4. Add code, which allows the function to run after a command is selected, to  `wait_for_command` in the below example format of:
```
if (ticket_command_choice == 'command_just_added_to_lowercase_list'):

    print("\n\n----------------------------------\n\n")

    self.function_just_created_by_contributer()

    self.wait_for_command()
```


## License
---

Copyright (c) <2022> Tai Jones

All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.

