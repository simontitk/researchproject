import os
from collections import deque
from threading import Thread

import requests
from flask import Flask, jsonify, render_template, request

from flask_cors import CORS
from instructions import Instruction, InstructionStatus
from xdlparser import XDLParser


class Orchestrator:

    def __init__(self, port: int, tile_map: dict[str, dict], reaction_xml: str) -> None:
        self.DAG = XDLParser().parse(reaction_xml)
        self.server = Flask(__name__)
        CORS(self.server)
        self.port = port
        self.tile_map = {vessel["vessel"]: vessel["port"] for vessel in tile_map}
        self._add_routes()


    def _add_routes(self) -> None:

        @self.server.route("/")
        def index():
            return jsonify({"message": f"Service is running for orchestrator at port {self.port}."})
        

        @self.server.route("/start", methods=["POST"])
        def start(): 
            self.process_instruction(self.DAG)
            return jsonify("Execution started.")


        @self.server.route("/send")
        def send():
            self.send_instruction("http://localhost:5001/execute")
            print("THIS ENDPOINT DID SOMETHING")
            return "", 200
        

        @self.server.route("/callback", methods=["POST"])
        def callback():
            data = request.json 
            finished_instruction = self.find(data["task_id"])
            finished_instruction.status = InstructionStatus.DONE
            self.process_instruction(finished_instruction)
            return "", 200
        

    def process_instruction(self, instruction: Instruction) -> None:
        for child in instruction.children:
            if all([dep.status == InstructionStatus.DONE for dep in child.dependencies]) & (child.status == InstructionStatus.NOT_STARTED):
                self.send_instruction(child)


    def send_instruction(self, instruction: Instruction) -> None:
        data = {
            "callback_url": f"http://localhost:{self.port}/callback",
            "task_id": instruction.id,
            "task": instruction.to_json(),
        }
        port = self.tile_map[instruction.vessel]
        response = requests.post(f"http://localhost:{port}/execute", json=data)
        instruction.status = InstructionStatus.STARTED


    def find(self, instruction_id: int) -> Instruction:
            visited = set()  
            queue = deque([self.DAG])  
            while queue:
                node = queue.popleft()
                if node.id == instruction_id:
                    return node
                visited.add(node)
                for child in node.children:
                    if child not in visited:
                        queue.append(child)
            return None


    def run(self) -> None:
        self.server.run(port=self.port)
    

    def run_thread(self) -> Thread:
        thread = Thread(target=self.run)
        thread.start()
        return thread