'''Code for FTP Status
'''
from ftplib import FTP
import argparse


DESCRIPTION = 'Input The path to the directory'
HELP = 'Input the path'
PARSER = argparse.ArgumentParser(description=DESCRIPTION)
PARSER.add_argument('-input_path', '--input_path', action='store',
                    help=HELP, default='/home/user-u0xzU/')

RESULT = PARSER.parse_args()
PRIMARY_PATH = "/home/user-u0xzU" + RESULT.input_path
print PRIMARY_PATH


def connect():
    '''
    TO connect to ftp
    '''
    global ftp, CURRENT_DIR
    ftp = FTP('*****', user='****', passwd='****')
    print "connected to FTP"
    CURRENT_DIR = ftp.cwd(PRIMARY_PATH)

def last_modified():
    '''
    To count the total no.of files and last modified file in a directory
    '''
    names = ftp.nlst()
    latest_time = None
    latest_name = None
    count = 0

    for name in names:
        if (name[-3:] == 'wav') or (name[-3:] == 'WAV'):
            time1 = ftp.voidcmd("MDTM " + name)
            count += 1
            if (latest_time is None) or (time1 > latest_time):
                latest_name = name
                latest_time = time1

    print "Last uploaded file is", latest_name, latest_time[4:]
    print "Total no.of files is :", count

def download_files(flag):
    """
    Download the wav file into local drive if uploaded into
    ftp server
    """
    if flag == 1:
        ex = ftp.nlst()
        ex_wav = []
        wav_file_count = 0
        for wav in ex:
            if (wav[-3:] == 'wav') or (wav[-3:] == 'WAV'):
                ex_wav.append(wav)
        for each_file in ex_wav:
            if each_file[-3:] == 'wav' or 'WAV':
                try:
                    wav_file_count = wav_file_count + 1
                    print "Download count:", wav_file_count
                    with open(each_file, 'wb') as file_obj:
                        ftp.retrbinary('RETR '+ each_file, file_obj.write)
                except:
                    print "File Error"
            else:
                pass

        return wav_file_count


def clearing(flag):
    '''to delete the files from FTP
    '''
    if flag == 1:
        lis = ftp.nlst()
        for filename in lis:
            print "file deleted ", filename
            ftp.delete(filename)


if __name__ == '__main__':
    connect()
    last_modified()
    TOTAL_FILES_DOWNLOADED = download_files(1)
    # clearing(1)
