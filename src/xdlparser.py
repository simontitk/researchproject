import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element
from instructions import InstructionMapper, Instruction, StartInstruction

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

    def get_queue(self, e: Element):
        return e.attrib.get("queue", None)
    
    def has_queues(self):
        return bool(self.queues.keys())
 
    
    def parse(self, path: str):
        root_head = self.graph
        tree = ET.parse(path)
        root = tree.getroot()

        for child in root:

            q = self.get_queue(child)
            i = self.mapper.map(child.tag, **child.attrib)

            if q is None:
                if not self.has_queues():
                    root_head.add_child(i)
                    print(i, "goes to root q")
                else:
                    for qn in self.queues.values():
                        qn.add_child(i)
                    self.queues = {}
                    print(i, "closes queues")
                root_head = i

            else:
                if q not in self.queues:
                    self.queues[q] = i
                    root_head.add_child(i)
                    print(i, "starts queue")
                else:
                    self.queues[q].add_child(i)
                    self.queues[q] = i
                    print(i, "builds queue")
        return self.graph


if __name__ == "__main__":
    p = XDLParser()
    DAG = p.parse("data/example.xml")