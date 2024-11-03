import xml.etree.ElementTree as ET
from instructions import InstructionMapper, Instruction, StartInstruction

class XDLParser:

    def __init__(self) -> None:
        self.queues: dict[str, Instruction] = {
            None: StartInstruction()
        }


    def parse(self, path: str):
        tree = ET.parse(path)
        root = tree.getroot()

        for child in root:
            inst = InstructionMapper.map(instruction=child.tag, **child.attrib)
            
            """
            TODO: what types of synthesis/example processes to expect?
            
            """

        return self.queues[None]


if __name__ == "__main__":
    parser = XDLParser()
    xdl_dag = parser.parse("data/example.xml")