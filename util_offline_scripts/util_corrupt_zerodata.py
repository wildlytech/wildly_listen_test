import argparse
import glob
import os
import shutil
import util_offline

DESCRIPTION = 'Input The path to the directory'
HELP = 'Input the path'
PARSER = argparse.ArgumentParser(description=DESCRIPTION)
PARSER.add_argument('-input_path', '--input_path', action='store', help='Input path to wav files')
PARSER.add_argument('-input_first_character', '--input_first_character', action='store', \
	help='Input required first character of the file name series')

RESULT = PARSER.parse_args()
PATH = RESULT.input_path
CHARACTER = RESULT.input_first_character
print "Path:", PATH
print "character:", CHARACTER

os.chdir(PATH)
files_list = glob.glob(str(CHARACTER)+'*')

def corrupt_zero_data():
	src = PATH
	zero_data_dst = PATH+'/'+'zero_data_files'
	corrupt_dst = PATH+'/'+'corrupt_files'
	for each_wav_file in files_list:
		if os.path.getsize(each_wav_file) > 264:
			wav_header, extra_header = util_offline.get_wavheader_extraheader(each_wav_file)
			blockalign = wav_header["BlockAlign"]
			samplerate = wav_header["SampleRate"]

			if util_offline.check_wav_file_size(each_wav_file, samplerate, blockalign):
				if util_offline.zero_data(each_wav_file):
					if not os.path.exists(zero_data_dst):
						os.makedirs(zero_data_dst)
						shutil.move(src +'/'+each_wav_file, zero_data_dst)
					else:
						shutil.move(src +'/'+each_wav_file, zero_data_dst)
			else:
				if not os.path.exists(corrupt_dst):
					os.makedirs(corrupt_dst)
					shutil.move(src +'/'+each_wav_file, corrupt_dst)
				else:
					shutil.move(src +'/'+each_wav_file, corrupt_dst)

	if not os.path.exists(corrupt_dst):
		corrupt_count = 0
	else:
		corrupt_count = len(os.listdir(corrupt_dst))

	if not os.path.exists(zero_data_dst):
		zero_data_count = 0
	else:
		zero_data_count = len(os.listdir(zero_data_dst))

	return corrupt_count, zero_data_count

if __name__ == '__main__':
	corrupt_count, zero_data_count = corrupt_zero_data()
	print "Corrupt files count:", corrupt_count
	print "Zero Data files count:", zero_data_count
