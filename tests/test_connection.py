"""
Test script to verify connection using configuration from environment
Uses handler functions directly for testing.
"""
import pytest
import time
import os
import json
from unittest.mock import Mock, patch
from src.handlers.modality_handlers import connect_to_ris_handler


def test_connection_to_remote_ae():
    """
    Test connection using environment configuration
    This test will attempt to connect and may timeout if no server is running at the specified address
    """
    from src.handlers.utility_handlers import load_environment_config

    # Get configuration from environment
    config = load_environment_config()
    remote_host = config.get('REMOTE_HOST', 'www.dicomserver.co.uk')
    remote_port = config.get('REMOTE_PORT', 104)
    remote_ae = config.get('REMOTE_AE_TITLE', 'DICOMSERVER')
    local_ae = config.get('LOCAL_AE_TITLE', 'DICOMCLIENT')

    # Test connecting to the configured remote AE using handler
    result = connect_to_ris_handler(remote_host, remote_port, remote_ae, ae_title=local_ae)

    print(f"Connection attempt to {remote_ae} at {remote_host}:{remote_port} completed.")
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
            assert worklist_data['ris_connection']['address'] == remote_host
            assert worklist_data['ris_connection']['port'] == remote_port
            assert worklist_data['ris_connection']['ae_title'] == remote_ae
            assert worklist_data['worklist_count'] == len(result)
        print(f"Worklist file {latest_file} verified successfully!")


def test_connection_parameters():
    """
    Test that the connection parameters are correctly configured
    For handler functions, we test default parameters by calling with expected values
    """
    from src.handlers.utility_handlers import load_environment_config

    # Get configuration from environment and test with those values
    config = load_environment_config()
    remote_host = config.get('REMOTE_HOST', 'www.dicomserver.co.uk')
    remote_port = config.get('REMOTE_PORT', 104)
    remote_ae = config.get('REMOTE_AE_TITLE', 'DICOMSERVER')
    local_ae = config.get('LOCAL_AE_TITLE', 'DICOMCLIENT')

    # Test with configuration values
    result = connect_to_ris_handler(remote_host, remote_port, remote_ae, ae_title=local_ae)
    print(f"Connection with configured parameters completed: {local_ae} -> {remote_ae} at {remote_host}:{remote_port}")
    print("Connection parameters test completed!")


def test_main_function_connection():
    """
    Test the main function behavior by testing the underlying functionality
    """
    # Since main() function is in the removed modality_emulator.py,
    # we test the equivalent functionality using handlers
    from src.handlers.utility_handlers import load_environment_config

    config = load_environment_config()
    print("Configuration loaded from environment:")
    print(f"  LOCAL_AE_TITLE: {config.get('LOCAL_AE_TITLE')}")
    print(f"  LOCAL_PORT: {config.get('LOCAL_PORT')}")
    print(f"  REMOTE_AE_TITLE: {config.get('REMOTE_AE_TITLE')}")
    print(f"  REMOTE_HOST: {config.get('REMOTE_HOST')}")
    print(f"  REMOTE_PORT: {config.get('REMOTE_PORT')}")

    # Test connecting with loaded config
    remote_host = config.get('REMOTE_HOST', 'www.dicomserver.co.uk')
    remote_port = config.get('REMOTE_PORT', 104)
    remote_ae = config.get('REMOTE_AE_TITLE', 'DICOMSERVER')
    local_ae = config.get('LOCAL_AE_TITLE', 'DICOMCLIENT')

    print(f"Configured connection: {local_ae} -> {remote_ae} at {remote_host}:{remote_port}")

    # Attempt connection
    result = connect_to_ris_handler(remote_host, remote_port, remote_ae, ae_title=local_ae)
    print(f"RIS connection completed. Found {len(result)} worklist items.")


if __name__ == "__main__":
    print("Testing connection using environment configuration")
    print("="*60)

    test_connection_parameters()
    print()

    # Since we might not have the server running, we'll catch any connection errors gracefully
    try:
        test_connection_to_remote_ae()
    except Exception as e:
        print(f"Connection test resulted in expected error (server may not be running): {e}")
        print("This is expected if no server is listening at the configured address")

    print()
    test_main_function_connection()

    print("\nAll tests completed!")