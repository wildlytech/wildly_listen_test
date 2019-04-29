''' to read details of wav file
'''
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
                    help=HELP, default='/home/user-u0xzU/')

RESULT = PARSER.parse_args()
PRIMARY_PATH = "/home/user-u0xzU" + RESULT.input_path
print PRIMARY_PATH

'''https://stackoverflow.com/questions/53143518/get-files-names-inside-a-zip-file-on-ftp-server
-without-downloading-whole-archiv#53144697
'''
#Code of class FTPFile is taken from the above link
class FtpFile:
    """ Class to download only header files """

    def __init__(self, ftp, name):
        self.ftp = ftp
        self.name = name
        self.size = 44
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

    def read(self, size=None):
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

def connect():
	'''To connect to FTP server
	'''
	global ftp, Y, destination
	ftp = FTP('******', user='******', passwd='******')
	print "connected to FTP"
	ftp.cwd(PRIMARY_PATH)
	Y = ftp.pwd()
	destination = Y+"/"+"corrupt/"
	ftp.mkd(destination)
	print destination


def read_wav_file():
	''' To read the details of wav_file
	'''
	names = ftp.nlst()
	# open(fname,mode) is the Python way of reading files 32-40

	#code to read wavf was taken from http://pythonaudio.blogspot.com/2014/04/3-reading-wave-file.html
	with open('wav_file_detailes.csv', 'wb') as myfile:
	    wr_1 = csv.writer(myfile)
	    wr_1.writerow(['Name', 'ChunkID', 'TotalSize', 'DataSize', 'Format', 'SubChunk1ID',
                  		'SubChunk1Size', 'AudioFormat', 'NumChannels', 'SampleRate', 'ByteRate',
                  		'BlockAlign', 'BitsPerSample', 'SubChunk2ID', 'SubChunk2Size', 'Time duration'])
	    for name in names:
			if (name[-3:] == 'wav') or (name[-3:] == 'WAV'):

				fin = BytesIO(FtpFile(ftp, name).read(44))
				# First four bytes are ChunkID which must be "RIFF" in ASCII
				chunkid = fin.read(4)
				print("ChunkID=", chunkid)

				# Total Size of File in Bytes - 8 Bytes
				chunksizestring = fin.read(4)
				# 'I' Format is to to treat the 4 bytes as unsigned 32-bit interger
				chunksize = struct.unpack('I', chunksizestring)
				# The subscript is used because struct unpack returns everything as tuple
				totalsize = chunksize[0]+8


				print("TotalSize=", totalsize)
				# This is the number of bytes of data
				datasize = totalsize-124


				print("DataSize=", datasize)
				# "WAVE" in ASCII
				format_1 = fin.read(4)
				print("Format=", format_1)

				# "fmt " in ASCII
				subchunk1id = fin.read(4)
				print("SubChunk1ID=", subchunk1id)

				 # Should be 16 (PCM, Pulse Code Modulation)
				subchunk1sizestring = fin.read(4)
				 # 'I' format to treat as unsigned 32-bit integer
				subchunk1size = struct.unpack("I", subchunk1sizestring)
				print "SubChunk1Size=", subchunk1size[0]

				# Should be 1 (PCM)
				audioformatstring = fin.read(2)
				# 'H' format to treat as unsigned 16-bit integer
				audioformat = struct.unpack("H", audioformatstring)
				print("AudioFormat=", audioformat[0])

				# Should be 1 for mono, 2 for stereo
				numchannelsstring = fin.read(2)
				 # 'H' unsigned 16-bit integer
				numchannels = struct.unpack("H", numchannelsstring)
				print("NumChannels=", numchannels[0])

				# Should be 44100 (CD sampling rate)
				sampleratestring = fin.read(4)
				samplerate = struct.unpack("I", sampleratestring)
				print("SampleRate=", samplerate[0])

				# 44100*NumChan*2 (88200 - Mono, 176400 - Stereo)
				byteratestring = fin.read(4)
				# 'I' unsigned 32 bit integer
				byterate = struct.unpack("I", byteratestring)
				print("ByteRate=", byterate[0])

				# NumChan*2 (2 - Mono, 4 - Stereo)
				blockalignstring = fin.read(2)
				 # 'H' unsigned 16-bit integer
				blockalign = struct.unpack("H", blockalignstring)
				print("BlockAlign=", blockalign[0])

				# 16 (CD has 16-bits per sample for each channel)
				bitspersamplestring = fin.read(2)
				# 'H' unsigned 16-bit integer
				bitspersample = struct.unpack("H", bitspersamplestring)
				print("BitsPerSample=", bitspersample[0])
				# "data" in ASCII
				subchunk2id = fin.read(4)
				print("SubChunk2ID=", subchunk2id)
				# Number of Data Bytes, Same as DataSize
				subchunk2sizestring = fin.read(4)
				subchunk2size = struct.unpack("I", subchunk2sizestring)
				print("SubChunk2Size=", subchunk2size[0])

				time = datasize/byterate[0]
				print "Time duration = ", time
				wr_1.writerow([name, chunkid, totalsize, datasize, format_1, subchunk1id, subchunk1size[0],
                 		audioformat[0], numchannels[0], samplerate[0], byterate[0], blockalign[0],
                 		bitspersample[0], subchunk2id, subchunk2size[0], time])

				file_path_source = Y + "/" + name
				flag = 0

				#Block Alignment = (Channels) * (BytesPerSample)
				#check if the Block Aling is fine
				if (numchannels[0]*(bitspersample[0]/8)) == blockalign[0]:
					print "Block align is fine"
				else:
					print "Error in block align"
					ftp.rename(file_path_source, destination + "/" + name)
					flag = 1
				if flag == 0:
					if (blockalign[0]*samplerate[0]) == byterate[0]:
						print "Byte rate is fine"
					else:
						print "error in Byte Rate"
						ftp.rename(file_path_source, destination + "/" + name)
				#fileSize = (bitsPerSample * samplesPerSecond * channels * duration) / 8;

				fin.close()


if __name__ == '__main__':
	connect()
	read_wav_file()

