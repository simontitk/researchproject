class Instruction:
    """Base class for instructions extracted from XDL elements"""

    def __init__(self, queue: None) -> None:
        self.children = []
        self.queue = queue
    
    def add_child(self, child: "Instruction") -> None:
        self.children.append(child)
    
    def __repr__(self) -> str:
        return f"{self.__class__}(queue={self.queue})"


class StartInstruction(Instruction):
    """Dummy instruction class implicitly added as the root of every procedure."""
    def __init__(self, queue: None) -> None:
        super().__init__(queue)


class Add(Instruction):
    def __init__(self, vessel, reagent, amount, queue) -> None:
        super().__init__(queue)
        self.vessel = vessel
        self.reagent = reagent
        self.amount = amount


class Stir(Instruction):
    def __init__(self, vessel, time, queue) -> None:
        super().__init__(queue)
        self.vessel = vessel
        self.time = time


class Irradiate(Instruction):
    def __init__(self, vessel, time) -> None:
        super().__init__()
        self.vessel = vessel
        self.time = time


#TODO: implement other instruction classes and add them to mapper


class InstructionMapper:
    mappings = {
        "Add": Add,
        "Stir": Stir,
        "Irradiate": Irradiate,
    }

    @classmethod
    def map(cls, instruction, **kwargs) -> Instruction:
        return cls.mappings[instruction](**kwargs)
