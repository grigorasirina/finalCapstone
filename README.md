Project Name
Task Manager

Description
This Python-based application serves as a comprehensive solution for managing tasks and user accounts through a command-line interface. Designed for small teams or personal projects, it allows for efficient tracking of task assignments, due dates, and completion status. The program features user authentication, task assignment to specific users, viewing and editing tasks, and generating detailed reports on tasks and user activities. It aims to streamline the process of task management without the need for complex or costly software.

Table of Contents
Installation
Usage
Starting the Application
Registering a User
Adding a Task
Viewing Tasks
Generating Reports
Displaying Statistics
Contributing
License
Installation
To install the Task Manager CLI on your local machine, follow these steps:

Clone the repository to your local machine:
git clone https://github.com/grigorasirina/finalCapstone.git

Navigate to the cloned repository:
cd finalCapstone

Ensure you have Python 3.x installed on your machine. You can download it from python.org.

(Optional) Set up a virtual environment:
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

Run the application:
python task_manager.py

Upon starting, you will be prompted to log in. The default username and password are admin and password, respectively.

Registering a User
To register a new user, select the r option from the main menu and follow the prompts.

Adding a Task
To add a new task, choose the a option and provide the necessary details as prompted.

Viewing Tasks
View All Tasks: Select va to list all tasks.
View My Tasks: Choose vm to see tasks assigned to the logged-in user.
Generating Reports
To generate task and user reports, select gr. This creates or updates task_report.txt and user_overview.txt with detailed statistics.

Displaying Statistics
If logged in as the admin, selecting ds displays overall statistics, including the total number of users and tasks.

Contributing
For contributions, please fork the repository, create a feature branch, and submit a pull request for review.

License
MIT License
