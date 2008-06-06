import sys
sys.path.append("../lib")
import config

import cgi
import cgitb; cgitb.enable()

from utils import *
from navi import navi
import extract_code

# get form data
form = cgi.FieldStorage()

# get code objects
objs = extract_code.extract_objs(config.in_filename)

# create java array data
# must print a newline before the actual data to end the headers
print
print "["

for obj_name, obj_data in objs.iteritems():
    nav_obj = navi(obj_data)
    
    data = build_js_tree_input(nav_obj)
    
    print data[1:-1] + ","

print "]"
