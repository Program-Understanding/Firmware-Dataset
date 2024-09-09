import requests
import os
import pandas as pd
import multiprocessing

def download_firmware(firmware_data_path, save_path, n_samples):
    global SAVE_PATH 
    SAVE_PATH = save_path
    if not os.path.exists(save_path):
        os.makedirs(save_path)  # Create the folder if it doesn't exist

    data = pd.read_csv(firmware_data_path)

    # Randomly sample the rows based on the calculated sample size
    sampled_data = data.sample(n=int(n_samples), random_state=1)  # random_state ensures reproducibility if needed

    urls = sampled_data['url'].tolist()

    # Use multiprocessing to download files
    num_processes = multiprocessing.cpu_count()  # Use the number of CPU cores
    with multiprocessing.Pool(processes=num_processes) as pool:
        pool.map(download_file, urls)

def download_file(url):
    try:
        # Extract the original file name from the URL
        original_filename = os.path.basename(url)
        full_save_path = os.path.join(SAVE_PATH, original_filename)
        
        # Make the request to download the file
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Check for HTTP errors

        with open(full_save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:  # Filter out keep-alive new chunks
                    file.write(chunk)
        print(f"Firmware downloaded successfully and saved to {full_save_path}")

    except requests.exceptions.RequestException as e:
        print(f":Failed to download the firmware from {url}: {e}")