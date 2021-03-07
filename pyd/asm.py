import sys
sys.path.extend(['.', '..', '../lib'])
import config

import cgi
import cgitb; cgitb.enable()

import marshal
from xml2dict import xml2dict

import pyasm
import codefu
import extract_code
from navi import navi

######################################
form = cgi.FieldStorage()
xmlStr  = form.getvalue('xmlData')

xmlStr = '''<?xml version="1.0"?><code><name>direct.directtools.DirectGlobals</name><asm><![CDATA[    load_const       0                                   # -> "('Vec3', 'Point3')"
    import_name      0                                   # -> "'pandac.PandaModules'"
    import_from      1                                   # -> "'Vec3'"
    store_name       1                                   # -> "'Vec3'"

    import_from      2                                   # -> "'Point3'"
    store_name       2                                   # -> "'Point3'"

    pop_top         
    load_const       1                                   # -> "'x-disc-visible'"
    load_const       2                                   # -> "'y-disc-visible'"
    load_const       3                                   # -> "'z-disc-visible'"
    load_const       4                                   # -> "'GridBack'"
    load_const       5                                   # -> "'unpickable'"
    build_list       5                                   # -> 'None'
    store_name       3                                   # -> "'UNPICKABLE'"

    load_name        1                                   # -> "'Vec3'"
    load_const       6                                   # -> '1'
    load_const       7                                   # -> '0'
    load_const       7                                   # -> '0'
    call_function    3                                   # -> 'None'

    store_name       4                                   # -> "'X_AXIS'"

    load_name        1                                   # -> "'Vec3'"
    load_const       7                                   # -> '0'
    load_const       6                                   # -> '1'
    load_const       7                                   # -> '0'
    call_function    3                                   # -> 'None'

    store_name       5                                   # -> "'Y_AXIS'"

    load_name        1                                   # -> "'Vec3'"
    load_const       7                                   # -> '0'
    load_const       7                                   # -> '0'
    load_const       6                                   # -> '1'
    call_function    3                                   # -> 'None'

    store_name       6                                   # -> "'Z_AXIS'"

    load_name        1                                   # -> "'Vec3'"
    load_const       8                                   # -> '-1'
    load_const       7                                   # -> '0'
    load_const       7                                   # -> '0'
    call_function    3                                   # -> 'None'

    store_name       7                                   # -> "'NEG_X_AXIS'"

    load_name        1                                   # -> "'Vec3'"
    load_const       7                                   # -> '0'
    load_const       8                                   # -> '-1'
    load_const       7                                   # -> '0'
    call_function    3                                   # -> 'None'

    store_name       8                                   # -> "'NEG_Y_AXIS'"

    load_name        1                                   # -> "'Vec3'"
    load_const       7                                   # -> '0'
    load_const       7                                   # -> '0'
    load_const       8                                   # -> '-1'
    call_function    3                                   # -> 'None'

    store_name       9                                   # -> "'NEG_Z_AXIS'"

    load_name        1                                   # -> "'Vec3'"
    load_const       7                                   # -> '0'
    call_function    1                                   # -> 'None'

    dup_top         
    store_name       10                                  # -> "'ZERO_VEC'"

    store_name       11                                  # -> "'ORIGIN'"

    load_name        1                                   # -> "'Vec3'"
    load_const       6                                   # -> '1'
    call_function    1                                   # -> 'None'

    store_name       12                                  # -> "'UNIT_VEC'"

    load_name        2                                   # -> "'Point3'"
    load_const       7                                   # -> '0'
    call_function    1                                   # -> 'None'

    store_name       13                                  # -> "'ZERO_POINT'"

    load_const       9                                   # -> '1.5'
    store_name       14                                  # -> "'DIRECT_FLASH_DURATION'"

    load_const       10                                  # -> '0.65000000000000002'
    store_name       15                                  # -> "'MANIPULATION_MOVE_DELAY'"

    load_const       11                                  # -> '1e-010'
    store_name       16                                  # -> "'Q_EPSILON'"

    load_const       7                                   # -> '0'
    store_name       17                                  # -> "'DIRECT_NO_MOD'"

    load_const       6                                   # -> '1'
    store_name       18                                  # -> "'DIRECT_SHIFT_MOD'"

    load_const       12                                  # -> '2'
    store_name       19                                  # -> "'DIRECT_CONTROL_MOD'"

    load_const       13                                  # -> '4'
    store_name       20                                  # -> "'DIRECT_ALT_MOD'"

    load_const       7                                   # -> '0'
    store_name       21                                  # -> "'SKIP_NONE'"

    load_const       6                                   # -> '1'
    store_name       22                                  # -> "'SKIP_HIDDEN'"

    load_const       12                                  # -> '2'
    store_name       23                                  # -> "'SKIP_BACKFACE'"

    load_const       13                                  # -> '4'
    store_name       24                                  # -> "'SKIP_CAMERA'"

    load_const       14                                  # -> '8'
    store_name       25                                  # -> "'SKIP_UNPICKABLE'"

    load_name        22                                  # -> "'SKIP_HIDDEN'"
    load_name        23                                  # -> "'SKIP_BACKFACE'"
    binary_or       
    load_name        24                                  # -> "'SKIP_CAMERA'"
    binary_or       
    load_name        25                                  # -> "'SKIP_UNPICKABLE'"
    binary_or       
    store_name       26                                  # -> "'SKIP_ALL'"

    load_const       6                                   # -> '1'
    store_name       27                                  # -> "'EDIT_TYPE_UNMOVABLE'"

    load_const       12                                  # -> '2'
    store_name       28                                  # -> "'EDIT_TYPE_UNSCALABLE'"

    load_const       13                                  # -> '4'
    store_name       29                                  # -> "'EDIT_TYPE_UNROTATABLE'"

    load_name        27                                  # -> "'EDIT_TYPE_UNMOVABLE'"
    load_name        28                                  # -> "'EDIT_TYPE_UNSCALABLE'"
    binary_or       
    load_name        29                                  # -> "'EDIT_TYPE_UNROTATABLE'"
    binary_or       
    store_name       30                                  # -> "'EDIT_TYPE_UNEDITABLE'"

    load_const       15                                  # -> 'None'
    return_value    ]]></asm>undefined<path>PYD->direct.directtools.DirectGlobals</path></code>
    '''
#
xmlData = xml2dict(xmlStr)

# the disassembly to assemble
toAsm = str(xmlData[u'code'][u'asm'])

# namespace hierarchy
path = xmlData[u'code'][u'path']

# code object name
objName = str(xmlData[u'code'][u'name'])

# bypass fake root node from the tree
path = str(path).split("->")[1:]

objs = extract_code.extract_objs(config.in_filename)
root_obj = objs[path[0]]


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


'''
# if there are constants to update, do it 
newConsts = list(found.co_consts)

# if a single constant was changed
if isinstance(xmlData.code.co_consts, dict):
    xmlData[u'code'].co_consts = [xmlData.code.co_consts]

for item in xmlData.code.co_consts:
    idx  = int(item['index'])
    data = item['value']

    if isinstance(newConsts[idx], float):
        logTxt += "changing %f to %f\n" % (newConsts[idx], float(data))
        newConsts[idx] = float(data)
    elif isinstance(newConsts[idx], int):
        logTxt += "changing %d to %d\n" % (newConsts[idx], int(data))
        newConsts[idx] = int(data)
    elif isinstance(newConsts[idx], long):
        logTxt += "changing %d to %d\n" % (newConsts[idx], long(data))
        newConsts[idx] = long(data)
    else:
        logTxt += "changing %s to %s\n" % (newConsts[idx], repr(data))
        newConsts[idx] = data
'''
    
newConsts = tuple(newConsts)

original = found
clone    = codefu.code_clone(found, co_code=bytes, co_consts=newConsts)
logTxt += "Clone of code object complete\n"

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

print "-"*80
print logTxt
print "-"*80
print "SUCCESS"

if __name__ == '__main__':
    xmlStr='''
<code><name>direct.directtools.DirectGlobals</name><asm><![CDATA[    load_const       0                                   # -> "('Vec3', 'Point3')"
    import_name      0                                   # -> "'pandac.PandaModules'"
    import_from      1                                   # -> "'Vec3'"
    store_name       1                                   # -> "'Vec3'"

    import_from      2                                   # -> "'Point3'"
    store_name       2                                   # -> "'Point3'"

    pop_top         
    load_const       1                                   # -> "'x-disc-visible'"
    load_const       2                                   # -> "'y-disc-visible'"
    load_const       3                                   # -> "'z-disc-visible'"
    load_const       4                                   # -> "'GridBack'"
    load_const       5                                   # -> "'unpickable'"
    build_list       5                                   # -> 'None'
    store_name       3                                   # -> "'UNPICKABLE'"

    load_name        1                                   # -> "'Vec3'"
    load_const       6                                   # -> '1'
    load_const       7                                   # -> '0'
    load_const       7                                   # -> '0'
    call_function    3                                   # -> 'None'

    store_name       4                                   # -> "'X_AXIS'"

    load_name        1                                   # -> "'Vec3'"
    load_const       7                                   # -> '0'
    load_const       6                                   # -> '1'
    load_const       7                                   # -> '0'
    call_function    3                                   # -> 'None'

    store_name       5                                   # -> "'Y_AXIS'"

    load_name        1                                   # -> "'Vec3'"
    load_const       7                                   # -> '0'
    load_const       7                                   # -> '0'
    load_const       6                                   # -> '1'
    call_function    3                                   # -> 'None'

    store_name       6                                   # -> "'Z_AXIS'"

    load_name        1                                   # -> "'Vec3'"
    load_const       8                                   # -> '-1'
    load_const       7                                   # -> '0'
    load_const       7                                   # -> '0'
    call_function    3                                   # -> 'None'

    store_name       7                                   # -> "'NEG_X_AXIS'"

    load_name        1                                   # -> "'Vec3'"
    load_const       7                                   # -> '0'
    load_const       8                                   # -> '-1'
    load_const       7                                   # -> '0'
    call_function    3                                   # -> 'None'

    store_name       8                                   # -> "'NEG_Y_AXIS'"

    load_name        1                                   # -> "'Vec3'"
    load_const       7                                   # -> '0'
    load_const       7                                   # -> '0'
    load_const       8                                   # -> '-1'
    call_function    3                                   # -> 'None'

    store_name       9                                   # -> "'NEG_Z_AXIS'"

    load_name        1                                   # -> "'Vec3'"
    load_const       7                                   # -> '0'
    call_function    1                                   # -> 'None'

    dup_top         
    store_name       10                                  # -> "'ZERO_VEC'"

    store_name       11                                  # -> "'ORIGIN'"

    load_name        1                                   # -> "'Vec3'"
    load_const       6                                   # -> '1'
    call_function    1                                   # -> 'None'

    store_name       12                                  # -> "'UNIT_VEC'"

    load_name        2                                   # -> "'Point3'"
    load_const       7                                   # -> '0'
    call_function    1                                   # -> 'None'

    store_name       13                                  # -> "'ZERO_POINT'"

    load_const       9                                   # -> '1.5'
    store_name       14                                  # -> "'DIRECT_FLASH_DURATION'"

    load_const       10                                  # -> '0.65000000000000002'
    store_name       15                                  # -> "'MANIPULATION_MOVE_DELAY'"

    load_const       11                                  # -> '1e-010'
    store_name       16                                  # -> "'Q_EPSILON'"

    load_const       7                                   # -> '0'
    store_name       17                                  # -> "'DIRECT_NO_MOD'"

    load_const       6                                   # -> '1'
    store_name       18                                  # -> "'DIRECT_SHIFT_MOD'"

    load_const       12                                  # -> '2'
    store_name       19                                  # -> "'DIRECT_CONTROL_MOD'"

    load_const       13                                  # -> '4'
    store_name       20                                  # -> "'DIRECT_ALT_MOD'"

    load_const       7                                   # -> '0'
    store_name       21                                  # -> "'SKIP_NONE'"

    load_const       6                                   # -> '1'
    store_name       22                                  # -> "'SKIP_HIDDEN'"

    load_const       12                                  # -> '2'
    store_name       23                                  # -> "'SKIP_BACKFACE'"

    load_const       13                                  # -> '4'
    store_name       24                                  # -> "'SKIP_CAMERA'"

    load_const       14                                  # -> '8'
    store_name       25                                  # -> "'SKIP_UNPICKABLE'"

    load_name        22                                  # -> "'SKIP_HIDDEN'"
    load_name        23                                  # -> "'SKIP_BACKFACE'"
    binary_or       
    load_name        24                                  # -> "'SKIP_CAMERA'"
    binary_or       
    load_name        25                                  # -> "'SKIP_UNPICKABLE'"
    binary_or       
    store_name       26                                  # -> "'SKIP_ALL'"

    load_const       6                                   # -> '1'
    store_name       27                                  # -> "'EDIT_TYPE_UNMOVABLE'"

    load_const       12                                  # -> '2'
    store_name       28                                  # -> "'EDIT_TYPE_UNSCALABLE'"

    load_const       13                                  # -> '4'
    store_name       29                                  # -> "'EDIT_TYPE_UNROTATABLE'"

    load_name        27                                  # -> "'EDIT_TYPE_UNMOVABLE'"
    load_name        28                                  # -> "'EDIT_TYPE_UNSCALABLE'"
    binary_or       
    load_name        29                                  # -> "'EDIT_TYPE_UNROTATABLE'"
    binary_or       
    store_name       30                                  # -> "'EDIT_TYPE_UNEDITABLE'"

    load_const       15                                  # -> 'None'
    return_value    ]]></asm>undefined<path>PYD->direct.directtools.DirectGlobals</path></code>
    '''
