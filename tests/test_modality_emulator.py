"""
Tests for Modality Emulator
"""
import pytest
from unittest.mock import Mock, patch
from src.modality_emulator import ModalityEmulator
from pynetdicom.sop_class import ModalityWorklistInformationFind


class TestModalityEmulator:
    """Tests for the ModalityEmulator class"""

    def test_initialization(self):
        """Test basic initialization of ModalityEmulator"""
        emulator = ModalityEmulator()
        assert emulator.ae_title == "DVTK_MW_SCU"
        assert emulator.port == 11112
        assert emulator.ae is not None

    def test_custom_initialization(self):
        """Test initialization with custom parameters"""
        emulator = ModalityEmulator(ae_title="TEST_MODALITY", port=12345)
        assert emulator.ae_title == "TEST_MODALITY"
        assert emulator.port == 12345

    @patch('src.modality_emulator.AE')
    def test_connect_to_ris_success(self, mock_ae_class):
        """Test successful connection to RIS"""
        # Create a mock AE instance
        mock_ae_instance = Mock()
        mock_ae_class.return_value = mock_ae_instance

        # Mock association object
        mock_assoc = Mock()
        mock_assoc.is_established = True

        # Create a mock status object with the Status attribute
        mock_status = Mock()
        mock_status.Status = 0x0000  # Success status

        # Mock the responses for C-FIND
        mock_responses = [(mock_status, None)]  # Success status, no identifier
        mock_assoc.send_c_find.return_value = mock_responses
        mock_ae_instance.associate.return_value = mock_assoc

        emulator = ModalityEmulator()
        result = emulator.connect_to_ris('127.0.0.1', 11114, 'RIS')

        assert mock_ae_instance.associate.called
        assert mock_assoc.send_c_find.called
        assert mock_assoc.release.called
        assert result == []  # Empty list because identifier was None
        # The save_worklist_to_file method would also be called, but it's harder to mock

    @patch('src.modality_emulator.AE')
    def test_connect_to_ris_failure(self, mock_ae_class):
        """Test failed connection to RIS"""
        # Create a mock AE instance
        mock_ae_instance = Mock()
        mock_ae_class.return_value = mock_ae_instance

        # Mock association object with failed connection
        mock_assoc = Mock()
        mock_assoc.is_established = False
        mock_ae_instance.associate.return_value = mock_assoc

        emulator = ModalityEmulator()
        result = emulator.connect_to_ris('127.0.0.1', 11114, 'RIS')

        assert not mock_assoc.send_c_find.called  # Should not call C-FIND if not connected
        assert result == []  # Should return empty list
        # The save_worklist_to_file method would also be called for failed connections

    @patch('src.modality_emulator.AE')
    def test_connect_to_pacs_success(self, mock_ae_class):
        """Test successful connection to PACS"""
        # Create a mock AE instance
        mock_ae_instance = Mock()
        mock_ae_class.return_value = mock_ae_instance

        # Mock association object
        mock_assoc = Mock()
        mock_assoc.is_established = True
        mock_ae_instance.associate.return_value = mock_assoc

        emulator = ModalityEmulator()
        result = emulator.connect_to_pacs('127.0.0.1', 11116, 'PACS')

        assert mock_ae_instance.associate.called
        assert mock_assoc.release.called
        assert result is True

    @patch('src.modality_emulator.AE')
    def test_connect_to_pacs_failure(self, mock_ae_class):
        """Test failed connection to PACS"""
        # Create a mock AE instance
        mock_ae_instance = Mock()
        mock_ae_class.return_value = mock_ae_instance

        # Mock association object with failed connection
        mock_assoc = Mock()
        mock_assoc.is_established = False
        mock_ae_instance.associate.return_value = mock_assoc

        emulator = ModalityEmulator()
        result = emulator.connect_to_pacs('127.0.0.1', 11116, 'PACS')

        assert not mock_assoc.send_c_store.called  # Should not attempt C-STORE if not connected
        assert result is False


def test_main_function():
    """Test the main function"""
    from src.modality_emulator import main
    # Just ensure the main function runs without error
    main()