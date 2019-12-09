'''Code for FTP Status
'''
from ftplib import FTP
import argparse
from datetime import date, datetime, time, timedelta


DESCRIPTION = 'Input The path to the directory'
HELP = 'Input the path'
PARSER = argparse.ArgumentParser(description=DESCRIPTION)
PARSER.add_argument('-input_path', '--input_path', action='store',
                    help=HELP, default='/home/user-u0xzU/')

RESULT = PARSER.parse_args()
PRIMARY_PATH = "/home/user-u0xzU" + RESULT.input_path
print PRIMARY_PATH

# first character of file nmaes
LETTER = 'A*'
datetimeFormat = '%Y%m%d%H%M%S'

def connect():
    '''
    TO connect to ftp
    '''
    global ftp, CURRENT_DIR
    ftp = FTP('*****', user='****', passwd='****')
    print "connected to FTP"
    CURRENT_DIR = ftp.cwd(PRIMARY_PATH)

def first_modified():
    '''to get first modified file in a directory
    '''
    names = ftp.nlst(LETTER)
    oldest_time = None
    oldest_name = None
    count = 0

    for name in names:
        try:
            if (name[-3:] == 'wav') or (name[-3:] == 'WAV'):
                time1 = ftp.voidcmd("MDTM " + name)
                #print name
                count += 1
                if (oldest_time is None) or (time1 < oldest_time):
                    oldest_name = name
                    oldest_time = time1
        except:
            connect()
    lt=oldest_time[4:]
    # adding 330 min to get time in IST
    time2 = datetime.strptime(lt, datetimeFormat) + timedelta(minutes=330)
    print "Number of files:", count
    print "First uploaded File name:", oldest_name, ", Date and Time:", time2

def last_modified():
    '''to get last modified file in a directory
    '''
    names = ftp.nlst(LETTER)
    latest_time = None
    latest_name = None
    count = 0

    for name in names:
        try:
            if (name[-3:] == 'wav') or (name[-3:] == 'WAV'):
                time1 = ftp.voidcmd("MDTM " + name)
                #print name
                count += 1
                if (latest_time is None) or (time1 > latest_time):
                    latest_name = name
                    latest_time = time1
        except:
            connect()
    lt = latest_time[4:]
    # adding 330 min to get time in IST
    time2 = datetime.strptime(lt, datetimeFormat) + timedelta(minutes=330)
    print "Number of files:", count
    print "Last uploaded File name:", latest_name, ", Date and Time:", time2    

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
    first_modified()
    last_modified()
    #TOTAL_FILES_DOWNLOADED = download_files(1)
    # clearing(1)
