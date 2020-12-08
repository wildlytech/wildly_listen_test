import argparse
import os
import shutil
import util_offline

DESCRIPTION = 'Input the path to the directory'
HELP = 'Input the path'
PARSER = argparse.ArgumentParser(description=DESCRIPTION)
PARSER.add_argument('-input_path', '--input_path', action='store', help='Input path to wav files')

RESULT = PARSER.parse_args()
PATH = RESULT.input_path
print ("Path:", PATH)


def corrupt_zero_data():
	# corrupt files and zero data files will be moved their respective folders
	zero_data_dst = PATH+'/'+'zero_data_files'
	corrupt_dst = PATH+'/'+'corrupt_files'
	files_list = util_offline.iter_over_folders(PATH)
	for each_wav_file in files_list:
		try:
			# check for file size(primary check)
			if os.path.getsize(each_wav_file) > 264:
				wav_header, extra_header = util_offline.get_wavheader_extraheader(each_wav_file)
			else:
				print(each_wav_file)
				continue
		except TypeError:
			continue
		blockalign = wav_header["BlockAlign"]
		samplerate = wav_header["SampleRate"]
		# check for file size
		if util_offline.check_wav_file_size(each_wav_file, samplerate, blockalign):
			# create zero data folder and move zero data files
			if util_offline.zero_data(each_wav_file):
				if not os.path.exists(zero_data_dst):
					os.makedirs(zero_data_dst)
					shutil.move(each_wav_file, zero_data_dst)
				else:
					shutil.move(each_wav_file, zero_data_dst)
		else:
			# create corrupt folder and move corrupt data files
			if not os.path.exists(corrupt_dst):
				os.makedirs(corrupt_dst)
				shutil.move(each_wav_file, corrupt_dst)
			else:
				shutil.move(each_wav_file, corrupt_dst)

	# count number of corrupt files in corrupt folder
	if not os.path.exists(corrupt_dst):
		corrupt_count = 0
	else:
		corrupt_count = len(os.listdir(corrupt_dst))

	# count number of zero data files in corrzero data folder
	if not os.path.exists(zero_data_dst):
		zero_data_count = 0
	else:
		zero_data_count = len(os.listdir(zero_data_dst))

	return corrupt_count, zero_data_count

if __name__ == '__main__':
	corrupt_count1, zero_data_count1 = corrupt_zero_data()
	print ("Corrupt files count:", corrupt_count1)
	print ("Zero Data files count:", zero_data_count1)
