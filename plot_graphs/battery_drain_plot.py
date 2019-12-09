''' plot the graph for battery percentage from csv '''
import pandas as pd
import matplotlib.pyplot as plt
from mpldatacursor import datacursor
import glob
import os
import argparse


DESCRIPTION = 'Input The path to the CSV files'
HELP = 'Input the path'
PARSER = argparse.ArgumentParser(description=DESCRIPTION)
PARSER.add_argument('-input_csv_path', '--input_csv_path', action='store', \
    help='Input path for CSV files')

RESULT = PARSER.parse_args()
PATH = RESULT.input_csv_path
print "Given path to csv files:", PATH

os.chdir(PATH)

width_in_inches = 13
height_in_inches = 7.5
dots_per_inch = 180

plt.figure(figsize=(width_in_inches, height_in_inches), dpi=dots_per_inch)

def battery_drain_plot(csv):
    # read csv and get battery percentage column
	df = pd.read_csv(csv)
	list_of_battery_percentage = df['Battery_Percentage'].values.tolist()
	print 'Length of list_of_battery_percentage:', len(list_of_battery_percentage)
	return list_of_battery_percentage


########################################################################################


# add all csv present in the given path
csv_files = glob.glob(PATH + "/*.csv")
print "No. of CSV files:", len(csv_files)
# print "CSV file(s):", csv_files

for csv_file in csv_files:
	list_of_battery_percentage1 = battery_drain_plot(csv_file)
	plt.plot(list_of_battery_percentage1, label=str(csv_file.split('/')[-1]), linewidth=2.5)
	# plt.plot(list_of_battery_percentage1, label="Battery")
	datacursor(formatter='Files: {x:.0f}, Battery: {y:.0f}'.format)
	plt.ylim(0, 100)
	# plt.xlim(1,1600)

plt.xlabel('Number of files')
plt.ylabel('Percentage')
plt.title('Battery Percentage')
plt.legend()
plt.show()
