# Written by Dragon Enjoyer
# Goal of this program is to access SD Card and split JPEG and RAW files into their own folders one at a time

import os
import platform
import shutil
import logging
from time import sleep
from tqdm import tqdm

revision = "1.2.0"  # <-- Update me every time a change is made


SD_FOLDER_NAME = "DCIM"
FOLDER_SAVE_LOCATION = "/Desktop/"


def validate_input(userinput, available_folders, type):
    if type == "exit":
        while True:
            try:
                if userinput == "Y" or userinput == "N":
                    break
                else:
                    print("Invalid input.")
                    userinput = input("Exit?: Y/N")
            except:
                print("Invalid input.")

    elif type == "filename":
        while True:
            try:
                if userinput in available_folders:
                    return userinput
                    break
                else:
                    print("No folders match that name")
                    userinput = input("Enter name of fuji f2older to transfer files from: ")
                    userinput = userinput.upper()
            except:
                print("No folders match that name")
                userinput = input("Enter name of fuji f1older to transfer files from: ")
                userinput = userinput.upper()


def transfer_jpeg(jpeg_total_size, jpeg_file_size, SD_PATH, JPEG_FOLDER_PATH, selected_jpeg):
    with tqdm(desc="JPG Transfer Progress", total=jpeg_total_size, initial=0, unit="B", unit_divisor=1024, leave=True,
              unit_scale=True) as jpg_progress:
        for i, file_name in enumerate(selected_jpeg):
            shutil.copy(os.path.join(SD_PATH, file_name), JPEG_FOLDER_PATH)
            jpg_progress.update(jpeg_file_size)


def transfer_raw(raw_total_size, raw_file_size, SD_PATH, RAW_FOLDER_PATH, selected_raw):
    with tqdm(desc="RAW Transfer Progress", total=raw_total_size, initial=0, unit="B", unit_divisor=1024, leave=True,
              unit_scale=True) as raw_progress:
        for i, file_name in enumerate(selected_raw):
            shutil.copy(os.path.join(SD_PATH, file_name), RAW_FOLDER_PATH)
            raw_progress.update(raw_file_size)


def get_file_extension(file):
    extension = os.path.splitext(file)
    return extension[1]


def run_macos():
    USER_PATH = os.path.expanduser('~')
    jpeg_folder_name = input("Enter Folder name for JPEG's: ")
    raw_folder_name = input("Enter Folder name for RAW's: ")

    JPEG_FOLDER_PATH = USER_PATH + FOLDER_SAVE_LOCATION + jpeg_folder_name
    RAW_FOLDER_PATH = USER_PATH + FOLDER_SAVE_LOCATION + raw_folder_name

    try:  # Check and see if the folders for LDCM and impedance board already exist, if so just keep going on
        os.mkdir(JPEG_FOLDER_PATH)  # Created the directory for the impedance board files
        os.mkdir(RAW_FOLDER_PATH)  # Create the directory for the LDCM measurements
    except OSError as error:
        logging.warning("Filepaths already exist")

    SD_NAME = input("Enter SD Card Name: ")

    run = True
    while run:
        SD_PATH = "/Volumes/" + SD_NAME + "/" + SD_FOLDER_NAME + "/"

        try:
            available_folders = os.listdir(SD_PATH)
        except OSError as error:
            logging.error("No SD Card found with name: {}".format(SD_NAME))
            break

        print("Available Folders for File Transfer: {}".format(available_folders))

        fuji_folder_name = input("Enter name of fuji folder to transfer files from: ")
        fuji_folder_name = fuji_folder_name.upper()
        fuji_folder_name = validate_input(fuji_folder_name, available_folders, "filename")

        SD_PATH = SD_PATH + fuji_folder_name

        sd_files = os.listdir(SD_PATH)

        JPEG_EXTENSION = get_file_extension(sd_files[1])  # Assumes that the files start with raw, then jpg
        RAW_EXTENSION = get_file_extension(sd_files[0])

        print("JPG Extension found: {}".format(JPEG_EXTENSION))
        print("RAW Extension found: {}\n".format(RAW_EXTENSION))

        selected_jpeg = [jpg for jpg in sd_files if jpg.endswith(JPEG_EXTENSION)]
        selected_raw = [raw for raw in sd_files if raw.endswith(RAW_EXTENSION)]

        jpeg_cnt = len(selected_jpeg)
        raw_cnt = len(selected_raw)

        print("{} JPEG Files".format(jpeg_cnt))
        print("{} RAW Files".format(raw_cnt))

        jpeg_file_size = (os.path.getsize(SD_PATH + "/" + selected_jpeg[0]))
        raw_file_size = (os.path.getsize(SD_PATH + "/" + selected_raw[0]))

        jpeg_total_size = (os.path.getsize(SD_PATH + "/" + selected_jpeg[0])) * jpeg_cnt
        raw_total_size = (os.path.getsize(SD_PATH + "/" + selected_raw[0])) * raw_cnt

        print("\nTransferring JPG Files")
        transfer_jpeg(jpeg_total_size, jpeg_file_size, SD_PATH, JPEG_FOLDER_PATH, selected_jpeg)
        print("JPEG File transfer Complete\n")
        sleep(1)

        print("\nTransferring RAW Files")
        transfer_raw(raw_total_size, raw_file_size, SD_PATH, RAW_FOLDER_PATH, selected_raw)
        print("RAW File transfer Complete\n")
        sleep(1)

        leave = input("Exit?: Y/N\n")
        leave = leave.upper()
        validate_input(leave, [], "exit")
        if leave == "Y":
            break


def run_windows():
    USER_PATH = os.path.expanduser('~')
    jpeg_folder_name = input("Enter Folder name for JPEG's: ")
    raw_folder_name = input("Enter Folder name for RAW's: ")

    JPEG_FOLDER_PATH = USER_PATH + "\\" + FOLDER_SAVE_LOCATION + "\\" + jpeg_folder_name
    RAW_FOLDER_PATH = USER_PATH + "\\" + FOLDER_SAVE_LOCATION + "\\" +  raw_folder_name

    try:  # Check and see if the folders for LDCM and impedance board already exist, if so just keep going on
        os.mkdir(JPEG_FOLDER_PATH)  # Created the directory for the impedance board files
        os.mkdir(RAW_FOLDER_PATH)  # Create the directory for the LDCM measurements
    except OSError as error:
        logging.warning("Filepaths already exist")

    SD_NAME = input("Enter SD Card Name: ")
    SD_DRIVE_NAME = input("Enter SD Card Drive Letter: ")

    run = True
    while run:
        SD_PATH = SD_DRIVE_NAME + ":" + SD_FOLDER_NAME + "\\"

        try:
            available_folders = os.listdir(SD_PATH)
        except OSError as error:
            logging.error("No SD Card found with name: {}".format(SD_NAME))
            break

        print("Available Folders for File Transfer: {}".format(available_folders))

        fuji_folder_name = input("Enter name of fuji folder to transfer files from: ")
        fuji_folder_name = fuji_folder_name.upper()
        fuji_folder_name = validate_input(fuji_folder_name, available_folders, "filename")

        SD_PATH = SD_PATH + fuji_folder_name

        sd_files = os.listdir(SD_PATH)

        JPEG_EXTENSION = get_file_extension(sd_files[0])  # Assumes that the files start with raw, then jpg
        RAW_EXTENSION = get_file_extension(sd_files[1])

        print("JPG Extension found: {}".format(JPEG_EXTENSION))
        print("RAW Extension found: {}\n".format(RAW_EXTENSION))

        selected_jpeg = [jpg for jpg in sd_files if jpg.endswith(JPEG_EXTENSION)]
        selected_raw = [raw for raw in sd_files if raw.endswith(RAW_EXTENSION)]

        jpeg_cnt = len(selected_jpeg)
        raw_cnt = len(selected_raw)

        print("{} JPEG Files".format(jpeg_cnt))
        print("{} RAW Files".format(raw_cnt))

        jpeg_file_size = (os.path.getsize(SD_PATH + "/" + selected_jpeg[0]))
        raw_file_size = (os.path.getsize(SD_PATH + "/" + selected_raw[0]))

        jpeg_total_size = (os.path.getsize(SD_PATH + "/" + selected_jpeg[0])) * jpeg_cnt
        raw_total_size = (os.path.getsize(SD_PATH + "/" + selected_raw[0])) * raw_cnt

        print("\nTransferring JPG Files")
        transfer_jpeg(jpeg_total_size, jpeg_file_size, SD_PATH, JPEG_FOLDER_PATH, selected_jpeg)
        print("JPEG File transfer Complete\n")
        sleep(1)

        print("\nTransferring RAW Files")
        transfer_raw(raw_total_size, raw_file_size, SD_PATH, RAW_FOLDER_PATH, selected_raw)
        print("RAW File transfer Complete\n")
        sleep(1)

        leave = input("Exit?: Y/N\n")
        leave = leave.upper()
        validate_input(leave, [], "exit")
        if leave == "Y":
            break


if __name__ == '__main__':
    print("Written By: Dragon Enjoyer :3")
    print("Program Version: {}\n".format(revision))

    os_type = platform.system()

    if os_type == "Darwin":
        print("Running MacOS Version\n")
        sleep(0.5)
        run_macos()
    elif os_type == "Windows":
        print("Running Windows Version\n")
        sleep(0.5)
        run_windows()

