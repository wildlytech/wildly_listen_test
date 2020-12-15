from ftplib import FTP
import socket
import ftplib
import os
import argparse

DESCRIPTION = 'Input The path to the directory'
HELP = 'Input the path'
PARSER = argparse.ArgumentParser(description=DESCRIPTION)
PARSER.add_argument('-input_path', '--input_path', action='store', help='Input path to wav files')
PARSER.add_argument('-input_first_character', '--input_first_character', action='store', \
	help='Input required first character of the file name series')
PARSER.add_argument('-download_delete', '--download_delete', action='store',\
 help='Input 1 to download files, 2 to delete files, \
 3 to download and delete files or a enter wav_file_name to download')

RESULT = PARSER.parse_args()
PRIMARY_PATH = "/home/user-u0xzU" + RESULT.input_path
CHARACTER = RESULT.input_first_character
FLAG = RESULT.download_delete
print("Path:", PRIMARY_PATH)
print("character:", CHARACTER)
dirpath = os.getcwd()

# add ftp credentials to connect
def connect(PRIMARY_PATH):
    '''Connect to ftp'''
    global ftp
    ftp = FTP('**********', user='**********', passwd='**********')
    ftp.cwd(PRIMARY_PATH)
    print("connected to FTP")


def delete_files():
    '''Delete files'''
    files_list = ftp.nlst(str(CHARACTER)+'*')
    count = 0
    print("Deleting files..")
    for f in files_list:
        try:
            count += 1
            ftp.delete(f)
        except ftplib.error_temp:
            connect(PRIMARY_PATH)
        except socket.error:
            connect(PRIMARY_PATH)
    print("No. of files deleted:", count)
    print("Finished deleting files..")


def download_files():
    '''Download files'''
    count1 = 0
    files_list = ftp.nlst(str(CHARACTER)+'*')
    print("Downloading files..")
    path_to_save_wav_files = dirpath+'/downloaded_files'+RESULT.input_path
    print("Wav files downloaded to:", path_to_save_wav_files)

    if not os.path.exists(path_to_save_wav_files):
    	os.makedirs(path_to_save_wav_files)
    for each_wav_file in files_list:
        with open(path_to_save_wav_files+each_wav_file, 'wb') as file_obj:
            ftp.retrbinary('RETR '+ each_wav_file, file_obj.write)
            count1 += 1
    print("Number of files downloaded:", count1)
    print("Finished downloading files..")


def download_file(each_wav_file):
    ''' download single file '''
    with open(each_wav_file, 'wb') as file_obj:
        ftp.retrbinary('RETR '+ each_wav_file, file_obj.write)


connect(PRIMARY_PATH)
if FLAG == "1":
    download_files()

if FLAG == "2":
    delete_files()

if FLAG == "3":
    download_files()
    delete_files()

if (FLAG[-3:] == 'wav') or (FLAG[-3:] == 'WAV'):
	download_file(FLAG)
	