import argparse
import struct
import os
import io
from scipy.io import wavfile
import shutil

DESCRIPTION = 'Input The path to the directory'
HELP = 'Input the path'
PARSER = argparse.ArgumentParser(description=DESCRIPTION)
PARSER.add_argument('-input_path', '--input_path', action='store', help=HELP)

RESULT = PARSER.parse_args()
PATH = RESULT.input_path
print PATH

os.chdir(PATH)

def missing_files():
	# to get missing files
	wav_file_list = []
	missing_element = []
	count1 = 0
	for wav_file in os.listdir(PATH):
	    if (wav_file[-3:] == 'wav') or (wav_file[-3:] == 'WAV'):
	    	character = wav_file[0:1]
	    	extension = wav_file[-4:]
	        wav_file_list.append(str(wav_file.rsplit(".", 1)[0]))

	filenames = [fname[1:] for fname in wav_file_list]
	print "No. files :", len(filenames)
	#print filenames
	filenames_toint = map(int, filenames)
	sorted_filenames = sorted(filenames_toint, reverse=False)

	for file_name in range(sorted_filenames[0], sorted_filenames[-1]+1):
	    if file_name not in sorted_filenames:
	        count1 += 1
	        missing_element.append(character+str(file_name) + extension)
	        
	print "Missing filenames :\n", missing_element
	print "No. files missing :", count1


def wav_header():
	count2 = 0
	# to get corrupt files
	for wav_file in os.listdir(PATH):
		try:
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

		        aformat, channels, samplerate, byterate, blockalign, bps = struct.unpack('HHIIHH', file_header_info.read(16))
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
	       
		        if os.path.getsize(wav_file) < samplerate*blockalign*10:
		            print "Corrupt file :", wav_file, "& filesize :", os.path.getsize(wav_file)
		            count2 += 1
		        else:
		            pass
		except struct.error:
			continue
	print "Total no.of corrupt files :", count2


def zero_data_check():
	# to check zero data files
	zero_data = []
	count3 = 0
	src = PATH
	dst = PATH+'/'+'zero_data'
	for each_wav_file in os.listdir(PATH):
		try:
		    if (each_wav_file[-3:] == 'wav') or (each_wav_file[-3:] == 'WAV'):
		        wavdata = wavfile.read(each_wav_file)[1]
		        # print "wavdata:",each_wav_file,"\n", wavdata
		        if wavdata.sum() == 0:
		            zero_data.append(each_wav_file)
		            count3 += 1
		            if not os.path.exists(dst):
		                os.makedirs(dst)
		                shutil.move(src +'/'+each_wav_file, dst)
		            else:
		                shutil.move(src +'/'+each_wav_file, dst)
		except ValueError:
			continue

	print "Zero data files :", zero_data
	print "Total no. zero data files :", count3

if __name__=='__main__':
	missing_files()
	wav_header()
	zero_data_check()
