from .continuous import Continuous
from .dummy import Dummy
from .average import Average


def processor_factory(processor_name):
    if processor_name.lower() == 'continuous':
        return Continuous
    elif processor_name.lower() == 'dummy':
        return Dummy
    elif processor_name.lower() == 'avg':
        return Average
    else:
        raise ValueError("Unknown processor type.")
