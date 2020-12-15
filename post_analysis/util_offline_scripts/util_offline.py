import struct
import os
import io
import operator
import glob
from scipy.io import wavfile
import numpy as np


def get_wavheader_extraheader(wav_file):
    # get wav header and extra header information
    wavheader_dict = {}
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

        extra_header = file_header_info.read(180)
        chunkoffset = file_header_info.tell()

        struct.unpack('<4sI', file_header_info.read(8))
        struct.unpack('<4s4sI', file_header_info.read(12))
        chunkoffset = file_header_info.tell()

        file_header_info.seek(chunkoffset)
        subchunk2id, subchunk2size = struct.unpack('<4sI', file_header_info.read(8))
        chunkoffset = file_header_info.tell()

        wav_header = riff, size, fformat, subchunkid, subchunksize, aformat, \
        channels, samplerate, byterate, blockalign, bps, subchunk2id, subchunk2size

        for each_value in zip(wav_header, ["ChunkID", "TotalSize", "Format", "SubChunk1ID", \
            "SubChunk1Size", "AudioFormat", "NumChannels", "SampleRate", "ByteRate", \
            "BlockAlign", "BitsPerSample", "SubChunk2ID", "SubChunk2Size"]):

            if isinstance(each_value[0], int):
                wavheader_dict[each_value[1]] = each_value[0]
            else:
                wavheader_dict[each_value[1]] = each_value[0].decode()
        extra_header_info = extra_header.decode("ascii").split(',')

    return wavheader_dict, extra_header_info


def sort_on_timestamp(wav_files_list):
    # sort wav files on timestamp
    DICT1 = {}
    for each_wav_file in wav_files_list:
        try:
            if (each_wav_file[-3:] == 'wav') or (each_wav_file[-3:] == 'WAV'):
                if os.path.getsize(each_wav_file) > 264:
                    wav_header, extra_header = get_wavheader_extraheader(each_wav_file)
                    for index_value, each_tag_value in enumerate(extra_header):
                        timestamp_tag = extra_header[index_value].split(":", 1)[0]
                        if timestamp_tag == ' Timestamp':
                            timestamp_value = extra_header[index_value].split(":", 1)[1]
                            DICT1[timestamp_value] = each_wav_file
        except TypeError:
            # print "TypeError:", each_wav_file
            continue
        except UnicodeDecodeError:
            # print "UnicodeDecodeError:", each_wav_file
            continue
        except IOError:
            # print "IOError:", each_wav_file
            continue
    # sort based timestamp time
    sorted_wav_files_list = sorted(list(DICT1.items()), key=operator.itemgetter(0))
    # get wav file names from the sorted list
    files_list = [element[1] for element in sorted_wav_files_list]
    return files_list


def iter_over_folders(PATH):
    # iterate over the folders and return the files list with absolute path
    files_with_path = []
    folders = glob.glob(PATH + "/D*")
    print ("No. of Folders:", len(folders))
    for folder in folders:
        files_with_path.append(glob.glob(folder+'/'+'*.wav'))
    file_list1 = np.concatenate(files_with_path).ravel().tolist()
    print ("No. of files:", len(file_list1))
    return file_list1


def check_wav_file_size(wav_file, samplerate, blockalign):
    # check for wav file size
    if os.path.getsize(wav_file) > samplerate*blockalign*10:
        return True
    else:
        return False


def zero_data(each_wav_file):
    # check for zero date in wav files
    wavdata = wavfile.read(each_wav_file)[1]
    if wavdata.sum() == 0:
        return True
    else:
        return False
