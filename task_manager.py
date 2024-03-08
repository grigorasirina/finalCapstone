import os
import sys
import time
from datetime import datetime, date

""" 
Global Variables
These variables maintain the state of the application across 
various functions. This includes tracking the login status, 
the current user, a list of tasks, a dictionary for username 
and password pairs, a format for datetime strings, 
and a counter for tasks.
"""

logged_in = False
current_user = None
task_list = []
username_password = {}
DATETIME_STRING_FORMAT = "%Y-%m-%d"
task_counter = 0

def populate_task_list():
    global task_list

    if not task_list: 
        with open('tasks.txt', 'r') as tasks_file:
            # Strip to remove leading/trailing whitespace
            tasks = tasks_file.read().strip().split("\n")  
            for task_str in tasks:
                # Ensure the string is not empty
                if task_str:  
                    parts = task_str.split(';')
                    # Now, parts is a list of strings. Convert these 
                    # strings to the appropriate data types as needed.
                    new_task = {
                        # Assuming task_number should be an integer
                        "task_number": int(parts[0]),  
                        "username": parts[1],
                        "title": parts[2],
                        "description": parts[3],
                        "due_date": parts[4],
                        "assigned_date": parts[5],
                         # Convert the string 'Yes'/'No' to a boolean
                        "completed": parts[6] == 'Yes', 
                    }
                    task_list.append(new_task)


def populate_username_password_list():
    global username_password

    if not username_password:
        with open('user.txt', 'r') as users_file:
            users = users_file.read().strip().split("\n")
            for user_line in users:
                if user_line:  # Ensure the line is not empty
                    username, password = user_line.split(';')
                    # Add the username and password to the dictionary
                    username_password[username] = password

        
'''
This function generates a comprehensive report of all tasks, 
categorizing them into completed, uncompleted, and overdue 
tasks based on their due dates. It calculates and displays 
the total number of tasks, the number of completed tasks, 
uncompleted tasks, and overdue tasks, along with their 
respective percentages. The report is both printed to 
the console and written to a file named "task_report.txt"
'''


def task_overview():
    # Accessing the global task_list variable to modify or read
    # its content
    global task_list

    # Initializing counters for total, completed, uncompleted,
    # and overdue tasks
    total_number_of_tasks = len(task_list)
    completed_tasks = 0
    uncompleted_tasks = 0
    overdue_tasks = 0

    # Getting the current date to compare with task due dates
    current_date = date.today()

    # Iterating over each task in the task list
    for task in task_list:
        # If a task is marked as completed, increment the
        # completed_tasks counter
        if task["completed"]:
            completed_tasks += 1
        else:
            # If a task is not completed, increment the
            # uncompleted_tasks counter
            uncompleted_tasks += 1
            # Further check if an uncompleted task is overdue
            # by comparing its due date with the current date
            due_date = datetime.strptime(task["due_date"], 
                             DATETIME_STRING_FORMAT).date()
            if due_date < current_date:
                overdue_tasks += 1

    # Calculating the percentage of incomplete and overdue tasks
    # relative to the total number of tasks
    # The results are rounded to 2 decimal places for clarity
    incomplete_tasks_percentage = (
    uncompleted_tasks / total_number_of_tasks * 100)
    incomplete_tasks_percentage = round(incomplete_tasks_percentage, 2)

    overdue_tasks_percentage = (overdue_tasks / total_number_of_tasks) * 100
    overdue_tasks_percentage = round(overdue_tasks_percentage, 2)

    # Preparing a report dictionary with all calculated statistics
    task_report = {
        "total_number_of_tasks": total_number_of_tasks,
        "completed_tasks": completed_tasks,
        "uncompleted_tasks": uncompleted_tasks,
        "overdue_tasks": overdue_tasks,
        "incomplete_tasks_percentage": incomplete_tasks_percentage,
        "overdue_tasks_percentage": overdue_tasks_percentage,
    }

    # Printing the task report to the console for immediate visibility
    print("Task Report:")
    for key, value in task_report.items():
        print(f"{key}: {value}")

    # Writing the task report to a file named 'task_report.txt' for
    # record-keeping
    # Each statistic is written on a new line in a key-value format
    # separated by a semicolon
    with open("task_report.txt", "w") as file:
        for key, value in task_report.items():
            file.write(f"{key};{value}\n")

    # Confirming to the user that the task report has been 
    # successfully written to the file
    print("Task report written successfully!")


def user_overview():
    # Calculate the total number of users and tasks from the
    # provided data structures
    total_users = len(username_password)
    total_tasks = len(task_list)

    # Initialize dictionaries to track task counts per user
    user_task_counts = {}  # Total tasks assigned per user
    user_completed_tasks = {}  # Total completed tasks per user
    user_incomplete_tasks = {}  # Total incomplete tasks per user
    user_overdue_tasks = {}  # Total overdue tasks per user

    # Populate the dictionaries with users from username_password,
    # initializing their counts to 0
    for user in username_password.keys():
        user_task_counts[user] = 0
        user_completed_tasks[user] = 0
        user_incomplete_tasks[user] = 0
        user_overdue_tasks[user] = 0

    # Get the current date for overdue task comparison
    current_date = date.today()  

    # Iterate over each task in task_list to update
    # the count dictionaries
    for task in task_list:
        # Get the username associated with the task
        user = task["username"]
        # Increment the total task count for the user  
        user_task_counts[user] += 1  
        
        # Check if the task is completed and update the respective
        # count
        if task["completed"]:
            user_completed_tasks[user] += 1
        else:
             # Increment incomplete task count
            user_incomplete_tasks[user] += 1 
            # Check if the task is overdue and update the overdue
            # task count
            due_date = datetime.strptime(task["due_date"], 
                             DATETIME_STRING_FORMAT).date()
            if due_date < current_date:
                user_overdue_tasks[user] += 1

    # Writing the overview to 'user_overview.txt' file
    with open("user_overview.txt", "w") as file:
        # Write total user and task counts at the top of the file
        file.write(f"Total number of users: {total_users}\n")
        file.write(f"Total number of tasks: {total_tasks}\n")

        # Iterate over users to calculate and write detailed task
        # statistics
        for user in username_password.keys():
            # Retrieve task counts for the user
            tasks_assigned = user_task_counts[user]
            tasks_completed = user_completed_tasks[user]
            tasks_incomplete = user_incomplete_tasks[user]
            tasks_overdue = user_overdue_tasks[user]

            # Calculate task percentages, handling division by zero
            # where necessary
            assigned_tasks_percentage = (
                (tasks_assigned / total_tasks * 100) if total_tasks > 0 else 0
            )
            completed_tasks_percentage = (
                (tasks_completed / tasks_assigned * 100) 
                 if tasks_assigned > 0 else 0
            )
            incomplete_tasks_percentage = (
                (tasks_incomplete / tasks_assigned * 100) 
                 if tasks_assigned > 0 else 0
            )
            overdue_tasks_percentage = (
                (tasks_overdue / tasks_assigned * 100) 
                 if tasks_assigned > 0 else 0
            )

            # Format the user report with calculated statistics
            user_report = (
                f"\nUser: {user}\n"
                f"Total tasks assigned: {tasks_assigned}\n"
                f"Percentage of total tasks assigned: {assigned_tasks_percentage:.2f}%\n"
                f"Percentage of tasks completed: {completed_tasks_percentage:.2f}%\n"
                f"Percentage of tasks still to be completed: {incomplete_tasks_percentage:.2f}%\n"
                f"Percentage of overdue tasks not yet completed: {overdue_tasks_percentage:.2f}%\n"
            )

            # Write each user's report to the file and also print to
            # console for immediate feedback
            file.write(user_report)
            print(user_report)


def reg_user():
    print("\nRegister a New User\n")
    global username_password

    while True:
        new_username = input("Enter new username: ").strip()

        # Check if the username already exists
        if new_username in username_password:
            print("Username already exists. Please try a different username.")
            continue

        new_password = input("Enter new password: ").strip()
        confirm_password = input("Confirm new password: ").strip()

        # Check if passwords match
        if new_password != confirm_password:
            print("Passwords do not match. Please try again.")
            continue

        # If we reach here, it means the input is valid
        break

    # Add the new user to the username_password dictionary
    username_password[new_username] = new_password

    # Append the new user to the user.txt file
    with open("user.txt", "a") as file:
        file.write(f"\n{new_username};{new_password}")

    print("New user added successfully.")
    show_menu()



def add_task():
    global username_password, task_list, task_counter

    # Increment the global task counter to ensure each task has a 
    #unique identifier
    task_counter += 1
    # Assign the incremented value as the new task's number
    task_number = task_counter  

    # Loop until a valid username is provided for the task assignment
    while True:
        task_username = input("Name of person assigned to task: ")
        if task_username not in username_password.keys():
            # Prompt again if the username doesn't exist
            print("User does not exist.")  
            continue  # Continue looping for a valid input
        else:
            break  # Exit the loop if a valid username is found

    # Prompt for the remaining task details (title, description)
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")

    # Loop until a valid due date is entered, using a try-except
    # block to catch format errors
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")

            break  # Exit loop if successful
        except ValueError:
            # Inform the user of the format error and prompt again
            print("Invalid datetime format. Please use the format specified")

    # Record the current date as the assignment date for the new task
    curr_date = date.today()
    str_curr_date = curr_date.strftime(DATETIME_STRING_FORMAT)

    # Construct a dictionary representing the new task with all
    # collected information
    new_task = {
        "task_number": task_number,
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": task_due_date,
        "assigned_date": str_curr_date,
        "completed": False,  
        # New tasks are marked as incomplete by default
    }

    # Add the new task to the global task list
    task_list.append(new_task)

    # Write the updated task list to a file, formatting each task
    # as a string
    with open("tasks.txt", "a") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                str(t["task_number"]),
                t["username"],
                t["title"],
                t["description"],
                t["due_date"],
                t["assigned_date"],  # Ensure this is a string
                "Yes" if t["completed"] else "No",
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))
        
    # Confirm to the user that the task was successfully added
    print("Task successfully added.")
    show_menu()

def view_all():
    global task_list
    for task in task_list:
         # Print newlines for better readability between tasks
        print("\n\n") 
        # Convert string dates back to datetime objects for formatting
        assigned_date_obj = datetime.strptime(task['assigned_date'],
                                               DATETIME_STRING_FORMAT)
        due_date_obj = datetime.strptime(task['due_date'],
                                          DATETIME_STRING_FORMAT)

        disp_str = f"Task number: \t\t {task['task_number']}\n"
        disp_str += f"Task: \t\t {task['title']}\n"
        disp_str += f"Assigned to: \t {task['username']}\n"
        disp_str += f"Date Assigned: \t {assigned_date_obj.strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {due_date_obj.strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {task['description']}\n"

        print(disp_str)
    show_menu()


def view_mine():
    global task_list
    global current_user

    for task in task_list:
        if current_user == task["username"]:
            print("\n-----------TASK-------------\n")
            # Ensure this line comes first
            disp_str = f"Task number: \t\t {task['task_number']}\n"  
            disp_str += f"Task: \t\t {task['title']}\n"  
            disp_str += f"Assigned to: \t {task['username']}\n"
            # Use string directly
            disp_str += f"Date Assigned: \t {task['assigned_date']}\n" 
             # Use string directly 
            disp_str += f"Due Date: \t {task['due_date']}\n" 
            disp_str += f"Task Description: \n {task['description']}\n"
            print(disp_str)
            print("\n")
    show_menu()


def generate_reports():
    user_overview()
    task_overview()
    show_menu()


def display_statistics():

    if not os.path.exists("user.txt"):
        with open("user.txt", "w") as default_file:
            default_file.write("admin;password")
    with open("user.txt", "r") as user_file:
        user_data = user_file.read().split("\n")
    username = []
    for user in user_data:
        user, password = user.split(";")
        username.append(user)

    if not os.path.exists("tasks.txt"):
        with open("tasks.txt", "w"):
            pass
    with open('tasks.txt', 'r') as tasks_file:
        tasks = tasks_file.read().split("\n")
    
    print("-----------------------------------")
    print(f"Number of users: \t\t {len(username)}")
    print(f"Number of tasks: \t\t {len(tasks)}")
    print("-----------------------------------")


def check_login():
    global logged_in
    return logged_in


def show_menu():
    global current_user
    print(
        """
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
gr - Generate Reports
ds - Display statistics
e - Exit
          """
    )

    choice = input("Please choose an option from above: ").lower().strip()

    if choice == "r":
        reg_user()
    elif choice == "a":
        add_task()
    elif choice == "va":
        view_all()
    elif choice == "vm":
        view_mine()
    elif choice == "gr":
        generate_reports()
    elif choice == "ds" and current_user == "admin":
        display_statistics()
    elif choice == "e":
        sys.exit()
    else:
        show_menu()


def login():
    user_data = {}
    if not os.path.exists("user.txt"):
        with open("user.txt", "w") as default_file:
            default_file.write("admin;password")
    with open("user.txt", "r") as user_file:
        user_data = user_file.read().split("\n")

    # Convert to a dictionary
    global username_password
    for user in user_data:
        username, password = user.split(";")
        username_password[username] = password

    global logged_in
    while not logged_in:

        print("LOGIN")
        curr_user = input("Username: ")
        curr_pass = input("Password: ")
        if curr_user not in username_password.keys():
            print("User does not exist")
            continue
        elif username_password[curr_user] != curr_pass:
            print("Wrong password")
            continue
        else:
            print("Login Successful!")
            logged_in = True
            global current_user
            current_user = curr_user
            show_menu()


#############################################################################
"""
Checking authentication state of user
"""
populate_task_list()
populate_username_password_list()
logged_in_status = check_login()
if logged_in_status:
    show_menu()
else:
    login()
