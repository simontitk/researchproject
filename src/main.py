from flasktile import TileServer
from orchestrator import Orchestrator
from tile import Tile, TileStates

if __name__ == "__main__":

    tile_map = {
        "RootReactor": 5001,
        "AReactor": 5002,
        "BReactor": 5003,
    }

    orc = Orchestrator(port="5000", tile_map=tile_map, reaction_xml="data/example.xml")
    tile1 = Tile(id="RootReactor")
    tile2 = Tile(id="AReactor")
    tile3 = Tile(id="BReactor")
    server1 = TileServer(tile=tile1, port=tile_map[tile1.id])
    server2 = TileServer(tile=tile2, port=tile_map[tile2.id])
    server3 = TileServer(tile=tile2, port=tile_map[tile3.id])
    t0 = orc.run_thread()
    t1 = server1.run_thread()
    t2 = server2.run_thread()
    t3 = server3.run_thread()
    t0.join()
    t1.join()
    t2.join()
    t3.join()
