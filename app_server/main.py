import cherrypy
from jinja2 import Environment, FileSystemLoader
import requests
from time import sleep
from pdb import set_trace as d
import os
from threading import Thread
import logging


logging.basicConfig(filename='helper.log',filemode='a',format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
					datefmt='%H:%M:%S',level=logging.DEBUG)

current_dir = os.path.dirname(os.path.abspath(__file__))
env = Environment(loader=FileSystemLoader('templates'))
glpi_ip = '192.168.112.112'
request_old = 5

def old_cheker():
	while True:
		sleep(10)
		for user_request in User_Request.request_list:
	
			if user_request.old > request_old:
				logging.info(f"Removing request {user_request.computername} {user_request.username}")
				User_Request.request_list.remove(user_request)

			else:
				user_request.old += 1


class Agent:   # class deprecated
	agent_list = list()

	def __init__(self, username, ip):
		self.ip = ip
		self.name = username
		Agent.agent_list.append(self)
		self.status = 'Registred'
		self.update = 0
	
	def __str__ (self):
		return 'Agent:' + self.ip + ', Status' + self.status

class User_Request():
	request_list = list()
	def __init__(self, username, computername, iplist):
		self.computername = computername
		self.username = username
		self.glpi_link = "http://{}/glpi/front/computer.php?is_deleted=0&as_map=0&criteria%5B0%5D%5Blink%5D=AND&criteria%5B0%5D%5Bfield%5D=1&criteria%5B0%5D%5Bsearchtype%5D=contains&criteria%5B0%5D%5Bvalue%5D={}&search=%D0%9F%D0%BE%D0%B8%D1%81%D0%BA&itemtype=Computer&start=0".format(glpi_ip, self.computername)
		self.status = "new"
		self.ip = iplist
		self.old = 0
		User_Request.request_list.append(self)

class Root:

	@cherrypy.expose
	def index(self):
		tmpl = env.get_template('userlist.html')
		print(len(Agent.agent_list))
		return tmpl.render(title='Запросы юзверей',request_list=User_Request.request_list)

	@cherrypy.expose
	def register_user_request(self,username,computername,iplist):
		#ip = cherrypy.request.remote.ip
		#print("Agent {} registred from {}".format(username, ip))
		User_Request(username, computername, iplist)

	@cherrypy.expose
	def connect(self):
		pass

	def error_page_404(status, message, traceback, version):
		return "404 Error!"
	
	def setstatus(self, username, status):											# status: 0 - connected, 1 - wait connect
		for agent in Agent.agent_list:
			if agent.name == username and agent.ip == cherrypy.request.remote.ip:
				agent.status = status



cherrypy.config.update({'error_page.404': Root.error_page_404})
cherrypy.config.update({'server.socket_host': '0.0.0.0',
						'server.socket_port': 80,
						})
conf = {'/images': {'tools.staticdir.on': True,
                      'tools.staticdir.dir': os.path.join(current_dir, 'images')}}
#checker_Thread = Thread(target=old_cheker).start()
#checker_Thread.join()
cherrypy.quickstart(Root(),'/',config=conf)