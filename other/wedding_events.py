import json

def intro():
    print("###################################")
    print("###WELCOME TO THE WEDDING PLANNER###")
    print("###################################")
    print("-----------------------------------")

def main_menu():
    main_menu = ("Add Task (Vendor/Guest/Other)", "View All Tasks", "Edit Task", "Delete Task", "Delete All Tasks", "Exit Program")
    for i, m in enumerate(main_menu, start=1):
        print(f"{i}. {m}")

def get_user_input():
    while True:
        try:
            user_input = int(input("Please enter a number from the menu above: "))
            if user_input in [1, 2, 3, 4, 5, 6]:
                return user_input
            else:
                print("Invalid input, please choose a number from the menu above.")
        except ValueError:
            print("Invalid input, please choose a number from the menu above.")

def show_username(full_name):
    print(f"Welcome {full_name}")

def add_task(tasks):
    task_name = input('Enter task name (e.g., Book Caterer, Send Invitations): ')
    description = input('Enter task description: ')
    category = input('Category (Vendor/Guest/Other): ').capitalize()
    deadline = input('Enter task deadline (e.g., 2024-05-10): ')
    is_important = bool(int(input('Is this task important? (1 for Yes, 0 for No): ')))
    notes = []
    while True:
        note = input('Enter any extra notes (type "exit" to stop): ')
        if note == 'exit':
            break
        else:
            notes.append(note)
    task = {"name": task_name, "description": description, "category": category, "deadline": deadline, "isImportant": is_important, "notes": notes}
    tasks.append(task)
    return tasks

def exit_program(db):
    print('Exiting program...')
    save_json('db.json', db)
    exit()

def show_tasks(tasks):
    if len(tasks) < 1:
        print("Task list is empty")
    else:
        print('Your tasks are:')
        for i, task in enumerate(tasks, start=1):
            print(f"{i}. {task['name']} - {task['description']} - Deadline: {task['deadline']}")
        user_input = int(input('Enter the number of a task to view details: '))
        if 0 < user_input <= len(tasks):
            task = tasks[user_input - 1]
            print("--------------------------------")
            for key in task:
                if isinstance(task[key], bool):
                    print(f"{key.upper()} = {'IMPORTANT' if task[key] else 'NOT IMPORTANT'}")
                elif isinstance(task[key], list):
                    print("EXTRA NOTES:")
                    for i, note in enumerate(task[key], start=1):
                        print(f"{i}. {note}")
                else:
                    print(f"{key.upper()} = {task[key]}")
            print("--------------------------------")
        else:
            print("Invalid input, please select a valid task number.")

def show_tasks_simpler(tasks):
    if len(tasks) < 1:
        print("Task list is empty")
    else:
        print('Your tasks are:')
        for i, task in enumerate(tasks, start=1):
            print(f"{i}. {task['name']} - {task['description']} - Deadline: {task['deadline']}")

def delete_task(tasks):
    while True:
        try:
            task_delete = int(input('Enter the number of the task you want to delete, or type 0 to cancel: ')) - 1
            if task_delete == -1:
                return tasks
            elif 0 <= task_delete < len(tasks):
                deleted_task = tasks.pop(task_delete)
                print(f"Task '{deleted_task['name']}' has been deleted.")
            else:
                print("Invalid input, please select a valid task number.")
        except ValueError:
            print("Invalid input")

def delete_all_tasks(tasks, username):
    sure = input("Are you sure you want to delete all tasks? (y or n): ")
    if sure == 'y':
        tasks.clear()
        print(f"All {username}'s tasks have been deleted.")
        return tasks
    else:
        return tasks

def read_json(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    if isinstance(data, list):
        raise TypeError("Data file format is incorrect. Resetting to empty list.")
    return data

def save_json(filename, db):
    with open(filename, 'w') as file:
        json.dump(db, file, indent=4)

def login(db):
    username = input('Username: ')
    password = input('Password: ')
    if username in db and db[username]['password'] == password:
        print(f'Login successful, welcome {username}!')
        return db[username]
    else:
        raise ValueError('Login failed, username or password is incorrect.')

def register(db):
    username = input('Username: ')
    password1 = input('Password: ')
    password2 = input('Confirm password: ')
    if password1 == password2 and username not in db:
        db[username] = {"name": username, "password": password1, 'tasks': []}
        save_json('db.json', db)
        print("Registration successful!")
        exit()
    else:
        raise Exception('Passwords did not match, or username already in use.')

# Main flow
if __name__ == "__main__":
    db = read_json('db.json')
    intro()

    login_or_register = input('Login or Register: ')
    if login_or_register == 'login':
        user = login(db)
    elif login_or_register == 'register':
        register(db)
    else:
        print("Invalid input. Please input 'login' or 'register'.")
        exit()

    while True:
        main_menu()
        user_input = get_user_input()
        match user_input:
            case 1:
                user['tasks'] = add_task(user['tasks'])
                save_json('db.json', db)
            case 2:
                show_tasks(user['tasks'])
            case 3:
                print("This is the edit task menu.")
                show_tasks_simpler(user['tasks'])
                task_input = int(input('Enter the task number you want to edit: ')) - 1
                if task_input < 0 or task_input >= len(user['tasks']):
                    print("Invalid input")
                else:
                    task = user['tasks'][task_input]
                    print(task)
                    for i, key in enumerate(task, start=1):
                        print(f"{i}. {key}")
                    edit_input = int(input('Enter the number of the field you want to edit: '))
                    match edit_input:
                        case 1:
                            task['name'] = input('Enter updated task name: ')
                        case 2:
                            task['description'] = input('Enter updated task description: ')
                        case 3:
                            task['category'] = input('Enter updated category (Vendor/Guest/Other): ').capitalize()
                        case 4:
                            task['deadline'] = input('Enter updated deadline (e.g., 2024-05-10): ')
                        case 5:
                            task['isImportant'] = bool(int(input('Enter new important status, 1 -> Important, 0 -> Not important: ')))
                        case 6:
                            print("Extra notes:")
                            for i, note in enumerate(task['notes'], start=1):
                                print(f"{i}. {note}")
                            note_index = int(input('Enter the note number to edit: ')) - 1
                            if 0 <= note_index < len(task['notes']):
                                task['notes'][note_index] = input("Enter the updated note: ")
                            else:
                                print("Invalid note number.")
                    save_json('db.json', db)
            case 4:
                show_tasks_simpler(user['tasks'])
                user['tasks'] = delete_task(user['tasks'])
                save_json('db.json', db)
            case 5:
                user['tasks'] = delete_all_tasks(user['tasks'], user['name'])
                save_json('db.json', db)
            case 6:
                exit_program(db)
