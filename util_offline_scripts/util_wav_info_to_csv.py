import argparse
import glob
import os
import csv
import util_offline

DESCRIPTION = 'Input The path to the directory'
HELP = 'Input the path'
PARSER = argparse.ArgumentParser(description=DESCRIPTION)
PARSER.add_argument('-input_path', '--input_path', action='store', help='Input path to wav files')
PARSER.add_argument('-input_first_character', '--input_first_character', action='store', \
	help='Input required first character of the file name series')
PARSER.add_argument('-path_to_save_csv', '--path_to_save_csv', action='store', \
	help='Input path to save csv')

RESULT = PARSER.parse_args()
PATH = RESULT.input_path
PATH_2 = RESULT.path_to_save_csv
CHARACTER = RESULT.input_first_character
print "Given Path:", PATH
print "character:", CHARACTER
print "Given path to save CSV:", PATH_2

os.chdir(PATH)
files_list = glob.glob(str(CHARACTER)+'*')
# print "files:", files_list

def get_wavheader_extraheader_to_csv():

	wav_info_tags = ["Filename", "Operator", "DeviceID", "Battery_Voltage", "Battery_Percentage",\
	"Network_Status", "Network_Type", "Firmare_Revision", "Time_Stamp", "Latitude", "Longitude", \
	"Clock", "ChunkID", "TotalSize", "Format", "SubChunk1ID", "SubChunk1Size", "AudioFormat", \
	"NumChannels", "SampleRate", "ByteRate", "BlockAlign", "BitsPerSample", "SubChunk2ID", \
	"SubChunk2Size"]
	wav_info_tags2 = ["ChunkID", "TotalSize", "Format", "SubChunk1ID", "SubChunk1Size", \
	"AudioFormat", "NumChannels", "SampleRate", "ByteRate", "BlockAlign", \
	"BitsPerSample", "SubChunk2ID", "SubChunk2Size"]

	CSV_FILE_NAME = "wav_header_info.csv"
	print "CSV File name:", CSV_FILE_NAME
	with open(PATH_2 +'/'+ CSV_FILE_NAME, "w") as file_object:
		wav_information_object = csv.writer(file_object)
		wav_information_object.writerow(wav_info_tags)
		file_object.flush()
		# sorting files based on wav header timestamp
		sorted_wav_files_list = util_offline.sort_on_timestamp(files_list)

		# get wavheader and extraheader
		for each_wav_file in sorted_wav_files_list:
			if os.path.getsize(each_wav_file) > 264:
				wav_header, extra_header = util_offline.get_wavheader_extraheader(each_wav_file)
				blockalign = wav_header["BlockAlign"]
				samplerate = wav_header["SampleRate"]

				if util_offline.check_wav_file_size(each_wav_file, samplerate, blockalign):
					wav_header, extra_header = util_offline.get_wavheader_extraheader(each_wav_file)
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
	print "wav file information saved to CSV.."

if __name__ == '__main__':
	get_wavheader_extraheader_to_csv()
