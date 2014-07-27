from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from os import curdir, sep

class myHandler(BaseHTTPRequestHandler):
	def do_GET(self):

		items = []
		page = ""
		try:
			with open("txt/items.txt",'r') as f:
				items = f.read().split('\n')
				del items[items.index("")]
				items = [i.split(',') for i in items]
		except:
			pass
		try:
			with open("txt/headerbegin.txt", 'r') as f:
				page += f.read()
		except:
			pass
		page += """
		<body>
		<table>
		"""
		row = 0
		for listi in items:
			print "in"
			row += 1
			if row > 1:
				page += """
				</tr>
				
				"""
			page += "<tr>"
			for i in listi:
				page += "<td>" + str(i) + "</td>"
		page += "</tr>\n</table>"
		page += "</body>\n</html>"
		try:
			with open("index.html", 'w') as o:
				o.write(page)
		except:
			pass

		if self.path == "/":
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

SERVER_LOCATION = '0.0.0.0'
PORT_NUMBER = 8080

try:
	server = HTTPServer((SERVER_LOCATION,PORT_NUMBER),myHandler)
	print "Started HTTP server at ", SERVER_LOCATION, " port ", PORT_NUMBER
	server.serve_forever()
except KeyboardInterrupt:
	print "Kill signal received, server shutting down"
	server.socket.close()
