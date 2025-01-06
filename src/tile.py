from enum import StrEnum
from time import sleep


class TileStates(StrEnum):
    READY = "ready"
    BUSY = "busy"
    ERROR = "error"


class Tile:
    def __init__(self, id: str, status: TileStates = TileStates.READY) -> None:
        self.status = status
        self.params = {}
        self.id = id
    
    def execute(self, params):
        """Method overridden in each subclass for its corresponding instructions"""
        self.status = TileStates.BUSY
        self.params = params
        sleep(15)
        self.status = TileStates.READY
        self.params = {}
        


class HeatingTile(Tile):
    ...



class UvTile(Tile):
    ...