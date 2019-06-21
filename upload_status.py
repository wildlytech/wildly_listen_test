'''
Returns Device Id of each wav file and creates a folder for each device Id 
and moves the wav file to the respective directory.
'''

from ftplib import FTP
import time
import argparse
import requests
from scipy.io import wavfile
import numpy as np
import os


DESCRIPTION = 'Input The path to the directory'
HELP = 'Input the path'
PARSER = argparse.ArgumentParser(description=DESCRIPTION)
PARSER.add_argument('-input_path', '--input_path', action='store', help=HELP)

RESULT = PARSER.parse_args()
PRIMARY_PATH = "/home/user-u0xzU" + RESULT.input_path
print PRIMARY_PATH

# SET THE TIME INTERVAL AFTER IT CHECKS FOR NEW FILE, in seconds
SLEEP_TIME = 5

UPLOADED_FILES = []

#connect to ftp
def connect():
    '''
    fuction to connect it to FTP
    '''
    global ftp
    ftp = FTP('34.211.117.196', user='user-u0xzU', passwd='h3KAGsdMHDIqJU')
    ftp.cwd(PRIMARY_PATH)
    print "connected to FTP", ftp.pwd()


def sms():
    '''
    to send sms
    '''
    global URL, PAYLOAD, HEADERS
    URL = "https://www.fast2sms.com/dev/bulk"
    PAYLOAD = "sender_id=FSTSMS&message=NOTIFY_ME_ONCE&language=english&route=p&numbers=*********"
    HEADERS = {'authorization': "******",
               'Content-Type': "application/x-www-form-urlencoded",
               'Cache-Control': "no-cache"}


def check_for_wavfiles_only(list_of_files):
    wavfiles_only  = []
    for name_file in list_of_files:
        if name_file[-3:] == "wav" or name_file[-3:] == "WAV":
            wavfiles_only.append(name_file)
    return wavfiles_only    

def upload_status():
    '''
	Tell the status whether the file is uploaded or not
	'''
    names = ftp.nlst()
    names = check_for_wavfiles_only(names)
    print "No. of files in ftp directory:", len(names)
    #used flag to get notify only once if multiple files are uploaded
    flag = 0
    #store all the previous file in the dict to compare later
    before = dict([(file_name, None) for file_name in names])
    #print before
    while 1:
        #time after which it will compare
        time.sleep(SLEEP_TIME)

        #get the list after that time
        names = ftp.nlst()
        names = check_for_wavfiles_only(names)

        #store the list obtain in the dict
        after = dict([(file_name, None) for file_name in names])

        #Check if the new files are added
        added = [file_name for file_name in after if file_name not in before]
        if added:
            UPLOADED_FILES.append(added)
            print "\n", len(added), "file(s) added", ",", "Added file name(s): ", ", ".join(added)
            print "Checking for Mic connection by verfying wavfile Data.. "

            for each_wav_file in np.array(UPLOADED_FILES).flatten():
                ftp.sendcmd("TYPE i")
                if ftp.size(each_wav_file) >= 320000:
                    ftp.sendcmd("TYPE A")
                    with open(each_wav_file, 'wb') as file_obj:
                        ftp.retrbinary('RETR '+ each_wav_file, file_obj.write)
                    wavdata = wavfile.read(each_wav_file)[1]
                    if wavdata.sum() == 0:
                        print "\nFound Possible Mic Connection Error: ", each_wav_file
                        print "Moving to ZeroData folder\n"
                        if "ZeroData" not in ftp.nlst():
                            ftp.mkd("ZeroData")
                        else:
                            pass
                        ftp.rename(PRIMARY_PATH+"/"+each_wav_file, PRIMARY_PATH+"/ZeroData/"+each_wav_file)
                        os.remove(each_wav_file)
                    else:
                        pass     
                else:
                    ftp.sendcmd("TYPE A")
            if flag == 0:
                print "Upload has started..."
            	#response = requests.request("POST", URL, data=PAYLOAD, headers=HEADERS)
            	#print response.text
            flag = 1
        #check if there is no files added in the directory
        if after == before:
            print "\nNo files uploaded in last " + str(SLEEP_TIME) +" seconds"
        before = after

if __name__ == '__main__':
    connect()
    #sms()
    upload_status()

