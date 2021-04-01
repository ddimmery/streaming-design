import numpy as np

from design_app.design.base import Design


class SimpleRandomizer(Design):
    def initial_state(self):
        return {}

    def assign(self, state, covariates):
        return np.random.randint(0, 1, size=1).item(), {}
