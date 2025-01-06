from xdlparser import XDLParser
from tile import Tile
from flasktile import TileServer
from orchestrator import Orchestrator
from flask import Flask, request, jsonify
from flask_cors import CORS


class EntryPoint:

    def __init__(self, port: int):
        self.server = Flask(__name__)
        CORS(self.server)
        self.port = port
        self.parser = XDLParser()
        self.server
        self._add_routes()

    def _add_routes(self) -> None:

        @self.server.route("/", methods=["POST"])
        def process():
            xdl = request.json
            vessels = self.parser.get_vessels(xdl)
            url = request.base_url[:-6]
            for i, vessel in enumerate(vessels):
                tile = Tile(id=vessel["vessel"])
                port = self.port + i + 1
                server = TileServer(tile, port)
                thread = server.run_thread()
                vessel["port"] = port
                vessel["url"] = url

            port_o = port = self.port + i + 2
            orchestrator = Orchestrator(port=port_o, tile_map=vessels, reaction_xml=xdl)
            orchestrator.run_thread()

            response = {
                "vessels": vessels,
                "orchestrator": {"port": port_o, "url": url},
            }
            return jsonify(response)

    def run(self) -> None:
        self.server.run(port=self.port)


if __name__ == "__main__":
    ep = EntryPoint(port=5000)
    ep.run()
