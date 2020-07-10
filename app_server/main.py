import cherrypy
import os
from threading import Thread
import logging
from jinja2 import Environment, FileSystemLoader
from time import sleep, ctime

logging.basicConfig(filename='helper.log', filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S', level=logging.DEBUG)

current_dir = os.path.dirname(os.path.abspath(__file__))
env = Environment(loader=FileSystemLoader('templates'))

OLDER_LINER = 2


class UserRequest:
    """
    Класс - структура юзерского запроса для отображения в web-интерфейсе
    """
    request_list = list()

    def __init__(self, username, computername, iplist):
        self.computername = computername
        self.username = username
        self.status = "new"
        self.ip = iplist
        self.old = 0
        self.request_time = ctime()
        UserRequest.request_list.append(self)

    @staticmethod
    def old_checker(interval=180):
        """
        Функция проверяет возраст объектов каждые interval сек, возраст измеряется в количестве проверок
        если оюъект устарел, то удаляется.
        """
        while True:
            sleep(interval)
            for user_request in __class__.request_list:

                if user_request.old > OLDER_LINER:
                    logging.info(f"Removing request {user_request.computername} {user_request.username}")
                    __class__.request_list.remove(user_request)

                else:
                    user_request.old += 1


class Root:

    @cherrypy.expose
    def index(self):
        """
        вэб-роут для адреса index, основоной админский интерфейс, шаблон userlist.html

        """
        tmpl = env.get_template('userlist.html')

        return tmpl.render(title='Запросы юзерей', request_list=UserRequest.request_list)

    @cherrypy.expose
    def register_user_request(self, username, computername, iplist):
        """
        вэб-роут для приёма данных о компах юзеров от помошника, данные приходят в POST
        """

        if type(iplist) == str:
            """ если пришла строка, а не список, то лучше обернуть её в список"""
            ips = list()
            ips.append(iplist)
            UserRequest(username, computername, ips)
        else:
            UserRequest(username, computername, iplist)



    def default(self):
        """ Обработчик ошибки 404"""
        return "404 Page not Found!"
    default.exposed = True

    @cherrypy.expose
    def log(self, max_pages_to_show=500):
        """Вэброут для страницы чтения логов, читаем файл и переворачиваем,
         чтобы видеть сначала свежие логи. 500 строк обычно достаточно"""

        tmpl = env.get_template('log.html')
        f = open('helper.log', 'r')
        lines = f.readlines()
        lines.reverse()
        f.close()
        return tmpl.render(title='Логи', log_list=lines[0:int(max_pages_to_show)])


cherrypy.config.update({'server.socket_host': '0.0.0.0',
                        'server.socket_port': 80,
                        })
conf = {'/css':
            {'tools.staticdir.on': True,
             'tools.staticdir.dir': os.path.join(current_dir, 'css')},
        '/images': {'tools.staticdir.on': True,
                    'tools.staticdir.dir': os.path.join(current_dir, 'images')}}


checker_Thread = Thread(target=UserRequest.old_checker).start()
cherrypy.quickstart(Root(), '/', config=conf)
