import struct
import os
import io
import operator
from scipy.io import wavfile


def sort_wav_files(files_list):
	only_wavfiles = []
	wav_files_list = []

	for name in files_list:
		if (name[-3:] == 'wav') or (name[-3:] == 'WAV'):
			character = name[0:1]
			extension = name[-4:]
			only_wavfiles.append(name)
			wav_files = [e[1:-4] for e in only_wavfiles]
	wav_files_toint = map(int, wav_files)
	sorted_wavfiles = sorted(wav_files_toint)
	# print "sorted_wavfiles:", sorted_wavfiles

	for sorted_file in sorted_wavfiles:
		wav_files_list.append(character + str(sorted_file) + extension)
	# print "wav_files_list :\n", wav_files_list
	return wav_files_list


def get_wavheader_extraheader(wav_file):
	wavheader_dict = {}
	wavfiles_list = []
	if (wav_file[-3:] == 'wav') or (wav_file[-3:] == 'WAV'):
		fileIn = open(wav_file, 'rb')
		file_header_info = io.BytesIO(fileIn.read(264))

		# Get the header of the wav file
		riff, size, fformat = struct.unpack('<4sI4s', file_header_info.read(12))
		chunkoffset = file_header_info.tell()
		#     print "chunkoffset :", chunkoffset

		chunk_header = file_header_info.read(8)
		subchunkid, subchunksize = struct.unpack('<4sI', chunk_header)

		chunkoffset = file_header_info.tell()
		#     print "chunkoffset :", chunkoffset

		aformat, channels, samplerate, byterate, blockalign, bps = \
		struct.unpack('HHIIHH', file_header_info.read(16))
		chunkoffset = file_header_info.tell()
		#     print "chunkoffset :", chunkoffset

		struct.unpack('<4sI', file_header_info.read(8))
		chunkoffset = file_header_info.tell()
		#     print "chunkoffset :", chunkoffset

		struct.unpack('<4s4sI', file_header_info.read(12))
		chunkoffset = file_header_info.tell()
		#     print "chunkoffset :", chunkoffset

		extra_header = file_header_info.read(200)
		chunkoffset = file_header_info.tell()
		#     print "chunkoffset :", chunkoffset

		file_header_info.seek(chunkoffset)
		subchunk2id, subchunk2size = struct.unpack('<4sI', file_header_info.read(8))
		chunkoffset = file_header_info.tell()
		#     print "chunkoffset :", chunkoffset

		wav_header = riff, size, fformat, subchunkid, subchunksize, aformat, \
		channels, samplerate, byterate, blockalign, bps, subchunk2id, subchunk2size

		for each_value in zip(wav_header, ["ChunkID", "TotalSize", "Format", "SubChunk1ID", \
			"SubChunk1Size", "AudioFormat", "NumChannels", "SampleRate", "ByteRate", \
			"BlockAlign", "BitsPerSample", "SubChunk2ID", "SubChunk2Size"]):
			wavheader_dict[each_value[1]] = each_value[0]

		extra_header_info = extra_header.decode("ascii").split(',')

	return wavheader_dict, extra_header_info


def sort_on_timestamp(wav_files_list):
	DICT1 = {}
	for each_wav_file in wav_files_list:
		if os.path.getsize(each_wav_file) > 264:
			wav_header, extra_header = get_wavheader_extraheader(each_wav_file)
			for index_value, each_tag_value in enumerate(extra_header):
				timestamp_tag = extra_header[index_value].split(":", 1)[0]
				if timestamp_tag == ' Timestamp':
					timestamp_value = extra_header[index_value].split(":", 1)[1]
					DICT1[timestamp_value] = each_wav_file
	# sort based timestamp time
	sorted_wav_files_list = sorted(DICT1.items(), key=operator.itemgetter(0))
	# get wav file names from the sorted list
	files_list = [element[1] for element in sorted_wav_files_list]
	return files_list


def missing_files(wav_files_list):
	# to get missing files
	wav_file_list = []
	missing_element = []
	for wav_file in wav_files_list:
	    if (wav_file[-3:] == 'wav') or (wav_file[-3:] == 'WAV'):
	    	character = wav_file[0:1]
	    	extension = wav_file[-4:]
	        wav_file_list.append(str(wav_file.rsplit(".", 1)[0]))

	filenames = [fname[1:] for fname in wav_file_list]
	filenames_toint = map(int, filenames)
	sorted_filenames = sorted(filenames_toint, reverse=False)

	for file_name in range(sorted_filenames[0], sorted_filenames[-1]+1):
	    if file_name not in sorted_filenames:
	        missing_element.append(character+str(file_name) + extension)
	total_files = len(wav_file_list)
	missing_element_count =  len(missing_element) 

	return missing_element, missing_element_count, total_files


def check_wav_file_size(wav_file, samplerate, blockalign):
	if os.path.getsize(wav_file) > samplerate*blockalign*10:
		return True
	else:
		return False


def zero_data(each_wav_file):
	wavdata = wavfile.read(each_wav_file)[1]
	if wavdata.sum() == 0:
		return True
	else:
		return False
