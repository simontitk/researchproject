import xml.etree.ElementTree as ET
from os.path import isfile

from instructions import Instruction, InstructionMapper, StartInstruction


class Node:
    def __init__(self, instruction: Instruction) -> None:
        self.instruction = instruction

    
    def __repr__(self) -> str:
        name = self.instruction.__class__.__name__
        return f"Node({name}, {self.status}, queue={self.instruction.queue})"


class XDLParser:

    def __init__(self) -> None:
        self.mapper = InstructionMapper()
        self.graph = StartInstruction()
        self.queues: dict[str, Instruction] = {} 


    @staticmethod
    def _get_root(xdl: str):
        if isfile(xdl):
            return ET.parse(xdl).getroot()
        else:
            return ET.fromstring(xdl)
    

    def get_vessels(self, xdl: str) -> dict[str, str]:
        vessels: dict[str, str] = {}
        root = self._get_root(xdl)
        for element in root.iter():
            vessel = element.get("vessel")
            queue = element.get("queue")
            if vessel:
                vessels[vessel] = queue or "root"
        return vessels


    def has_queues(self):
        return bool(self.queues.keys())
    

    def parse(self, xdl: str):
        root = self._get_root(xdl)
        root_head = self.graph
        for child in root:

            i = self.mapper.map(child.tag, **child.attrib)
            q = i.queue

            if q is None:
                if not self.has_queues():
                    root_head.add_child(i)
                    i.add_dependency(root_head)
                    print(i, "goes to root q")
                else:
                    for qn in self.queues.values():
                        qn.add_child(i)
                        i.add_dependency(qn)
                    self.queues = {}
                    print(i, "closes queues")
                root_head = i

            else:
                if q not in self.queues:
                    self.queues[q] = i
                    root_head.add_child(i)
                    i.add_dependency(root_head)
                    print(i, "starts queue")
                else:
                    self.queues[q].add_child(i)
                    i.add_dependency(self.queues[q])
                    self.queues[q] = i
                    print(i, "builds queue")
        print(self.queues)
        return self.graph


if __name__ == "__main__":
    p = XDLParser()
    DAG = p.parse("data/example.xml")
