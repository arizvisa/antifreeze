#!c:\python\python.exe

import sys, os, time
import BaseHTTPServer, CGIHTTPServer

# class for handling the webserver (with cgi support)
class web_interface(BaseHTTPServer.BaseHTTPRequestHandler, CGIHTTPServer.CGIHTTPRequestHandler):
    mimelookup = dict([
        ('.html', 'text/html'),
        ('.js', 'text/html'),
        ('.txt', 'text/plain'),
        ('.gif', 'image/gif'),
        ('.png', 'image/png'),
        ('.css', 'text/css'),
#        (None, 'application/binary')
        (None, 'text/plain')
    ])
	
    def sendfile(self, path=None, errorcode=200, mime=None):

        def getextension(pathname):
            if '.' in pathname:
                ext = pathname[:pathname.find('.')+1]
                return ext
            return None

        try:
            if path:
                input = file(path, 'rb')

        except IOError, (x):            
            self.send_response(404)
            self.end_headers()
            return

        ext = getextension(path)

        print '> %s'% ext
        self.senddata(input.read(), errorcode, self.mimelookup[ext])

        if path:
            self.wfile.write(input.read())
            input.close()

    def senddata(self, data, errorcode=200, mime=None):
        self.send_response(errorcode)
        self.send_header("Content-Type", mime)
        self.end_headers()
        self.wfile.write(data)
	
    def do_GET(self):
        pathname = os.curdir + self.path
        if os.path.isdir(pathname):
            content_type = "text/html"
            data = ""
            for item in os.listdir(pathname):
                data += '<a href="%s">%s</a><br>' % (pathname.replace(os.sep, '/') + '/' + item, item)
            self.senddata(data, mime=content_type)
            return

#        if pathname.endswith('.py'):
#            self.send_error(501, "Can only POST to CGI scripts")
#            return

        self.sendfile(pathname)

    '''
    def do_POST(self):
        pathname = os.curdir + self.path

        if self.is_cgi():
            self.run_cgi()
        else:
            self.send_error(501, "Can only POST to CGI scripts %s [%s]"% (self.path, self.is_cgi()) )
    '''

			
#############################################################################################################################
if __name__ == '__main__':
	server_class = BaseHTTPServer.HTTPServer
	
	# our cgi path
	CGIHTTPServer.CGIHTTPRequestHandler.cgi_directories.append("/pyd")
	print CGIHTTPServer.CGIHTTPRequestHandler.cgi_directories
	
	
	httpd = server_class(('localhost', 80), web_interface)
	print time.asctime(), "Server starts - localhost:80"
	
	try:
		httpd.serve_forever()
	except KeyboardInterrupt: # XXX: doesnt work
		print "Caught keyboard interrupt"
		httpd.server_close()
		
		
	print time.asctime(), "Server stops - localhost:80" 
