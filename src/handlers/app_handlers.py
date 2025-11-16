"""
Handlers module for the Modality Emulator application.
Contains business logic and event handlers.
"""
import asyncio
import random
from datetime import datetime
from typing import List
from ..states.app_state import AppState, PatientData


class ScanHandler:
    """
    Handler for scan operations
    """
    def __init__(self, app_state: AppState):
        self.app_state = app_state
    
    async def start_scan(self):
        """Start the scanning process"""
        self.app_state.update_scanning_status(True)
        # Simulate scanning process
        await asyncio.sleep(2)  # Simulate time taken for scanning
        self.app_state.update_scanning_status(False)
        
        # Generate some dummy patient data for demonstration
        dummy_patients = [
            PatientData(
                patient_id=f"PID{1000 + i}",
                patient_name=f"Patient {i+1}",
                patient_birth_date=f"{1950 + i * 5}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
                patient_sex=random.choice(["M", "F"]),
                accession_number=f"ACC{2000 + i}",
                study_description=random.choice(["CT Abdomen", "MR Brain", "X-Ray Chest", "Ultrasound"]),
                modality=random.choice(["CT", "MR", "CR", "US"]),
                study_date=datetime.now().strftime("%Y-%m-%d")
            )
            for i in range(random.randint(3, 7))
        ]
        
        self.app_state.set_worklist(dummy_patients)


class CancelHandler:
    """
    Handler for cancel operations
    """
    def __init__(self, app_state: AppState):
        self.app_state = app_state
    
    def cancel_operation(self):
        """Cancel the current operation"""
        self.app_state.update_cancel_status()


class WorklistHandler:
    """
    Handler for worklist operations
    """
    def __init__(self, app_state: AppState):
        self.app_state = app_state
    
    async def get_worklist(self):
        """Get the worklist from the system"""
        # Simulate getting worklist data
        self.app_state.update_scanning_status(True)
        await asyncio.sleep(1.5)  # Simulate network delay
        
        # Generate dummy worklist data
        dummy_patients = [
            PatientData(
                patient_id=f"PID{3000 + i}",
                patient_name=f"Worklist Patient {i+1}",
                patient_birth_date=f"{1960 + i * 3}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
                patient_sex=random.choice(["M", "F", "O"]),
                accession_number=f"WL{4000 + i}",
                study_description=random.choice([
                    "CT Head without contrast", 
                    "MR Lumbar spine", 
                    "X-Ray Hand", 
                    "Ultrasound Abdomen",
                    "Mammography Screening"
                ]),
                modality=random.choice(["CT", "MR", "CR", "US", "MG"]),
                study_date=datetime.now().strftime("%Y-%m-%d")
            )
            for i in range(5)
        ]
        
        self.app_state.set_worklist(dummy_patients)
        self.app_state.update_scanning_status(False)
        self.app_state.reset_cancel_status()