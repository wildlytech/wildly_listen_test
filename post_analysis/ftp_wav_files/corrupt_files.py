import argparse
from ftplib import FTP
import socket
import ftplib
import struct
import util

DESCRIPTION = 'Input The path to the directory'
HELP = 'Input the path'
PARSER = argparse.ArgumentParser(description=DESCRIPTION)
PARSER.add_argument('-input_path', '--input_path', action='store', help=HELP)

PARSER.add_argument('-input_first_character', '--input_first_character', action='store', \
    help='Input required first character of the file name series')

RESULT = PARSER.parse_args()
PRIMARY_PATH = "/home/user-u0xzU" + RESULT.input_path
character = RESULT.input_first_character
print ("Character:", character)


def connect():
	'''TO connect to ftp
	'''
	global ftp
	ftp = FTP('**********', user='**********', passwd='**********')
	print ("connected to FTP")
	ftp.cwd(PRIMARY_PATH)


def corrupt_files():
	# connect to ftp
	util.connect(PRIMARY_PATH)
	global sorted_files_list
	#sort wav files
	wav_files_list_with_timestamp = util.sort_on_ftp_time(PRIMARY_PATH, character)
	sorted_files_list = [element[1] for element in wav_files_list_with_timestamp]
	# print sorted_files_list

	connect()
	if 'CorruptFiles' in ftp.nlst():
		pass
	else:
		ftp.mkd('CorruptFiles')
	#reading wav header
	wav_file_list = []
	for wav_file in sorted_files_list:
		try:
			wav_header, extra_header = util.get_wavheader_extraheader(wav_file)
			blockalign = wav_header["BlockAlign"]
			samplerate = wav_header["SampleRate"]

			# check for wav file size
			if util.check_wav_file_size(wav_file, blockalign, samplerate):
				pass
			else:
				wav_file_list.append(wav_file)
				ftp.rename(PRIMARY_PATH+wav_file, PRIMARY_PATH+'CorruptFiles/'+wav_file)
		except socket.error:
			util.connect(PRIMARY_PATH)
		except ftplib.error_temp:
			util.connect(PRIMARY_PATH)
		except struct.error:
			util.connect(PRIMARY_PATH)

	connect()
	ftp.cwd(PRIMARY_PATH+'CorruptFiles')
	corrupt_count = ftp.nlst()
	print ("Corrupt files:", corrupt_count)
	print ("No. of corrupt files moved:", len(corrupt_count))


if __name__ == '__main__':
	connect()
	corrupt_files()
