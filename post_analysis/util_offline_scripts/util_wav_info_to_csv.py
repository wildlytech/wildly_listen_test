import argparse
import os
import csv
from datetime import datetime
import pandas as pd
import util_offline

DESCRIPTION = 'Input The path to the directory'
HELP = 'Input the path'
PARSER = argparse.ArgumentParser(description=DESCRIPTION)
PARSER.add_argument('-input_path', '--input_path', action='store', help='Input path to wav files')
PARSER.add_argument('-path_to_save_csv', '--path_to_save_csv', action='store', \
	help='Input path to save csv')

RESULT = PARSER.parse_args()
PATH = RESULT.input_path
PATH_2 = RESULT.path_to_save_csv
print ("Given Path:", PATH)
print ("Given path to save CSV:", PATH_2)
os.chdir(PATH)


def get_wavheader_extraheader_to_csv():
	# csv is generated with details like header and extra header information and also time gaps
	wav_info_tags = ["Filename", "Operator", "DeviceID", "Battery_Voltage", "Battery_Percentage",\
	"Network_Status", "Network_Type", "Firmare_Revision", "Time_Stamp", "Latitude", "Longitude", \
	"Clock", "ChunkID", "TotalSize", "Format", "SubChunk1ID", "SubChunk1Size", "AudioFormat", \
	"NumChannels", "SampleRate", "ByteRate", "BlockAlign", "BitsPerSample", "SubChunk2ID", \
	"SubChunk2Size"]
	wav_info_tags2 = ["ChunkID", "TotalSize", "Format", "SubChunk1ID", "SubChunk1Size", \
	"AudioFormat", "NumChannels", "SampleRate", "ByteRate", "BlockAlign", \
	"BitsPerSample", "SubChunk2ID", "SubChunk2Size"]

	CSV_FILE_NAME = "sd_card_folders_wav_files_info.csv"
	print ("CSV File name:", CSV_FILE_NAME)
	with open(PATH_2 +'/'+ CSV_FILE_NAME, "w") as file_object:
		wav_information_object = csv.writer(file_object)
		wav_information_object.writerow(wav_info_tags)
		file_object.flush()
		files_list = util_offline.iter_over_folders(PATH)

		# sorting files
		sorted_wav_files_list = util_offline.sort_on_timestamp(files_list)
		# get wavheader and extraheader information
		for each_wav_file in sorted_wav_files_list:
			if os.path.getsize(each_wav_file) > 264:
				wav_header, extra_header = util_offline.get_wavheader_extraheader(each_wav_file)
				blockalign = wav_header["BlockAlign"]
				samplerate = wav_header["SampleRate"]

				if util_offline.check_wav_file_size(each_wav_file, samplerate, blockalign):
					wav_header, extra_header = util_offline.get_wavheader_extraheader(each_wav_file)
					each_wav_file = each_wav_file.split("/")[-1]
					information_value = [each_wav_file]
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
							information_value.append(corresponding_value)

					for tag in wav_info_tags2:
						value = wav_header[tag]
						information_value.append(value)
					wav_information_object.writerow(information_value)
					file_object.flush()

	csv_file_path = PATH_2 +'/'+ CSV_FILE_NAME
	# read csv generated and get Time_Stamp column and convert to list
	df = pd.read_csv(csv_file_path)
	list_of_time_stamps = df['Time_Stamp'].values.tolist()
	# get time difference of consecutive files timestamp and append to a list
	time_diff_sec = []
	for index, value in enumerate(list_of_time_stamps):
	    try:
	        datetimeFormat = '%Y/%m/%d-%H:%M:%S'
	        time_diff = datetime.strptime(list_of_time_stamps[index+1], datetimeFormat) - \
	        datetime.strptime(list_of_time_stamps[index], datetimeFormat)
	        time_diff2 = str(time_diff)
	        time_diff_sec.append(time_diff2)
	    except IndexError:
	        continue

	# get time gaps list and convert to seconds
	to_seconds = []
	to_seconds.append(0)
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
	# add seconds list to a separate column to the generated csv
	df['Time_Difference'] = to_seconds
	df.to_csv(csv_file_path, index=False)
	print("Wav files information saved to CSV file")

if __name__ == '__main__':
	get_wavheader_extraheader_to_csv()
