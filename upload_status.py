'''
Returns Device Id of each wav file and creates a folder for each device Id 
and moves the wav file to the respective directory.
'''

from ftplib import FTP
import time
import argparse
import requests



DESCRIPTION = 'Input The path to the directory'
HELP = 'Input the path'
PARSER = argparse.ArgumentParser(description=DESCRIPTION)
PARSER.add_argument('-input_path', '--input_path', action='store', help=HELP)

RESULT = PARSER.parse_args()
PRIMARY_PATH = "/home/user-u0xzU" + RESULT.input_path
print PRIMARY_PATH

# SET THE TIME INTERVAL AFTER IT CHECKS FOR NEW FILE, in seconds
SLEEP_TIME = 120

#connect to ftp
def connect():
    '''
    fuction to connect it to FTP
    '''
    global ftp
    ftp = FTP('*********', user='*********', passwd='*********')
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



def upload_status():
    '''
	Tell the status whether the file is uploaded or not
	'''
    names = ftp.nlst()
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

        #store the list obtain in the dict
        after = dict([(file_name, None) for file_name in names])

        #Check if the new files are added
        added = [file_name for file_name in after if file_name not in before]
        if added:
            print "\n", len(added), "file(s) added", ",", "Added file name(s): ", ", ".join(added)
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
