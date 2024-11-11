import flet as ft
from flet import Page as page
import mysql.connector


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
            ft.TextSpan("Register", ft.TextStyle(color="blue", weight="bold"), )  # The Register link is in blue
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