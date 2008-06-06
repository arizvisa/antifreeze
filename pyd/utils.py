from codefu import *
from navi import navi
from pyasm import pretty_dis

def indent(s, tab=4):
    return '\n'.join([' '*tab + s for s in s.split('\n')])

def uniqueid(start=0):
    while True:
        yield start
        start += 1

uniqueid = uniqueid()
def getid():
    return uniqueid.next()

def build_js_tree_input(value):
    def buildtree(value):
        res = []
        res.append("id: %d"% getid() )
        
        if value.object.co_name == "?":
            res.append("text: '%s'"%( value.object.co_filename ))
        else:
            res.append("text: '%s'"%( value.object.co_name ))

        children = value.down()
        if children:
            contents = []
            for x in children:
                contents.append( buildtree(x) )
            contents = ', '.join(contents)

            res.append('children: [%s]'% contents.strip())

        else:
            res.append('leaf: true')

        return '{\n%s\n}'% indent(',\n'.join(res))
    
    return '[%s]'% buildtree(value)

def navi_prtree(v):
    res = []
    res.append( repr(v) )
    res.append( indent('\n'.join([navi_prtree(x) for x in v.down()])) )
    return '\n'.join(res)

def decompose(value):
    res = []
    for x in value.down():
        res.append( decompose(x) )

    funcname = 'def %s(%s):'% (value.object.co_name, ', '.join([ 'arg_%x'%x for x in range(value.object.co_argcount)]))
    res.append(funcname)
    
    consts = []
    for x in value.object.co_consts:
        if type(x) == value.type:
            consts.append( x.co_name )
            continue
        consts.append( repr(x) )

    contents = []
    contents.append('co_consts = [ %s ]'% ', '.join(['%s'% x for x in consts]))
    contents.append('co_code = """')
    contents.extend(pretty_dis(value.object).split('\n'))
    contents.append('"""')

    res.append(indent('\n'.join(contents)))
    res.append('')

    return '\n'.join(res)

def getcode(cobj):
    '''convert a code's attributes to a dict'''
    attributes = [ x for x in dir(cobj) if x.startswith('co_') ]
    # convert co_const
    node = dict([(k, getattr(cobj, k)) for k in attributes])

    # co_consts
    res = []
    for x in node['co_consts']:
        if type(x) == code:
            res.append( x.co_name )
            continue

        res.append(x)

    node['co_consts'] = repr(res)

    # co_code
    node['co_code'] = repr(node['co_code'])

    # co_lnotab
    node['co_lnotab'] = repr(node['co_lnotab'])

    return node

def xmldict(node, name='code'):
    res = '\n'.join([ '<%s>%s</%s>'% (k,v,k) for k,v in node.items()])
    return '<%s>\n%s\n</%s>'%( name, indent(res), name )

if __name__ == '__main__':
    def fn():
        def fn_2a():
            def fn_3a():
                def fn_4():
                    pass
                pass
            pass
            def fn_3b():
                pass
        def fn_2b():
            pass
        pass

    cobj = fn.func_code

    # print the tree
    print navi_prtree( navi(cobj) )

    # print all the disassemblies of the children first
    print decompose(navi(cobj))

    # build the javascript tree data structure
    print build_js_tree_input(navi(cobj))

    # convert the contents of code object into xml for display
    print xmldict(getcode(cobj))

    # convert the contents of code object into xml for display w/ disassembly
    res = getcode(cobj)
    res['asm'] = '<![CDATA[%s]]>'% str(pretty_dis(cobj))
    print xmldict(res)
