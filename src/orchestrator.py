from enum import StrEnum

class Orchestrator:
    ...

"""
- receives the DAG representation of the synthesis process as input
- starts at the StartInstruction of the DAG and processes the subsequent ones:
    - fetch instruction
    - check if all dependencies are fulfilled
    - send out request to specified tile
    - poll the tile for fulfilment (?)
    - go to next instruction

- implemented as aiohttp client 

"""

class TileStates(StrEnum):
    READY = "ready"
    BUSY = "busy"
    ERROR = "error"


class Tile:
    def __init__(self, ip) -> None:
        self.status = TileStates.READY
        self.ip = ip
    
    def execute(self, args):
        """Method overridden in each subclass for its corresponding instructions"""
        self.status = TileStates.BUSY
        ... # mocking execution logic with some probability of error



class HeatingTile(Tile):
    ...

class UvTile(Tile):
    ...

"""
- implemented as REST API servers using Flask/FastAPI
- basic Tile class and specified subclasses
- can provide status infor:
    - ready: if free to take instructions
    - busy: if in the process of executing an instruction
    - error: if sensors detect a problem / faces network issues

"""