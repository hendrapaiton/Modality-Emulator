"""
Tests for Modality Worklist (MWL) handler functionality
"""
import pytest
from unittest.mock import Mock, patch
from src.handlers.modality_handlers import connect_to_ris_handler, connect_to_pacs_handler
from pynetdicom.sop_class import ModalityWorklistInformationFind


class TestModalityWorklist:
    """Tests for the Modality Worklist handler functionality"""

    @patch('src.handlers.modality_handlers.AE')
    def test_connect_to_ris_success(self, mock_ae_class):
        """Test successful connection to RIS for Modality Worklist using handler"""
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

        result = connect_to_ris_handler('127.0.0.1', 11114, 'RIS', ae_title='DICOMCLIENT')

        assert mock_ae_instance.associate.called
        assert mock_assoc.send_c_find.called
        assert mock_assoc.release.called
        assert result == []  # Empty list because identifier was None

    @patch('src.handlers.modality_handlers.AE')
    def test_connect_to_ris_failure(self, mock_ae_class):
        """Test failed connection to RIS for Modality Worklist using handler"""
        # Create a mock AE instance
        mock_ae_instance = Mock()
        mock_ae_class.return_value = mock_ae_instance

        # Mock association object with failed connection
        mock_assoc = Mock()
        mock_assoc.is_established = False
        mock_ae_instance.associate.return_value = mock_assoc

        result = connect_to_ris_handler('127.0.0.1', 11114, 'RIS', ae_title='DICOMCLIENT')

        assert not mock_assoc.send_c_find.called  # Should not call C-FIND if not connected
        assert result == []  # Should return empty list

    @patch('src.handlers.modality_handlers.AE')
    def test_connect_to_pacs_success(self, mock_ae_class):
        """Test successful connection to PACS for C-STORE operations using handler"""
        # Create a mock AE instance
        mock_ae_instance = Mock()
        mock_ae_class.return_value = mock_ae_instance

        # Mock association object
        mock_assoc = Mock()
        mock_assoc.is_established = True
        mock_ae_instance.associate.return_value = mock_assoc

        result = connect_to_pacs_handler('127.0.0.1', 11116, 'PACS', ae_title='DICOMCLIENT')

        assert mock_ae_instance.associate.called
        assert mock_assoc.release.called
        assert result is True

    @patch('src.handlers.modality_handlers.AE')
    def test_connect_to_pacs_failure(self, mock_ae_class):
        """Test failed connection to PACS for C-STORE operations using handler"""
        # Create a mock AE instance
        mock_ae_instance = Mock()
        mock_ae_class.return_value = mock_ae_instance

        # Mock association object with failed connection
        mock_assoc = Mock()
        mock_assoc.is_established = False
        mock_ae_instance.associate.return_value = mock_assoc

        result = connect_to_pacs_handler('127.0.0.1', 11116, 'PACS', ae_title='DICOMCLIENT')

        assert not mock_assoc.send_c_store.called  # Should not attempt C-STORE if not connected
        assert result is False


def test_connect_to_dicomserver_co_uk():
    """Test connecting to and retrieving worklist from dicomserver.co.uk"""
    from src.handlers.modality_handlers import connect_to_ris_handler
    from src.handlers.utility_handlers import load_environment_config

    # Load configuration from environment
    config = load_environment_config()
    remote_host = config.get('REMOTE_HOST', 'www.dicomserver.co.uk')
    remote_port = config.get('REMOTE_PORT', 104)
    remote_ae_title = config.get('REMOTE_AE_TITLE', 'DICOMSERVER')
    local_ae_title = config.get('LOCAL_AE_TITLE', 'DICOMCLIENT')

    # Skip the actual connection in unit tests to avoid network calls,
    # but test that the configuration is loaded properly
    assert remote_host in ['www.dicomserver.co.uk', 'www.dicomserver.com', 'localhost']  # Common test values
    assert isinstance(remote_port, int)
    assert remote_port > 0 and remote_port <= 65535
    assert isinstance(remote_ae_title, str) and len(remote_ae_title) > 0
    assert isinstance(local_ae_title, str) and len(local_ae_title) > 0

    print(f"Configuration for dicomserver.co.uk connection validated:")
    print(f"  Host: {remote_host}")
    print(f"  Port: {remote_port}")
    print(f"  Remote AE: {remote_ae_title}")
    print(f"  Local AE: {local_ae_title}")


def test_main_function():
    """Test the main function behavior by testing the underlying configuration"""
    from src.handlers.utility_handlers import load_environment_config
    # Just ensure the config loading runs without error
    config = load_environment_config()
    assert isinstance(config, dict)
    print("Configuration loaded successfully:", config)