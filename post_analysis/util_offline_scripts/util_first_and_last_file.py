import argparse
import struct
import util_offline

DESCRIPTION = 'Input The path to the directory'
HELP = 'Input the path'
PARSER = argparse.ArgumentParser(description=DESCRIPTION)
PARSER.add_argument('-input_path', '--input_path', action='store', help='Input path to wav files')

RESULT = PARSER.parse_args()
PATH = RESULT.input_path
print "Path:", PATH


def first_and_last_modified_files():
	# get first and last file with time
	wavfiles_list = []
	files_list = util_offline.iter_over_folders(PATH)
	# sort wav files
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
			continue

	first_and_last_modified_files1 = wavfiles_list[0], wavfiles_list[-1]
	return first_and_last_modified_files1


if __name__ == '__main__':
	first_and_last_modified_files2 = first_and_last_modified_files()
	print "First file:", first_and_last_modified_files2[0]
	print " Last file:", first_and_last_modified_files2[-1]
