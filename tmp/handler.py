# -*- coding:utf-8 -*-

from sys import argv
from time import sleep
import subprocess
from configparser import ConfigParser
import os


current_path = os.getcwd()
#print(current_path)
if os.path.exists(current_path + '\\StarterConfig.ini'):

	parser = ConfigParser()
	parser.read(current_path + '\\StarterConfig.ini')
else:
	print('No config file found.')
	sleep(0)
	exit()
#print(parser.get('vnc','password'))

if len(argv) < 2:
	#print('[-]',argv,' Ошибка в количестве параметров')
	sleep(0)
	exit()

targets = argv[1].split('//')
target_app = targets[0][16:-1]
target_ip = targets[1]

if target_app == "ping":
	
	command = parser.get('ping','start_file').split(',')
	command.append(target_ip)
	subprocess.call(command)
	

elif target_app == "vnc":
	try:
		command = [parser.get('vnc','start_file'), "-host="+target_ip,'-password='+ parser.get('vnc','password')]
		print(command)
		subprocess.Popen(command)
		
		sleep(50)
	except KeyboardInterrupt:
		exit()

elif target_app == "rdp":
	try:
		subprocess.Popen(["mstsc.exe","/v:"+target_ip])
	except KeyboardInterrupt:
		exit()
elif target_app == "ssh":
	try:
		subprocess.Popen(["ssh.exe",target_ip])
	except KeyboardInterrupt:
		exit()





