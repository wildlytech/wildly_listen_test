# wildly_listen_test


## 1. FTP Status/Information : 


   The code will give you the below information.
  * Number of folders/ number of files in a given folder.
  * Last file upload for a given folder.
  * Download all the file locally and Clearing all the files from that directory in FTP.

How to run the code:

   ``` python ftp_status.py --input_path [path_to_the_directory]```

## 2. Wav file information scraping
  
 
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
 
 
``` python read_wav_1.py --input_path [path_to_the_directory]```


## 3:  Wav file grouping by Device ID: 


This code will get the Device Id of each wav file and create a folder for each device Id and move it to that director.

How to run the code:

``` python read_device.py --input_path [path_to_the_directory]```


## 4:  Wav file monitor:


This code will notify whenever the first upload has started and also notify when there is no upload for certain time(1 min )

How to run the code:

``` python upload_stat.py --input_path [path_to_the_directory]```

