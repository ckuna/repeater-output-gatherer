from telnetlib import Telnet
import threading
import os
import argparse
import time

CONST_PARSER = argparse.ArgumentParser(description='Open a telnet connection from\
                                                    client to server, and log output.')
CONST_PARSER.add_argument('ip', type=str, help='ip address of the remote host')
CONST_PARSER.add_argument('port', type=int, help='port of the remote host')
CONST_PARSER.add_argument('filename', type=str, help='filename of the output file')
CONST_ARGS = CONST_PARSER.parse_args()

CONST_IP = CONST_ARGS.ip
CONST_PORT = CONST_ARGS.port
CONST_FILENAME_BASE = CONST_ARGS.filename

#define the telnet worker thread
def telnet_worker():
    """The telnet worker-thread, opens a telnet connection and logs incoming data"""
    filename = CONST_FILENAME_BASE
    if os.path.exists(filename):
        os.remove(filename)
    try:
        client = Telnet(CONST_IP, CONST_PORT)
        data = ''
        client.write(('').encode('ascii'))
        cnt = 0
        while True:
            data = client.read_very_eager()
            if data != b'':
                with open(filename, 'a') as file:
                    file.write(str(data))
            time.sleep(.1)
            cnt += 1
            if cnt >= 100:
                client.write(('PONG').encode('ascii'))
                cnt = 0
    except IOError as err:
        print("An error ocurred writing to " + filename + "\n" + err)
        quit()
    except:
        with open(filename, 'a') as file:
            file.write('Connection closed.' + '\n')

# create threads as daemons, and do not close until an exception (ctrl+c) is thrown
t = threading.Thread(target=telnet_worker)
t.daemon = True
t.start()

while True:
    try:
        if not t.isAlive():
            print(t.name + " connection has closed.")
            quit()
        time.sleep(.1)
    except:
        quit()
