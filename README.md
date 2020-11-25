## Wildly Listen Test

These scripts are used for testing a prototype.
- continuously_monitor
- plot_graphs
- post_analysis
<br>

### 1. continuously_monitor

These scripts can be run parallelly while the device is uploading wav_files to the FTP server.

- *continuous_wav_info_to_csv.py* : continuously save wav_files information to CSV file and continuously check for new wav_files uploaded to FTP directory.

- *device_status.py* :  To know the Device status for the last 5minutes. Script will return Device-ID, last active time and status.

Download or delete wav_files in the given FTP directory.

- *download_delete_files_in_ftp.py* : Download or delete wav_files or download single wav_file in the given FTP directory.
<br>


### 2. plot_graphs

Read the given CSV file(s) which contains wav_header and extra_header information to plot the graphs.

- *battery_drain_plot.py* -  Reads the Battery percentage column from the given CSV file to plot battery drain graph.

- *plot_network.py* - Reads the Network status column from the given CSV file to plot network status graph.
<br>


### 3. post_analysis

Post analysis has two set of scripts to test the prototype:
- ftp_wav_files
- util_offline_scripts

*ftp_wav_files* : Analyze the audio data uploaded to FTP server by running these scripts.

*util_offline_scripts* : Analyze the audio data stored in SD-Card by running these scripts.
