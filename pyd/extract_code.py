import sys
sys.path.append("../lib")
import config

import struct,marshal

import peepeelite
from peepeelite.ptypes import *

#sys.path.append(r"C:\code\pypee")
#sys.path.append(r"C:\code\ptypes")


PE = peepeelite.PE


################################################################################
def inject_obj(modified, orig):
    
    in_file = open(config.in_filename, 'rb')
    pyd_data = in_file.read()
    in_file.close()
    
    assert(len(pyd_data) > 1)
    assert(orig in pyd_data)
   
    import re
    starts = [match.start() for match in re.finditer(re.escape(orig), pyd_data)]
    
    counter = 0
    for offset in starts:
  
        new_buf = pyd_data[:offset]
        
        # now append the modified serialized data 
        new_buf += modified
        
        # now append the rest of phase_1.mf
        new_buf += pyd_data[offset+len(modified):]
        
        out_file = open(config.out_filename, 'wb')
        out_file.write(new_buf)
        wrote = len(new_buf)
        out_file.close()
        
        print "Operation completed successfully %d of %d, wrote %d bytes back to file" % (counter+1, len(starts), wrote)
        counter += 1
        
    if counter == 0:
        raise
        #print "Operation failed! No occurrences found!"

################################################################################
def extract_objs(fname):

    from frozenfind import lameGetFrozenTable       ## heh
    class frozenTable(pStruct):
        _fields_ = [
            ('<L', 'Name'),
            ('<L', 'Data'),
            ('<L', 'Length')
        ]
    
    objs    = dict()
    
    ## load executable
    executable = PE()
    executable.open(fname)
    executable.read()
    file = executable.file

    frozenTableOffset = lameGetFrozenTable(fname)
    
    ## iterate through all records
    file.seek( frozenTableOffset )
    rec = frozenTable()

    while True:
        rec.deserialize(file.read(rec.size()))
        
        # make sure we didnt go past the end of the object table
        if rec['Name'] == 0:
            break
        
        offset = file.tell()    # we're manipulating this file type, out from underneath the PE object
    
        name = executable.getStringByRVA( executable.getRVAByVA(rec['Name']) )
    
        # dump the code objects themselves
        recLen = abs(struct.unpack('l', struct.pack('L', int(rec['Length'])))[0] * -1)
    
        if recLen > 0 :
            # pull out the data
            data_ptr = executable.getOffsetByVA(rec['Data'])
            file.seek(data_ptr)
            data = file.read(recLen)
    
            # deserialize it, store in our dictionary
            objs[name] = marshal.loads(data)
    
        # jump to next item
        file.seek(offset + rec.size())  # so we save and restore

    return objs

if __name__ == '__main__':
    fname = 'Phase1.pyd'

    from frozenfind import lameGetFrozenTable       ## heh
    class frozenTable(pStruct):
        _fields_ = [
            ('<L', 'Name'),
            ('<L', 'Data'),
            ('<L', 'Length')
        ]

    def getLookupTable(fname):
        executable = PE()
        executable.open(fname)
        executable.read()
        file = executable.file

        frozenTableOffset = lameGetFrozenTable(fname)
        
        ## iterate through all records
        file.seek( frozenTableOffset )
        rec = frozenTable()

        while True:
            rec.deserialize(file.read(rec.size()))
            
            # make sure we didnt go past the end of the object table
            if rec['Name'] == 0:
                break
            
            offset = file.tell()    # we're manipulating this file type, out from underneath the PE object
        
            name = executable.getStringByRVA( executable.getRVAByVA(rec['Name']) )
        
            # dump the code objects themselves
            recLen = abs(struct.unpack('l', struct.pack('L', int(rec['Length'])))[0] * -1)
        
            if recLen > 0 :
                # pull out the data
                data_ptr = executable.getOffsetByVA(rec['Data'])
        
                # deserialize it, store in our dictionary
                table[name] = (data_ptr, recLen)
        
            # jump to next item
            file.seek(offset + rec.size())  # so we save and restore

        return table

    class pydNavi(object):
        lookup = None
        file = None

        def __init__(self, fname, table):
            super(pydNavi, self).__init__()
            self.lookup = table
            self.file = file(fname, 'rb')

        def __getitem__(self, key):
            offset,length = self.lookup[key]

            self.file.seek(offset)
            return marshal.loads( self.file.read(length) )

        def __setitem__(self, key, value):
            offset,length = self.lookup[key]
            res = marshal.dumps(value)

            assert len(res) <= length

            self.file.seek(offset)
            self.file.write(res)

        def keys(self):
            return self.lookup.keys()

    print fname
    res = getLookupTable(fname)
    x = pydNavi(fname, res)
