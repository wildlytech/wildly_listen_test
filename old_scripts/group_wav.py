""" code to group wav file """

import struct
from ftplib import FTP
from io import BytesIO
from ssl import SSLSocket
import argparse
import csv
import time

DESCRIPTION = 'Input The path to the directory'
HELP = 'Input the path'
PARSER = argparse.ArgumentParser(description=DESCRIPTION)
PARSER.add_argument('-input_path', '--input_path', action='store',
                    help=HELP)

RESULT = PARSER.parse_args()
PRIMARY_PATH = "/home/user-u0xzU" + RESULT.input_path

#####################################################
         # Define initial Gloabl Constant#
#####################################################
count = 0
name_of_devices = set()
initial_number_of_devices = 0
SLEEP_TIME = 120


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
    global ftp, CURRENT_PATH, NAMES
    ftp = FTP('*********', user='******', passwd='******')
    print "connected to FTP"
    ftp.cwd(PRIMARY_PATH)
    CURRENT_PATH = ftp.pwd()
    NAMES = ftp.nlst()


def group_wav_files():
    '''
    function to group wav files
    '''
    # varible to keep the count of no.of files
    global name_of_devices, count, initial_number_of_devices
    NAMES = ftp.nlst()

    for name in NAMES:
        # print name
        if (name[-3:] == 'wav') or (name[-3:] == 'WAV'):#check  if the file is wav file only
            file_header_info = BytesIO(FtpFile(ftp, name).read(264))

            # Get the header of the wav file
            riff, size, fformat = struct.unpack('<4sI4s', file_header_info.read(12))
            chunk_header = file_header_info.read(8)
            subchunkid, subchunksize = struct.unpack('<4sI', chunk_header)
            aformat, channels, samplerate, byterate, blockalign, bps = struct.unpack('HHIIHH', file_header_info.read(16))
            chunkoffset = file_header_info.tell()
            file_header_info.seek(chunkoffset)
            subchunk2id, subchunk2size = struct.unpack('<4sI', file_header_info.read(8))
            listtype = struct.unpack('<4s', file_header_info.read(4))
            listitemid, listitemsize = struct.unpack('<4sI', file_header_info.read(8))

            # Getting the wav information and writing the csv file rows
            listdata = file_header_info.read(200)
            # print "List data", listdata
            wav_information = listdata.decode("ascii").split(',')
            information_value = [name]
            for index_value, each_tag_value in enumerate(wav_information):
                try:
                    _, corresponding_value = each_tag_value.split(":")
                except ValueError:
                    corresponding_value = "".join(each_tag_value.split(":")[1:])
                if index_value == 1:
                    name_of_devices.add(corresponding_value)
                    # Switch to Binary mode
                    ftp.sendcmd("TYPE i")
                    # Get size of file
                    filesize = ftp.size(name)
                    # To switch back to ASCII
                    ftp.sendcmd("TYPE A")
                    if filesize < (samplerate*blockalign*10):
                        count += 1
                    else:
                        #moving files based on device ID
                        destination = CURRENT_PATH+"/"+corresponding_value +"/"
                        file_path_source = CURRENT_PATH + "/" + name
                        if corresponding_value not in ftp.nlst():
                            ftp.mkd(destination)
                            ftp.rename(file_path_source, destination + "/" + name)
                            count += 1
                        else:
                            ftp.rename(file_path_source, destination + "/" + name)
                            count += 1
                            print "No.of file moved ", count

            if len(name_of_devices) > initial_number_of_devices:
                print "New Device detected :", name_of_devices
                initial_number_of_devices = len(name_of_devices)

if __name__ == '__main__':
    connect()
    while(True):
        group_wav_files()
        print "Waiting for Files to Accumulate"
        time.sleep(SLEEP_TIME)

