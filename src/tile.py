from enum import StrEnum
from time import sleep


class TileStates(StrEnum):
    READY = "ready"
    BUSY = "busy"
    ERROR = "error"


class Tile:
    def __init__(self, id: str, status: TileStates = TileStates.READY) -> None:
        self.status = status
        self.id = id
    
    def execute(self, args):
        """Method overridden in each subclass for its corresponding instructions"""
        self.status = TileStates.BUSY
        sleep(30)
        self.status = TileStates.READY
        


class HeatingTile(Tile):
    ...



class UvTile(Tile):
    ...