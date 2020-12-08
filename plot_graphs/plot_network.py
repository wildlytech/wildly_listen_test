''' plot the graph for network status from csv '''
import pandas as pd
import os
import glob
import matplotlib.pyplot as plt
import math
from mpldatacursor import datacursor
import argparse

DESCRIPTION = 'Input The path to the CSV files'
HELP = 'Input the path'
PARSER = argparse.ArgumentParser(description=DESCRIPTION)
PARSER.add_argument('-input_csv_path', '--input_csv_path', action='store', \
    help='Input path for CSV files')

RESULT = PARSER.parse_args()
PATH = RESULT.input_csv_path
print("Given path to csv files:", PATH)

os.chdir(PATH)

width_in_inches = 13
height_in_inches = 7.5
dots_per_inch = 180
plt.figure(figsize=(width_in_inches, height_in_inches), dpi=dots_per_inch)


def plot_network(csv):
	# read csv and get network status column
    df = pd.read_csv(csv)
    new_df = df[['Network_Status']]
    batt_list = new_df['Network_Status'].values.tolist()
    return batt_list


# get all the csv files present in the given path
csv_files = glob.glob(PATH + "/*.csv")
print("No. of CSV files:", len(csv_files))
print("CSV file(s):", csv_files)

for csv_file in csv_files:
    files_count1 = plot_network(csv_file)
    plt.plot(files_count1, '+', label=str(csv_file.split('/')[-1]), linewidth=2.0)
    datacursor(formatter='Files: {x:.0f}, Network strength: {y:.0f}'.format)
#     plt.ylim(1,100)
#     plt.xlim(100, 1)
plt.xlabel('No. of files')
plt.ylabel('Network strength')
plt.title('Signal strength Vs Files')
plt.legend()
plt.show()
