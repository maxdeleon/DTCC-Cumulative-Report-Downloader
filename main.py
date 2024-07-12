## Maximo de Leon 07/11/2024
import pandas as pd
import numpy as np
import requests
import matplotlib.pyplot as plt
import zipfile
import os
import sys
from tqdm import tqdm
import argparse
import os


CTFC_DTCC_DATA_URL = 'https://pddata.dtcc.com/ppd/api/report/cumulative/cftc/'
get_cumulative_rate_swap_trade_file_data = lambda : requests.get('https://pddata.dtcc.com/ppd/api/cumulative/CFTC/IR').json()
cumulative_rate_swap_file_data = get_cumulative_rate_swap_trade_file_data()

get_cumulative_rate_swap_trade_urls = lambda file_data,endpoint=CTFC_DTCC_DATA_URL: list(map(lambda x: endpoint+x['fileName'],file_data))
cumulative_rate_swap_trade_urls = get_cumulative_rate_swap_trade_urls(cumulative_rate_swap_file_data)

get_missing_cumulative_rate_swap_trade_urls = lambda missing_files,endpoint=CTFC_DTCC_DATA_URL: list(map(lambda x: endpoint+x.replace('.csv','.zip'),missing_files))


def check_directory_for_cumulative_reports(target_directory):
    # checks target directory for cumulative reports. Returns list of missing reports
    cumulative_rate_swap_file_data = get_cumulative_rate_swap_trade_file_data()
    cumulative_rate_swap_file_data_csvs = list(map(lambda x:x['fileName'].replace('.zip','.csv'),cumulative_rate_swap_file_data))
    all_items = os.listdir(target_directory)
    files_not_included = [file for file in cumulative_rate_swap_file_data_csvs if file not in all_items]
    # return the list 
    return files_not_included

def download_zip(url, target_path):
    # Send HTTP GET request
    with requests.get(url, stream=True) as response:
        # Raise an exception in case of a bad response (e.g., failed download)
        response.raise_for_status()
        with open(target_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192): # Write the contents of the response to the file
                file.write(chunk)

def extract_and_delete_zip(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        # Assuming there's exactly one CSV file in the ZIP
        csv_name = [f for f in zip_ref.namelist() if f.endswith('.csv')][0]
        zip_ref.extract(csv_name, path=extract_to)
    os.remove(zip_path)
    return os.path.join(extract_to, csv_name)


def download_cumulative_swap_transactions_dtcc(target_directory,endpoint=CTFC_DTCC_DATA_URL):
    missing_cumulative_reports = check_directory_for_cumulative_reports(target_directory)
    missing_urls = get_missing_cumulative_rate_swap_trade_urls(missing_cumulative_reports)
    print(f'Target Directory: {target_directory} has {len(missing_cumulative_reports)} reports')
    for i,url in tqdm(enumerate(missing_urls)):
        zip_path = target_directory +url.replace(endpoint,'')
        # download the zip
        download_zip(url, zip_path)
        # unzip the zip
        csv_path = extract_and_delete_zip(zip_path, target_directory)
    print('Done')
    return True

def load_swap_data(target_directory):
    files = os.listdir(target_directory)
    trades = []
    for file in files:
        raw = pd.read_csv(target_directory+file)
        trades.append(raw)

    return pd.concat(trades,axis=0)





def load_swap_data():
    print("Loading swap data...")

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Process download and export directories.')
    parser.add_argument('--download_directory', type=str, default='./CFTC_CUMULATIVE_RATES/', help='Directory to store the downloaded csvs')
    parser.add_argument('--export_directory', type=str, help='Directory to export one big csv. Avoid doing this if you do not have a lot of memory ')

    # Parse arguments
    args = parser.parse_args()
    download_directory = args.download_directory
    export_directory = args.export_directory



    # Ensure download_directory exists
    if not os.path.exists(download_directory):
        os.makedirs(download_directory)
        print(f"Created directory: {download_directory}")


    target_directory = './CFTC_CUMULATIVE_RATES/'
    has_downloaded = False
    has_downloaded = download_cumulative_swap_transactions_dtcc(target_directory)
    
    raw_swap_data = load_swap_data(target_directory)

    # Load swap data only if export_directory is provided
    if export_directory:
        raw_swap_data = load_swap_data(target_directory)
        # Add logic here to use export_directory if needed
        print(f"Using export directory: {export_directory}")
        raw_swap_data.to_csv(f'{export_directory}/SDR_CUMULATIVE_RATES_EXPORT.csv')

    else:
        print("Done.")

if __name__ == "__main__":
    main()
