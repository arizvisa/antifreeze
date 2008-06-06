#!c:\python\python.exe
import sys, os, time

from SimpleHTTPServer import SimpleHTTPRequestHandler
from CGIHTTPServer import CGIHTTPRequestHandler
from BaseHTTPServer import HTTPServer

# class for handling the webserver (with cgi support)
class requestHandler(SimpleHTTPRequestHandler, CGIHTTPRequestHandler):
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
                ext = pathname[pathname.rfind('.')+1:]
                if len(ext) > 0:
                    return '.%s'% ext
            return None

        try:
            if path:
                input = file(path, 'rb')

        except IOError, (x):            
            self.senddata('four-oh-four', 404, 'plain/text')
            return

        ext = getextension(path)

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
        pathname = pathname.replace('/', os.sep)    # normalize to something that looks like a filename

        if os.path.isdir(pathname):
            content_type = "text/html"

            data = ""
            for item in os.listdir(pathname):
                res ='<a href="%s/%s">%s</a><br />' % (self.path, item, item)
                data += res

            self.senddata(data, mime='text/html')
            return

#        if pathname.endswith('.py'):
#            self.send_error(501, "Can only POST to CGI scripts")
#            return

        self.sendfile(pathname)

#############################################################################################################################
if __name__ == '__main__':
	
	# our cgi path
    requestHandler.cgi_directories.append("/pyd")
	
    httpd = HTTPServer(('localhost', 80), requestHandler)
    print time.asctime(), "Server starts - localhost:80"
	
    try:
        httpd.serve_forever()

    except KeyboardInterrupt: # XXX: doesnt work
        print "Caught keyboard interrupt"
        httpd.server_close()
		
    print time.asctime(), "Server stops - localhost:80" 
