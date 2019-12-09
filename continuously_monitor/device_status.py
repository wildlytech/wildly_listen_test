'''To know the device status for the last 5min
   Returns the device id, last time and status for the given FTP directory
'''
import sys
sys.path.insert(0, '../post_analysis/ftp_wav_files/')
import util
import argparse

DESCRIPTION = 'Input The path to the directory'
HELP = 'Input the FTP directory'
PARSER = argparse.ArgumentParser(description=DESCRIPTION)
PARSER.add_argument('-input_path', '--input_path', action='store', help=HELP)
RESULT = PARSER.parse_args()
PRIMARY_PATH = "/home/user-u0xzU" + RESULT.input_path
ftp_dir = RESULT.input_path

util.connect(PRIMARY_PATH)


dir_n_timestamp, directories_time_list = util.last_ftp_time(PRIMARY_PATH)

dir_n_timestamp, status = util.active_or_inactive(dir_n_timestamp, directories_time_list)

print "FTP Directory:", ftp_dir
for device_id, status in map(None, dir_n_timestamp, status):
    print "\nDevice ID:", device_id[0], ", Status:", status, ", Last Time:", device_id[1]
