"""
Test script for DICOM handler functionality
"""
import pytest
import os
import sys
import tempfile
from unittest.mock import Mock, patch, mock_open
import pydicom
from pydicom.dataset import Dataset
from pydicom.uid import generate_uid
import numpy as np
from src.handlers.dicom_handlers import (
    generate_random_dicom_handler,
    send_dicom_to_server_handler,
    send_random_dicom_series_handler
)


def test_generate_random_dicom_ct():
    """
    Test generating a random DICOM file with CT modality
    """
    # Generate a random DICOM file
    dicom_file_path = generate_random_dicom_handler(modality_type="CT")

    # Verify file exists
    assert os.path.exists(dicom_file_path)
    print(f"Generated DICOM file: {dicom_file_path}")

    # Load and verify the DICOM file
    ds = pydicom.dcmread(dicom_file_path)
    assert ds.Modality == "CT"
    # Note: The handler may map PT to SecondaryCapture instead of CTImageStorage
    assert ds.PatientName is not None
    assert ds.PatientID is not None
    assert ds.StudyInstanceUID is not None
    assert ds.SeriesInstanceUID is not None
    assert ds.Rows == 256
    assert ds.Columns == 256

    # Clean up
    os.remove(dicom_file_path)
    print("DICOM file verified and cleaned up successfully")


def test_generate_random_dicom_mr():
    """
    Test generating a random DICOM file with MR modality
    """
    # Generate a random DICOM file
    dicom_file_path = generate_random_dicom_handler(modality_type="MR")

    # Verify file exists
    assert os.path.exists(dicom_file_path)
    print(f"Generated DICOM file: {dicom_file_path}")

    # Load and verify the DICOM file
    ds = pydicom.dcmread(dicom_file_path)
    assert ds.Modality == "MR"

    # Clean up
    os.remove(dicom_file_path)
    print("MR DICOM file verified and cleaned up successfully")


def test_generate_random_dicom_pt():
    """
    Test generating a random DICOM file with PT modality
    Note: Using Secondary Capture as alternative since PET Image Storage may not be available
    """
    # Generate a random DICOM file
    dicom_file_path = generate_random_dicom_handler(modality_type="PT")

    # Verify file exists
    assert os.path.exists(dicom_file_path)
    print(f"Generated DICOM file: {dicom_file_path}")

    # Load and verify the DICOM file
    ds = pydicom.dcmread(dicom_file_path)
    assert ds.Modality == "PT"
    # Using SecondaryCapture as alternative for PET since PETImageStorage is not available

    # Clean up
    os.remove(dicom_file_path)
    print("PT DICOM file verified and cleaned up successfully")


def test_generate_random_dicom_sc():
    """
    Test generating a random DICOM file with SC (Secondary Capture) modality
    """
    # Generate a random DICOM file
    dicom_file_path = generate_random_dicom_handler(modality_type="SC")

    # Verify file exists
    assert os.path.exists(dicom_file_path)
    print(f"Generated DICOM file: {dicom_file_path}")

    # Load and verify the DICOM file
    ds = pydicom.dcmread(dicom_file_path)
    assert ds.Modality == "SC"

    # Clean up
    os.remove(dicom_file_path)
    print("SC DICOM file verified and cleaned up successfully")


def test_send_dicom_to_server_with_mock():
    """
    Test sending DICOM to server using mocked association
    This test validates that the send_dicom_to_server_handler function works properly
    """
    from pynetdicom import AE
    
    # Generate a random DICOM file for testing
    dicom_file_path = generate_random_dicom_handler(modality_type="CT")
    
    # Create a mock AE to intercept calls
    with patch('src.handlers.dicom_handlers.AE') as mock_ae_class:
        # Create a mock AE instance
        mock_ae_instance = Mock()
        mock_ae_class.return_value = mock_ae_instance
        
        # Create a mock association object
        mock_assoc = Mock()
        mock_assoc.is_established = True
        
        # Create a mock status object for successful C-STORE
        mock_status = Mock()
        mock_status.Status = 0x0000  # Success status
        mock_assoc.send_c_store.return_value = mock_status
        
        mock_ae_instance.associate.return_value = mock_assoc
        
        # Test sending the DICOM file using the handler
        result = send_dicom_to_server_handler(
            dicom_file_path,
            "localhost",
            11112,
            "TEST_SERVER"
        )

        # Verify the result
        assert result is True
        mock_ae_instance.associate.assert_called_once_with("localhost", 11112, ae_title="TEST_SERVER")
        mock_assoc.send_c_store.assert_called_once()
        mock_assoc.release.assert_called_once()

        print("DICOM send to server mocked test completed successfully")

    # Clean up
    os.remove(dicom_file_path)


def test_send_dicom_to_server_connection_failure():
    """
    Test sending DICOM to server when connection fails
    """
    # Generate a random DICOM file for testing
    dicom_file_path = generate_random_dicom_handler(modality_type="CT")

    # Mock the AE to simulate connection failure
    with patch('src.handlers.dicom_handlers.AE') as mock_ae_class:
        # Create a mock AE instance
        mock_ae_instance = Mock()
        mock_ae_class.return_value = mock_ae_instance
        
        # Create a mock association object with failed connection
        mock_assoc = Mock()
        mock_assoc.is_established = False
        mock_ae_instance.associate.return_value = mock_assoc

        # Test sending the DICOM file
        result = send_dicom_to_server_handler(
            dicom_file_path,
            "localhost",
            11112,
            "TEST_SERVER"
        )

        # Verify the result
        assert result is False
        mock_ae_instance.associate.assert_called_once_with("localhost", 11112, ae_title="TEST_SERVER")

        print("DICOM send to server connection failure test completed successfully")

    # Clean up
    os.remove(dicom_file_path)


def test_send_random_dicom_series():
    """
    Test sending multiple random DICOM files as a series
    """
    # Mock the send_dicom_to_server_handler to avoid actual network calls
    with patch('src.handlers.dicom_handlers.send_dicom_to_server_handler', return_value=True) as mock_send:
        # Test sending 3 random DICOM files
        success_count = send_random_dicom_series_handler(
            num_files=3,
            server_address="localhost",
            server_port=11112,
            server_ae_title="TEST_SERVER",
            modality_type="CT"
        )

        # Verify the results
        assert success_count == 3
        assert mock_send.call_count == 3
        print(f"Successfully sent {success_count}/3 files in series")


def test_send_random_dicom_series_partial_failure():
    """
    Test sending multiple random DICOM files with some failures
    """
    # Mock the send_dicom_to_server_handler to simulate partial failures
    # First call succeeds, second fails, third succeeds
    send_results = [True, False, True]
    def mock_send_side_effect(*args, **kwargs):
        return send_results.pop(0)

    with patch('src.handlers.dicom_handlers.send_dicom_to_server_handler', side_effect=mock_send_side_effect):
        # Test sending 3 random DICOM files
        success_count = send_random_dicom_series_handler(
            num_files=3,
            server_address="localhost",
            server_port=11112,
            server_ae_title="TEST_SERVER",
            modality_type="CT"
        )

        # Verify the results
        assert success_count == 2  # 2 succeeded, 1 failed
        print(f"Successfully sent {success_count}/3 files in series with partial failures")


def test_generate_random_dicom_patient_data():
    """
    Test that generated DICOM files have proper patient data
    """
    # Generate a random DICOM file
    dicom_file_path = generate_random_dicom_handler(modality_type="CT")

    # Load and verify patient data
    ds = pydicom.dcmread(dicom_file_path)

    assert ds.PatientName is not None
    assert ds.PatientID is not None
    assert ds.PatientBirthDate is not None
    assert ds.PatientSex in ["M", "F", "O"]

    # Verify the date format (YYYYMMDD)
    assert len(ds.PatientBirthDate) == 8
    year = int(ds.PatientBirthDate[:4])
    month = int(ds.PatientBirthDate[4:6])
    day = int(ds.PatientBirthDate[6:8])
    assert 1900 <= year <= 2025
    assert 1 <= month <= 12
    assert 1 <= day <= 31

    print("Patient data in generated DICOM is valid")

    # Clean up
    os.remove(dicom_file_path)


def test_generate_random_dicom_study_data():
    """
    Test that generated DICOM files have proper study data
    """
    # Generate a random DICOM file
    dicom_file_path = generate_random_dicom_handler(modality_type="CT")

    # Load and verify study data
    ds = pydicom.dcmread(dicom_file_path)

    assert ds.StudyDate is not None
    assert ds.StudyTime is not None
    assert ds.StudyInstanceUID is not None
    assert ds.StudyID is not None
    assert ds.AccessionNumber is not None

    print("Study data in generated DICOM is valid")

    # Clean up
    os.remove(dicom_file_path)


def test_generate_random_dicom_series_data():
    """
    Test that generated DICOM files have proper series data
    """
    # Generate a random DICOM file
    dicom_file_path = generate_random_dicom_handler(modality_type="CT")

    # Load and verify series data
    ds = pydicom.dcmread(dicom_file_path)

    assert ds.SeriesInstanceUID is not None
    assert ds.SeriesNumber is not None
    assert ds.Modality is not None
    assert ds.InstanceNumber is not None

    print("Series data in generated DICOM is valid")

    # Clean up
    os.remove(dicom_file_path)


def test_send_dicom_to_pacs_server():
    """
    Test sending a DICOM file to a PACS server at localhost:1112 with MYSTORE AET
    This test simulates the real-world use case of sending files to a PACS using user's configuration
    """
    # Generate a random DICOM file
    dicom_file_path = generate_random_dicom_handler(modality_type="CT")

    # Mock the AE to test with user's configuration
    with patch('src.handlers.dicom_handlers.AE') as mock_ae_class:
        # Create a mock AE instance
        mock_ae_instance = Mock()
        mock_ae_class.return_value = mock_ae_instance
        
        # Create a mock association object
        mock_assoc = Mock()
        mock_assoc.is_established = True

        # Create a mock status object for successful C-STORE
        mock_status = Mock()
        mock_status.Status = 0x0000  # Success status (0x0000 = Success)
        mock_assoc.send_c_store.return_value = mock_status

        mock_ae_instance.associate.return_value = mock_assoc

        # Test sending the DICOM file to the PACS server with user's configuration
        result = send_dicom_to_server_handler(
            dicom_file_path,
            'localhost',
            1112,  # User's port configuration
            'MYSTORE'  # User's AET configuration
        )

        # Verify the result
        assert result is True
        # Verify that the association was called with correct parameters
        mock_ae_instance.associate.assert_called_once_with('localhost', 1112, ae_title='MYSTORE')
        # Verify that C-STORE was called once
        mock_assoc.send_c_store.assert_called_once()
        # Verify that the association was released
        mock_assoc.release.assert_called_once()

        print("Mocked PACS send test completed successfully with user's configuration")

    # Clean up
    os.remove(dicom_file_path)


if __name__ == "__main__":
    print("Testing DICOM handler functionality")
    print("="*60)

    test_generate_random_dicom_ct()
    print()

    test_generate_random_dicom_mr()
    print()

    test_generate_random_dicom_pt()
    print()

    test_generate_random_dicom_sc()
    print()

    test_send_dicom_to_server_with_mock()
    print()

    test_send_dicom_to_server_connection_failure()
    print()

    test_send_random_dicom_series()
    print()

    test_send_random_dicom_series_partial_failure()
    print()

    test_generate_random_dicom_patient_data()
    print()

    test_generate_random_dicom_study_data()
    print()

    test_generate_random_dicom_series_data()
    print()

    test_send_dicom_to_pacs_server()
    print()

    print("All DICOM handler tests completed successfully!")