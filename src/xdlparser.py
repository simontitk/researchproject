import xml.etree.ElementTree as ET

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

    
    def has_queues(self):
        return bool(self.queues.keys())
 

    def parse_file(self, path: str):
        root = ET.parse(path).getroot()
        self._parse(root)


    def parse_str(self, content: str):
        root = ET.fromstring(content)
        self._parse(root)
    

    def _parse(self, root: ET.Element):
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
        return self.graph


if __name__ == "__main__":
    p = XDLParser()
    DAG = p.parse("data/example.xml")