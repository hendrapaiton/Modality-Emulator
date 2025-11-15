"""
DICOM StoreCP Client - Sends random DICOM files to your storescp server

This script generates random DICOM files and sends them to your storescp server:
storescp -v -aet MYSTORE -od C:\\dicom_store 11112
"""
import logging
import os
import random
import datetime
import tempfile
import numpy as np


def create_random_dicom(modality="CT"):
    """
    Create a random DICOM file with basic image data

    :param modality: Modality type (CT, MR, PT, etc.)
    :return: Path to the generated DICOM file
    """
    # Import pydicom and pynetdicom inside the function to avoid import errors
    import pydicom
    from pydicom.dataset import Dataset, FileDataset
    from pydicom.uid import generate_uid, ImplicitVRLittleEndian
    from pydicom import dcmwrite
    from pynetdicom.sop_class import CTImageStorage, MRImageStorage, PositronEmissionTomographyImageStorage, SecondaryCaptureImageStorage

    # Create a temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".dcm")
    temp_file.close()
    file_path = temp_file.name

    # Create file meta information
    file_meta = Dataset()
    if modality == "CT":
        file_meta.MediaStorageSOPClassUID = CTImageStorage
    elif modality == "MR":
        file_meta.MediaStorageSOPClassUID = MRImageStorage
    elif modality == "PT":
        file_meta.MediaStorageSOPClassUID = PositronEmissionTomographyImageStorage
    else:
        file_meta.MediaStorageSOPClassUID = SecondaryCaptureImageStorage

    file_meta.MediaStorageSOPInstanceUID = generate_uid()
    file_meta.ImplementationClassUID = generate_uid()
    file_meta.TransferSyntaxUID = ImplicitVRLittleEndian

    # Create the main dataset
    ds = FileDataset(file_path, {}, file_meta=file_meta, preamble=b"\0" * 128)

    # Set up the dataset using common DICOM tags
    ds.SOPClassUID = file_meta.MediaStorageSOPClassUID
    ds.SOPInstanceUID = file_meta.MediaStorageSOPInstanceUID

    # Patient information
    ds.PatientName = f"RANDOM^{random.choice(['SMITH', 'JOHNSON', 'WILLIAMS', 'BROWN', 'JONES', 'GARCIA', 'MILLER', 'DAVIS', 'RODRIGUEZ', 'MARTINEZ'])}"
    ds.PatientID = f"PID{random.randint(100000, 999999)}"
    ds.PatientBirthDate = f"{random.randint(1940, 2000):04d}{random.randint(1, 12):02d}{random.randint(1, 28):02d}"
    ds.PatientSex = random.choice(["M", "F", "O"])

    # Study information
    ds.StudyDate = datetime.date.today().strftime("%Y%m%d")
    ds.StudyTime = datetime.datetime.now().strftime("%H%M%S.%f")[:10]  # HHMMSS.FFFFFF
    ds.StudyInstanceUID = generate_uid()
    ds.StudyID = f"STUDY{random.randint(10000, 99999)}"
    ds.AccessionNumber = f"ACC{random.randint(1000000, 9999999)}"

    # Series information
    ds.SeriesInstanceUID = generate_uid()
    ds.SeriesNumber = random.randint(1, 999)
    ds.Modality = modality

    # Image information
    ds.InstanceNumber = random.randint(1, 9999)

    # Frame of reference
    ds.FrameOfReferenceUID = generate_uid()
    ds.PositionReferenceIndicator = "REF"

    # Image pixel data information
    rows, cols = random.choice([64, 128, 256, 512]), random.choice([64, 128, 256, 512])
    ds.Rows = rows
    ds.Columns = cols
    ds.BitsAllocated = 16
    ds.BitsStored = 16
    ds.HighBit = 15
    ds.PixelRepresentation = 1  # Signed
    ds.SamplesPerPixel = 1
    ds.PhotometricInterpretation = "MONOCHROME2"

    # Pixel spacing (optional but common)
    ds.PixelSpacing = [0.5 + random.random(), 0.5 + random.random()]

    # Create random image pixel data
    # Generate a more realistic test pattern
    pixel_data = np.zeros((rows, cols), dtype=np.int16)

    # Add various patterns to make it look more realistic
    for i in range(rows):
        for j in range(cols):
            # Base pixel value
            base_value = random.randint(-1000, 2000)

            # Add gradient patterns
            grad_x = int((j / cols) * 500)
            grad_y = int((i / rows) * 500)

            # Add circular pattern
            center_x, center_y = rows // 2, cols // 2
            distance = ((i - center_x) ** 2 + (j - center_y) ** 2) ** 0.5
            if distance < min(rows, cols) // 4:
                circle_value = 800
            else:
                circle_value = 0

            # Add some structured noise
            structured_noise = random.randint(-100, 100)

            # Combine all effects
            pixel_data[i, j] = base_value + grad_x + grad_y + circle_value + structured_noise

    ds.PixelData = pixel_data.tobytes()

    # Equipment information
    ds.Manufacturer = random.choice(["SIEMENS", "GE MEDICAL SYSTEMS", "PHILIPS", "TOSHIBA", "CANON", "HITACHI"])
    ds.ManufacturerModelName = f"{ds.Manufacturer} MODEL-{random.randint(100, 999)}"
    ds.DeviceSerialNumber = f"SER{random.randint(10000, 99999)}"
    ds.SoftwareVersions = f"SW{random.randint(100, 999)}.{random.randint(0, 99)}"

    # Set transfer syntax
    ds.is_little_endian = True
    ds.is_implicit_VR = True

    # Write the DICOM file
    dcmwrite(file_path, ds, write_like_original=False)

    print(f"Created DICOM file: {file_path} with modality {modality}")
    return file_path


def send_to_storescp(dicom_file_path, server_address="localhost", server_port=11112, server_ae_title="MYSTORE"):
    """
    Send a DICOM file to the storescp server

    :param dicom_file_path: Path to the DICOM file to send
    :param server_address: Server address (default: localhost)
    :param server_port: Server port (default: 11112)
    :param server_ae_title: Server AE title (default: MYSTORE)
    :return: True if successful, False otherwise
    """
    try:
        import pydicom
        from pynetdicom import AE
        from pynetdicom.sop_class import CTImageStorage, MRImageStorage, PositronEmissionTomographyImageStorage, SecondaryCaptureImageStorage

        # Load the DICOM file
        ds = pydicom.dcmread(dicom_file_path)

        # Determine the appropriate SOP class
        modality = ds.Modality if hasattr(ds, 'Modality') else 'CT'
        if modality == 'CT':
            sop_class = CTImageStorage
        elif modality == 'MR':
            sop_class = MRImageStorage
        elif modality == 'PT':
            sop_class = PositronEmissionTomographyImageStorage
        else:
            sop_class = SecondaryCaptureImageStorage

        # Create an Application Entity
        ae = AE(ae_title="RANDOM_MODALITY")

        # Add requested presentation contexts
        ae.add_requested_context(sop_class)

        # Associate with the peer AE
        assoc = ae.associate(server_address, server_port, ae_title=server_ae_title)

        if assoc.is_established:
            print(f"Connected to {server_address}:{server_port} ({server_ae_title})")

            # Send the C-STORE request
            responses = assoc.send_c_store(ds)

            # Check the response status
            status = responses.Status if hasattr(responses, 'Status') else responses
            if status == 0x0000:
                print(f"Successfully sent {dicom_file_path} to server")
                assoc.release()
                return True
            else:
                print(f"C-STORE failed with status: 0x{status:04X}")
                assoc.release()
                return False
        else:
            print(f"Failed to associate with {server_address}:{server_port}")
            return False

    except ImportError as e:
        print(f"Required library not found: {e}")
        print("Please install required libraries: pip install pydicom pynetdicom")
        return False
    except Exception as e:
        print(f"Error sending DICOM file: {e}")
        return False


def main():
    """
    Main function to generate and send random DICOM files to storescp
    """
    print("DICOM StoreCP Client")
    print("Sending random DICOM files to your storescp server...")
    print("Server configuration: storescp -v -aet MYSTORE -od C:\\dicom_store 11112")
    print()

    # Configuration for your server
    SERVER_ADDRESS = "localhost"
    SERVER_PORT = 11112
    SERVER_AE_TITLE = "MYSTORE"

    # Generate and send multiple random DICOM files
    num_files = 10
    modalities = ["CT", "MR", "PT", "SC"]

    success_count = 0

    for i in range(num_files):
        # Choose a random modality
        modality = random.choice(modalities)

        print(f"\n--- Generating and sending file {i+1}/{num_files} ---")
        print(f"Modality: {modality}")

        try:
            # Create a random DICOM file
            dicom_file = create_random_dicom(modality)

            # Send it to the storescp server
            if send_to_storescp(dicom_file, SERVER_ADDRESS, SERVER_PORT, SERVER_AE_TITLE):
                success_count += 1
                print(f"[SUCCESS] Successfully sent file {i+1}")
            else:
                print(f"[FAILED] Failed to send file {i+1}")

            # Clean up the temporary file
            if os.path.exists(dicom_file):
                os.remove(dicom_file)
                print(f"Cleaned up temporary file: {dicom_file}")

        except Exception as e:
            print(f"[ERROR] Error processing file {i+1}: {e}")

    print(f"\n--- Summary ---")
    print(f"Successfully sent: {success_count}/{num_files} files")
    print(f"Failed: {num_files - success_count}/{num_files} files")

    if success_count > 0:
        print("\nYour DICOM files have been sent to the storescp server!")
        print(f"The files should now be stored in C:\\dicom_store as specified in your storescp command.")
    else:
        print("\nNo files were successfully sent. Please check your storescp server configuration.")


if __name__ == "__main__":
    main()