import argparse
import struct
import os
import io

DESCRIPTION = 'Input The path to the directory'
HELP = 'Input the path'
PARSER = argparse.ArgumentParser(description=DESCRIPTION)
PARSER.add_argument('-input_path', '--input_path', action='store', help=HELP)

RESULT = PARSER.parse_args()
PATH = RESULT.input_path
print PATH

os.chdir(PATH)

def sort_wav_files(PATH):
    only_wavfiles = []
    wav_files_list = []

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
    return wav_files_list
    
def wav_header_info(wav_files_list):
    count = 0
    wavfiles_list = []
    for wav_file in wav_files_list:
        try:
            fileIn = open(PATH+'/'+wav_file, 'rb')
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

            if os.path.getsize(wav_file) == samplerate*blockalign*10 + 264:
                time_stamp2 = extra_header.split(",")[-3]
                count += 1
                device_id = extra_header.split(",")[-8]
                wavfiles_list.append((wav_file,time_stamp2))
            else:
                pass
        except struct.error:
            continue

#     print "wavfiles_list:\n",wavfiles_list
    print "No. of wav files:", count
    print device_id
    print '\nFirst Element:- ', wavfiles_list[0]
    print 'Last Element:- ', wavfiles_list[-1]
    

if __name__ == '__main__':
    wav_files_list = sort_wav_files(PATH)
    wav_header_info(wav_files_list)