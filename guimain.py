import flet as ft
import pyttsx3
from datetime import datetime
import mysql.connector as sql
import mysql.connector
import re

def main(page: ft.Page):
    page.title = "Library Management System"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = "black"  # Set the background color to black

    
    def admin_login_page(e):
        page.clean()
        def log_in(e):
            print("log in button clicked ")
        log_in_button = ft.ElevatedButton(
            text="LOG IN",
            bgcolor=ft.colors.CYAN_ACCENT,
            color="red",
            width=200,
            height=60,
            on_click=login_for_all
        )
        exit_button = ft.ElevatedButton(
            text="EXIT",
            bgcolor=ft.colors.GREEN_ACCENT_400,
            color="white",
            width=200,
            height=60,
            on_click=lambda e: page.window_close()
        )
        page.add(
            ft.Column(
                [
                    log_in_button,
                    ft.Container(padding=ft.padding.all(20)),
                    exit_button
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )
        
        
    def open_login_sigup_page(e):
        page.clean()
        
        def sign_up(e):
            print("Sign up button clicked")
            
        def log_in(e):
            print("log in button clicked ")
        
        sign_up_button = ft.ElevatedButton(
            text="SIGN UP",
            bgcolor=ft.colors.PURPLE_ACCENT,
            color="white",
            width=200,
            height=60,
            on_click=show_registration_form
        )  
        
        log_in_button = ft.ElevatedButton(
            text="LOG IN",
            bgcolor=ft.colors.CYAN_ACCENT,
            color="red",
            width=200,
            height=60,
            on_click=login_for_all
        )
        
        exit_button = ft.ElevatedButton(
            text="EXIT",
            bgcolor=ft.colors.GREEN_ACCENT_400,
            color="white",
            width=200,
            height=60,
            on_click=lambda e: page.window_close()
        )
        page.add(
            ft.Column(
                [
                    # admin_student_title,
                    # ft.Container(padding=ft.padding.all(20)),
                    sign_up_button,
                    ft.Container(padding=ft.padding.all(20)),
                    log_in_button,
                    ft.Container(padding=ft.padding.all(20)),
                    exit_button
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )
        def speak(text):
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()

        def greet_based_on_time():
            speak("okay so login now ")

        if __name__ == "__main__":
            greet_based_on_time()
    def login_for_all(e):
        page.bgcolor = "#EBEFFF"
        # page.color="black"
        page.clean()

        username = ft.TextField(label="Username:", width=300, text_style=ft.TextStyle(color="black"))
        password = ft.TextField(label="Password:", width=300, password=True, text_style=ft.TextStyle(color="black"))
      
        def on_login(e):
        # Connect to the database
            try:
                mycon = mysql.connector.connect(host='localhost', user='root', passwd='admin', database='deepak')
                cursor = mycon.cursor()
            
                # Query to check if the username and password exist
                query = "SELECT * FROM student WHERE full_name = %s AND password = %s"
                values = (username.value, password.value)
                cursor.execute(query, values)
            
                # Fetch result
                result = cursor.fetchone()
                if result:
                    print(f"Login successful for {username.value}")
                else:
                    print("User does not exist")
        
            except mysql.connector.Error as ex:
                print(f'An error occurred: {ex}')
        
            finally:
                cursor.close()
                mycon.close()
                
        # Login button
        login_button = ft.ElevatedButton(text="Login", width=300, on_click=on_login)

        # Register link text
        register_link = ft.Text(
            spans=[
                ft.TextSpan("Don't have an account? ", ft.TextStyle(color="black")),  # Setting color to black
                ft.TextSpan("Register", ft.TextStyle(color="blue", weight="bold"), on_click=show_registration_form)  # The Register link is in blue
            ],
            size=12
        )

        # Form column with the welcome back, username, password, and login button
        form_column = ft.Column(
            controls=[
                ft.Text("Welcome Back!", size=18, weight="bold", color="black"),
                username,
                password,
                login_button,
                register_link
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        # Left-side container (Login form)
        left_side = ft.Container(
            content=form_column,
            padding=ft.Padding(left=50, top=100,right=50,bottom=100),  # Add padding to position the form
            alignment=ft.alignment.top_left,
        )

        # Right-side container (Illustration)
        right_side = ft.Container(
            content=ft.Image(src="images/log_in.png", width=400),  # Placeholder for the image
            padding=ft.Padding(right=50, top=50,left=50,bottom=50),
            alignment=ft.alignment.center_right,
        )

        # Row Layout for the two sections
        layout = ft.Row(
            controls=[left_side, right_side],  # Form on the left, image on the right
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
        page.add(layout)
    
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
        if len(digits) == 0 or len(digits[0]) < 8:
            print("Email username should have at least 8 digits after '.'")
            return False

        return True

    def show_registration_form(e):
        page.clean()
        page.bgcolor = "#EBEFFF"
        
        full_name = ft.TextField(label="Full name", width=300,color="black")
        
        phone_number = ft.TextField(label="Phone Number", width=300,color="black")
        
        email = ft.TextField(label="Email", width=300,color="black")

        password = ft.TextField(label="Password", password=True, width=300,color="black")

        confirm_password = ft.TextField(label="Confirm Password", password=True, width=300,color="black")
        
        # Error message for phone number validation
        error_message = ft.Text(value="", color="red")
        
        def register_clicked(e):
            
            # Check if any field is blank
            if not full_name.value:
                error_message.value = "Full name is required."
                error_message.update()
                return
            if not phone_number.value:
                error_message.value = "Phone number is required."
                error_message.update()
                return
            
            # Validate phone number length
            if len(phone_number.value) != 10 or not phone_number.value.isdigit():
                error_message.value = "Please enter a valid 10-digit phone number."
                error_message.update()
                return
            else:
                error_message.value = "" 
                error_message.update()
                
            if not email.value:
                error_message.value = "Email is required."
                error_message.update()
                return
            
            # Validate email format
            if not check_email(email.value):
                error_message.value = "Invalid email format. Please use a valid 'gehu.ac.in' email."
                error_message.update()
                return
            else:
                error_message.value = ""  # Clear error message if all validations pass
                error_message.update()
                
            if not password.value:
                error_message.value = "Password is required."
                error_message.update()
                return
            if not confirm_password.value:
                error_message.value = "Confirm password is required."
                error_message.update()
                return
            
            # Validate if passwords match
            if password.value != confirm_password.value:
                error_message.value = "Passwords do not match. Please re-enter."
                error_message.update()
                return

            # Clear error message if all validations pass
            error_message.value = ""
            error_message.update()

            
            try:
                mycon = mysql.connector.connect(host='localhost', user='root', passwd='admin', database='deepak')
                cursor = mycon.cursor()
                mycon.autocommit = True

                # Check if user already exists based on full name, phone number, or email
                query = "SELECT * FROM student WHERE full_name = %s OR email = %s"
                cursor.execute(query, (full_name.value, email.value))
                existing_user = cursor.fetchone()

                if existing_user:
                    error_message.value = "User already exists. Try with another Name or email."
                    error_message.update()
                else:
                    # Insert new user if not a duplicate
                    query = "INSERT INTO student (full_name, phone_number, email, password) VALUES (%s, %s, %s, %s)"
                    values = (full_name.value, phone_number.value, email.value, password.value)
                    cursor.execute(query, values)

                    print("Registration successful")
                    error_message.value = "Registration successful!"
                    error_message.update()
        
            except mysql.connector.Error as ex:
                print(f"An error occurred: {ex}")
                error_message.value = f"An error occurred: {ex}"
                error_message.update()

            finally:
                cursor.close()
                mycon.close()
            
        register_button = ft.ElevatedButton(
            text="Register", 
            bgcolor=ft.colors.BLUE_ACCENT,
            color="white",
            on_click=register_clicked
        )
        
        def on_click(e):
            print(f"Full name entered: {full_name.value}")
            page.add(ft.Text(f"Full name is: {full_name.value}"))

        # TextField for full name
        full_name = ft.TextField(
            label="Full name", 
            width=300, 
            text_style=ft.TextStyle(color="black")  # Set the input text color to black
        )

        # ElevatedButton that prints full name on click
        full_name_button = ft.ElevatedButton(
            text="Submit Full Name", 
            color="black",
            on_click=on_click  # Calls the function when clicked
        )

        # Login link
        login_link = ft.TextButton(
            text="Yes I have an account? Login", 
            on_click=login_for_all
        )

        # Registration form layout

        form_column = ft.Column( 
            controls=[
                ft.Text("Please Fill out the form to Register!", size=18, weight="bold", color="black"),
                full_name,  # Full name input with black text
                phone_number,
                email,
                password,
                confirm_password,
                register_button,
                login_link
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )


        # Image section (left side)
        form_image = ft.Image(
            src="images/sign_up.png",  # You can replace this with the actual path or URL of your image
            width=600,
            # height=800,
            fit=ft.ImageFit.COVER,
        )

        # Add image and form side by side in a row
        page.add(
            ft.Row(
                controls=[
                    form_image,
                    form_column,
                    error_message
                ],
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            )
        )
        
        def speak(text):
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()

        def greet_based_on_time():
            speak("Please Fill out Details to Register! ")

        if __name__ == "__main__":
            greet_based_on_time()
        
        
    # Function to navigate to the new "Admin/Student" page
    def open_admin_student_page(e):
        # Clear the current page content
        page.clean()

        # Title text for the new page
        admin_student_title = ft.Text(
            value="Select Your Role",
            size=24,
            color="white"
        )

        # Function to handle Admin button click
        def admin_button_clicked(e):
            print("Admin button clicked")

        # Function to handle Student button click
        def student_button_clicked(e):
            print("Student button clicked")

        # Admin and Student buttons
        admin_button = ft.ElevatedButton(
            text="ADMIN",
            bgcolor=ft.colors.PURPLE_ACCENT,
            color="white",
            width=200,
            height=60,
            on_click=admin_login_page
        )

        student_button = ft.ElevatedButton(
            text="STUDENT",
            bgcolor=ft.colors.CYAN_ACCENT,
            color="red",
            width=200,
            height=60,
            on_click=open_login_sigup_page
        )

        # Display buttons in a column
        page.add(
            ft.Column(
                [
                    admin_student_title,
                    ft.Container(padding=ft.padding.all(20)),
                    admin_button,
                    ft.Container(padding=ft.padding.all(20)),
                    student_button
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )
        def speak(text):
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()

        def greet_based_on_time():
            speak("Select Your role ")

        if __name__ == "__main__":
            greet_based_on_time()
            
    title = ft.Text(
        value="WELCOME TO LIBRARY MANAGEMENT SYSTEM",
        size=24,
        color="white"
    )

    start_button = ft.ElevatedButton(
        text="START",
        bgcolor=ft.colors.PURPLE_ACCENT,
        # color="white",
        width=200,
        height=60,
        on_click=open_admin_student_page  # Open the new page on click
    )

    exit_button = ft.ElevatedButton(
        text="EXIT",
        bgcolor=ft.colors.CYAN_ACCENT,
        color="red",
        width=200,
        height=60,
        on_click=lambda e: page.window_close()
    )
    

    # Layout the main page elements
    page.add(
        ft.Column(
            [
                
                title,
                ft.Container(padding=ft.padding.all(20)),
                start_button,
                ft.Container(padding=ft.padding.all(20)),
                exit_button,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )
    

    def speak(text):
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()

    def greet_based_on_time():
        current_time = datetime.now()
        hour = current_time.hour

        if hour < 12:
            speak("Good morning!")
        elif 12 <= hour < 18:
            speak("Good afternoon!")
        else:
            speak("Good evening!")

        speak("Welcome to the Library Management System.")

    if __name__ == "__main__":
        greet_based_on_time()

ft.app(target=main)
