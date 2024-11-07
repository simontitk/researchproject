from enum import StrEnum
import requests
from flask import Flask, jsonify, request, render_template
import os


class Orchestrator:
    """
    - receives the DAG representation of the synthesis process as input
    - starts at the StartInstruction of the DAG and processes the subsequent ones:
        - fetch instruction
        - check if all dependencies are fulfilled
        - send out request to specified tile
        - poll the tile for fulfilment (?)
        - go to next instruction
    """

    def __init__(self, port: int) -> None:
        self.server = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), '../templates'))
        self.port = port
        self._add_routes()


    def _add_routes(self):

        @self.server.route("/")
        def index():
            return render_template("overview.html")


        @self.server.route("/send")
        def send():
            self.send_instruction("http://localhost:5001/execute")
            return "", 200
        

        @self.server.route("/callback", methods=["POST"])
        def callback():
            return 


    def send_instruction(self, address):
        data = {
            "callback_url": f"http://localhost:{self.port}/callback",
            "task": "do it",
        }
        response = requests.post(address, json=data)


    def run(self):
        self.server.run(port=self.port, debug=True)


if __name__ == "__main__":
    o = Orchestrator(port=5000)
    o.run()
