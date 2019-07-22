import argparse
import struct
import os
import io
import csv

DESCRIPTION = 'Input The path to the directory'
HELP = "Give the Required Arguments"
PARSER = argparse.ArgumentParser(description=DESCRIPTION)
PARSER.add_argument('-input_path', '--input_path', action='store', help=HELP)
PARSER.add_argument('-path_to_save_csv', '--path_to_save_csv', action='store', \
    help='Input path to save csv')
PARSER.add_argument('-csv_file_name', '--csv_file_name', action='store', \
    help='Input csv file name', default='wav_file_information.csv')


RESULT = PARSER.parse_args()
PATH = RESULT.input_path
PATH_2 = RESULT.path_to_save_csv
CSV_FILE_NAME = RESULT.csv_file_name

print "Given path:", PATH
print "CSV saved to:", PATH_2
os.chdir(PATH)

def sort_files():
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
    # print "sorted_wavfiles:", sorted_wavfiles

    for sorted_file in sorted_wavfiles:
        wav_files_list.append(character + str(sorted_file) + extension)
    # print "wav_files_list :\n", wav_files_list

def wav_header(wav_files_list):
    wav_info_tags = ["Filename", "Operator", "DeviceID", "Battery_Voltage", "Battery_Percentage", \
    "Network_Status", "Network_Type", "Firmare_Revision", "Time_Stamp", "Latitude", "Longitude", \
    "ChunkID", "TotalSize", "Format", "SubChunk1ID", "SubChunk1Size", "AudioFormat", "NumChannels", \
    "SampleRate", "ByteRate", "BlockAlign", "BitsPerSample", "SubChunk2ID", "SubChunk2Size"]
        
    print "CSV File name:", CSV_FILE_NAME
    with open(PATH_2 +'/'+ CSV_FILE_NAME, "w") as file_object:
        wav_information_object = csv.writer(file_object)
        wav_information_object.writerow(wav_info_tags)
        file_object.flush()

        for wav_file in wav_files_list:
            try:
                if (wav_file[-3:] == 'wav') or (wav_file[-3:] == 'WAV'):
                    fileIn = open(wav_file, 'rb')
                    file_header_info = io.BytesIO(fileIn.read(264))

                    riff, size, fformat = struct.unpack('<4sI4s', file_header_info.read(12))
                    chunkoffset = file_header_info.tell()

                    chunk_header = file_header_info.read(8)
                    subchunkid, subchunksize = struct.unpack('<4sI', chunk_header)
                    chunkoffset = file_header_info.tell()

                    aformat, channels, samplerate, byterate, blockalign, bps = \
                    struct.unpack('HHIIHH', file_header_info.read(16))
                    chunkoffset = file_header_info.tell()

                    struct.unpack('<4sI', file_header_info.read(8))
                    struct.unpack('<4s4sI', file_header_info.read(12))
                    chunkoffset = file_header_info.tell()

                    extra_header = file_header_info.read(200)
                    chunkoffset = file_header_info.tell()

                    file_header_info.seek(chunkoffset)
                    subchunk2id, subchunk2size = struct.unpack('<4sI', file_header_info.read(8))
                    chunkoffset = file_header_info.tell()

                    wav_header = riff, size, fformat, subchunkid, subchunksize, aformat, \
                    channels, samplerate, byterate, blockalign, bps, subchunk2id, subchunk2size

                    #Getting the wav information and writing the csv file rows
                    wav_information = extra_header.decode("ascii").split(',')
                    information_value = [wav_file]
                    for index_value, each_tag_value in enumerate(wav_information):
                        try:
                            corresponding_tag, corresponding_value = each_tag_value.split(":")
        #                     print corresponding_tag
                            if corresponding_tag == " Signal":
                                corresponding_value = corresponding_value.split("-")
                                for signal_split in corresponding_value:
                                    information_value.append(signal_split)
                            else:
                                information_value.append(corresponding_value)
        #                         
                        except ValueError:
                            corresponding_value = ":".join(each_tag_value.split(":")[1:])
                            information_value.append(corresponding_value)

                    for info in wav_header:
                        information_value.append(info)    
                    wav_information_object.writerow(information_value)
                    file_object.flush()
            except struct.error:
                continue
    print "wav file header information saved to csv.."

if __name__=='__main__':
    wav_files_list = sort_files()
    wav_header(wav_files_list)