'''To get average, maximum and minimum time taken to upload files to FTP server
'''

from ftplib import FTP
from datetime import datetime
import argparse
import numpy
from matplotlib import pyplot as plt


DESCRIPTION = 'Input The path to the directory'
HELP = 'Input the path'
PARSER = argparse.ArgumentParser(description=DESCRIPTION)
PARSER.add_argument('-input_path', '--input_path', action='store', help=HELP)

RESULT = PARSER.parse_args()
PRIMARY_PATH = "/home/user-u0xzU" + RESULT.input_path
print PRIMARY_PATH

def connect():
    '''TO connect to ftp
    '''
    global ftp, CURRENT_DIR
    ftp = FTP('********', user='********', passwd='********')
    print "connected to FTP"
    CURRENT_DIR = ftp.cwd(PRIMARY_PATH)

def average_min_max():
	'''To get average, maximum and minimum time taken to upload files to FTP server
	'''
	DICT = {}
	count = 0
	names = ftp.nlst()
	for name in names:
		try:
			if (name[-3:] == 'wav') or (name[-3:] == 'WAV'):
				# returns last uploaded file's time with utc
				time1 = ftp.voidcmd("MDTM " + name)
        		count += 1
       			DICT[name] = time1[4:]
		except:
			connect()		
	sorted_list = sorted((value, key) for (key, value) in DICT.items())
	sorted_list_timestamp = [element[0] for element in sorted_list]

	time_diff_sec = []
	for index, value in enumerate(sorted_list_timestamp):
		try:
			datetimeFormat = '%Y%m%d%H%M%S'
			time_diff = datetime.strptime(sorted_list_timestamp[index+1], \
				datetimeFormat) - datetime.strptime(sorted_list_timestamp[index], datetimeFormat)
			time_diff2 = str(time_diff)
			time_diff_sec.append(time_diff2)
		except IndexError: 
			break

	to_seconds = []
	for tt in time_diff_sec:
		h = int(tt[0:1])
		m = int(tt[2:4])
		s = int(tt[5:7])
		seconds = h*60*60 + m*60 + s
		to_seconds.append(seconds)

    # print "Time Difference list :\n", to_seconds
	print "Number of files :", count
	print "Average time:", numpy.average(to_seconds).round(2), "sec",
	print "\nMax :", max(to_seconds), "sec, Min :", min(to_seconds), "sec"
	# plt.boxplot(to_seconds)
	# plt.show()

if __name__ == '__main__':
	connect()
	average_min_max()