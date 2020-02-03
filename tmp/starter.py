# -*- coding:utf-8 -*-

from subprocess import call
from sys import argv
from time import sleep
import os

#call(['python'])
call(['python', 'C:\\tmp\\handler.py', argv[1]])
sleep(10)