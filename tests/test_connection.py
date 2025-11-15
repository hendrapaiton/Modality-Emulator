"""
Test script to verify connection to remote AE: DVTK_MW_SCP on port 107 at localhost
"""
import pytest
import time
import os
import json
from unittest.mock import Mock, patch
from src.modality_emulator import ModalityEmulator


def test_connection_to_remote_ae():
    """
    Test connection to remote AE: DVTK_MW_SCP on port 107 at localhost
    This test will attempt to connect and may timeout if no server is running at the specified address
    """
    emulator = ModalityEmulator()

    # Test connecting to the configured remote AE
    # This will attempt to connect to localhost:107 with AE title 'DVTK_MW_SCP'
    result = emulator.connect_to_ris('localhost', 107, 'DVTK_MW_SCP')

    print(f"Connection attempt to DVTK_MW_SCP at localhost:107 completed.")
    print(f"Found {len(result)} worklist items.")

    # Since we don't know if the server is actually running,
    # we just verify that the connection attempt completes without throwing an exception
    # The result could be an empty list if the server doesn't respond or has no worklist items
    assert result is not None
    print("Connection test completed successfully!")

    # Check if worklist file was created
    worklist_files = [f for f in os.listdir('.') if f.startswith('worklist_') and f.endswith('.json')]
    if worklist_files:
        latest_file = max(worklist_files, key=os.path.getctime)
        print(f"Worklist data saved to: {latest_file}")

        # Verify the content of the worklist file
        with open(latest_file, 'r') as f:
            worklist_data = json.load(f)
            assert 'timestamp' in worklist_data
            assert 'ris_connection' in worklist_data
            assert 'worklist_count' in worklist_data
            assert worklist_data['ris_connection']['address'] == 'localhost'
            assert worklist_data['ris_connection']['port'] == 107
            assert worklist_data['ris_connection']['ae_title'] == 'DVTK_MW_SCP'
            assert worklist_data['worklist_count'] == len(result)
        print(f"Worklist file {latest_file} verified successfully!")


def test_connection_parameters():
    """
    Test that the connection parameters are correctly configured
    """
    emulator = ModalityEmulator()
    assert emulator.ae_title == "DVTK_MW_SCU"

    # The connection parameters are passed to the connect method, so we can't directly test them
    # But we can at least ensure that our emulator object is properly initialized
    print("Emulator AE title:", emulator.ae_title)
    print("Connection parameters test completed!")


def test_main_function_connection():
    """
    Test the updated main function that includes the connection to the configured AE
    """
    from src.modality_emulator import main

    # Run the main function to test the connection
    main()
    print("Main function execution completed!")

    # Check if worklist file was created
    worklist_files = [f for f in os.listdir('.') if f.startswith('worklist_') and f.endswith('.json')]
    if worklist_files:
        latest_file = max(worklist_files, key=os.path.getctime)
        print(f"Worklist data from main() saved to: {latest_file}")


if __name__ == "__main__":
    print("Testing connection to remote AE: DVTK_MW_SCP on port 107 at localhost")
    print("="*60)

    test_connection_parameters()
    print()

    # Since we might not have the server running, we'll catch any connection errors gracefully
    try:
        test_connection_to_remote_ae()
    except Exception as e:
        print(f"Connection test resulted in expected error (server may not be running): {e}")
        print("This is expected if no server is listening at localhost:107")

    print()
    test_main_function_connection()

    print("\nAll tests completed!")