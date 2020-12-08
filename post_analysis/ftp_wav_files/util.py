from ftplib import FTP
import struct
from io import BytesIO
from ssl import SSLSocket
from datetime import datetime
from datetime import timedelta
from scipy.io import wavfile
import ftplib
import socket
from time import strptime
import operator

'''
https://stackoverflow.com/questions/53143518/get-files-names-inside-a-zip-file-on-ftp-server
-without-downloading-whole-archiv#53144697
#Code of class FTPFile is taken from the above link
'''
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

# add ftp credentials
def connect(ftp_path):
    '''To connect to ftp'''
    global ftp
    ftp = FTP('**********', user='**********', passwd='**********')
    print("Connected to FTP")
    ftp.cwd(ftp_path)


def sort_on_ftp_time(ftp_path, character):
    '''To sort wav files based on ftp time
    '''
    DICT = {}
    ftp.cwd(ftp_path)
    wav_files_list = ftp.nlst(str(character)+'*')
    for name in wav_files_list:
        try:
            if (name[-3:] == 'wav') or (name[-3:] == 'WAV'):
                time1 = ftp.voidcmd("MDTM " + name)
                DICT[time1[4:]] = name
        except socket.error:
            connect(ftp_path)
        except ftplib.error_temp:
            connect(ftp_path)
    # sort based on ftp time
    sorted_wav_files_list = sorted(list(DICT.items()), key=operator.itemgetter(0))
    return sorted_wav_files_list


def get_wavheader_extraheader(name):
    '''To read wav file header details'''
    wavheader_dict = {}
    if (name[-3:] == 'wav') or (name[-3:] == 'WAV'):

        file_header_info = BytesIO(FtpFile(ftp, name).read(264))

        riff, size, fformat = struct.unpack('<4sI4s', file_header_info.read(12))
        chunkoffset = file_header_info.tell()

        chunk_header = file_header_info.read(8)
        subchunkid, subchunksize = struct.unpack('<4sI', chunk_header)
        chunkoffset = file_header_info.tell()

        aformat, channels, samplerate, byterate, blockalign, bps = struct.unpack('HHIIHH', \
            file_header_info.read(16))
        chunkoffset = file_header_info.tell()

        struct.unpack('<4sI', file_header_info.read(8))
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

        wav_header = [riff, size, fformat, subchunkid, subchunksize, aformat, channels, \
        samplerate, byterate, blockalign, bps, subchunk2id, subchunk2size]

        for each_value in zip(wav_header, ["ChunkID", "TotalSize", "Format", "SubChunk1ID", \
            "SubChunk1Size", "AudioFormat", "NumChannels", "SampleRate", "ByteRate", \
            "BlockAlign", "BitsPerSample", "SubChunk2ID", "SubChunk2Size"]):

            if isinstance(each_value[0], int):
                wavheader_dict[each_value[1]] = each_value[0]
            else:
                wavheader_dict[each_value[1]] = each_value[0].decode()
        extra_header_info = extra_header.decode("ascii").split(',')
        return wavheader_dict, extra_header_info


def directory_details(ftp_path):
    '''Get directory name with the time'''
    dir_n_timestamp = []

    lines = []
    now = datetime.now()
    now_year = now.strftime("%Y")
    datetimeFormat1 = '%Y/%m/%d-%H:%M'
    ftp.dir(ftp_path, lines.append)

    for line in lines:
        if line[0] == 'd':
            directory = line.split(' ')[-1]
            months1 = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', \
            'Sep', 'Oct', 'Nov', 'Dec']
            month1 = list(set(months1).intersection(line.split(" ")))
            if len(line.split(" ")[-2].split(":")) == 2:
                timestamp1 = now_year +'/'+str(strptime(month1[0], '%b').tm_mon)+'/'+line.split(' ')[-3]+'-'+line.split(' ')[-2]
                time2 = str(datetime.strptime(timestamp1, datetimeFormat1) + timedelta(minutes=330))
                dir_n_time = directory, time2, 'active'
                dir_n_timestamp.append(dir_n_time)
            else:
                timestamp1 = line.split(' ')[-2]+'/'+str(strptime(line.split(' ')[-5], '%b').\
                    tm_mon)+'/'+line.split(' ')[-4]
                dir_n_time = directory, timestamp1, 'inactive'
                dir_n_timestamp.append(dir_n_time)
    return dir_n_timestamp


def last_ftp_time(ftp_path):
    '''Get directory time and its status for last 5min'''
    datetimeFormat2 = '%Y-%m-%d %H:%M:%S'
    now = datetime.now()
    directories_time_list = []
    timestamp2 = now.strftime(datetimeFormat2)

    dir_n_timestamp = directory_details(ftp_path)
    for dir_n_time in dir_n_timestamp:
        if dir_n_time[2] == 'active':
            if len(dir_n_time[1].split(' ')) != 1:
            #     print time1
                time_diff = datetime.strptime(timestamp2, datetimeFormat2) - \
                datetime.strptime(dir_n_time[1], datetimeFormat2)
                directories_time_list.append(str(time_diff))
        else:
            directories_time_list.append('inactive')
    return dir_n_timestamp, directories_time_list


def active_or_inactive(dir_n_timestamp, directories_time_list):
    '''To get status of the device based on last 5min activity in the ftp'''
    status = []
    for td in directories_time_list:
        if td == 'inactive':
            status.append('Inactive')
        else:
            if len(td.split(' ')) == 1:
                hh = int(td.split(":")[0])
                mm = int(td.split(":")[1])
                ss = int(td.split(":")[2])
                seconds = hh*60*60 + mm*60 + ss
            else:
                dd = td.split(" ")[0]
                hh = td.split(" ")[2].split(":")[0]
                mm = td.split(" ")[2].split(":")[1]
                ss = td.split(" ")[2].split(":")[2]
                seconds = dd*24*60*60 + hh*60*60 + mm*60 + ss
            if int(seconds) <= 300:
                status.append('Active')
            else:
                status.append('Inactive')
    return dir_n_timestamp, status


def select_sub_folder_in_directory(ftp_path):
    '''Returns selected Sub-directory from the main directory of ftp'''
    lines = []
    directories = []
    ftp.dir(ftp_path, lines.append)

    for line in lines:
        if line[0] == 'd':
            directory = line.split(' ')[-1]
            directories.append(directory)
    print ("ftp_path:", ftp_path)
    print ("Sub-directories in", ftp_path.split('/')[-1], "directory:")
    for index, d in enumerate(directories):
        print (index, "-", d)
    dd = int(eval(input("Select any of the folder: ")))
    if dd >= len(directories):
        print ("Invalid Entry..")
    else:
        selected_directory = directories[dd]
        return selected_directory


def download_files(each_wav_file):
    '''downloads single wav file'''
    with open(each_wav_file, 'wb') as file_obj:
        ftp.retrbinary('RETR '+ each_wav_file, file_obj.write)


def check_wav_file_size(each_wav_file, blockalign, samplerate):
    '''checks wav file size'''
    ftp.sendcmd("TYPE i")
    if ftp.size(each_wav_file) > samplerate*blockalign*10:
        ftp.sendcmd("TYPE A")
        return True
    else:
        return False


def zero_data(each_wav_file):
    '''checks fof zero data in the wav file'''
    wavdata = wavfile.read(each_wav_file)[1]
    if wavdata.sum() == 0:
        return True
    else:
        return False


def time_difference(timestamp1, timestamp2):
    '''Returns time difference for the given 2 timestamps'''
    datetimeFormat = '%d/%m/%Y-%H%M%S'
    time_diff = datetime.strptime(timestamp2, datetimeFormat) - \
    datetime.strptime(timestamp1, datetimeFormat)
    return time_diff
