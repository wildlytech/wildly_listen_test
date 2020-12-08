## Wildly Listen Test - Continuously monitor/delete

- Monitoring the devices in real time by running these scripts:
  - Read wav_header and extra_header information of each wav file in given the **FTP** directory and save it to CSV file and continuously check for new wav_files uploaded to the given FTP directory and save their header and extra_header information to CSV file.
  - Know the device status for the last 5minutes.

- Download or delete wav_files or download single wav_file in the given **FTP** directory.

> Note: Add FTP credentials to the scripts before running them.

<br>

#### 1. Continuously save wav_files information to CSV file :
-  Wav_file header and extra header information of each wav_file from the selected FTP directory is added to CSV file given first_character of wav_file.
- Continuously checks for new wav_files in the selected FTP directory and these newly uploaded wav_files header and extra_header information will be added to CSV file.
        
 ```shell
$ python continuous_wav_info_to_csv.py -input_path /ftp/folder/path/
                                       -input_first_character input_first_character_of_wav_file
                                       -path_to_save_csv /path/to/save/csv/file/
```

<br>

#### 2. To know the Device status for the last 5minutes :
Based on the wav_file uploads to the given FTP directory, script will return Device-ID, last active time and status for the last 5minutes.

```shell
$ python device_status.py -input_path /ftp/folder/path/
```

> Example: 
> ```shell
> $ python device_status.py -input_path /BNP/
> output :
> Device ID: DEV5487100_20:06:19-22:17:51 , Status: Inactive , Last Time: 2020-06-26 12:37:00
> ```

<br>

#### 3. Download or delete wav_files in the given **FTP** directory.
```shell
$ python download_delete_files_in_ftp.py -input_path /ftp/folder/path/
                                         -input_first_character input_first_character_of_wav_file 
                                         -download_delete enter_argument
```

> Example:
> ```shell
> $ python download_delete_files_in_ftp.py -input_path /BNP/DEV5487102_19:10:01-12:27:51/
>                                          -input_first_character A
>                                          -download_delete 3
> ```