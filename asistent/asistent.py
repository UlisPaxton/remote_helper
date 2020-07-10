import requests
import os
import subprocess
import ifaddr

APP_SERVER_HOST = 'print01'    # !!!!! ИСПРАВИТЬ ПРИ РАЗВЕРТЫВАНИИ

iplist = list()
adapters = ifaddr.get_adapters()

for adapter in adapters:
    """ Получаем сетевые адаптеры с ПК, формируем список адресов, сключаем петлю 127.0.0.1"""
    for ip in adapter.ips:
        if type(ip.ip) == str and ip.ip != '127.0.0.1':
            iplist.append(ip.ip)

try:
    subprocess.call(["taskkill", "/f", "/im", "tvnserver.exe"])
    requests.post(f"http://{APP_SERVER_HOST}/register_user_request",
                  data={'username': os.environ['USERNAME'],
                        'computername': os.environ['COMPUTERNAME'],
                        'iplist': iplist,
                        }
                  )
    subprocess.call(['reg', 'import', f'\\\\{APP_SERVER_HOST}\\Tig\\tig.reg'])
    subprocess.Popen([f'\\\\{APP_SERVER_HOST}\\Tig\\tvnserver.exe'])

except:
    """Пользователь не должен видеть исключение"""
    exit()
