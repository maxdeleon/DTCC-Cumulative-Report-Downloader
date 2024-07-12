# DTCC-Cumulative-Report-Downloader

This script downloads and processes cumulative rates swap transaction data from the DTCC CFTC data repository. If you would like to contribute please feel free to make a pull request.

## Requirements

The following Python packages are required:
- `pandas`
- `numpy`
- `requests`
- `matplotlib`
- `tqdm`
- `argparse`

You can use `environment.yml` to create the environment via:

```sh
conda env create -f environment.yml
```

## Usage

### Command Line Arguments

- `--download_directory`: Directory to store the downloaded CSV files (default: `./CFTC_CUMULATIVE_RATES/`).
- `--export_directory`: Directory to export one big CSV file. This step is optional and will be skipped if not provided.

### Running the Script

To run the script, use the following command:

```sh
python script.py --download_directory <your_download_directory> --export_directory <your_export_directory>
```

If you do not provide the `--download_directory` argument, it will default to `./CFTC_CUMULATIVE_RATES/`. If you do not provide the `--export_directory` argument, the `load_swap_data` function will be skipped.

#### Examples

1. With default `download_directory` and no `export_directory`:
    ```sh
    python script.py
    ```

2. With specified `download_directory` and `export_directory`:
    ```sh
    python script.py --download_directory my_downloads --export_directory my_exports
    ```

3. With default `download_directory` and specified `export_directory`:
    ```sh
    python script.py --export_directory my_exports
    ```

## Notes

- The script will create the `download_directory` if it does not exist.
- The script will skip the data loading block if the `export_directory` is not provided.

## License

This project is licensed under the MIT License.