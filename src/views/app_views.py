"""
Views module for the Modality Emulator application.
Contains UI components and views.
"""
import flet as ft
from typing import Callable
from ..states.app_state import AppState, PatientData


class HeaderView:
    """
    Header view component displaying the application title
    """
    def __init__(self):
        self.container = ft.Container(
            content=ft.Text(
                "Modality Emulator",
                size=32,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.PRIMARY
            ),
            padding=ft.Padding(15, 15, 15, 10),
            alignment=ft.Alignment(-1, 0)
        )
    
    def get_view(self):
        return self.container


class ControlPanelView:
    """
    Control panel view with Scan and Cancel buttons
    """
    def __init__(self, on_scan: Callable[[], None], on_cancel: Callable[[], None], app_state: AppState):
        self.on_scan = on_scan
        self.on_cancel = on_cancel
        self.app_state = app_state
        self.app_state.add_observer(self)
        
        self.scan_button = ft.ElevatedButton(
            "Scan",
            on_click=lambda e: self.on_scan(),
            disabled=self.app_state.status.is_scanning
        )
        
        self.cancel_button = ft.ElevatedButton(
            "Cancel",
            on_click=lambda e: self.on_cancel(),
            disabled=not self.app_state.status.is_scanning
        )
        
        self.container = ft.Container(
            content=ft.Column([
                self.scan_button,
                ft.Divider(height=10, thickness=0),
                self.cancel_button
            ], 
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=15,
            margin=ft.Margin(10, 10, 10, 10),
            border=ft.border.all(1, ft.Colors.OUTLINE),
            border_radius=ft.BorderRadius(8, 8, 8, 8)
        )
    
    def get_view(self):
        return self.container
    
    def update(self):
        """Update the control panel based on state changes"""
        self.scan_button.disabled = self.app_state.status.is_scanning
        self.cancel_button.disabled = not self.app_state.status.is_scanning
        self.container.update()


class WorklistHeaderView:
    """
    Header for the worklist section with Get Worklist button
    """
    def __init__(self, on_get_worklist: Callable[[], None], app_state: AppState):
        self.on_get_worklist = on_get_worklist
        self.app_state = app_state
        self.app_state.add_observer(self)
        
        self.get_worklist_button = ft.ElevatedButton(
            "Get Worklist",
            on_click=lambda e: self.get_worklist()
        )
        
        self.row = ft.Row(
            controls=[
                ft.Text("Modality Worklist", size=18, weight=ft.FontWeight.W_500),
                ft.Container(expand=True),
                self.get_worklist_button
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )
    
    def get_view(self):
        return self.row
    
    def update(self):
        """Update the header based on state changes"""
        # No need to update anything specific in this view
        pass


class WorklistTableView:
    """
    Table view to display patient worklist data
    """
    def __init__(self, app_state: AppState):
        self.app_state = app_state
        self.app_state.add_observer(self)
        
        self.data_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Patient ID")),
                ft.DataColumn(ft.Text("Patient Name")),
                ft.DataColumn(ft.Text("Birth Date")),
                ft.DataColumn(ft.Text("Sex")),
                ft.DataColumn(ft.Text("Accession No.")),
                ft.DataColumn(ft.Text("Study Description")),
                ft.DataColumn(ft.Text("Modality")),
                ft.DataColumn(ft.Text("Study Date")),
            ],
            rows=[]
        )
        
        self.status_text = ft.Text(self.app_state.status.message, color=ft.Colors.AMBER)
        
        self.column = ft.Column([
            self.status_text,
            ft.Divider(thickness=1),
            ft.Container(
                content=self.data_table,
                expand=True,
                padding=ft.Padding(0, 5, 0, 0)
            )
        ], expand=True)
    
    def get_view(self):
        return self.column
    
    def update(self):
        """Update the table based on state changes"""
        # Update status message
        self.status_text.value = self.app_state.status.message
        
        # Update table rows
        self.data_table.rows = []
        for patient in self.app_state.status.worklist:
            self.data_table.rows.append(
                ft.DataRow([
                    ft.DataCell(ft.Text(patient.patient_id)),
                    ft.DataCell(ft.Text(patient.patient_name)),
                    ft.DataCell(ft.Text(patient.patient_birth_date)),
                    ft.DataCell(ft.Text(patient.patient_sex)),
                    ft.DataCell(ft.Text(patient.accession_number)),
                    ft.DataCell(ft.Text(patient.study_description)),
                    ft.DataCell(ft.Text(patient.modality)),
                    ft.DataCell(ft.Text(patient.study_date)),
                ])
            )
        
        self.column.update()


class MainDashboardView:
    """
    Main dashboard view that combines all components
    """
    def __init__(self, 
                 header_view: HeaderView, 
                 control_panel_view: ControlPanelView,
                 worklist_header_view: WorklistHeaderView,
                 worklist_table_view: WorklistTableView):
        self.header_view = header_view
        self.control_panel_view = control_panel_view
        self.worklist_header_view = worklist_header_view
        self.worklist_table_view = worklist_table_view
        
        self.column = ft.Column([
            self.header_view.get_view(),
            ft.Row([
                ft.Container(
                    content=self.control_panel_view.get_view(),
                    width=300,  # Left column takes 1/3 of the space approximately
                    padding=ft.Padding(10, 0, 10, 0)
                ),
                ft.Container(
                    content=ft.Column([
                        self.worklist_header_view.get_view(),
                        self.worklist_table_view.get_view()
                    ], expand=True),
                    expand=True,  # Right column takes 2/3 of the space
                    padding=ft.Padding(10, 0, 10, 0)
                )
            ], expand=True)
        ], expand=True)
    
    def get_view(self):
        return self.column