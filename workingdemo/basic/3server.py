from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from os import curdir, sep
import urlparse, pickle, os
p = 'htmlsnips/'
nofile = 'Bud, I can\'t find the file.'
def makePage():
	if not os.path.isfile('login.html'):
		try:
			with open(p+'header.xml', 'r') as h, open(p+'login.xml','r') as i, open(p+'login.html', 'w') as o:
				page += h.read() + i.read() + '</html>'
				o.write(page)
		except IOError:
			print nofile
	if not os.path.isfile('register.html'):
		try:
			with open(p+'header.xml', 'r') as h, open(p+'register.xml','r') as i, open(p+'register.html', 'w') as o:
				page += h.read() + i.read() + '</html>'
				o.write(page)
		except IOError:
			print nofile
def makeTable(itemname='',loginuser=''):
	items = []
	page = ""
	try:
		with open('clubinventory/seekequipment.pickle') as f:
			items = pickle.load(f)
	except:
		pass
	try:
		with open("htmlsnips/header.xml", 'rU') as f:
			page += f.read()
	except:
		pass
	try:
		with open('users/oldusers.pickle') as f:
			oldusers += pickle.load()
	except:
		print "oldusers is not there in file"
	page += """
	<body>
	<h1>SEEK Hardware</h1>
	<p>Software and Electrical Engineering Klub hardware for members.</p>
	<p><a href="/login/">Log In</a> or <a href="/register/">Register</a> to sign out hardware on weekly loans.</p>
	"""
	page += """
	<table>
	"""
	row = 0
	for listi in items:
		counter = 0
		#print "in"
		row += 1
		if row > 1:
			page += """
			</tr>
			
			"""
		page += "<tr>"
		listilength = len(listi)
		founditem = False
		##print "len(listi): ", listilength
		firsti = ''
		for i in listi:
			if counter == 0:
				firsti = i.lower()
			counter += 1
			##print counter
			if firsti == itemname and loginuser != '':
				founditem = True
			##print founditem
			if counter == listilength:
				if founditem:
					rowtodec = items.index(listi)
					celltodec = listi.index(i)
					#print "not yet decremented item in row ", rowtodec, " cell ", celltodec
					num = int(items[rowtodec][celltodec])
					num -= 1
					items[rowtodec][celltodec] = num
					page += "<td>" + str(num) + "</td>"
				else:
					page += "<td>" + str(i) + "</td>"
				if loginuser != '':
					page += '<td><form method="POST"><input type="radio" name="itemtosignout"'+' value="'+firsti+'"'+'></input><input type="submit" value="Sign Out"></input></form></td>'
			else:
				page += "<td>" + str(i) + "</td>"
	page += "</tr>\n</table>"
	page += "</body>\n</html>"
	try:
		with open("index.html", 'w') as o:
			o.write(page)
	except:
		pass
	try:
		with open('clubinventory/seekequipment.pickle', 'wb') as o:
			pickle.dump(items, o)
	except:
		pass

class myHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		if self.path == "/":
			makeTable()
			self.path = "/index.html"
		elif self.path == "/login":
			makeTable()
			self.path = "/login/index.html"
		elif self.path == "/register":
			makeTable()
			self.path = "/register/index.html"
		sendreply = False
		try:
			if self.path.endswith(".html"):
				mimetype = 'text/html'
				sendreply = True
			if (sendreply == True):
				f = open(curdir + sep + self.path)
				self.send_response(200)
				self.send_header('Content-type',mimetype)
				self.end_headers()
				self.wfile.write(f.read())
				f.close()
			return
		except IOError:
			self.send_error(404, 'File not found: %s' % self.path)
			
	def do_POST(self):
		"""Handler for POST requests"""    
		length = int(self.headers['Content-Length'])
		post_data = urlparse.parse_qs(self.rfile.read(length).decode('utf-8'))
		try:
			whotodecrement = post_data['itemtosignout'][0]
		except KeyError:
			whotodecrement = ''
		makeTable(whotodecrement)
		try:
			registeruser = post_data['register'][0]
			registeruser = lower(registeruser)
			if registeruser.endswith('@uoit.net') or registeruser.endswith('@uoit.ca'):
				if not registeruser in oldusers:
					oldusers[registeruser] = ['abcd']
		except KeyError:
			pass
		try:
			loginuser = post_data['login'][0]
			password = post_data['login'][1]
			if loginuser.endswith('@uoit.net') or loginuser.endswith('@uoit.ca'):
				if loginuser in oldusers:
					makeTable('',loginuser)
		except:
			pass
		if self.path == "/":
			self.path = "/index.html"
		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.end_headers()
		f = open(curdir + sep + self.path)
		self.wfile.write(f.read())
		f.close()

SERVER_LOCATION = '0.0.0.0'
PORT_NUMBER = 8080

try:
	server = HTTPServer((SERVER_LOCATION,PORT_NUMBER),myHandler)
	print "Started HTTP server at ", SERVER_LOCATION, " port ", PORT_NUMBER
	server.serve_forever()
except KeyboardInterrupt:
	print "\nKill signal received, server shutting down"
	server.socket.close()
