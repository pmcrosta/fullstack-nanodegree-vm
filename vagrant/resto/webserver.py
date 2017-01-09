from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

class webserverHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		if self.path.endswith("/hello"):
			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.end_headers()

			output = ""
			output += "<html><body>Hello!"
			output += "<form method='POST' enctype= 'multipart/form-data' action='\
			/hello'><h2> What would you like me to say?</h2><input name='message' \
			type='text' ><input type='submit' value='Submit'></form>"
			output += "</body></html>"
			self.wfile.write(output)
			return

		elif self.path.endswith("/hola"):
			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.end_headers()

			output = ""
			output += "<html><body>&#161Hola!<a href='/hello'>Back to Hello</a>"
			output += "<form method='POST' enctype= 'multipart/form-data' action='\
			/hello'><h2> What would you like me to say?</h2><input name='message' \
			type='text' ><input type='submit' value='Submit'></form>"
			output += "</body></html>"
			self.wfile.write(output)
			return

		elif self.path.endswith("/restaurants"):
			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.end_headers()

			restos = session.query(Restaurant).all()

			output = ""
			output += "<html><body>"
			
			output += "<a href='/restaurants/new'>Make a new restaurant here</a><br><br>"

			for resto in restos:
				output += resto.name + "<br><a href='/restaurants/%s/edit'>Edit</a>" % resto.id
				output += "<br><a href='/restaurants/%s/delete'>Delete</a>" % resto.id
				output += "<br><br>"

			output += "</body></html>"
			self.wfile.write(output)			
			return

		elif self.path.endswith("/restaurants/new"):
			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.end_headers()

			output = ""
			output += "<html><body>"
			output += "<form method='POST' enctype= 'multipart/form-data' action='\
			/restaurants/new'><h2>Make a New Restaurant!</h2><input name='newRestaurantName' \
			type='text' placeholder='New Restaurant Name'> <input type='submit' value='Create'></form>"
			output += "</body></html>"
			self.wfile.write(output)
			return

		elif self.path.endswith("/edit"):
			restoPath = self.path.split("/")
			restoId = restoPath[len(restoPath)-2]
			
			resto = session.query(Restaurant).filter_by(id = restoId).one()

			if resto != []:
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				output = ""
				output += "<html><body>"
				output += "<form method='POST' enctype= 'multipart/form-data'"
				output += "action='/restaurants/%s/edit'>" % restoId
				output += "<h2>Rename " + resto.name + "...</h2>"
				output += "<input name='newRestaurantName' \
				type='text' placeholder='New Restaurant Name'> \
				 <input type='submit' value='Create'></form>"
				output += "</body></html>"
				self.wfile.write(output)
			return

		elif self.path.endswith("/delete"):
			restoPath = self.path.split("/")
			restoId = restoPath[len(restoPath)-2]			
			resto = session.query(Restaurant).filter_by(id = restoId).one()

			if resto != []:
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				output = ""
				output += "<html><body>"
				output += "<form method='POST' enctype= 'multipart/form-data'"
				output += "action='/restaurants/%s/delete'>" % restoId
				output += "<h2>Are you sure you want to delete %s?</h2>" % resto.name 
				output += "<input type='submit' value='Delete'></form>"
				output += "</body></html>"
				self.wfile.write(output)
			return	

		else:
			self.send_error(404, "File Not Found %s" % self.path)

	def do_POST(self):
		try:
			if self.path.endswith("/restaurants/new"):
				ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
				
				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile, pdict)
				messagecontent = fields.get('newRestaurantName')

				newRestaurant = Restaurant(name=messagecontent[0])
				session.add(newRestaurant)
				session.commit()

				self.send_response(301)
				self.send_header('Content-type', 'text/html')
				self.send_header('Location', '/restaurants')
				self.end_headers()

			if self.path.endswith("/edit"):
				ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
				
				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile, pdict)
				messagecontent = fields.get('newRestaurantName')

				restoPath = self.path.split("/")
				restoId = restoPath[len(restoPath)-2]

				resto = session.query(Restaurant).filter_by(id = restoId).one()

				resto.name = messagecontent[0]
				session.add(resto)
				session.commit()

				self.send_response(301)
				self.send_header('Content-type', 'text/html')
				self.send_header('Location', '/restaurants')
				self.end_headers()

			if self.path.endswith("/delete"):
				
				ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))

				restoPath = self.path.split("/")
				restoId = restoPath[len(restoPath)-2]
				resto = session.query(Restaurant).filter_by(id = restoId).one()

				if resto != []:
					session.delete(resto)
					session.commit()

					self.send_response(301)
					self.send_header('Content-type', 'text/html')
					self.send_header('Location', '/restaurants')
					self.end_headers()

		except:
			pass

def main():
	try:
		port = 8080
		server = HTTPServer(('',port), webserverHandler)
		print "Web server running on port %s" % port
		server.serve_forever()

	except KeyBoardInterrupt:
		print "^C entered, stopping web server..."
		server.socket.close()


if __name__ == '__main__':
	main()