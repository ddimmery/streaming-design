from abc import abstractmethod, ABCMeta


class Processor(metaclass=ABCMeta):
    def __init__(self, var_name, cfg):
        self.var_name = var_name
        self.cfg = cfg

    @abstractmethod
    def process(self, cov_dict):
        pass

    @abstractmethod
    def mock_value(self):
        pass