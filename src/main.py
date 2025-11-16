import flet as ft


def main(page: ft.Page):
    """
    The main function that runs the Flet application.

    Args:
        page: The Flet page object that represents the UI
    """
    # Set the page title
    page.title = "Hello World with Flet"

    # Set the page alignment to center
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Create a text element with "Hello, World!"
    hello_text = ft.Text(
        value="Hello, World!",
        size=30,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.BLUE_600
    )

    # Add the text to the page
    page.add(hello_text)


# Run the Flet application
if __name__ == "__main__":
    ft.run(main)