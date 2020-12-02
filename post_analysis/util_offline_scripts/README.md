## Wildly Listen Test - SD-Card scripts

Analyze the audio data stored in **SD-Card** by running these scripts. To each script, below mentioned information will be output for the given **wav_files path** as input :
-   First and last wav file name with timestamp for the given wav_files directory.
-   Minimum, maximum and average time gap (in seconds) between the consecutive wav files in SD-card.
-   Read wav_header and extra_header information of each wav file in SD-card and save it to a CSV file.
-   Corrupt data and Zero data wav files will be moved to the respective folders in the SD-card.

>Note: 
> - Given wav files folder path should be *'absolute path'*.
> - Wav files folder name should start with '**D**'.

<br>

### Scripts to analyze wav files in SD-Card
#### 1. To get minimum, maximum and average time gaps (in seconds) of consecutive wav files in SD-card :
```shell
$ python util_average_time_gap.py  -input_path /path/to/wav/files/
```
<br>

#### 2. To move corrupt data and zero data wav files in SD-card :
This script moves all the corrupt and zero data wav files to respective folders if found.
```shell
$ python util_corrupt_zerodata.py  -input_path /path/to/wav/files/
```
<br>

####  3. To get first and last wav file names with timestamp in SD-card : 
```shell
$ python util_first_and_last_file.py  -input_path /path/to/wav/files/
```
<br>

#### 4. Read wav_header and extra_header information of each wav file in SD-card and save it to a CSV file :
```shell
python util_wav_info_to_csv.py  -input_path /path/to/wav/files 
                                -path_to_save_csv /path/to/save/csv/file/
```
<br>
