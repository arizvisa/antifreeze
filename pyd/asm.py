import sys
sys.path.extend(['.', '..', '../lib'])
import config

import cgi
import cgitb; cgitb.enable()

import marshal
from xml2dict import xml2dict

import pyasm
import utils
import codefu
import extract_code
from navi import navi

xmlStr  = cgi.FieldStorage().getvalue('xmlData')
xmlData = xml2dict(xmlStr)

# the disassembly to assemble
toAsm = str(xmlData[u'code'][u'asm'][None])
# namespace hierarchy
path = xmlData[u'code'][u'path'][None]

# code object name
objName = str(xmlData[u'code'][u'name'][None])

# bypass fake root node from the tree
path = str(path).split("->")[1:]

pyd = extract_code.pydOpen( config.in_filename )
root_obj = pyd[path[0]]

if root_obj.co_name == "?":
    root_obj_name = root_obj.co_filename


# create the navigator object
nav = navi(root_obj)

# if its a root object, set found appropriately
if objName == root_obj_name:
    found = nav.object    

# otherwise, find the object
else:
    found = None

    # get the downlist
    children = nav.down()
    
    while children:
        child = children.pop()
        if child.object.co_name in path:
            if child.object.co_name == objName:
                found = child.object
                break
            children = child.down()
            
assert(found != None)

bytes = pyasm.assemble(toAsm)


# if there are constants to update, do it 
newConsts = list(found.co_consts)

# if a single constant was changed
co_consts = xmlData[u'code'][u'co_consts']
if co_consts:
    if isinstance(co_consts[u'value'], dict):
        co_consts[u'value'] = [co_consts[u'value']]

    if len(xmlData[u'code'][u'co_consts'][u'value']) > 0:
        for item in xmlData[u'code'][u'co_consts'][u'value']:
            idx  = int(item[u'index'])
            data = item[None]
        
            if isinstance(newConsts[idx], float):
                newConsts[idx] = float(data)
            elif isinstance(newConsts[idx], int):
                newConsts[idx] = int(data)
            elif isinstance(newConsts[idx], long):
                newConsts[idx] = long(data)
            else:
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


## time to inject

# FIXME: we only need the new object and the object name to pass to
#        pydOpen
#
# pyd = pydOpen(config.out_filename)
# pyd[root_obj_name] = done
#
# XXX: now update .mf file
#
 
serialized_new = marshal.dumps(done)
serialized_old = marshal.dumps(root_obj)

fh = open('OUTPUT.DATA', 'wb')
marshal.dump(done, fh)
fh.close()
extract_code.inject_obj(serialized_new, serialized_old)

print "-"*80
print "SUCCESS"
