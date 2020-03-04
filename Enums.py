from enum import Enum


class ObjTypes(Enum):
    Empty = 0,
    Border = 1,
    Liver = 2,
    Food = 3,
    Poison = 4,
    Corpse = 5


class LiverStatus(Enum):
    Corpse = 0,
    Alive = 1,
    Child = 2
