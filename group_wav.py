""" code to group wav file """

import struct
from ftplib import FTP
from io import BytesIO
from ssl import SSLSocket
import argparse


DESCRIPTION = 'Input The path to the directory'
HELP = 'Input the path'
PARSER = argparse.ArgumentParser(description=DESCRIPTION)
PARSER.add_argument('-input_path', '--input_path', action='store',
                    help=HELP, default='/home/user-u0xzU/')

RESULT = PARSER.parse_args()
PRIMARY_PATH = "/home/user-u0xzU" + RESULT.input_path
print PRIMARY_PATH

'''https://stackoverflow.com/questions/53143518/get-files-names-inside-a-zip-file-on-ftp-server
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
	ftp = FTP('******', user='******', passwd='******')
	print "connected to FTP"
	ftp.cwd(PRIMARY_PATH)
	CURRENT_PATH = ftp.pwd()#assingn the current path to a variable y
	NAMES = ftp.nlst()#get the list of all files


def group_wav_files():
	''' function to group wav files
	'''

	count = 0#varible to keep the count of no.of files
	for name in NAMES:
		print name

		if (name[-3:] == 'wav') or (name[-3:] == 'WAV'):#check if the file is wav file only
			fh_1 = BytesIO(FtpFile(ftp, name).read(128))
			#Get the header of the wav file

			riff, size, fformat = struct.unpack('<4sI4s', fh_1.read(12))
			chunk_header = fh_1.read(8)
			subchunkid, subchunksize = struct.unpack('<4sI', chunk_header)
			aformat, channels, samplerate, byterate, blockalign, bps = struct.unpack('HHIIHH', fh_1.read(16))
			chunkoffset = fh_1.tell()
			fh_1.seek(chunkoffset)

			subchunk2id, subchunk2size = struct.unpack('<4sI', fh_1.read(8))

			listtype = struct.unpack('<4s', fh_1.read(4))

			listitemid, listitemsize = struct.unpack('<4sI', fh_1.read(8))
			listdata = fh_1.read(listitemsize)
			#read the Header that is added manually
			print " real information: %s " %(listdata.decode("ascii"))
			#split the list by :
			li_1 = listdata.decode("ascii").split(':')
			i = li_1.index('Operator')#get the index of operator
			print "This is Operator Name ::", li_1[i+1].split(',')[0]#print the operator name
			print "Device Id ::", li_1[i+2].split(',')[0]#get the device id

			device_id = li_1[i+2].split(',')[0]

			print name, device_id#Print the name of wav files and device id
			destination = CURRENT_PATH+"/"+device_id +"/"#Destination path
			print destination
			file_path_source = CURRENT_PATH + "/" + name
			print file_path_source
			if device_id not in ftp.nlst():
				#if the directory does not exist make a directory
				ftp.mkd(destination)
				#move the wav file to the destination direc
				ftp.rename(file_path_source, destination + "/" + name)
				count += 1
				print "directory created"
			else:
				#if the directory already exists just move the file to that directory
				ftp.rename(file_path_source, destination + "/" + name)
				count += 1
				print "No.of file moved ", count
if __name__ == '__main__':
	connect()
	group_wav_files()

