import requests
import os
import subprocess

subprocess.call(["taskkill","/f","/im","tvnserver.exe"])
requests.get(f"http://print01/register_user_request?username={os.environ['USERNAME']}&computername={os.environ['COMPUTERNAME']}")
subprocess.call(['reg','import','\\\\print01\\Tig\\tig.reg'])
subprocess.Popen(['\\\\print01\\Tig\\tvnserver.exe'])