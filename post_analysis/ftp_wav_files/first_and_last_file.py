import argparse
from datetime import datetime
from datetime import timedelta
from ftplib import FTP
import operator
import ftplib
import util

DESCRIPTION = 'Input The path to the directory'
HELP = 'Input the path'
PARSER = argparse.ArgumentParser(description=DESCRIPTION)
PARSER.add_argument('-input_path', '--input_path', action='store',
                    help=HELP)
PARSER.add_argument('-input_first_character', '--input_first_character', action='store', \
    help='Input required first character of the file name series')

RESULT = PARSER.parse_args()
PRIMARY_PATH = "/home/user-u0xzU" + RESULT.input_path
character = RESULT.input_first_character
print "Character:", character


def connect():
	'''To connect to ftp'''
	global ftp
	ftp = FTP('**********', user='**********', passwd='**********')
	print "connected to FTP"
	ftp.cwd(PRIMARY_PATH)


def first_and_last_modified():
	'''Returns first and last file with timestamp'''
	util.connect(PRIMARY_PATH)
	selected_dir = util.select_sub_folder_in_directory(PRIMARY_PATH)
	print "Selected Directory:", selected_dir
	if selected_dir == None:
		quit()
	else:
		PRIMARY_PATH2 = PRIMARY_PATH+'/'+selected_dir
		# sort files
		wav_files_list_with_timestamp = util.sort_on_ftp_time(PRIMARY_PATH2, character)

		# first and last file
		datetimeFormat = '%Y%m%d%H%M%S'
		first_file1 = wav_files_list_with_timestamp[0][1]
		first_time1 = datetime.strptime(wav_files_list_with_timestamp[0][0], \
			datetimeFormat) + timedelta(minutes=330)

		last_file2 = wav_files_list_with_timestamp[-1][1]
		last_time2 = datetime.strptime(wav_files_list_with_timestamp[-1][0], \
			datetimeFormat) + timedelta(minutes=330)

		first_file_with_datetime = first_file1, str(first_time1)
		last_file_with_datetime = last_file2, str(last_time2)

		return first_file_with_datetime, last_file_with_datetime

if __name__ == '__main__':
	# connect()
	first_file, last_file = first_and_last_modified()
	print "First file, Date and time:", first_file
	print "Last file, Date and time:", last_file
