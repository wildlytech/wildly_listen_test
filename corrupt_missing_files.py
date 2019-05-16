from ftplib import FTP
import struct
from io import BytesIO
from ssl import SSLSocket
import argparse

DESCRIPTION = 'Input The path to the directory'
HELP = 'Input the path'
PARSER = argparse.ArgumentParser(description=DESCRIPTION)
PARSER.add_argument('-input_path', '--input_path', action='store', help=HELP)

RESULT = PARSER.parse_args()
PRIMARY_PATH = "/home/user-u0xzU" + RESULT.input_path
print PRIMARY_PATH

LETTER = 'D*'
character = LETTER[0]

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
    '''TO connect to ftp
    '''
    global ftp, CURRENT_DIR
    ftp = FTP('*********', user='*********', passwd='*********')
    print "connected to FTP"
    CURRENT_DIR = ftp.cwd(PRIMARY_PATH)
    names = ftp.nlst(LETTER)
    print "Total no.of files :", len(names)



def corrupt_files():
    '''to count the total no.of corrupt files
    '''
    names = ftp.nlst(LETTER)
    count = 0

    for name in names:
        try:
            if (name[-3:] == 'wav') or (name[-3:] == 'WAV'):
                fin = BytesIO(FtpFile(ftp, name).read(44))
                # First four bytes are ChunkID which must be "RIFF" in ASCII
                chunkid = fin.read(4)
        
                # Total Size of File in Bytes - 8 Bytes
                chunksizestring = fin.read(4)
                # 'I' Format is to to treat the 4 bytes as unsigned 32-bit interger
                chunksize = struct.unpack('I', chunksizestring)
                # The subscript is used because struct unpack returns everything as tuple
                totalsize = chunksize[0]+8
    
                # This is the number of bytes of data
                datasize = totalsize-124

                # "WAVE" in ASCII
                format_1 = fin.read(4)

                # "fmt " in ASCII
                subchunk1id = fin.read(4)

                # Should be 16 (PCM, Pulse Code Modulation)
                subchunk1sizestring = fin.read(4)
                # 'I' format to treat as unsigned 32-bit integer
                subchunk1size = struct.unpack("I", subchunk1sizestring)

                # Should be 1 (PCM)
                audioformatstring = fin.read(2)
                # 'H' format to treat as unsigned 16-bit integer
                audioformat = struct.unpack("H", audioformatstring)

                # Should be 1 for mono, 2 for stereo
                numchannelsstring = fin.read(2)
                # 'H' unsigned 16-bit integer
                numchannels = struct.unpack("H", numchannelsstring)

                # Should be 44100 (CD sampling rate)
                sampleratestring = fin.read(4)
                samplerate = struct.unpack("I", sampleratestring)

                # 44100*NumChan*2 (88200 - Mono, 176400 - Stereo)
                byteratestring = fin.read(4)
                # 'I' unsigned 32 bit integer
                byterate = struct.unpack("I", byteratestring)

                # NumChan*2 (2 - Mono, 4 - Stereo)
                blockalignstring = fin.read(2)
                # 'H' unsigned 16-bit integer
                blockalign = struct.unpack("H", blockalignstring)

                # 16 (CD has 16-bits per sample for each channel)
                bitspersamplestring = fin.read(2)
                # 'H' unsigned 16-bit integer
                bitspersample = struct.unpack("H", bitspersamplestring)
        
                # "data" in ASCII
                subchunk2id = fin.read(4)
                # Number of Data Bytes, Same as DataSize
                subchunk2sizestring = fin.read(4)
                subchunk2size = struct.unpack("I", subchunk2sizestring)
                time = datasize/byterate[0]
                
                # Switch to Binary mode
                ftp.sendcmd("TYPE i")
                # Get size of file
                filesize = ftp.size(name)
                # To switch back to ASCII
                ftp.sendcmd("TYPE A")
                if filesize < (samplerate[0]*blockalign[0]*10):
                    print "Corrupt file :", name, "& filesize :", filesize
                    count += 1
                else:
                    pass
        except:
            connect()

    print "Total no.of corrupt files :", count

def missing_files():
    ''' to check for missing file names
    '''
    missing_element = []
    count = 0
    names = ftp.nlst(LETTER)
    filenames = [fname[1:7] for fname in names]
    filenames_toint = map(int, filenames)
    sorted_filenames = sorted(filenames_toint, reverse=False)
    for file_name in range(sorted_filenames[0], sorted_filenames[-1]+1):
        if file_name not in sorted_filenames:
            count += 1
            missing_element.append(character + str(file_name) + '.wav')
        
    print "Missing filenames :\n", missing_element
    print "No. files missing :", count

if __name__ == '__main__':
    connect()
    corrupt_files()
    missing_files()