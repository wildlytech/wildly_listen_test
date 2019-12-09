import argparse
from ftplib import FTP
import struct
import os
import io
import csv
import socket
import ftplib
from datetime import datetime
import pandas as pd
import util

DESCRIPTION = 'Input The path to the directory'
HELP = 'Input the path'
PARSER = argparse.ArgumentParser(description=DESCRIPTION)
PARSER.add_argument('-input_path', '--input_path', action='store',
                    help=HELP)
PARSER.add_argument('-path_to_save_csv', '--path_to_save_csv', action='store', \
	help='Input path to save csv')
PARSER.add_argument('-input_first_character', '--input_first_character', action='store', \
    help='Input required first character of the file name series')

RESULT = PARSER.parse_args()
PRIMARY_PATH = "/home/user-u0xzU" + RESULT.input_path
PATH_2 = RESULT.path_to_save_csv
print "Given path to save CSV:", PATH_2
character = RESULT.input_first_character
print "Character:", character

CSV_FILE_NAME = "Transmitted_wav_files_info.csv"

def connect(PRIMARY_PATH):
    '''TO connect to ftp
    '''
    global ftp
    ftp = FTP('**********', user='**********', passwd='**********')
    print "connected to FTP"
    ftp.cwd(PRIMARY_PATH)


def wav_header_to_csv(PRIMARY_PATH, character):

	global wav_info_tags, wav_info_tags2
	# connect to ftp
	util.connect(PRIMARY_PATH)

	selected_dir = util.select_sub_folder_in_directory(PRIMARY_PATH)
	print "Selected Directory:", selected_dir
	if selected_dir == None:
		quit()
	else:
		PRIMARY_PATH2 = PRIMARY_PATH+selected_dir

	wav_info_tags = ["Filename", "Operator", "DeviceID", "Battery_Voltage", "Battery_Percentage",\
	"Network_Status", "Network_Type", "Firmare_Revision", "Time_Stamp", "Latitude", "Longitude", \
	"Clock", "ChunkID", "TotalSize", "Format", "SubChunk1ID", "SubChunk1Size", "AudioFormat", \
	"NumChannels", "SampleRate", "ByteRate", "BlockAlign", "BitsPerSample", "SubChunk2ID", \
	"SubChunk2Size", "Time_Difference"]
	wav_info_tags2 = ["ChunkID", "TotalSize", "Format", "SubChunk1ID", "SubChunk1Size", \
	"AudioFormat", "NumChannels", "SampleRate", "ByteRate", "BlockAlign", \
	"BitsPerSample", "SubChunk2ID", "SubChunk2Size"]

	print "CSV File name:", CSV_FILE_NAME
	with open(PATH_2 +'/'+ CSV_FILE_NAME, "w") as file_object:
		wav_information_object = csv.writer(file_object)
		wav_information_object.writerow(wav_info_tags)
		file_object.flush()
		# sort the wav files based on ftp time
		wav_files_list_with_timestamp = util.sort_on_ftp_time(PRIMARY_PATH2, character)
		sorted_wav_files_list = [element[1] for element in wav_files_list_with_timestamp]

		for wav_file in sorted_wav_files_list:
			try:
				# get wavheader and extraheader information
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

				for tag in wav_info_tags2:
					value = wav_header[tag]
					information_value.append(value)
				# read the csv into a dataframe and get Time_Stamp column to a list
				df = pd.read_csv(PATH_2 +'/'+ CSV_FILE_NAME)
				list_of_time_stamps = df['Time_Stamp'].values.tolist()

				if len(list_of_time_stamps) == 0:
				    information_value.append(str(0))
				else:
					# get time difference of consecutive file's timestamp
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
					    seconds = dd*24*60*60 + hh*60*60 + mm*60 + ss
					information_value.append(seconds)


				wav_information_object.writerow(information_value)
				file_object.flush()
			except socket.error:
				util.connect(PRIMARY_PATH)
			except ftplib.error_temp:
				util.connect(PRIMARY_PATH)
			except struct.error:
				print "File size error, file name:", wav_file
				continue
	return PRIMARY_PATH2

if __name__ == '__main__':
	connect(PRIMARY_PATH)
	wav_header_to_csv(PRIMARY_PATH, character)
