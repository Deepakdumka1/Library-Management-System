import flet as ft
from flet import Page as page
from .login import show_registration_form, login_for_all
import pyttsx3


def open_login_sigup_page(e):
    page.clean()
    def sign_up(e):
        print("Sign up button clicked")  
    def log_in(e):
        print("log in button clicked ")
    sign_up_button = ft.ElevatedButton(text="SIGN UP",bgcolor=ft.colors.PURPLE_ACCENT,color="white",width=200,height=60,on_click=show_registration_form)  
    log_in_button = ft.ElevatedButton(text="LOG IN",bgcolor=ft.colors.CYAN_ACCENT,color="red",    width=200,
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