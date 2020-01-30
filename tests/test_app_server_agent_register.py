import requests
import os
import subprocess

requests.get(f"http://print01/register_user_request?username={os.environ['USERNAME']}&computername={os.environ['COMPUTERNAME']}")
subprocess.call(['reg','import','\\\\print01\\Tig\\tig.reg'])
subprocess.call(['\\\\print01\\Tig\\tvnserver.exe'])