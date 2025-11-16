"""
State management module for the Modality Emulator application.
Contains data models and application state.
"""
from dataclasses import dataclass
from typing import List, Optional
from enum import Enum


class PatientData:
    """
    Represents a patient record in the worklist
    """
    def __init__(self, patient_id: str, patient_name: str, patient_birth_date: str, 
                 patient_sex: str, accession_number: str, study_description: str,
                 modality: str, study_date: str):
        self.patient_id = patient_id
        self.patient_name = patient_name
        self.patient_birth_date = patient_birth_date
        self.patient_sex = patient_sex
        self.accession_number = accession_number
        self.study_description = study_description
        self.modality = modality
        self.study_date = study_date


@dataclass
class AppStatus:
    """
    Represents the current status of the application
    """
    is_scanning: bool = False
    is_cancelled: bool = False
    message: str = ""
    worklist: List[PatientData] = None
    
    def __post_init__(self):
        if self.worklist is None:
            self.worklist = []


class AppState:
    """
    Main application state manager
    """
    def __init__(self):
        self.status = AppStatus()
        self._observers = []
    
    def add_observer(self, observer):
        """Add an observer to be notified of state changes"""
        self._observers.append(observer)
    
    def remove_observer(self, observer):
        """Remove an observer"""
        if observer in self._observers:
            self._observers.remove(observer)
    
    def notify_observers(self):
        """Notify all observers of state changes"""
        for observer in self._observers:
            observer.update()
    
    def update_scanning_status(self, is_scanning: bool):
        """Update scanning status"""
        self.status.is_scanning = is_scanning
        if is_scanning:
            self.status.message = "Scanning..."
        else:
            self.status.message = ""
        self.notify_observers()
    
    def update_cancel_status(self):
        """Update cancel status"""
        self.status.is_cancelled = True
        self.status.is_scanning = False
        self.status.message = "Operation cancelled"
        self.notify_observers()
    
    def reset_cancel_status(self):
        """Reset cancel status"""
        self.status.is_cancelled = False
        self.notify_observers()
    
    def set_worklist(self, worklist: List[PatientData]):
        """Set the worklist data"""
        self.status.worklist = worklist
        self.notify_observers()
    
    def clear_worklist(self):
        """Clear the worklist data"""
        self.status.worklist = []
        self.notify_observers()
    
    def add_patient(self, patient: PatientData):
        """Add a patient to the worklist"""
        self.status.worklist.append(patient)
        self.notify_observers()