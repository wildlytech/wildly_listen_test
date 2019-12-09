""" wav header and extra information is saved to csv """

import struct
from ftplib import FTP
from io import BytesIO
from ssl import SSLSocket
import argparse
import csv

DESCRIPTION = 'Input The path to the directory'
HELP = 'Input the path'
PARSER = argparse.ArgumentParser(description=DESCRIPTION)
PARSER.add_argument('-input_path', '--input_path', action='store',
                    help=HELP)

RESULT = PARSER.parse_args()
PRIMARY_PATH = "/home/user-u0xzU" + RESULT.input_path

'''
Code is copied from the below link
https://stackoverflow.com/questions/53143518/get-files-names-inside-a-zip-file-on-ftp-server
-without-downloading-whole-archiv#53144697'''
#Code of class FTPFile is taken from the above link

#A class used to read wav header files
class FtpFile:
    """ sdfsg """

    def __init__(self, ftp, name):
        self.ftp = ftp
        self.name = name
        self.size = 10240
        self.pos = 0

    def seek(self, offset, whence):
        if whence == 0:
            self.pos = offset
        if whence == 1:
            self.pos += offset
        if whence == 2:
            self.pos = self.size + offset

    def tell(self):
        return self.pos

    def read(self, size= None):
        if size == None:
            size = self.size - self.pos
        data = B""

        # based on FTP.retrbinarys
        # (but allows stopping after certain number of bytes read)
        ftp.voidcmd('TYPE I')
        cmd = "RETR {}".format(self.name)
        conn = ftp.transfercmd(cmd, self.pos)
        try:
            while len(data) < size:
                buf = conn.recv(min(size - len(data), 8192))
                if not buf:
                    break
                data += buf
            # shutdown ssl layer (can be removed if not using TLS/SSL)
            if SSLSocket is not None and isinstance(conn, SSLSocket):
                conn.unwrap()
        finally:
            conn.close()
        try:
            ftp.voidresp()
        except:
            pass
        self.pos += len(data)
        return data

#To connect to FTP server
def connect():
    ''' TO connect to ftp server
	'''
    global ftp, CURRENT_PATH, NAMES, directory_name
    ftp = FTP('*********', user='********', passwd='********')
    print "connected to FTP"
    ftp.cwd(PRIMARY_PATH)
    CURRENT_PATH = ftp.pwd()
    NAMES = ftp.nlst()

def wav_info_to_csv():
    '''
    To save wav files details to csv of a directory
    '''
    wav_info_tags = ["Filename", "Operator", "DeviceID", "Battery_Voltage", "Battery_Percentage",
                     "Network_status", "Firmare_Revision", "Time_Stamp", "Latitude", "Longitude",
                     "ChunkID", "TotalSize", "Format", "SubChunk1ID", "SubChunk1Size",
                     "AudioFormat", "NumChannels", "SampleRate", "ByteRate", "BlockAlign",
                     "BitsPerSample", "SubChunk2ID", "SubChunk2Size"]
    initial_number_of_devices = 0
    count = 0
    DICT = {}
    wav_file_name = "wav_file_extra_information_"+CURRENT_PATH.split("/")[-1]+".csv"
    print wav_file_name
    with open(wav_file_name, "w") as file_object:
        wav_information_object = csv.writer(file_object)
        wav_information_object.writerow(wav_info_tags)
        file_object.flush()

        for name in NAMES:
            if (name[-3:] == 'wav') or (name[-3:] == 'WAV'):
                time1 = ftp.voidcmd("MDTM " + name)
                count += 1
                DICT[name] = time1[4:]
        sorted_wav_files_list = sorted((value,key) for (key,value) in DICT.items())
        sorted_file_name_list = [element[1] for element in sorted_wav_files_list]

        for name in sorted_file_name_list:
            if (name[-3:] == 'wav') or (name[-3:] == 'WAV'):

                file_header_info = BytesIO(FtpFile(ftp, name).read(264))

                riff, size, fformat = struct.unpack('<4sI4s', file_header_info.read(12))
                chunkoffset = file_header_info.tell()

                chunk_header = file_header_info.read(8)
                subchunkid, subchunksize = struct.unpack('<4sI', chunk_header)
                chunkoffset = file_header_info.tell()

                aformat, channels, samplerate, byterate, blockalign, bps = struct.unpack('HHIIHH', file_header_info.read(16))
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
                information_value = [name]
                for index_value, each_tag_value in enumerate(wav_information):
                    try:
                        _, corresponding_value = each_tag_value.split(":")
                    except ValueError:
                        corresponding_value = "".join(each_tag_value.split(":")[1:])
                    information_value.append(corresponding_value)
                for info in wav_header:
                    information_value.append(info)    
                wav_information_object.writerow(information_value)
                file_object.flush()
        print "wav file information saved to csv.."

if __name__ == '__main__':
    connect()
    wav_info_to_csv()