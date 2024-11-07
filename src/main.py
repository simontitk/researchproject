from flasktile import TileServer
from tile import Tile, TileStates


if __name__ == "__main__":
    tile1 = Tile(id="111")
    tile2 = Tile(id="222", status=TileStates.ERROR)
    server1 = TileServer(tile=tile1, port="5001")
    server2 = TileServer(tile=tile2, port="5002")
    t1 = server1.run_thread()
    t2 = server2.run_thread()
    t1.join()
    t2.join()
