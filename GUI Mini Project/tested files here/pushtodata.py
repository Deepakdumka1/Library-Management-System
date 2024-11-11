import sqlite3
import flet as ft

# Initialize the SQLite3 database
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # Create users table if not exists
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT UNIQUE
    )
    """)
    conn.commit()
    conn.close()

# Function to handle login and store username
def on_login(e):
    username_input = username.value.strip()

    if username_input:
        print(f"Logging in with Username: {username_input}")
        
        # Insert username into SQLite3 database
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        
        try:
            cursor.execute("INSERT INTO users (username) VALUES (?)", (username_input,))
            conn.commit()
            print("Username stored successfully in the database.")
        except sqlite3.IntegrityError:
            print("This username is already stored.")
        finally:
            conn.close()
    else:
        print("Username cannot be empty.")

# Initialize the database
init_db()

# Username and Password TextFields
username = ft.TextField(label="Username:", width=300, text_style=ft.TextStyle(color="black"))

# Use the on_login function when the login button is clicked
login_button = ft.ElevatedButton("Login", on_click=on_login)

# Add the username field and login button to your Flet page
def main(page: ft.Page):
    page.add(username, login_button)

# Start the Flet app
ft.app(target=main)
