import flet as ft
from datetime import datetime


def main(page: ft.Page):
    page.title = "Modality Emulator"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.bgcolor = "#f5f5f5"

    # --- HEADER ---
    header = ft.Container(
        content=ft.Column([
            ft.Text("Modality Emulator", size=24,
                    weight=ft.FontWeight.BOLD, color="white"),
            ft.Text("Medical Imaging System Interface",
                    size=14, color="white70")
        ], spacing=3),
        # Reduced vertical padding
        padding=ft.Padding.symmetric(horizontal=20, vertical=15),
        bgcolor="#1976d2",
        border_radius=ft.BorderRadius(
            top_left=0, top_right=0, bottom_left=0, bottom_right=0)
    )

    # --- DATA WORKLIST ---
    worklist_data = [
        {"id": "P001", "name": "John Doe", "age": 45, "gender": "M",
            "date": "2025-11-15", "modality": "CT", "desc": "CT Abdomen"},
        {"id": "P002", "name": "Jane Smith", "age": 32, "gender": "F",
            "date": "2025-11-15", "modality": "MR", "desc": "MRI Brain"},
        {"id": "P003", "name": "Robert Johnson", "age": 58, "gender": "M",
            "date": "2025-11-14", "modality": "X-Ray", "desc": "Chest X-Ray"},
        {"id": "P004", "name": "Emily Davis", "age": 29, "gender": "F",
            "date": "2025-11-14", "modality": "US", "desc": "Abdominal Ultrasound"},
    ]

    # --- HELPER: GENDER BADGE ---
    def get_gender_badge(gender):
        color = "#bbdefb" if gender == "M" else "#ffcdd2"
        return ft.Container(
            content=ft.Text(gender, size=12, weight=ft.FontWeight.BOLD),
            bgcolor=color,
            padding=ft.Padding.symmetric(horizontal=8, vertical=2),
            border_radius=15,
        )

    # --- HELPER: MODALITY BADGE ---
    def get_modality_badge(modality):
        colors = {
            "CT": "#e1bee7",
            "MR": "#c8e6c9",
            "X-Ray": "#ffcc80",
            "US": "#bbdefb"
        }
        color = colors.get(modality, "#ffffff")
        return ft.Container(
            content=ft.Text(modality, size=12, weight=ft.FontWeight.BOLD),
            bgcolor=color,
            padding=ft.Padding.symmetric(horizontal=8, vertical=2),
            border_radius=15,
        )

    # --- CUSTOM WORKLIST TABLE ---
    # Create the header row - with consistent structure to data rows
    header_row = ft.Container(
        content=ft.Row(
            controls=[
                ft.Container(content=ft.Row([ft.Text("PATIENT ID", size=12, weight=ft.FontWeight.BOLD)], spacing=5), expand=True, padding=ft.Padding(10, 10, 5, 10)),
                ft.Container(content=ft.Text("NAME", size=12, weight=ft.FontWeight.BOLD), expand=True, padding=ft.Padding(5, 10, 5, 10)),
                ft.Container(content=ft.Text("AGE", size=12, weight=ft.FontWeight.BOLD), expand=True, padding=ft.Padding(5, 10, 5, 10)),
                ft.Container(content=ft.Text("GENDER", size=12, weight=ft.FontWeight.BOLD), expand=True, padding=ft.Padding(5, 10, 5, 10)),
                ft.Container(content=ft.Row([ft.Text("STUDY DATE", size=12, weight=ft.FontWeight.BOLD)], spacing=5), expand=True, padding=ft.Padding(5, 10, 5, 10)),
                ft.Container(content=ft.Text("MODALITY", size=12, weight=ft.FontWeight.BOLD), expand=True, padding=ft.Padding(5, 10, 10, 10)),
            ],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        ),
        bgcolor="#f0f0f0",
        border=ft.Border.all(1, "#d0d0d0"),
        border_radius=ft.BorderRadius(5, 5, 0, 0)
    )

    # Create the data rows - match structure and padding of header
    data_rows = []
    for item in worklist_data:
        row = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(content=ft.Row([ft.Icon(ft.Icons.PERSON, size=16), ft.Text(item["id"])], spacing=5), expand=True, padding=ft.Padding(10, 10, 5, 10)),
                    ft.Container(content=ft.Text(item["name"]), expand=True, padding=ft.Padding(5, 10, 5, 10)),
                    ft.Container(content=ft.Text(str(item["age"])), expand=True, padding=ft.Padding(5, 10, 5, 10)),
                    ft.Container(content=get_gender_badge(item["gender"]), expand=True, padding=ft.Padding(5, 10, 5, 10)),
                    ft.Container(content=ft.Row([ft.Icon(ft.Icons.CALENDAR_TODAY, size=16), ft.Text(item["date"])], spacing=5), expand=True, padding=ft.Padding(5, 10, 5, 10)),
                    ft.Container(content=get_modality_badge(item["modality"]), expand=True, padding=ft.Padding(5, 10, 10, 10)),
                ],
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            ),
            border=ft.Border.only(bottom=ft.BorderSide(1, "#e0e0e0")),
            bgcolor="white"
        )
        data_rows.append(row)

    # Combine header and data rows in a column
    worklist_table = ft.Column(
        controls=[header_row] + data_rows,
        spacing=0,
        expand=True,
        scroll=ft.ScrollMode.AUTO
    )

    # --- GET WORKLIST BUTTON ---
    get_worklist_btn = ft.FilledButton(
        "Get Worklist",
        icon=ft.Icons.SEARCH,
        bgcolor="#1976d2",
        color="white",
        on_click=lambda e: print("Get Worklist clicked"),
        height=40,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8)
        )
    )

    # --- PAGINATION ---
    pagination = ft.Row(
        alignment=ft.MainAxisAlignment.END,
        controls=[
            ft.OutlinedButton("Previous", disabled=True),
            ft.OutlinedButton("Next", disabled=True)
        ]
    )

    # --- WORKLIST PANEL ---
    worklist_panel = ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text("Worklist", size=20, weight=ft.FontWeight.BOLD),
                    ft.Container(expand=True),
                    get_worklist_btn
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Divider(height=1, thickness=1, color="transparent"),
                ft.Container(
                    content=worklist_table,
                    bgcolor="white",
                    border=ft.Border(
                        left=ft.BorderSide(1, "transparent"),
                        top=ft.BorderSide(1, "transparent"),
                        right=ft.BorderSide(1, "transparent"),
                        bottom=ft.BorderSide(1, "transparent")
                    ),
                    border_radius=8,
                    padding=10,
                    expand=True  # Ensure container expands to fill space
                ),
                ft.Divider(height=1, thickness=1, color="transparent"),
                ft.Row([
                    ft.Text("Showing 4 of 4 results", size=12, color="gray"),
                    ft.Container(expand=True),
                    pagination
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER)
            ], spacing=15),
            padding=20,
            bgcolor="white",
            border_radius=10,
            shadow=ft.BoxShadow(
                blur_radius=5, spread_radius=1, color=ft.Colors.GREY_200)
        )
    )

    # --- CONTROLS PANEL ---
    scan_btn = ft.FilledButton(
        "Scan",
        icon=ft.Icons.PLAY_ARROW,
        bgcolor="#388e3c",
        color="white",
        on_click=lambda e: print("Scan clicked"),
        height=50,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8)
        )
    )

    cancel_btn = ft.FilledButton(
        "Cancel",
        icon=ft.Icons.CLOSE,
        bgcolor="#bdbdbd",
        color="black",
        on_click=lambda e: print("Cancel clicked"),
        height=50,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8)
        )
    )

    controls_panel = ft.Card(
        content=ft.Container(
            content=ft.Row([
                ft.Text("Modality Control", size=18,
                        weight=ft.FontWeight.BOLD),
                ft.Divider(height=1, thickness=1, color="transparent"),
                scan_btn,
                ft.Divider(height=5, thickness=1, color="transparent"),
                cancel_btn
            ], spacing=15),
            padding=20,
            bgcolor="white",
            border_radius=10,
            shadow=ft.BoxShadow(
                blur_radius=5, spread_radius=1, color=ft.Colors.GREY_200)
        )
    )

    # --- SYSTEM STATUS PANEL ---
    system_status_panel = ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Text("System Status", size=18, weight=ft.FontWeight.BOLD),
                ft.Divider(height=1, thickness=1, color="transparent"),
                ft.Row([
                    ft.Text("Status", size=14),
                    ft.Container(expand=True),
                    ft.Text("Ready", size=14, color="green",
                            weight=ft.FontWeight.BOLD)
                ]),
                ft.Row([
                    ft.Text("Worklist", size=14),
                    ft.Container(expand=True),
                    ft.Text("4 records", size=14, color="blue",
                            weight=ft.FontWeight.BOLD)
                ])
            ], spacing=10),
            padding=20,
            bgcolor="white",
            border_radius=10,
            shadow=ft.BoxShadow(
                blur_radius=5, spread_radius=1, color=ft.Colors.GREY_200)
        )
    )

    # --- LAYOUT UTAMA ---
    left_column = ft.Column([
        controls_panel,
        ft.Divider(height=20, thickness=1, color="transparent"),
        system_status_panel
    ], spacing=20, expand=False)

    right_column = ft.Column([
        worklist_panel
    ], spacing=20)

    main_layout = ft.Row([
        ft.Container(left_column, width=300, padding=10),
        ft.Container(right_column, expand=True, padding=10)
    ], spacing=20, expand=True)  # Main row expands to fill available width

    # Add all elements to page with proper expansion
    page.add(
        ft.Column([
            ft.Container(
                header,
                expand=False,  # Make header container expand to full width
            ),
            main_layout
        ], expand=True, horizontal_alignment=ft.CrossAxisAlignment.STRETCH)
    )


# Jalankan aplikasi
if __name__ == "__main__":
    ft.run(main)
