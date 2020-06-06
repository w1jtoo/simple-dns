from typing import Any

class Cache: 
    def __init__() -> None: 
        pass

    def contains(self, qname: str, qtype: str) -> bool:
        pass

    def push(self, qname: str, qtype: str, question: str, data: str) -> None:
        pass

    def get(self, qname: str, qtype: str) -> Any:
        pass

class Query: 
    # Serialize with JSON and go to DB value raw
    def __init__(self, packet:str, qtype:str, question:str) -> None: 
        self.question = question
        self.qtype = qtyp
        self.sections = []
        self.head = b''
        self.addiction = b'' 


