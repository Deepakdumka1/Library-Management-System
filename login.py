import sqlite3
import re
import os

class User:
    def __init__(self, full_name="", email="", password="", username="", phone="", student_id=""):
        self.full_name = full_name
        self.email = email
        self.password = password
        self.username = username
        self.phone = phone
        self.student_id = student_id

def init_db():
    # Create a connection to the SQLite3 database (it will create a file if it doesn't exist)
    conn = sqlite3.connect("users.db")
    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    # Create table if not exists
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        full_name TEXT,
        email TEXT UNIQUE,
        password TEXT,
        username TEXT UNIQUE,
        phone TEXT,
        student_id TEXT
    )
    """)
    conn.commit()
    conn.close()

def take_input():
    return input().strip()

def generate_username(email):
    return email.split('@')[0]

def take_password():
    import getpass
    password = getpass.getpass(prompt="Enter password: ")
    return password

def check_email(email):
    end = "gehu.ac.in"
    email = email.strip()

    # Check if email ends with 'gehu.ac.in'
    if not email.endswith(end):
        print(f"Email must end with {end}. Please check and re-enter.")
        return False

    # Validate if there is an '@' character before the domain
    if '@' not in email or email.count('@') > 1:
        print("Invalid email format: '@' missing or appears more than once.")
        return False

    username, domain = email.split('@')

    # Validate format of username
    if '.' not in username or not username.split('.')[-1].isdigit():
        print("Invalid email format: missing valid number after '.' before '@'.")
        return False

    # Check if 9 digits follow the first '.' character
    digits = re.findall(r'\d+', username)
    if len(digits) == 0 or len(digits[0]) != 9:
        print("Email username should have exactly 9 digits after '.'")
        return False

    return True

def check_phone_number(phone):
    if len(phone) != 10 or not phone.isdigit():
        print("Phone number must be 10 digits long and should contain only digits.")
        return False
    return True

def take_phone_number():
    while True:
        phone = take_input()
        if check_phone_number(phone):
            return phone
        else:
            print("Invalid phone number. Please enter a valid 10-digit phone number.")

def sign_up():
    user = User()

    print("\nEnter your full name:")
    user.full_name = take_input()

    print("\nEnter your phone number (10 digits):")
    user.phone = take_phone_number()

    print("\nEnter your email:")
    email = take_input()
    while not check_email(email):
        print("Re-enter a valid email ID:")
        email = take_input()
        
    user.email = email

    user.username = generate_username(email)

    print("Enter your password:")
    user.password = take_password()
    print("Confirm your password:")
    password2 = take_password()

    if user.password == password2:
        try:
            # Open a connection to the SQLite3 database
            conn = sqlite3.connect("users.db")
            cursor = conn.cursor()

            # Insert the new user into the database
            cursor.execute("INSERT INTO users (full_name, email, password, username, phone, student_id) VALUES (?, ?, ?, ?, ?, ?)", 
                           (user.full_name, user.email, user.password, user.username, user.phone, user.student_id))

            conn.commit()
            conn.close()
            print(f"\n\nUser registration successful! Your username is {user.username}")
        except sqlite3.IntegrityError:
            print("\n\nThis email or username is already registered. Try again with a different email or username.")
    else:
        print("\n\nPasswords do not match.")

def log_in():
    print("\nEnter your username:")
    username = take_input()
    print("Enter your password:")
    password = take_password()

    # Open a connection to the SQLite3 database
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("SELECT full_name, email, password, username, phone, student_id FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()

    conn.close()

    if user:
        full_name, email, stored_password, stored_username, phone, student_id = user
        if stored_password == password:
            print(f"\nWelcome {full_name}!")
            print(f"\n|Full Name: {full_name}")
            print(f"|Email: {email}")
            print(f"|Username: {username}")
            print(f"|Contact No: {phone}")
        else:
            print("Invalid password!")
    else:
        print("User not registered!")

def main():
    # Initialize the database and create the table if it doesn't exist
    init_db()

    while True:
        print("\n\t\t\t----------Welcome to the authentication system----------")
        print("Please choose your operation:")
        print("1. Signup")
        print("2. Login")
        print("3. Exit")
        opt = input("\nYour choice: ")

        if opt == '1':
            sign_up()
        elif opt == '2':
            log_in()
        elif opt == '3':
            print("Bye Bye :)")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
