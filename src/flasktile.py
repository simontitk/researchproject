from flask import Flask, request, jsonify
from tile import Tile
from threading import Thread
from requests import post


class TileServer:
    def __init__(self, tile: Tile, port: int) -> None:
        self.tile = tile
        self.port = port
        self.server = Flask(tile.id)
        self._add_routes()
    

    def _add_routes(self):

        @self.server.route("/")
        def index():
            return jsonify({"message": f"Service is running for tile {self.tile.id}."})
        
        @self.server.route("/status")
        def status():
            return self.tile.status
        
        @self.server.route("/execute", methods=["POST"])
        def execute():
            data = request.json
            callback_url = data["callback_url"]
            task = data["task"]
            thread = Thread(target=self.execute, args=(callback_url, task))
            thread.start()

            return jsonify({
                "message": "execution started",
                "status": self.tile.status
            })
    

    def execute(self, callback_url: str, task):
        self.tile.execute(task)
        post(url=callback_url, json={"status": self.tile.status})

        
    def run(self):
        self.server.run(port=self.port)
        print("running server")
    

    def run_thread(self):
        thread = Thread(target=self.run)
        thread.start()
        return thread
