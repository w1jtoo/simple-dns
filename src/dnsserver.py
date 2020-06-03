import asyncio, socket

from typing import List, Tuple

class DNSServer(): 
    # take from docs.python
    def __init__(self, forwarder) -> None:
        self._forwarder = forwarder

    def connection_made(self, transport) -> None:
        print("connection made")
        self.transport = transport

    def 
    
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
