import argparse
from datetime import datetime
import numpy
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


def average_upload_time():
	'''Get minimum, maximum and average time difference'''
	util.connect(PRIMARY_PATH)

	selected_dir = util.select_sub_folder_in_directory(PRIMARY_PATH)
	print "Selected Directory:", selected_dir
	if selected_dir == None:
		quit()
	else:
		PRIMARY_PATH2 = PRIMARY_PATH+'/'+selected_dir

	# sort wav files
	wav_files_list_with_timestamp = util.sort_on_ftp_time(PRIMARY_PATH2, character)
	sorted_timestamp_list = [element[0] for element in wav_files_list_with_timestamp]

	# append time difference to list
	time_diff_sec = []
	for index, value in enumerate(sorted_timestamp_list):
		try:
			datetimeFormat = '%Y%m%d%H%M%S'
			time_diff = datetime.strptime(sorted_timestamp_list[index+1], \
				datetimeFormat) - datetime.strptime(sorted_timestamp_list[index], datetimeFormat)
			time_diff2 = str(time_diff)
			time_diff_sec.append(time_diff2)
		except IndexError:
			break

	# convert the time difference to seconds and append to a list
	to_seconds = []
	for td in time_diff_sec:
	    if len(td.split(' ')) == 1:
	        hh = int(td.split(":")[0])
	        mm = int(td.split(":")[1])
	        ss = int(td.split(":")[2])
	        seconds = hh*60*60 + mm*60 + ss
	        to_seconds.append(seconds)
	    else:
			dd = int(td.split(" ")[0])
			hh = int(td.split(" ")[2].split(":")[0])
			mm = int(td.split(" ")[2].split(":")[1])
			ss = int(td.split(" ")[2].split(":")[2])
			seconds = dd*24*60*60 + hh*60*60 + mm*60 + ss
			to_seconds.append(seconds)

	# getting minimum, maximum and average from seconds list
	average_time1 = numpy.average(to_seconds).round(3)
	min_max1 = min(to_seconds), max(to_seconds)

	return average_time1, min_max1

if __name__ == '__main__':
	average_time, min_max = average_upload_time()
	print "Average time:", average_time, "sec",
	print "\nMin :", min_max[0], "sec, Max :", min_max[1], "sec"
