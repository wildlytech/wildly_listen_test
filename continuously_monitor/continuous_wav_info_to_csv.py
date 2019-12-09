import sys
sys.path.insert(0, '../post_analysis/ftp_wav_files/')
import util
import wavheader_info_to_csv
from ftplib import FTP
import time
import argparse
import socket
import ftplib
import struct
import numpy as np
import os
import csv
import pandas as pd
import operator
from datetime import datetime


DESCRIPTION = 'Input The path to the directory'
HELP = 'Input the path'
PARSER = argparse.ArgumentParser(description=DESCRIPTION)
PARSER.add_argument('-input_path', '--input_path', action='store', help=HELP)
PARSER.add_argument('-path_to_save_csv', '--path_to_save_csv', action='store', \
    help='Input path to save csv')
PARSER.add_argument('-input_first_character', '--input_first_character', action='store', \
    help='Input required first character of the file name series')
RESULT = PARSER.parse_args()


PRIMARY_PATH = "/home/user-u0xzU" + RESULT.input_path
PATH_2 = RESULT.path_to_save_csv
print "Given path to save CSV:", PATH_2

CHARACTER = RESULT.input_first_character
print "Character:", CHARACTER

CSV_FILE_NAME = "Transmitted_wav_files_info.csv"

# add ftp credentials
def connect(PRIMARY_PATH):
    '''Connect to ftp'''
    global ftp
    ftp = FTP('********', user='********', passwd='********')
    ftp.cwd(PRIMARY_PATH)


def check_for_wavfiles_only(list_of_files):
    '''returns only wav file'''
    wavfiles_only = []
    for name_file in list_of_files:
        if name_file[-3:] == "wav" or name_file[-3:] == "WAV":
            wavfiles_only.append(name_file)
    return wavfiles_only


def continuous_wav_info_to_csv():
    '''
     i. wav file header and extra header information is added to csv from the
        selected ftp directory and character series.
    ii. continuously checks for new wav files in the selected ftp directory
        and newly uploaded wav files information is added to csv.
    '''
    # add wav files header and extra header information to csv
    primary_path2 = wavheader_info_to_csv.wav_header_to_csv(PRIMARY_PATH, CHARACTER)
    print "primary_path2:", primary_path2
    # connect to selected ftp directory
    connect(primary_path2)
    list_of_files = ftp.nlst(str(CHARACTER)+'*')
    names = check_for_wavfiles_only(list_of_files)
    print "No. of files in ftp directory:", len(names)

    # save all the previous wav files list in a dict to compare later
    before = dict([(file_name, None) for file_name in names])

    while 1:
        UPLOADED_FILES = []
        connect(primary_path2)
        names = ftp.nlst(str(CHARACTER)+'*')

        files_in_csv = pd.read_csv(PATH_2 +'/'+ CSV_FILE_NAME, \
            error_bad_lines=False)
        all_filenames = files_in_csv["Filename"].values.tolist()
        files_set = set(names) - set(all_filenames)
        files_not_in_csv = list(files_set)

        names = check_for_wavfiles_only(names)
        #store the list obtain in the dict
        after = dict([(file_name, None) for file_name in names])

        #Check if the new files are added
        added = [file_name for file_name in after if file_name not in before]
        if added:
            DICT1 = {}
            UPLOADED_FILES.append(added)
            print len(added), "file(s) added", ",", "Added file name(s): ", ", ".join(added)
            # sort the wav files based on ftp time
            for name in files_not_in_csv:
                try:
                    if (name[-3:] == 'wav') or (name[-3:] == 'WAV'):
                        time1 = ftp.voidcmd("MDTM " + name)
                        DICT1[time1[4:]] = name
                except ftplib.error_temp:
                    connect(PRIMARY_PATH)
                except socket.error:
                    connect(PRIMARY_PATH)
            # sort based on ftp time
            sorted_time_list = sorted(DICT1.items(), key=operator.itemgetter(0))
            sorted_wav_files_list = [element[1] for  element in sorted_time_list]

            # open csv where wav header infomation is added and
            # append newly added wav file header information to the same csv
            with open(PATH_2 +'/'+ CSV_FILE_NAME, "a") as file_object:
                wav_information_object = csv.writer(file_object)

                for wav_file in sorted_wav_files_list:
                    try:
                        wav_header, extra_header = util.get_wavheader_extraheader(wav_file)
                        information_value = [wav_file]
                        for index_value, each_tag_value in enumerate(extra_header):
                            try:
                                corresponding_tag, corresponding_value = each_tag_value.split(":")
                                if corresponding_tag == " Signal":
                                    corresponding_value = corresponding_value.split("-")
                                    for signal_split in corresponding_value:
                                        information_value.append(signal_split)
                                else:
                                    information_value.append(corresponding_value)

                            except ValueError:
                                corresponding_value = ":".join(each_tag_value.split(":")[1:])
                                timestamp1 = corresponding_value
                                information_value.append(corresponding_value)

                        for tag in wavheader_info_to_csv.wav_info_tags2:
                            value = wav_header[tag]
                            information_value.append(value)
                        # read the csv into a dataframe and get Time_Stamp column to a list
                        df = pd.read_csv(PATH_2 +'/'+ CSV_FILE_NAME)
                        list_of_time_stamps = df['Time_Stamp'].values.tolist()

                        # get time difference of consecutive files timestamp
                        datetimeFormat = '%Y/%m/%d-%H:%M:%S'
                        time_diff = datetime.strptime(timestamp1, datetimeFormat) - \
                        datetime.strptime(list_of_time_stamps[-1], datetimeFormat)
                        td = str(time_diff)

                        # convert timestamp difference to seconds and append to the row
                        if len(td.split(' ')) == 1:
                            hh = int(td.split(":")[0])
                            mm = int(td.split(":")[1])
                            ss = int(td.split(":")[2])
                            seconds = hh*60*60 + mm*60 + ss
                        elif td.split(" ")[0][0] == '-':
                            dd = int(td.split(" ")[0][1])
                            hh = int(td.split(" ")[2].split(":")[0])
                            mm = int(td.split(" ")[2].split(":")[1])
                            ss = int(td.split(" ")[2].split(":")[2])
                            seconds = int('-'+str(dd*24*60*60 + hh*60*60 + mm*60 + ss))
                        else:
                            dd = int(td.split(" ")[0])
                            hh = int(td.split(" ")[2].split(":")[0])
                            mm = int(td.split(" ")[2].split(":")[1])
                            ss = int(td.split(" ")[2].split(":")[2])
                        information_value.append(seconds)

                        wav_information_object.writerow(information_value)
                        file_object.flush()
                    except socket.error:
                        connect(primary_path2)
                    except ftplib.error_temp:
                        connect(primary_path2)
                    except struct.error:
                        print "File size error, file name:", wav_file
                        continue

        before = after


continuous_wav_info_to_csv()
