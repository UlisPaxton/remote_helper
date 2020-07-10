# -*- coding:utf-8 -*-

from sys import argv
from time import sleep
import subprocess
from configparser import ConfigParser
import os

current_path = os.getcwd()

if os.path.exists(current_path + '\\StarterConfig.ini'):
    parser = ConfigParser()
    parser.read(current_path + '\\StarterConfig.ini')

    targets = argv[1].split('//')
    target_app = targets[0][16:-1]
    target_ip = targets[1]

    if target_app == "ping":
        command = parser.get('ping', 'start_file').split(',')
        command.append(target_ip)
        subprocess.call(command)

    elif target_app == "vnc":
        command = [parser.get('vnc', 'start_file'), "-host=" + target_ip, '-password=' + parser.get('vnc', 'password')]
        subprocess.Popen(command)
        sleep(50)

    elif target_app == "rdp":
        subprocess.Popen(["mstsc.exe", "/v:" + target_ip])

    elif target_app == "ssh":
        subprocess.Popen(["ssh.exe", target_ip])

else:
    print('No config file found.')
    sleep(20)
    exit()
