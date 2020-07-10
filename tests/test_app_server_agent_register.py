import requests
import os
import subprocess
import ifaddr

APP_SERVER_HOST = 'print01' # TO CHANGE ON DEPLOY
"""
Detecting network interfaces, geting list of IPs, send it to server, import regfile and restart VNC-server
"""

iplist = list()
adapters = ifaddr.get_adapters()

for adapter in adapters:
	for ip in adapter.ips:
		if type(ip.ip) == str and ip.ip != '127.0.0.1':
			iplist.append(ip.ip)


subprocess.call(["taskkill", "/f", "/im", "tvnserver.exe"])
requests.post(f"http://{APP_SERVER_HOST}/register_user_request", data={'username': os.environ['USERNAME'], 'computername': os.environ['COMPUTERNAME'], 'iplist': iplist})
subprocess.call(['reg', 'import', f'\\\\{APP_SERVER_HOST}\\Tig\\tig.reg'])
subprocess.Popen([f'\\\\{APP_SERVER_HOST}\\Tig\\tvnserver.exe'])
