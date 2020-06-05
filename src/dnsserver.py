import asyncio, socket, struct

from typing import List, Tuple

from src.utils import with_padding

class DNSServer(): 
    # take from docs.python
    def __init__(self, forwarder) -> None:
        self._forwarder = forwarder

    def connection_made(self, transport) -> None:
        print("connection made")
        self.transport = transport

    def _make_error_pkg(self, packet: str) -> str:  
        flags = '1' + with_padding(bin(packet[2])[2:])[1:]
        rcode = with_padding(bin(packet[3])[2:])

        return packet[:2] + struct.pack('>H', int(flags + rcode[:4] + '0010', 2)) + packet[4:]

    def datagram_received(self, data, addr) -> None: 
        self.transport.sendto(data, addr)

def start_server(address: str, port: int, forwader: List[Tuple[str, int]]) -> None: 
    async def _start():
        loop = asyncio.get_running_loop()
        
        transport, protocol = await loop.create_datagram_endpoint(
                lambda: DNSServer(),
                local_addr=(address, port)
                )
        # TODO: fix timeout
        try: 
            await asyncio.sleep(1000)
        finally:
            transport.close()
    
    asyncio.run(_start())
