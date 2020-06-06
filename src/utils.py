import struct, codecs

PADDING = '11'

def with_padding(data: str):
    return (8 - len(data)) * '0' + data

def get_question(packet: str) -> str: 
    pos = packet[12:].find(b'\x00') + 5 + 12
    return packet[12: pos]

def get_qname(question: str) -> str: 
    index, qname = 0, []
    packet = None

    while True:
        if question[index] == 0:
            break
        
        size = question[index]
        if with_padding(bin(size)[2:])[:2] == PADDING:
            offset = codecs.encode(question[index: index + 2], 'hex').decode()
            offset = int(bin(int(offset, 16))[4:], 2)
            index = offset
            continue

        index += 1
        qname.extend(map(chr, question[index: index+size]))
        qname.append('.')
        index += size

    return ''.join(qname)
            
def get_qtype(question: str) -> str:
    pos = question.find(b'\x00') + 1
    return struct.unpack('>H', question[pos:pos+2])[0]
