"""
Fast PortScanner tool
operates on ports 1-100
"""

import sys
import socket
from datetime import datetime
import re
import threading


# Checking Input
ip_syntax = re.compile(r'^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})$')

if re.match(ip_syntax, sys.argv[1]):
    globals()['ip'] = sys.argv[1]
elif sys.argv[1]:
    try:
        globals()['ip'] = socket.gethostbyname(sys.argv[1])
    except socket.gaierror:
        print('target hostname was not found')
        sys.exit()
else:
    print('\nIP is not valid. Exiting')
    print('argument syntax: X.X.X.X')
    sys.exit()

# threading list
threads = []


# scan function
def scan(target, port, file):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        con = s.connect((target, port))
        file.write('Port {} is OPEN!\n'.format(port))
        con.close()

    except Exception as res:
        string = 'port ' + str(port) + " => " + res.__str__() + '\n'
        file.write(string)
    s.close()


# scan loop , output to a file
with open('scan_result.txt', 'a') as f:
    # pretty banner
    f.write('-' * 50 + '\n')
    f.write('Started ' + str(datetime.now()) + '\n')
    f.write('scanning target {} ...\n'.format(ip))
    f.write('-' * 50 + '\n')

    for x in range(1, 101, 1):
        t = threading.Thread(target=scan, args=[ip, x, f])
        threads.append(t)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    
sys.exit()  # End the process

# improvements to make:
# 1) order of the threads (maybe order the results , like in dictionary?)
# 2) comments , better names for variables
# 3) option = set port range?
# 4) settimeout() , problematic or useful?

