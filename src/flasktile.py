from threading import Thread

from flask import Flask, jsonify, request
from requests import post

from tile import Tile


class TileServer:
    def __init__(self, tile: Tile, port: int) -> None:
        self.tile = tile
        self.port = port
        self.server = Flask(tile.id)
        self._add_routes()
    

    def _add_routes(self) -> None:

        @self.server.route("/")
        def index():
            return jsonify({"message": f"Service is running for tile {self.tile.id}."})
        
        @self.server.route("/status")
        def status():
            return self.tile.status
        
        @self.server.route("/execute", methods=["POST"])
        def execute():
            data = request.json
            thread = Thread(target=self.execute, args=(data,))
            thread.start()

            return jsonify({
                "message": "execution started",
                "status": self.tile.status
            })
    

    def execute(self, data: dict) -> None:
        self.tile.execute(data["task"])
        post(url=data["callback_url"], json={
            "status": self.tile.status,
            "task_id": data["task_id"]
        })

        
    def run(self) -> None:
        self.server.run(port=self.port)
        print("running server")
    

    def run_thread(self) -> None:
        thread = Thread(target=self.run)
        thread.start()
        return thread
