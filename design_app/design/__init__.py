from .bwd import BWDRandomizer
from .simple import SimpleRandomizer


def design_factory(design_name):
    if design_name.lower() == "bwd":
        return BWDRandomizer
    elif design_name.lower() == 'simple':
        return SimpleRandomizer
    else:
        raise ValueError("Unknown design")
