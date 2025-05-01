'''A sql and python program that can:
Add, Remove, Update, and List films in the films.db database'''
# import required libraries
import sqlite3

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


# integer check
def isint(input):
    try:
        int(input)
        return True
    except ValueError:
        return False


# check if within constraints
def is_valid_rating(input):
    if int(input) <= 10 and int(input) >= 1:
        return True
    else:
        return False


# check if id exists
def findid(input):
    data = [input]
    cursor.execute("SELECT id FROM films WHERE id=?", data)
    connection.commit()
    output = cursor.fetchall()
    if len(output) == 0 or int(input) <= 0:
        return False
    else:
        return True


# check if style input is valid
def style_check(input):
    if input.lower() == "f" or input.lower() == "s":
        return True
    else:
        return False


# check if order input is valid
def order_check(input):
    if input.lower() == "i" or input.lower() == "n" or input.lower() == "r":
        return True
    else:
        return False


while True:
    print("Press \033[1mA\033[0m to add a film")
    print("Press \033[1mU\033[0m to update a film")
    print("Press \033[1mD\033[0m to delete a film")
    print("Press \033[1mL\033[0m to list all films")
    choice = input("").upper()

    # Add a new film
    if choice == "A":
        add_name = input("\nPlease enter the name of the film\n").upper()
        add_rating = input("\nPlease enter your rating of the film (1 - 10)\n")
        # check if valid
        while not isint(add_rating) or not is_valid_rating(add_rating):
            print("\n\033[1mPlease input an integer from 1 to 10!\033[0m\n")
            add_rating = input("Please enter your rating of the film (1 - 10)\n")
        # add to database
        data = [add_name, add_rating]
        cursor.execute("INSERT INTO 'films' ('name', 'rating') VALUES (?, ?)", data)
        connection.commit()

        # add successful notice
        add_id = cursor.execute("SELECT id FROM films ORDER BY id DESC LIMIT 1")
        add_id_confirmation = add_id.fetchall()
        print(f"\n\033[1m'{add_name}'\033[0m has been added into the database with:")
        print(f"Id: \033[1m'{add_id_confirmation[0][0]}'\033[0m")
        print(f"Rating: \033[1m'{add_rating}'\033[0m\n")

        print("\n")

    # Update a film name
    elif choice == "U":
        update_id = input("\nPlease enter the ID of the film you want to update\n")
        # check if valid
        while not isint(update_id) or not findid(update_id):
            print("\n\033[1mPlease input an integer of an existing film's id!\033[0m\n")
            update_id = input("Please enter the ID of the film you want to update\n")

        update_name = input("\nPlease enter a new name for the film\n").upper()
        update_rating = input("\nPlease enter your rating of the film (1 - 10)\n")
        # check if valid
        while not isint(update_rating) or not is_valid_rating(update_rating):
            print("\n\033[1mPlease input an integer from 1 to 10!\033[0m\n")
            update_rating = input("\nPlease enter your rating of the film (1 - 10)\n")

        # update confirmation
        data = [update_id]
        update_id_name = cursor.execute("SELECT name FROM films WHERE id=?", data)
        confirm_name = update_id_name.fetchall()

        update_id_rating = cursor.execute("SELECT rating FROM films WHERE id=?", data)
        confirm_rating = update_id_rating.fetchall()

        print(f"\nAre you sure you want to update the film with id \033[1m{update_id}\033[0m:")
        print(f"Name: From \033[1m{confirm_name[0][0]}\033[0m to \033[1m{update_name}\033[0m")
        print(f"Rating: From \033[1m{confirm_rating[0][0]}\033[0m to \033[1m{update_rating}\033[0m?")
        confirmation = input("\n(Y/N):\n").strip().upper()
        if confirmation == "N":
            print("\n\033[1mUpdating canceled.\033[0m\n")
            continue

        # update database
        data = [update_name, update_rating, update_id]
        cursor.execute("UPDATE films SET name=?, rating=? WHERE id=?", data)
        connection.commit()

        # update successful notice
        print(f"\nThe film with ID \033[1m'{update_id}'\033[0m has been updated into the database with:")
        print(f"Name: From \033[1m{confirm_name[0][0]}\033[0m to \033[1m{update_name}\033[0m")
        print(f"Rating: From \033[1m{confirm_rating[0][0]}\033[0m to \033[1m{update_rating}\033[0m?\n")
        print("\n")

    # Delete a film
    elif choice == "D":
        delete_id = input("\nPlease enter the ID of the film you want to delete\n")
        # check if valid
        while not isint(delete_id) or not findid(delete_id):
            print("\n\033[1mPlease input a positive integer of an existing film's ID!\033[0m")
            delete_id = input("\nPlease enter the ID of the film you want to delete\n")

        # ask for confirmation
        data = [delete_id]
        delete_id_name = cursor.execute("SELECT name FROM films WHERE id=?", data)
        confirm_name = delete_id_name.fetchall()
        print("\nAre you sure you want to delete the film:")
        print(f"\033[1m{confirm_name[0][0]}\033[0m with ID \033[1m{delete_id}\033[0m?")
        confirmation = input("(Y/N):\n").strip().upper()
        if confirmation == "N":
            print("\n\033[1mDeletion canceled.\033[0m\n")
            continue

        # update database
        data = [delete_id]
        cursor.execute("DELETE FROM films WHERE id=?", data)
        connection.commit()

        # deletion successful notice
        print(f"\n\033[1mDeletion of '{confirm_name[0][0]}' was successful.\033[0m\n")

        print("\n")

    # List all films
    elif choice == "L":
        # get style
        print("\nWhat style do you want the information in?")
        style = input("Fancy (F) | Simple (S)\n")
        while not style_check(style):
            print("\n\033[1mPlease input either 'F' or 'S'!\033[0m\n")

            print("\nWhat style do you want the information in?")
            style = input("Fancy (F) | Simple (S)\n")

        # get order
        print("\nWhat do you want the list ordered by?")
        order_input = input("ID (I) | Name (N) | Rating (R)\n")
        while not order_check(order_input):
            print("\n\033[1mPlease input either 'I', 'N' or 'R'!\033[0m\n")
            print("\nWhat do you want the list ordered by?")
            order_input = input("ID (I) | Name (N) | Rating (R)\n")

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

        print("\n")

    # Stop when nothing is inputed
    else:
        break
