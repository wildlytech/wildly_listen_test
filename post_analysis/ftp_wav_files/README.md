## Wildly Listen Test - FTP scripts

Analyze the audio data uploaded to **FTP** by running these scripts. 
Below mentioned information will be the output for the given FTP directory as input to each script:
- First and last wav file name with timestamp for the given FTP directory.
- Minimum, maximum and average time gap (in seconds) between the consecutive wav files in FTP.
- Read wav_header and extra_header information of each wav file in FTP and save it to csv file.
- Corrupt wav files will be moved to the *Corrupt_files* folder in the FTP.

> Note: Add FTP credentials to the scripts before running them.

<br>

### Scripts to analyze wav files in FTP


#### 1. To get first and last wav file names with timestamp : 
```shell
$ python first_and_last_file.py -input_path /ftp/folder/path/to/wav/files 
                                -input_first_character input_first_character_of_wav_file
```
> Example: 
> ```shell
> $ python first_and_last_file.py -input_path /BNP/ 
>                                 -input_first_character A
> ```

<br>

#### 2. To get minimum, maximum and average time gaps (in seconds) of consecutive wav files:
```shell
$ python average_upload_time.py -input_path /ftp/folder/path/to/wav/files 
                                -input_first_character input_first_character_of_wav_file
```
<br>

####  3. Read wav_header and extra_header information of each wav file in FTP and save it to CSV file:
```shell
$ python wavheader_info_to_csv.py -input_path /ftp/folder/path/to/wav/files 
                                  -input_first_character input_first_character_of_wav_file
                                  -path_to_save_csv /path/to/save/csv
```
<br>

####  4. Move corrupt wav files to Corrupt_files folder if found:
```shell
$ python corrupt_files.py  -input_path /ftp/folder/path/to/wav/files 
                           -input_first_character input_first_character_of_wav_file
```
> Example: 
> ```shell
> $ python corrupt_files.py -input_path /BNP/DEV5487102_19:10:01-12:27:51/
>                           -input_first_character A
> ```
