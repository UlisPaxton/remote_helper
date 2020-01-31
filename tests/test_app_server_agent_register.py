import requests
import os
import subprocess
import ifaddr

iplist = list()
adapters = ifaddr.get_adapters()
for adapter in adapters:
	for ip in adapter.ips:
		if type(ip.ip) == str and ip.ip != '127.0.0.1':
			iplist.append(ip.ip)

print(iplist)


subprocess.call(["taskkill","/f","/im","tvnserver.exe"])
requests.post(f"http://localhost/register_user_request",data={'username': os.environ['USERNAME'],'computername': os.environ['COMPUTERNAME'],'iplist': iplist})
#subprocess.call(['reg','import','\\\\print01\\Tig\\tig.reg'])
#subprocess.Popen(['\\\\print01\\Tig\\tvnserver.exe'])