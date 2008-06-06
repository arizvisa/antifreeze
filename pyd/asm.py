import sys
sys.path.extend(['.', '..', '../lib'])
import config

import cgi
import cgitb; cgitb.enable()

import marshal
import xml2dict

import pyasm
import codefu
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

if not config.debug:
    form = cgi.FieldStorage()
    xmlStr  = form.getvalue('xmlData')

xmlData = xml2dict.dict_from_xml(xmlStr)

# the disassembly to assemble
toAsm = xmlData.code.asm

# namespace hierarchy
path = xmlData.code.path

# code object name
objName = xmlData.code.name

# bypass fake root node from the tree
path = path.split("->")[1:]

objs = extract_code.extract_objs()
root_obj = objs[path[0]]


if root_obj.co_name == "?":
    root_obj_name = root_obj.co_filename

if objName == root_obj_name:
    raise
    
found = None

# create the navigator object
nav = navi(root_obj)

# get the downlist
children = nav.down()

while children:
    child = children.pop()
    if child.object.co_name in path:
        if child.object.co_name == objName:
            found = child.object
            break
        else:
            children = child.down()
            
assert(found != None)

bytes = pyasm.assemble(toAsm)


# if there are constants to update, do it 
newConsts = list(found.co_consts)

# multiple constants were changed
if isinstance(xmlData.code.co_consts, list):
    
    for item in xmlData.code.co_consts:
        idx  = int(item['index'])
        data = item['value']
    
        newConsts[idx] = data
        
# this means there is only one constant that was changed
elif isinstance(xmlData.code.co_consts, dict):
    idx = int(xmlData.code.co_consts['index'])
    data = xmlData.code.co_consts['value']
    newConsts[idx] = data
    
newConsts = tuple(newConsts)

original = found
clone    = codefu.code_clone(found, co_code=bytes, co_consts=newConsts)


chain = []
chain.append(root_obj)

children = nav.down()

while children:
    child = children.pop()
    if child.object.co_name in path:
        chain.append(child.object)
        nav = navi(child.object)
        children = nav.down()
        
chain.reverse()

chain = chain[1:]
    
for node in chain:
    consts_list = list(node.co_consts)
    
    new_consts = []
    
    for const in consts_list:
        if const is original:
            new_consts.append(clone)
        else:
            new_consts.append(const)
            
    clone = codefu.code_clone(node, co_consts=tuple(new_consts))
    original = node
    
done = clone


# time to inject
serialized_new = marshal.dumps(done)
serialized_old = marshal.dumps(root_obj)

fh = open('OUTPUT.DATA', 'wb')
marshal.dump(done, fh)
fh.close()
extract_code.inject_obj(serialized_new, serialized_old)

print "SUCCESS"
