from xml.dom.minidom import parseString

"""
from xml_to_dict import xml_to_dict

x = xml_to_dict("/Users/pedram/Desktop/test.xml")['advisory']
print x['ids']['internal'].value

for vendor in x['affected_vendors']:
    print vendor['name'].value, vendor['name'].ATTRIBUTES["link"]
"""

class _node_not_text:
    pass

class _xml_to_dict_node:
    def __init__ (self, node, text):
        self.value      = text
        self.ATTRIBUTES = {}
        
        for k, v in node.attributes.items():
            self.ATTRIBUTES[k] = v

    def __str__ (self):
        return self.value

def _get_text_from_node (node):
    t = ""

    for n in node.childNodes:
        if n.nodeType in [n.TEXT_NODE, n.CDATA_SECTION_NODE]:
            t += n.nodeValue
        else:
            raise _node_not_text

    return t

def _node_to_dict (node):
    dic = {} 

    for n in node.childNodes:
        if n.nodeType != n.ELEMENT_NODE:
            continue
                
        if n.getAttribute("list").lower() == "true":
            l = []
            for c in n.childNodes:
                if c.nodeType != n.ELEMENT_NODE:
                    continue

                try:
                    l.append(_xml_to_dict_node(c, _get_text_from_node(c)))
                except _node_not_text:
                    l.append(_node_to_dict(c))

                dic.update({n.nodeName:l})

            continue

        try:
            text = _get_text_from_node(n)
        except _node_not_text:
            dic.update({n.nodeName:_node_to_dict(n)})
            continue

        dic.update({n.nodeName:_xml_to_dict_node(n, text)})
        continue

    return dic

def xml_to_dict (input):
    '''
    @author: pedram
    '''

    # <arizvisa comment="lazily skip past xml version tag">
    if input.startswith('<?'):
        input = input[input.index('?>') + 2: ]
    # </arizvisa>
    return _node_to_dict(parseString(input))

if __name__ == "__main__":
    s = '''<?xml version="1.0"?><code><name>direct.controls</name><asm><![CDATA[    load_const       0                                   # -> 'None'
    return_value    ]]></asm>undefined<path>PYD->direct.controls</path></code>
    '''
    x = xml_to_dict(s)
    
    for vendor in x['affected_vendors']:
        print vendor["name"]
        
        print vendor.get("response", "no response")
        
        for product in vendor.get("products", []):
            print "\t", product, product.ATTRIBUTES["link"]
    
    print x['details']
