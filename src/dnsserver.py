import asyncio, socket

class DNSServer(): 
    # take from docs.python
    def connection_made(self, transport) -> None:
        print("connection made")
        self.transport = transport
    
    def datagram_received(self, data, addr) -> None: 
        msg = data.decode()
        print(msg)
        self.transport.sendto(data, addr)

def start_server(address: str, port: int) -> None: 
    async def _start():
        loop = asyncio.get_running_loop()
        
        transport, protocol = await loop.create_datagram_endpoint(
                lambda: DNSServer(),
                local_addr=(address, port)
                )
        try: 
            await asyncio.sleep(1000)
        finally:
            transport.close()
    
    asyncio.run(_start())
