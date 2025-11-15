"""
Test script to run the DICOM StoreCP Client from tests directory
"""
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from storescp_client import main

if __name__ == "__main__":
    main()