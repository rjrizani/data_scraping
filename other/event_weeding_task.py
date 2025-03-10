import json

def intro():
    print("*"*8)
    print("WELCOME TO THE WEDDING PLANNER")
    print("*"*8)
    print("-"*8)

def main_menu():
    main_menu = ("Add Task (Vendor/Guest/Other)", "View All Tasks", "Edit Task", "Delete Task", "Delete All Tasks", "Exit Program")
    for i,m in enumerate(main_menu, start=1):
        print(f"{i}. {m}")

def exit_program(db):
    with open("db.json", "w") as file:
        json.dump(db, file)
    print("Goodbye!")

def add_task(db):
    task_name = input("Enter the name of the task: ")
    description = input("Enter the description of the task: ")
    deadline = input("Enter the deadline of the task (YYYY-MM-DD): ")
    is_important = bool(int(input("Is this task important? 1 for Yes, 0 for No: ")))
    task_extra_notes = []

def read_json(db):
    with open(db, "r") as file:
        return json.load(file)

def save_json(db):
    with open("db.json", "w") as file:
        json.dump(db, file, indent=4)

def login(db):
    username = input("Username: ")
    password = input("Password: ")
    if username in db and db[username]["password"] == password:
        print(f"Login successful, welcome {username}!")
        return db[username]
    else:
        raise ValueError("Login failed, username or password is incorrect.")

def register(db):
    username = input("Username: ")
    password1 = input("Password: ")
    password2 = input("Confirm password: ")
    if password1 == password2 and username not in db:
        db[username] = {"name": username, "password": password1}
        save_json("wedding_events.json", db)
        print("Registration successful!")
        exit()
    else:
        raise Exception("Passwords did not match, or username already in use.")

#main_flow
if __name__ == "__main__":
    db = read_json("wedding_events.json")
    intro()

    login_or_register = input("Login or Register: ")
    if login_or_register == "login":
        user = login(db)
    elif login_or_register == "register":
        register(db)
    else:
        print("Invalid input. Please input 'login' or 'register'.")
        exit()
    while True:
        main_menu()
        user_input = int(input("Enter the number of the option you want to select: "))
        match user_input:
            case 1:
                add_task(db)
            case 2:
                pass
            case 3:
                pass
            case 4:
                pass
            case 5:
                pass
            case 6:
                exit_program(db)