#!c:\python\python.exe

import sys, os, time
sys.path = ['./'] + sys.path
import BaseHTTPServer, CGIHTTPServer

# class for handling the webserver (with cgi support)
class requestHandler(BaseHTTPServer.BaseHTTPRequestHandler, CGIHTTPServer.CGIHTTPRequestHandler):
    mimelookup = dict([
        ('.html', 'text/html'),
        ('.js', 'text/html'),
        ('.txt', 'text/plain'),
        ('.gif', 'image/gif'),
        ('.png', 'image/png'),
        ('.css', 'text/css'),
        ('.xml', 'text/xml'),
#        (None, 'application/binary')
        (None, 'text/plain')
    ])
	
    def sendfile(self, path, errorcode=200, mime=None):

        def getextension(pathname):
            if '.' in pathname:
                ext = pathname[pathname.rfind('.')+1:]
                if len(ext) > 0:
                    return '.%s'% ext
            return None

        try:
            input = file(path, 'rb')

        except IOError, (x):         
            self.senddata("404 what the fuck", errorcode=404, mime='text/plain')
            return

        ext = getextension(path)
        if ext not in self.mimelookup.keys():
            ext = None

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
        # check to see if we're a directory
        local_path = os.getcwd() + self.path.replace('/', os.sep)
        url_path = self.path[1:]

        if os.path.isdir(local_path):
            res = []
            for fn in os.listdir(local_path):
                s = '<a href="%s/%s">%s</a><br />\n' % (url_path, fn, fn)
                res.append(s)
            res = ''.join(res)
            self.senddata(res, mime='text/html')
            return

        if self.path.endswith('.py'):
            self.run_cgi()
            return

        self.sendfile(local_path)

#############################################################################################################################
if __name__ == '__main__':
	server_class = BaseHTTPServer.HTTPServer
	
	# our cgi path
	CGIHTTPServer.CGIHTTPRequestHandler.cgi_directories.append("/pyd")
	
	httpd = server_class(('localhost', 80), requestHandler)
	print time.asctime(), "Server starts - localhost:80"
	
	try:
		httpd.serve_forever()

	except KeyboardInterrupt: # XXX: doesnt work
		print "Caught keyboard interrupt"
		httpd.server_close()
		
		
	print time.asctime(), "Server stops - localhost:80" 
