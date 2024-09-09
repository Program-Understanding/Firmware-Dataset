from fw_downloader import download_firmware
from fw_unpacker import unpack_firmware
import argparse

def main(firmware_urls, save_path, n_samples):
    download_firmware(firmware_urls, save_path, n_samples)
    unpack_firmware(save_path)

if __name__ == '__main__':
    # Initialize the argument parser
    parser = argparse.ArgumentParser(description="Process a percentage of URLs from a CSV file.")
    
    # Add arguments for the CSV file path and the percentage
    parser.add_argument('save_path', type=str, help='Path to the output directory')
    parser.add_argument('n_samples', type=float, help='Number of samples of the database to pull')

    # Parse the arguments
    args = parser.parse_args()


    firmware_data_path = "/home/nathan/Documents/Data/Firmware-Dataset/dat/firmware_download_list.csv"
    save_path = "../fws"
    main(firmware_data_path, save_path, args.n_samples)
    