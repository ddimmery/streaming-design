from abc import abstractmethod, ABCMeta


class Design(metaclass=ABCMeta):
    @abstractmethod
    def initial_state(self):
        pass

    @abstractmethod
    def assign(self, state, covariates):
        pass

    @abstractmethod
    def backup_assign(self, state):
        pass
