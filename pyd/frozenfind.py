import ia32
from peepeelite import PE
import struct

def find_call(address, code):
    for i,insn in zip(range(len(code)), code):
        if insn['opcode'] == '\xff' and insn['modrm'] == '\x15':
            if struct.unpack('<L', insn['disp']) == (address,):
                return i
    raise ValueError, '"call $0x%x" not found'% address

def find_repmovsd(code):
    for i,insn in zip(range(len(code)), code):
        if insn['opcode'] == '\xa5' and '\xf3' in insn['prefix']:
            return i

    raise ValueError, '"rep movs %esi, %edi" not found'

def findFrozenTableNameInFunction(code, initmodule_thunk):
    '''
    Collect every push up to a call initmodule_thunk,
    pull the 5th one
    '''
    i = find_call(initmodule_thunk, code)

    pushes = []
    for x in code[:i]:
        if x['opcode'] == '\x68' or x['opcode'] == '\x51':
            pushes.append(x)

    res, = struct.unpack('<L', pushes[-5]['imm'])
    return res

def findFrozenTableInFunction(code, malloc_thunk):
    '''
    this looks for a rep movsd and is probably
    the wrongest way of doing this
    '''

    ## identify the first call malloc
    i = find_call(malloc_thunk, code)
    code = code[i+1:]

    ## find the next rep movsd
    i = find_repmovsd(code)
    code = code[:i]

    ## find the last assignment to esi
    code = list(reversed(code))
    for i,insn in zip(range(len(code)), code):
        if insn['opcode'] == '\xbe':
            break

    # yay
    va, = struct.unpack('<L', insn['imm'])
    return va

def readFunction(file):
    code = file.read(0x1000)      #XXX: hopefully a function's length isn't >4096

    res = []
    code = iter(code)
    while True:
        insn = ia32.decode(code)
        res.append(insn)
        if insn['opcode'] == '\xc3':
            break

    return res

def lameGetFrozenTable(filename, export=None):
    input = PE()
    input.open(filename)
    input.read()

    # collect the VA of all the imports we care about
    res = []
    for dllname in input['imports']:
        res.extend( input.getImports(dllname) )

    selected = ['malloc', 'Py_InitModule4']
    imp_lookup = dict([(a, input.getVAByRVA(b)) for a,b,c in res if a in selected])

    # collect offsets to all exports
    res = [(a,input.getOffsetByRVA(b)) for a,b in input.getExports()]
    exp_lookup = dict(res)

    ## try out some different exports
    if export:
        export = [export]
    else:
        export = exp_lookup.keys()

    for x in export:
        try:
            input.file.seek( exp_lookup[x] )
            code = readFunction(input.file) #harhar
            table_va = findFrozenTableInFunction(code, imp_lookup['malloc'])
            return input.getOffsetByVA(table_va)

        except ValueError:
            pass

    raise ValueError('Frozen Module pattern not found!')

if __name__ == '__main__':
    print repr(lameGetFrozenTable('../Pirates/Phase1.pyd'))
#    print '%x'% lameGetFrozenTable('/work/deasm/Phase1.pyd')
#    print '%x'% lameGetFrozenTable('/windows/system32/user32.dll')
#    print '%x'% lameGetFrozenTable('/windows/system32/notepad.exe')
