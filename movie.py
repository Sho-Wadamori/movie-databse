'''A sql and python program that can:
Add, Remove, Update, and List films in the films.db database'''
# import required libraries
import sqlite3
import os

# import tabulate library (table formatting)
import subprocess
import sys

try:
    # Try importing tabulate
    from tabulate import tabulate
except ImportError:
    # If not installed, prompt to install
    print("Installing 'tabulate'...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "tabulate"])
    print("'tabulate' installed successfully. Please restart the program.")
    sys.exit()
header = ['\033[1mID\033[0m', '\033[1mNAME\033[0m', '\033[1mRATING\033[0m']

# establish connection to films.db database
connection = sqlite3.connect("films.db")
cursor = connection.cursor()


# clear screen
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


# integer check
def isint(value):
    try:
        int(value)
        return True
    except ValueError:
        return False


# check if within constraints
def is_valid_rating(rating_str):
    try:
        rating = int(rating_str)
        return 1 <= rating <= 10
    except ValueError:
        return False


# check if id exists
def findid(film_id):
    data = [film_id]
    cursor.execute("SELECT id FROM films WHERE id=?", data)
    connection.commit()
    output = cursor.fetchall()
    if len(output) == 0 or int(film_id) <= 0:
        return False
    else:
        return True


# check if style input is valid
def style_check(style_choice):
    if style_choice.lower() == "f" or style_choice.lower() == "s":
        return True
    else:
        return False


# check if order input is valid
def order_check(order_key):
    if order_key.lower() == "i" or order_key.lower() == "n" or order_key.lower() == "r":
        return True
    else:
        return False


def confirm_check(confirm_input):
    if confirm_input.lower() == 'y' or confirm_input.lower() == 'n':
        return True
    else:
        return False


while True:
    clear()
    print("Press \033[1;46m A \033[0m to add a film\n")
    print("Press \033[1;46m U \033[0m to update a film\n")
    print("Press \033[1;46m D \033[0m to delete a film\n")
    print("Press \033[1;46m L \033[0m to list all films\n")
    choice = input("").upper()

    # Add a new film
    if choice == "A":
        add_name = input("\n\nEnter the name of the film\n").upper()
        add_rating = input("\n\nEnter your rating of the film (1 - 10)\n")
        # check if valid
        while not isint(add_rating) or not is_valid_rating(add_rating):
            print("\n\n\033[1;31mInvalid input. Please input an integer from 1 to 10\033[0m\n")
            add_rating = input("\nEnter your rating of the film (1 - 10)\n")
        # add to database
        data = [add_name, add_rating]
        cursor.execute("INSERT INTO 'films' ('name', 'rating') VALUES (?, ?)", data)
        connection.commit()

        # add successful notice
        add_id = cursor.execute("SELECT id FROM films ORDER BY id DESC LIMIT 1")
        add_id_confirmation = add_id.fetchall()
        print(f"\n\n\033[1;32m{add_name}\033[0m has been added into the database with:")
        print(f"Id: \033[1;32m{add_id_confirmation[0][0]}\033[0m")
        print(f"Rating: \033[1;32m{add_rating}\033[0m\n")

        input("\nPress \033[1;46m Enter \033[0m to return to the main menu...")

    # Update a film name
    elif choice == "U":
        update_id = input("\n\nEnter the \033[1;4mID\033[0m of the film you want to update\n")
        # check if valid
        while not isint(update_id) or not findid(update_id):
            print("\n\n\033[1;31mInvalid input. Please input the id of an existing film\033[0m\n")
            update_id = input("\nEnter the \033[1;4mID\033[0m of the film you want to update\n")

        update_name = input("\n\nEnter a \033[1;4mnew name\033[0m for the film\n").upper()
        update_rating = input("\n\nEnter \033[1;4myour rating\033[0m of the film (1 - 10)\n")
        # check if valid
        while not isint(update_rating) or not is_valid_rating(update_rating):
            print("\n\n\033[1;31mInvalid input. Please input an integer from 1 to 10\033[0m\n")
            update_rating = input("\nEnter \033[1;4myour rating\033[0m of the film (1 - 10)\n")

        # update confirmation
        data = [update_id]
        update_id_name = cursor.execute("SELECT name FROM films WHERE id=?", data)
        confirm_name = update_id_name.fetchall()

        update_id_rating = cursor.execute("SELECT rating FROM films WHERE id=?", data)
        confirm_rating = update_id_rating.fetchall()

        print(f"\n\nAre you sure you want to update the film with id \033[1;32m{update_id}\033[0m to:")
        print(f"Name: \033[1;32m{confirm_name[0][0]}\033[0m → \033[1;32m{update_name}\033[0m")
        print(f"Rating: \033[1;32m{confirm_rating[0][0]}\033[0m → \033[1;32m{update_rating}\033[0m")
        confirmation = input("\n\033[1;42m Y \033[0m / \033[1;41m N \033[0m:\n").strip().upper()

        while not confirm_check(confirmation):
            print("\n\033[1;31mInvalid input. Please enter either \033[1;42m Y \033[0m \033[1;31mor \033[1;41m N \033[0m\033[0m")
            confirmation = input("\n\033[1;42m Y \033[0m / \033[1;41m N \033[0m:\n").strip().upper()

        if confirmation == "N":
            print("\n\n\033[1;31mUpdating canceled.\033[0m\n")
            input("\nPress \033[1;46m Enter \033[0m to return to the main menu...")
            continue

        # update database
        data = [update_name, update_rating, update_id]
        cursor.execute("UPDATE films SET name=?, rating=? WHERE id=?", data)
        connection.commit()

        # update successful notice
        print(f"\n\nThe film with ID \033[1;32m{update_id}\033[0m has been updated to:")
        print(f"Name: \033[1;32m{confirm_name[0][0]}\033[0m → \033[1;32m{update_name}\033[0m")
        print(f"Rating: \033[1;32m{confirm_rating[0][0]}\033[0m → \033[1;32m{update_rating}\033[0m")

        input("\n\nPress \033[1;46m Enter \033[0m to return to the main menu...")

    # Delete a film
    elif choice == "D":
        delete_id = input("\n\nEnter the \033[1;4mID\033[0m of the film you want to delete\n")
        # check if valid
        while not isint(delete_id) or not findid(delete_id):
            print("\n\n\033[1;31mInvalid input. Please input the ID of an existing film\033[0m\n")
            delete_id = input("\nEnter the \033[1;4mID\033[0m of the film you want to delete\n")

        # ask for confirmation
        data = [delete_id]
        delete_id_name = cursor.execute("SELECT name FROM films WHERE id=?", data)
        confirm_name = delete_id_name.fetchall()
        print("\nAre you sure you want to \033[1;31mdelete\033[0m the film:")
        print(f"\033[1;32m{confirm_name[0][0]}\033[0m with ID \033[1;32m{delete_id}\033[0m?\n")
        confirmation = input("\033[1;42m Y \033[0m / \033[1;41m N \033[0m:\n").strip().upper()

        while not confirm_check(confirmation):
            print("\n\033[1;31mInvalid input. Please enter either \033[1;42m Y \033[0m \033[1;31mor \033[1;41m N \033[0m")
            confirmation = input("\n\033[1;42m Y \033[0m / \033[1;41m N \033[0m:\n").strip().upper()

        if confirmation == "N":
            print("\n\n\033[1;31mDeletion canceled.\033[0m\n")
            input("\nPress \033[1;46m Enter \033[0m to return to the main menu...")
            continue

        # update database
        data = [delete_id]
        cursor.execute("DELETE FROM films WHERE id=?", data)
        connection.commit()

        # deletion successful notice
        print(f"\n\n\033[1;31mDeletion of \033[1;32m{confirm_name[0][0]}\033[0m \033[1;31mwas successful.\033[0m\n")

        input("\nPress \033[1;46m Enter \033[0m to return to the main menu...")

    # List all films
    elif choice == "L":
        # get style
        print("\n\nWhat style do you want the information in?")
        style = input("Fancy: \033[1;46m F \033[0m | Simple: \033[1;46m S \033[0m\n")
        while not style_check(style):
            print("\n\n\033[1;31mInvalid input. Please input either \033[1;46m F \033[0m \033[1;31mor \033[1;46m S \033[0m\n")

            print("\nWhat style do you want the information in?")
            style = input("Fancy: \033[1;46m F \033[0m | Simple: \033[1;46m S \033[0m\n")

        # get order
        print("\n\nWhat do you want the list ordered by?")
        order_input = input("ID: \033[1;46m I \033[0m | Name: \033[1;46m N \033[0m | Rating: \033[1;46m R \033[0m\n")
        while not order_check(order_input):
            print("\n\033[1;31mInvalid input. Please input either \033[1;46m I \033[0m\033[1;31m, \033[1;46m N \033[0m\033[1;31m, or \033[1;46m R \033[0m\n")
            print("\nWhat do you want the list ordered by?")
            order_input = input("ID: \033[1;46m I \033[0m | Name: \033[1;46m N \033[0m | Rating: \033[1;46m R \033[0m\n")

        print("\n\n")

        # change ordering to inputed order
        if order_input.lower() == "i":
            order = "id"
        elif order_input.lower() == "n":
            order = "name"
        else:
            order = "rating"

        data = [order]
        if order == "rating":
            cursor.execute(f'SELECT * FROM films ORDER BY {order} DESC')
        else:
            cursor.execute(f'SELECT * FROM films ORDER BY {order}')
        output = cursor.fetchall()
        if style.lower() == "f":
            print(tabulate(output, headers=header, tablefmt="fancy_grid"))
        else:
            print(tabulate(output, headers=header))

        input("\n\nPress \033[1;46m Enter \033[0m to return to the main menu...")

    # Stop when nothing is inputed
    else:
        break
