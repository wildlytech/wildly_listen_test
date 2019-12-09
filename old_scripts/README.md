
# Wildly Listen Test

There are two set of scripts for testing prototype
1. Contious Monitoring 
2. Post Transmission Analysis

## Continuous Monitoring : 
These scripts could be parllely while the device is uploading files to the FTP server.

##### 1. To Group wave files ```(.wav)``` that are being uploaded onto FTP server, on their ```Device ID ```

```shell
$ python group_wav.py --input_path /FTP_DIR_PATH/
```
######  output
* Creates the directory as and when a file from a new ```Device ID``` is found.
* Checks for the complete upload of the file and moves the file to the corresponding directory.
* You can set the time interval after which the files are to be moved i.e window period for ```wav``` files to be uploaded by Device  using the changes shown below. You can change ```SLEEP_TIME```variable ```(seconds)```.

```python

#####################################################
         # Define initial Gloabl Constant#
#####################################################

count = 0
name_of_devices = set()
initial_number_of_devices = 0
SLEEP_TIME = 120

```

##### 2. To monitor the Upload status of the device that is being uploaded onto FTP server.

```shell
$ python upload_status.py --input_path /FTP_DIR_PATH/
```
###### output 
* Checks for the new files that are uploaded to the specified directory
* ```Prints``` if no ```wav``` files are uploaded for the specified amount of time. ```( 2 Minutes)```
* You can set the time you want to be popped up with the status by changing the sleep time in the code snipped mentioned below.
```python
# SET THE TIME INTERVAL AFTER WHICH IT CHECKS FOR NEW FILE, in seconds
SLEEP_TIME = 120
```


## Post Transmission Analysis
These python scripts should be run after the transmission test is done.

Follow the link below for more details of these scripts

[Post Transmission Analysis](https://github.com/wildlytech/wildly_listen_test/tree/master/post_transmission_analysis)
