"""
Utility Handlers - Common utility functions for the Modality Emulator GUI

This module contains utility functions that can be called from the GUI.
"""
import os
import logging
from dotenv import load_dotenv


def load_environment_config():
    """
    Load environment configuration variables
    
    :return: Dictionary containing configuration values
    """
    load_dotenv()
    
    config = {
        'LOCAL_AE_TITLE': os.getenv('LOCAL_AE_TITLE', 'DVTK_MW_SCU'),
        'LOCAL_PORT': int(os.getenv('LOCAL_PORT', 11112)),
        'REMOTE_AE_TITLE': os.getenv('REMOTE_AE_TITLE', 'DVTK_MW_SCP'),
        'REMOTE_HOST': os.getenv('REMOTE_HOST', 'localhost'),
        'REMOTE_PORT': int(os.getenv('REMOTE_PORT', 107))
    }
    
    return config


def setup_logging(level=logging.INFO):
    """
    Setup logging configuration
    
    :param level: Logging level (default: INFO)
    """
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def get_worklist_files():
    """
    Get list of worklist files in the current directory
    
    :return: List of worklist JSON files
    """
    import glob
    return glob.glob("worklist_*.json")


def get_dicom_files(directory=None):
    """
    Get list of DICOM files in a directory
    
    :param directory: Directory to search (default: current directory)
    :return: List of DICOM files
    """
    import glob
    if directory is None:
        directory = "."
    
    dicom_pattern = os.path.join(directory, "*.dcm")
    return glob.glob(dicom_pattern)