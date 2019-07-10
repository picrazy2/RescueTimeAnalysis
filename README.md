# RescueTimeAnalysis

## Dependencies
- Python 3
- modules `request`,  `pandas`. Run `pip3 install request` and `pip3 install pandas`.

## Directions

### Directions to download data (no need to run if data already downloaded)
- Run `python3 download_data.py begin_date end_date` in the home directory to download data for days beginning on `begin_date` and ending on `end_date` (inclusive). Date format is YYYY-MM-DD.
- Then run `python3 combine_data.py` to combine all data from all files into one csv, `all_data.csv`.

### Directions for analysis
