from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from os import curdir, sep
import urlparse, pickle

def makeTable(itemname=''):
	items = []
	page = ""
	try:
		with open('pickle/equipment.pickle') as f:
			items = pickle.load(f)
	except:
		pass
	try:
		with open("txt/headerbegin.txt", 'rU') as f:
			page += f.read()
	except:
		pass
	page += """
	<body>
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
			if firsti == itemname:
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
		with open('pickle/equipment.pickle', 'wb') as o:
			pickle.dump(items, o)
	except:
		pass

class myHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		if self.path == "/":
			makeTable()
			self.path = "/index.html"
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
