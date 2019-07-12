# RescueTimeAnalysis

## Dependencies
- Python 3
- modules `request`,  `pandas`. Run `pip3 install request` and `pip3 install pandas`.

## Directions

### Directions to download data (no need to run if data already downloaded)
- Run `python3 download_data.py begin_date end_date` in the home directory to download data for days beginning on `begin_date` and ending on `end_date` (inclusive). Date format is YYYY-MM-DD.
- Then run `python3 combine_data.py` to combine all data from all files into one csv, `all_data.csv`.

### Directions for analysis

### Directions for kmeans

- Run `python3 aggregate_by_month.py` to ensure that all month aggregated data is up to date.

- (Optional) go into `kmeans.py` and modify the year and month arrays such that it analyzes the subset of data you desire. Make sure you only include years that have a full year of data.

- Run `python3 kmeans.py` in the home directory and input the desired number of clusters when prompted. A graph will automatically be generated and displayed, as well a text info regarding each cluster in the console. The results from this run will be saved in `saved_results`, and its index will be based off the current number in `index.txt`. To view the results from any previous run, run `python3 kmeans_from_txt.py` in the home directory and when prompted, input the desired index. 

### Directions for lfa

- Run `python3 aggregate_by_month.py` to ensure that all month aggregated data is up to date.

- (Optional) go into `kmeans.py` and modify the year and month arrays such that it analyzes the subset of data you desire. Make sure you only include years that have a full year of data.

- Run `python3 lfa.py` in the home directory and input the desired number of clusters and apps in each cluster when prompted. A graph will automatically be generated and displayed, as well a text info regarding each cluster in the console. Results are deterministic, so in order to view results of a specific run, simply run again with the same parameters.

### Directions for kmeans/lfa animations

- Results from kmeans or lfa runs are saved in `clusters.txt`. Run `python3 cluster_animation.py` to view an animated view of the time spent in each cluster over time. This view might make more sense than viewing a 72-D point using a line graph.

- Note: Only one kmeans or lfa run is saved at a time. 
