
descriptor = open('registers.txt','r')
registers_lines = descriptor.readlines()

for line in registers_lines:
	splited_line = line.split(" ")
	request_link = splited_line[8]
	login = request_link.split("=")[1].split("&")[0]
	if login != 'donets' and login != 'bodyu_rv' and login !='testing':
		print(login)