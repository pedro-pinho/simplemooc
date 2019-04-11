from enum import Enum

class Status_Course(Enum):
    PEN = 'Pendente'
    APR = 'Aprovado'
    CAN = 'Cancelado'
    INS = 'Inscrito'

    def __str__(self):
        return self.value 