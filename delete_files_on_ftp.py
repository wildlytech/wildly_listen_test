from ftplib import FTP
import argparse

DESCRIPTION = 'Input The path to the directory'
HELP = 'Input the path'
PARSER = argparse.ArgumentParser(description=DESCRIPTION)
PARSER.add_argument('-input_path', '--input_path', action='store', help='Input path to wav files')
PARSER.add_argument('-input_first_character', '--input_first_character', action='store', \
	help='Input required first character of the file name series')

RESULT = PARSER.parse_args()
PRIMARY_PATH = "/home/user-u0xzU" + RESULT.input_path
CHARACTER = RESULT.input_first_character
print "Path:", PRIMARY_PATH
print "character:", CHARACTER

def connect():
	'''TO connect to ftp
	'''
	global ftp
	ftp = FTP('***********', user='**********', passwd='***********')
	print "connected to FTP"
	ftp.cwd(PRIMARY_PATH)
	# ftp_files = ftp.nlst()

def delete():
	files_list = ftp.nlst(str(CHARACTER)+'*')
	count = 0
	# delete files in dir
	print "Deleting files.."
	for f in files_list:
	    try:
	        count += 1
	        ftp.delete(f)
	    except:
	        connect()
	print "No. of files deleted:", count
	print "Finished deleting files.."

connect()
delete()
