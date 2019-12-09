"""
Serial Command
"""
import subprocess
import serial
import argparse


# Listing all the ports
COMMAND_TO_LIST_PORT = "python -m serial.tools.list_ports"
PROCESS_PORT = subprocess.Popen(COMMAND_TO_LIST_PORT, stdout=subprocess.PIPE, shell=True)
RESULT_PORTS = PROCESS_PORT.communicate()[0]
print "Ports with Device(s): ", RESULT_PORTS
RESULT_PORTS = RESULT_PORTS.split("\n")[0].strip()

#Global define of serial communication object
SER = serial.Serial(RESULT_PORTS)


def get_query_result(command):
    """
    Sending the serial command and waiting till it outputs the information
    """
    SER.write(command)

    while True:
        if SER.inWaiting():
            print SER.read(SER.inWaiting())
            SER.flush()
            break


if __name__ == "__main__":
    while True:
        send = raw_input("Enter Command: ")
        get_query_result(send)


		