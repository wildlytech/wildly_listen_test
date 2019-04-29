# Wildly_listen_test


## 1. FTP Status : 


   The code will give you the below information.
  * Number of folders/ number of files in a given folder.
  * Last file upload for a given folder.
  * Download all the file locally(if required) and Clearing all the files from that directory in FTP(if required).

How to run the code:

   ``` shell
   python ftp_status.py --input_path [path_to_the_directory]
   ```

## 2. Reading Wav files :
  
 
 The code will give details of each wav file in a directory and if some of the wav file are corrupt it will move that wav file in that directory.

### Details it will provide:


  * Subchunk 1 size
  * Audioformat
  * Number of channels
  * Sample rate
  * Bits per sample
  * Subchunk 2 size
  * Time duration
### Calculate and verify:

   * Byte rate
   * Block align

 How to run  the code :
 
 
``` shell
python read_wav_details.py --input_path [path_to_the_directory]
```

Output:
Output will be a csv file which contains the details of all wav files


## 3:  Wav file grouping by Device ID: 


This code will get the Device Id of each wav file and create a folder for each device Id and move it to that director.

How to run the code:

``` shell
python group_wav.py --input_path [path_to_the_directory]
```


## 4:  Wav file monitor:


This code will notify(send sms to the user) whenever the first upload has started and also notify when there is no upload for certain time(1 min )

How to run the code:

```shell
python upload_status.py --input_path [path_to_the_directory]
```

