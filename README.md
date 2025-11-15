# Modality Emulator

A Python-based open source modality emulator designed to communicate with DVTK RIS Emulator and PACS systems, focusing on MWL (Modality Worklist) with C-FIND and PACS with C-STORE operations.

## Overview

This project implements a modality emulator that simulates medical imaging devices (such as CT, MR, US, etc.) in a DICOM network. It provides communication capabilities with RIS (Radiology Information System) and PACS (Picture Archiving and Communication System) using standard DICOM protocols.

## Features

- **MWL (Modality Worklist) Support**: Implementation of C-FIND operations to retrieve worklist entries from RIS systems
- **PACS Communication**: Implementation of C-STORE operations for sending images to PACS systems
- **DVTK RIS Emulator Integration**: Compatible with DVTK RIS Emulator for testing and development
- **DICOM Standard Compliance**: Adheres to DICOM networking and communication standards
- **Configurable Settings**: Easy configuration for different network environments and systems

## Architecture

The modality emulator supports:
- C-FIND operations for worklist queries to MWL
- C-STORE operations for image storage to PACS
- Network communication following DICOM protocols

## Installation

1. Clone the repository:
```bash
git clone https://github.com/hendrapaiton/Modality-Emulator.git
cd Modality-Emulator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure the system with your DICOM network settings

## Usage

1. Configure the DICOM settings in the configuration file
2. Run the modality emulator:
```bash
python -m src.modality_emulator
```

## Testing

The project includes comprehensive tests using pytest:

1. Install test dependencies:
```bash
pip install -r requirements.txt
```

2. Run the tests:
```bash
pytest
```

3. Run tests with coverage:
```bash
pytest --cov=src tests/
```

## Configuration

The system can be configured with:
- AE Title for the modality
- IP address and port for the modality
- RIS/PACS destination settings
- Supported SOP classes
- Network timeouts and retry settings

## DICOM Conformance

This implementation follows DICOM Standard Part 4 (Service Class Specifications) for:
- Modality Worklist Service (MWL)
- Storage Service Class (C-STORE)

## Contributing

We welcome contributions to the project! Please see our contributing guidelines for more information.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Based on DICOM standard for medical imaging communication
- Compatible with DVTK RIS Emulator for testing purposes
- Inspired by medical imaging workflow requirements

---

*This project is maintained by the open source community and is intended for educational and development purposes in medical imaging systems.*