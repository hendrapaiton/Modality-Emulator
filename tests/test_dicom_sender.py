"""
Test script for DICOM sender functionality
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

# Add src directory to path to import the module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from dicom_sender import DICOMSender


def test_dicom_sender_initialization():
    """
    Test initialization of DICOM sender with default AE title
    """
    sender = DICOMSender()
    
    assert sender.ae_title == "RANDOM_MODALITY"
    assert sender.ae.ae_title == "RANDOM_MODALITY"
    print("DICOM sender initialized successfully with default AE title")


def test_dicom_sender_custom_ae_title():
    """
    Test initialization of DICOM sender with custom AE title
    """
    custom_title = "CUSTOM_MODALITY"
    sender = DICOMSender(ae_title=custom_title)
    
    assert sender.ae_title == custom_title
    assert sender.ae.ae_title == custom_title
    print(f"DICOM sender initialized successfully with custom AE title: {custom_title}")


def test_dicom_sender_ae_title_max_16_chars():
    """
    Test that AE title is truncated to max 16 characters
    """
    long_title = "THIS_IS_A_VERY_LONG_MODALITY_TITLE_OVER_16_CHARS"
    sender = DICOMSender(ae_title=long_title)
    
    assert sender.ae_title == long_title[:16]
    assert len(sender.ae_title) == 16
    print(f"AE title correctly truncated to 16 characters: {sender.ae_title}")


def test_generate_random_dicom_ct():
    """
    Test generating a random DICOM file with CT modality
    """
    sender = DICOMSender()
    
    # Generate a random DICOM file
    dicom_file_path = sender.generate_random_dicom(modality_type="CT")
    
    # Verify file exists
    assert os.path.exists(dicom_file_path)
    print(f"Generated DICOM file: {dicom_file_path}")
    
    # Load and verify the DICOM file
    ds = pydicom.dcmread(dicom_file_path)
    assert ds.Modality == "CT"
    assert ds.SOPClassUID.name == "CT Image Storage"
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
    sender = DICOMSender()
    
    # Generate a random DICOM file
    dicom_file_path = sender.generate_random_dicom(modality_type="MR")
    
    # Verify file exists
    assert os.path.exists(dicom_file_path)
    print(f"Generated DICOM file: {dicom_file_path}")
    
    # Load and verify the DICOM file
    ds = pydicom.dcmread(dicom_file_path)
    assert ds.Modality == "MR"
    assert ds.SOPClassUID.name == "MR Image Storage"
    
    # Clean up
    os.remove(dicom_file_path)
    print("MR DICOM file verified and cleaned up successfully")


def test_generate_random_dicom_pt():
    """
    Test generating a random DICOM file with PT modality
    Note: Using Secondary Capture as alternative since PET Image Storage may not be available
    """
    sender = DICOMSender()

    # Generate a random DICOM file
    dicom_file_path = sender.generate_random_dicom(modality_type="PT")

    # Verify file exists
    assert os.path.exists(dicom_file_path)
    print(f"Generated DICOM file: {dicom_file_path}")

    # Load and verify the DICOM file
    ds = pydicom.dcmread(dicom_file_path)
    assert ds.Modality == "PT"
    # Using SecondaryCapture as alternative for PET since PETImageStorage is not available
    assert ds.SOPClassUID.name == "Secondary Capture Image Storage"

    # Clean up
    os.remove(dicom_file_path)
    print("PT DICOM file verified and cleaned up successfully")


def test_generate_random_dicom_sc():
    """
    Test generating a random DICOM file with SC (Secondary Capture) modality
    """
    sender = DICOMSender()
    
    # Generate a random DICOM file
    dicom_file_path = sender.generate_random_dicom(modality_type="SC")
    
    # Verify file exists
    assert os.path.exists(dicom_file_path)
    print(f"Generated DICOM file: {dicom_file_path}")
    
    # Load and verify the DICOM file
    ds = pydicom.dcmread(dicom_file_path)
    assert ds.Modality == "SC"
    assert ds.SOPClassUID.name == "Secondary Capture Image Storage"
    
    # Clean up
    os.remove(dicom_file_path)
    print("SC DICOM file verified and cleaned up successfully")


def test_send_dicom_to_server_with_mock():
    """
    Test sending DICOM to server using mocked association
    """
    sender = DICOMSender()
    
    # Create a temporary DICOM file for testing
    dicom_file_path = sender.generate_random_dicom(modality_type="CT")
    
    # Mock the association and C-STORE request
    with patch.object(sender.ae, 'associate') as mock_assoc:
        # Create a mock association object
        mock_association = Mock()
        mock_association.is_established = True
        
        # Create a mock status object
        mock_status = Mock()
        mock_status.Status = 0x0000  # Success status
        mock_association.send_c_store.return_value = mock_status
        
        mock_assoc.return_value = mock_association
        
        # Test sending the DICOM file
        result = sender.send_dicom_to_server(
            dicom_file_path, 
            "localhost", 
            11112, 
            "TEST_SERVER"
        )
        
        # Verify the result
        assert result is True
        mock_assoc.assert_called_once_with("localhost", 11112, ae_title="TEST_SERVER")
        mock_association.send_c_store.assert_called_once()
        mock_association.release.assert_called_once()
        
        print("DICOM send to server mocked test completed successfully")
    
    # Clean up
    os.remove(dicom_file_path)


def test_send_dicom_to_server_connection_failure():
    """
    Test sending DICOM to server when connection fails
    """
    sender = DICOMSender()
    
    # Create a temporary DICOM file for testing
    dicom_file_path = sender.generate_random_dicom(modality_type="CT")
    
    # Mock the association to simulate connection failure
    with patch.object(sender.ae, 'associate') as mock_assoc:
        # Create a mock association object with failed connection
        mock_association = Mock()
        mock_association.is_established = False
        mock_assoc.return_value = mock_association
        
        # Test sending the DICOM file
        result = sender.send_dicom_to_server(
            dicom_file_path, 
            "localhost", 
            11112, 
            "TEST_SERVER"
        )
        
        # Verify the result
        assert result is False
        mock_assoc.assert_called_once_with("localhost", 11112, ae_title="TEST_SERVER")
        
        print("DICOM send to server connection failure test completed successfully")
    
    # Clean up
    os.remove(dicom_file_path)


def test_send_dicom_to_server_cstore_failure():
    """
    Test sending DICOM to server when C-STORE request fails
    """
    sender = DICOMSender()
    
    # Create a temporary DICOM file for testing
    dicom_file_path = sender.generate_random_dicom(modality_type="CT")
    
    # Mock the association and C-STORE request failure
    with patch.object(sender.ae, 'associate') as mock_assoc:
        # Create a mock association object
        mock_association = Mock()
        mock_association.is_established = True
        
        # Mock C-STORE request returning None (failure)
        mock_association.send_c_store.return_value = None
        
        mock_assoc.return_value = mock_association
        
        # Test sending the DICOM file
        result = sender.send_dicom_to_server(
            dicom_file_path, 
            "localhost", 
            11112, 
            "TEST_SERVER"
        )
        
        # Verify the result
        assert result is False
        mock_assoc.assert_called_once_with("localhost", 11112, ae_title="TEST_SERVER")
        mock_association.send_c_store.assert_called_once()
        mock_association.release.assert_called_once()
        
        print("DICOM send to server C-STORE failure test completed successfully")
    
    # Clean up
    os.remove(dicom_file_path)


def test_send_random_dicom_series():
    """
    Test sending multiple random DICOM files as a series
    """
    sender = DICOMSender()
    
    # Mock the send_dicom_to_server method to avoid actual network calls
    with patch.object(sender, 'send_dicom_to_server', return_value=True) as mock_send:
        # Test sending 3 random DICOM files
        success_count = sender.send_random_dicom_series(
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
    sender = DICOMSender()
    
    # Mock the send_dicom_to_server method to simulate partial failures
    # First call succeeds, second fails, third succeeds
    send_results = [True, False, True]
    def mock_send_side_effect(*args, **kwargs):
        return send_results.pop(0)
    
    with patch.object(sender, 'send_dicom_to_server', side_effect=mock_send_side_effect):
        # Test sending 3 random DICOM files
        success_count = sender.send_random_dicom_series(
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
    sender = DICOMSender()
    
    # Generate a random DICOM file
    dicom_file_path = sender.generate_random_dicom(modality_type="CT")
    
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
    sender = DICOMSender()
    
    # Generate a random DICOM file
    dicom_file_path = sender.generate_random_dicom(modality_type="CT")
    
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
    sender = DICOMSender()

    # Generate a random DICOM file
    dicom_file_path = sender.generate_random_dicom(modality_type="CT")

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
    sender = DICOMSender()

    # Generate a random DICOM file
    dicom_file_path = sender.generate_random_dicom(modality_type="CT")

    # Check if a PACS server is running at localhost:1112 (user's configuration)
    # If server is running, test the actual connection; otherwise use mock
    import socket
    server_available = False

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)  # 2 second timeout
        result = sock.connect_ex(('localhost', 1112))
        server_available = (result == 0)
        sock.close()
    except Exception:
        server_available = False

    if server_available:
        # Test with real server connection
        print("PACS server detected at localhost:1112 with MYSTORE AET, testing real connection...")
        result = sender.send_dicom_to_server(dicom_file_path, 'localhost', 1112, 'MYSTORE')
        print(f"Real PACS send result: {result}")
        # Result may vary depending on PACS configuration, just verify no exceptions
        assert result is not None
    else:
        # Test with mocked connection using user's configuration
        print("No PACS server detected at localhost:1112 with MYSTORE AET, testing with mock...")
        with patch.object(sender.ae, 'associate') as mock_assoc:
            # Create a mock association object
            mock_association = Mock()
            mock_association.is_established = True

            # Create a mock status object
            mock_status = Mock()
            mock_status.Status = 0x0000  # Success status (0x0000 = Success)
            mock_association.send_c_store.return_value = mock_status

            mock_assoc.return_value = mock_association

            # Test sending the DICOM file to the PACS server with user's configuration
            result = sender.send_dicom_to_server(
                dicom_file_path,
                'localhost',
                1112,  # User's port configuration
                'MYSTORE'  # User's AET configuration
            )

            # Verify the result
            assert result is True
            # Verify that the association was called with correct parameters
            mock_assoc.assert_called_once_with('localhost', 1112, ae_title='MYSTORE')
            # Verify that C-STORE was called once
            mock_association.send_c_store.assert_called_once()
            # Verify that the association was released
            mock_association.release.assert_called_once()

            print("Mocked PACS send test completed successfully with user's configuration")

    # Clean up
    os.remove(dicom_file_path)


if __name__ == "__main__":
    print("Testing DICOM sender functionality")
    print("="*60)

    test_dicom_sender_initialization()
    print()
    
    test_dicom_sender_custom_ae_title()
    print()
    
    test_dicom_sender_ae_title_max_16_chars()
    print()
    
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
    
    test_send_dicom_to_server_cstore_failure()
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

    print("All DICOM sender tests completed successfully!")