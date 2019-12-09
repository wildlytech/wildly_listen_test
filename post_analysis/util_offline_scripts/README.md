##  Wildly Listen Test 
### Scripts to analyse wav files in SD Card

##### 1. To get first and last wav file names with timestamp : 

```shell
$ python util_first_and_last_file.py  -input_path /path/to/wav/files
```
<br>

##### 2. To get average, minimum, maximum time gaps of consecutive wav files in sd-card:
```shell
$ python util_average_time_gap.py  -input_path /path/to/wav/files
```
<br>

##### 3. To get a CSV file which has wav files header and extra-header:
```shell
python util_wav_info_to_csv.py  -input_path /path/to/wav/files 
                                -path_to_save_csv /path/to/save/csv
```
<br>

##### 4. To get corrupt and zero data wav files in sd-card:
This moves all the corrupt and zero data wav files to respective folders if found.
```shell
$ python util_corrupt_zerodata.py.py  -input_path /path/to/wav/files
```