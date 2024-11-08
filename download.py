import os
import argparse
import requests
import pandas as pd
import subprocess

def main(firmware_data_path, save_path):
    """Main function to download all firmware samples and unpack them."""
    download_firmware(firmware_data_path, save_path)
    unpack_firmware_files(save_path)

def download_firmware(firmware_data_path, save_path):
    """Download all firmware files from URLs in a CSV in a single-threaded manner."""
    os.makedirs(save_path, exist_ok=True)  # Create the output folder if it doesn't exist

    # Load firmware URLs from the CSV file
    data = pd.read_csv(firmware_data_path)
    urls = data['url'].tolist()

    # Download each file sequentially
    for url in urls:
        download_file(url, save_path)

def download_file(url, save_path):
    """Download a single firmware file from a URL."""
    try:
        # Extract the original filename from the URL and set the full save path
        filename = os.path.basename(url)
        full_path = os.path.join(save_path, filename)
        
        # Make the request and save the file in chunks
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(full_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:  # Write only if chunk is not empty
                    file.write(chunk)
        print(f"Downloaded: {full_path}")

    except requests.exceptions.RequestException as e:
        print(f"Failed to download {url}: {e}")

def unpack_firmware_files(save_path):
    """Unpack firmware files in the specified directory using binwalk."""
    for root, _, files in os.walk(save_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                subprocess.run(['binwalk', '-Mre', '--directory', save_path, file_path], check=True)
                print(f"Unpacked: {file_path}")
            except subprocess.CalledProcessError as e:
                print(f"Failed to unpack {file_path} with binwalk: {e}")

if __name__ == '__main__':
    # Argument parsing for command-line usage
    parser = argparse.ArgumentParser(description="Download and unpack all firmware files from a CSV file.")
    parser.add_argument('firmware_data_path', type=str, help='Path to the CSV file with firmware URLs')
    parser.add_argument('save_path', type=str, help='Directory to save downloaded firmware files')

    args = parser.parse_args()
    
    main(args.firmware_data_path, args.save_path)
