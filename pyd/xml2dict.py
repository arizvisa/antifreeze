from xml.dom import minidom 
Node = minidom.Node

def parseNode(node):
    res = {}
    if node.attributes:
        res = dict( node.attributes.items() )

    for n in node.childNodes:
        fn = nodelookup[n.nodeType]
        name = n.nodeName

        ## XXX: hack to join anything that's considered content
        if name.startswith('#'):
            name = None

        if name in res.keys():
            if not isinstance(res[name], list):
                res[name] = [ res[name] ]
            res[name].append(fn(n))
            continue

        res[name] = fn(n)
    return res

def getData(node):
    return node.data

# directions to parse each node
nodelookup = {
    # has children
    Node.DOCUMENT_NODE : parseNode,
    Node.ELEMENT_NODE : parseNode,
    Node.DOCUMENT_NODE : parseNode,

    # returns constants
    Node.CDATA_SECTION_NODE : getData,
    Node.TEXT_NODE : getData
}

def xml2dict(data):
    node = minidom.parseString(data)
    fn = nodelookup[ node.nodeType ]
    return fn(node)

if __name__ == "__main__":
    data = '''<?xml version="1.0"?><code><name>direct.controls</name><asm><![CDATA[    load_const       0                                   # -> 'None'
    return_value    ]]></asm>undefined<path>PYD->direct.controls</path></code>
    '''
    res = xml2dict(data)
    top = res[u'code']

#    print top
#    print top[u'name']
    print repr(top[u'name'][None])

#    print top[u'asm']
    print repr(top[u'asm'][None])

#    print top[u'path']
    print repr(top[u'path'][None])

    print '-'*7
    # thank you thunder for informing me about the existence of this module
    from pprint import pprint
    data = '''<?xml version="1.0"?>
            <code>
                <name>DynamicHuman</name>
                <asm><![CDATA[cdata blahbala]]></asm>
                <co_consts>
                    <value index="22"><![CDATA[9]]></value>
                    <value index="23"><![CDATA[9]]></value>
                    <value index="24"><![CDATA[9]]></value>
                </co_consts>
                <path>PYD->pirates.pirate.DynamicHuman->DynamicHuman</path>
            </code>
    '''
    res = xml2dict(data)
    pprint(res)
