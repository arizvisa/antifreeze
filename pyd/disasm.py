import sys
sys.path.extend(["./", "../", "../lib"])
import config

import cgi
import cgitb; cgitb.enable()

import pyasm
import extract_code
from navi import navi

######################################
def find_obj(navObj, nodeName):
    '''
    returns a code object, if it finds it
    '''    
    
    if navObj.object.co_name == "?":
        if navObj.object.co_filename == nodeName:
            raise
            #return navObj.object
            
    elif navObj.object.co_name == nodeName:
        raise
        #return navObj.object
    
    # get downgraph
    children = navObj.down()
    
    while children:
        child = children.pop()
        
        if child.object.co_name == nodeName:
            return child.object
        else:
            children.extend(child.down())
            
    else:
        return None
    

######################################

form = cgi.FieldStorage()

# the node that was clicked
codeName = form.getvalue('codeName')
#codeName = "direct.directnotify.Logger"

# find and disassemble the code object
objs = extract_code.extract_objs(config.in_filename)

# get disassembly of the correct code object
disasm = ""
if objs.has_key(codeName):
    disasm = pyasm.pretty_dis(objs[codeName])
    found = objs[codeName]
else:
    # we need to find the embedded code object with the name 'codeName'
    path = form.getvalue('path')
    nodePath = path.split("->")
    
    # get the root node code object
    try:
        # index 1 so that we bypass the fake root node placeholder in the tree
        rootCodeObj = objs[nodePath[1]]
    except KeyError:
        raise

    nav = navi(rootCodeObj)
    
    found = find_obj(nav, codeName)    
    assert(found != None)
    
    disasm = pyasm.pretty_dis(found)


co_code_fix   = ['0x%02x' % ord(x) for x in found.co_code]


co_consts_fix = ""
for x in found.co_consts:
    if isinstance(x, int) or isinstance(x, float):
        co_consts_fix += "INT:%s," % repr(x)
    elif isinstance(x, str):
        co_consts_fix += "STR:%s," % x
    elif x == None:
        co_consts_fix += "NON:None,"
    else:
        co_consts_fix += "UNK:%s" % repr(x)




data = """<?xml version="1.0"?>                   
<code>                   
    <item>                   
        <name>%s </name>                   
        <asm><![CDATA[%s]]></asm>                   
        <co_argcount>%d</co_argcount>                   
        <co_cellvars>%s</co_cellvars>                   
        <co_code><![CDATA[%s]]></co_code>                   
        <co_consts><![CDATA[%s]]></co_consts>                   
        <co_filename>%s</co_filename>                   
        <co_firstlineno>%d</co_firstlineno>                   
        <co_flags>%s</co_flags>                   
        <co_freevars>%s</co_freevars>                   
        <co_lnotab><![CDATA[%s]]></co_lnotab>                   
        <co_name>%s</co_name>                   
        <co_names>%s</co_names>                   
        <co_nlocals>%s</co_nlocals>                   
        <co_stacksize>%d</co_stacksize>                   
        <co_varnames>%s</co_varnames>                   
    </item>                   
</code>""" % (codeName, disasm, found.co_argcount, found.co_cellvars, co_code_fix, 
              co_consts_fix, found.co_filename, found.co_firstlineno, found.co_flags,  
              found.co_freevars, list(found.co_lnotab), found.co_name, found.co_names,   
              found.co_nlocals, found.co_stacksize, found.co_varnames)                   

print "Content-type: text/xml\r\n"
print data
#print disasm

