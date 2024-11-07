from enum import StrEnum


class InstructionStatus(StrEnum):
    DONE = "done"
    STARTED = "started"
    NOT_STARTED = "not_started"


class Instruction:
    """Base class for instructions extracted from XDL elements"""
    id = 0
    def __init__(self, queue=None) -> None:
        self.queue = queue
        self.dependencies: list[Instruction]= []
        self.children: list[Instruction] = []
        self.status = InstructionStatus.NOT_STARTED
        self.id = Instruction.id
        Instruction.id += 1
    

    def add_child(self, instruction: "Instruction") -> None:
        self.children.append(instruction)

    
    def __repr__(self) -> str:
        name = self.__class__.__name__
        return f"{name}(queue={self.queue})"


class StartInstruction(Instruction):
    """Dummy instruction class implicitly added as the root of every procedure."""
    def __init__(self) -> None:
        super().__init__()


class Add(Instruction):
    def __init__(self, vessel, reagent, amount, queue=None) -> None:
        super().__init__(queue)
        self.vessel = vessel
        self.reagent = reagent
        self.amount = amount


class Stir(Instruction):
    def __init__(self, vessel, time, queue=None) -> None:
        super().__init__(queue)
        self.vessel = vessel
        self.time = time


class Irradiate(Instruction):
    def __init__(self, vessel, time) -> None:
        super().__init__()
        self.vessel = vessel
        self.time = time


class InstructionMapper:
    mappings: dict[str] = {
        "Add": Add,
        "Stir": Stir,
        "Irradiate": Irradiate,
    }

    @classmethod
    def map(cls, instruction: str, **kwargs) -> Instruction:
        return cls.mappings[instruction](**kwargs)
