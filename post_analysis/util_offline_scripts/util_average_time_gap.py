import argparse
import struct
from datetime import datetime
import numpy
import util_offline

DESCRIPTION = 'Input The path to the directory'
HELP = 'Input the path'
PARSER = argparse.ArgumentParser(description=DESCRIPTION)
PARSER.add_argument('-input_path', '--input_path', action='store', help='Input path to wav files')
RESULT = PARSER.parse_args()
PATH = RESULT.input_path
print "Path:", PATH


def average_time_gap():
	# get average time gap and also minimum and maximum time gaps
	wavfiles_list = []
	files_list = util_offline.iter_over_folders(PATH)
	# sorting files
	sorted_wav_files_list = util_offline.sort_on_timestamp(files_list)

	# get wavheader and extraheader information
	for each_wav_file in sorted_wav_files_list:
		try:
			wav_header, extra_header = util_offline.get_wavheader_extraheader(each_wav_file)
			blockalign = wav_header["BlockAlign"]
			samplerate = wav_header["SampleRate"]

			if util_offline.check_wav_file_size(each_wav_file, samplerate, blockalign):
				for index_value, each_tag_value in enumerate(extra_header):
					timestamp_tag = extra_header[index_value].split(":", 1)[0]
					if timestamp_tag == ' Timestamp':
						timestamp_value = extra_header[index_value].split(":", 1)[1]
						wavfiles_list.append((each_wav_file, str(timestamp_value)))
		except struct.error:
			print "struct.error:", each_wav_file
			continue

	sorted_timestamp_list = [element[1] for element in wavfiles_list]

	# get time difference of consecutive files timestamp and append to a list
	time_diff_sec = []
	for index, value in enumerate(sorted_timestamp_list):
		try:
			# datetimeFormat = '%Y%m%d%H%M%S'
			datetimeFormat = '%Y/%m/%d-%H:%M:%S'

			time_diff = datetime.strptime(sorted_timestamp_list[index+1], \
				datetimeFormat) - datetime.strptime(sorted_timestamp_list[index], datetimeFormat)
			time_diff2 = str(time_diff)
			time_diff_sec.append(time_diff2)
		except IndexError:
			continue

	# get time gaps list and convert to seconds and append to a list
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

	average_time = numpy.average(to_seconds).round(3)
	min_max = min(to_seconds), max(to_seconds)

	return average_time, min_max

if __name__ == '__main__':
	average_time1, min_max1 = average_time_gap()
	print "Average time:", average_time1, "sec",
	print "\nMin :", min_max1[0], "sec, Max :", min_max1[1], "sec"
