import argparse
import struct
import os
import io
from datetime import datetime
import numpy


DESCRIPTION = 'Input The path to the directory'
HELP = 'Input the path'
PARSER = argparse.ArgumentParser(description=DESCRIPTION)
PARSER.add_argument('-input_path', '--input_path', action='store', help=HELP)

RESULT = PARSER.parse_args()
PATH = RESULT.input_path
print PATH

os.chdir(PATH)

only_wavfiles = []
wav_files_list = []
timestamp_list = []

for name in os.listdir(PATH):
    if (name[-3:] == 'wav') or (name[-3:] == 'WAV'):
        character = name[0:1]
        extension = name[-4:]
        only_wavfiles.append(name)
        wav_files = [e[1:-4] for e in only_wavfiles]
wav_files_toint = map(int, wav_files)
sorted_wavfiles = sorted(wav_files_toint)

for sorted_file in sorted_wavfiles:
    wav_files_list.append(character + str(sorted_file) + extension)
# print "wav_files_list :\n", wav_files_list


for wav_file in wav_files_list:
    try:
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

        time_stamp2 = [extra_header.split(",")[-3]]
        timestamp_list.append(time_stamp2[0][11:])
    except struct.error:
        continue

print "No. of wav files:", len(only_wavfiles)
# print "timestamp_list:", timestamp_list

time_diff_sec = []
for index, value in enumerate(timestamp_list):
    try:
        datetimeFormat = '%d/%m/%Y-%H:%M:%S'
        time_diff = datetime.strptime(timestamp_list[index+1], datetimeFormat) - datetime.strptime(timestamp_list[index],datetimeFormat)
        time_diff2 = str(time_diff)
        time_diff_sec.append(time_diff2)
    except IndexError: 
        continue
# print "\nDiff :", time_diff_sec

to_seconds = []
for td in time_diff_sec:
    hh = int(td.split(":")[0])
    mm = int(td.split(":")[1])
    ss = int(td.split(":")[2])
    seconds = hh*60*60 + mm*60 + ss
    to_seconds.append(seconds)

# print "Time Difference list :\n", to_seconds
print "Average time:", numpy.average(to_seconds).round(2), "seconds",
print "\nMax :", max(to_seconds), "sec, Min :", min(to_seconds), "sec"