#!/usr/local/bin/python25
# pulled from http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/522991
# because that other guy sucks at recursive functions
# fixed the 3-space indent issue

def list_to_xml(name, l, stream):
     for d in l:
          dict_to_xml(d, name, stream)

def dict_to_xml(d, root_node_name, stream):
    """ Transform a dict into a XML, writing to a stream """
    stream.write('\n<' + root_node_name)
    attributes = StringIO() 
    nodes = StringIO()
    for item in d.items():
        key, value = item
        if isinstance(value, dict):
            dict_to_xml(value, key, nodes)
        elif isinstance(value, list):
            list_to_xml(key, value, nodes)
        elif isinstance(value, str) or isinstance(value, unicode):
            attributes.write('\n  %s="%s" ' % (key, value))
        else:
            raise TypeError('sorry, we support only dicts, lists and strings')

    stream.write(attributes.getvalue())
    nodes_str = nodes.getvalue()
    if len(nodes_str) == 0:
        stream.write('/>')
    else:
        stream.write('>')
        stream.write(nodes_str)
        stream.write('\n</%s>' % root_node_name)

def dict_from_xml(xml):
    """ Load a dict from a XML string """

    def list_to_dict(l, ignore_root = True):
        """ Convert our internal format list to a dict. We need this
             because we use a list as a intermediate format during xml load """
        root_dict = {}
        inside_dict = {}
        # index 0: node name
        # index 1: attributes list
        # index 2: children node list
        root_dict[l[0]] = inside_dict
        inside_dict.update(l[1])
        # if it's a node containing lot's of nodes with same name,
        # like <list><item/><item/><item/><item/><item/></list>
        for x in l[2]:
            d = list_to_dict(x, False)
            for k, v in d.iteritems():
                if not inside_dict.has_key(k):
                    inside_dict[k] = []
                    
                inside_dict[k].append(v)

        ret = root_dict
        if ignore_root:
            ret = root_dict.values()[0]
            
        return ret
    
    class M:
        """ This is our expat event sink """
        def __init__(self):
            self.lists_stack = []
            self.current_list = None
        def start_element(self, name, attrs):
            l = []
            # root node?
            if self.current_list is None:
                self.current_list = [name, attrs, l]
            else:
                self.current_list.append([name, attrs, l])

            self.lists_stack.append(self.current_list)
            self.current_list = l
            pass
             
        def end_element(self, name):
            self.current_list = self.lists_stack.pop()
        def char_data(self, data):
            # We don't write char_data to file (beyond \n and spaces).
            # What to do? Raise?
            pass

if __name__ == '__main__':
     s = """<?xml version="1.0" encoding="utf-8" ?>
     <result>
          <count n="1">10</count>
          <data><id>491691</id><name>test</name></data>
          <data><id>491692</id><name>test2</name></data>
          <data><id>503938</id><name>hello, world</name></data>
     </result>"""

     r = fromstring(s)
     import pprint
     pprint.pprint(r)

     print r.result.count.value
     print r.result.count.n

     for data in r.result.data:
          print data.id, data.name 
