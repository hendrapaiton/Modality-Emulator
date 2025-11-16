import flet as ft
import sys
import os

# Add the project root to sys.path for imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.states.app_state import AppState
from src.handlers.app_handlers import ScanHandler, CancelHandler, WorklistHandler
from src.views.app_views import (
    HeaderView,
    ControlPanelView,
    WorklistHeaderView,
    WorklistTableView,
    MainDashboardView
)


def main(page: ft.Page):
    """
    The main function that runs the Modality Emulator application.

    Args:
        page: The Flet page object that represents the UI
    """
    # Set the page title and properties
    page.title = "Modality Emulator Dashboard"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.spacing = 0

    # Initialize application state
    app_state = AppState()

    # Initialize handlers
    scan_handler = ScanHandler(app_state)
    cancel_handler = CancelHandler(app_state)
    worklist_handler = WorklistHandler(app_state)

    # Initialize views
    header_view = HeaderView()

    async def handle_scan():
        await scan_handler.start_scan()

    async def handle_get_worklist():
        await worklist_handler.get_worklist()

    control_panel_view = ControlPanelView(
        on_scan=lambda e: page.run_task(handle_scan()),
        on_cancel=cancel_handler.cancel_operation,
        app_state=app_state
    )
    worklist_header_view = WorklistHeaderView(
        on_get_worklist=lambda e: page.run_task(handle_get_worklist()),
        app_state=app_state
    )
    worklist_table_view = WorklistTableView(app_state)

    # Create main dashboard view
    main_dashboard_view = MainDashboardView(
        header_view=header_view,
        control_panel_view=control_panel_view,
        worklist_header_view=worklist_header_view,
        worklist_table_view=worklist_table_view
    )

    # Add the main dashboard to the page
    page.add(main_dashboard_view.get_view())

    # Update page to render all components
    page.update()


# Run the Flet application
if __name__ == "__main__":
    ft.run(main)