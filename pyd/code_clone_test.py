#!c:\python\python.exe

import sys

sys.path.append("pyrev")

from navi import navi
import codefu


code_type = type(eval('lambda:True').func_code)


def fn1():
    def fn2a():
        pass
        
    def fn2b():
        def fn3():
            return 12
        pass

    pass
        
    
# get the parent
c1 = fn1.func_code

# our version of the namespace objs dict
objs = dict({"fn1": c1})
    
# path is
path = ["fn1", "fn2b", "fn3"]

# we want to modify fn3

# use navi.down() on this
root_obj = objs[path[0]]


FINDME = "fn3"
found  = None

nav = navi(root_obj)
children = nav.down()

# first, we must find the node we're looking for (in this case, fn3)
while children:
    child = children.pop()
    if child.object.co_name in path:
        if child.object.co_name == FINDME:
            found = child.object
            break
        else:
            children = child.down()

# make sure we found it
assert(found != None)

# now the found variable should be our code object we want to modify

# fn3.co_code = ['d', '\x01', '\x00', 'S']
bytes = "d\x01\x01S"
clone = codefu.code_clone(found, co_code=bytes)
original = found

# we need to build a path of objects for the chain we need
chain = []
chain.append(root_obj)

children = nav.down()

while children:
    child = children.pop()
    if child.object.co_name in path:
        chain.append(child.object)
        nav = navi(child.object)
        children = nav.down()
        

# chain now consists of the path of code objects from root->foo->bar->...->FINDME

# reverse it
chain.reverse()

# chain now consists of the path of code objects from FINDME->...->bar->foo->root
#print chain

# skip the node we already cloned
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


# done is the final ready to be serialized code object
done = clone

    




    