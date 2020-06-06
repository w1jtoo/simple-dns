import asyncio, socket, struct

from typing import List, Tuple

from src.utils import with_padding, get_question, get_qname, get_qtype 

BUFFER_SIZE = 1024
TIME_OUT = 2

class DNSServer(): 
    def __init__(self, forwarder: List[Tuple[str, int]], on_lost) -> None:
        self._forwarders = forwarder
        self._on_lost = on_lost

    def connection_made(self, transport) -> None:
        print("connection made")
        self.transport = transport

    def _make_error_pkg(self, packet: str) -> str:  
        flags = '1' + with_padding(bin(packet[2])[2:])[1:]
        rcode = with_padding(bin(packet[3])[2:])

        return packet[:2] + struct.pack('>H', int(flags + rcode[:4] + '0010', 2)) + packet[4:]

    def datagram_received(self, data: str, addr: Tuple[str, int]) -> None: 
        question = get_question(data)
        qname = get_qname(question)
        qtype = get_qtype(question)


        # making request to forwarder: 
        answer = None
        for forwarder in self._forwarders:
            try: 
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
           	sock.settimeout(TIME_OUT)
                sock.sendto(data, forwarder)
    	        answer, address = sock.recvfrom(BUFFER_SIZE)
                break
            except socket.error as e:
                # print(e) TODO: logging
           	# answer =  self._make_error_pkg(data)
                pass
            finally:
           	sock.close()
        if answer is None:
            print("No valid forwarder were found. Please update forwarders and restart DNS server.")
            answer = self._make_error_pkg(data)
        
        self.transport.sendto(answer, addr)
        print(f"{addr} was served")

def start_server(address: str, port: int, forwarders: List[Tuple[str, int]]) -> None: 
    async def _start():
        loop = asyncio.get_running_loop()
        on_con_lost = loop.create_future()

        transport, protocol = await loop.create_datagram_endpoint(
                lambda: DNSServer(forwarders, on_con_lost)  ,
                local_addr=(address, port)
                )
        # TODO: fix timeout
        try: 
            await on_con_lost
        finally:
            transport.close()
    
    asyncio.run(_start())
