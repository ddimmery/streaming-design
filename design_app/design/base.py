from abc import abstractmethod, ABCMeta


class Design(metaclass=ABCMeta):
    def __init__(self, D):
        self.D = D

    @abstractmethod
    def initial_state(self):
        pass

    @abstractmethod
    def state_keys(self):
        pass

    @abstractmethod
    def assign(self, state, covariates):
        pass

    @abstractmethod
    def backup_assign(self, state):
        pass
