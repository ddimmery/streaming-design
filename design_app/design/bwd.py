import numpy as np

from design_app.design.base import Design


class BWDRandomizer(Design):
    def __init__(self, D=5):
        self.D = D
        self.q = 0.5
        self.value_plus = 1 - self.q
        self.value_minus = -self.q
        self.p_upper = 2 * self.q

    def initial_state(self):
        return {'w': [0] * self.D}

    def state_keys(self):
        return ['w']

    def assign(self, state, covariates):
        dot = sum(x * w for x, w in zip(covariates, state['w']))
        if dot > 1.0 * self.q:
            p_i = 0.0
        elif dot < -self.q:
            p_i = self.p_upper
        else:
            p_i = self.q - dot

        if np.random.rand() < p_i:
            assignment = 1
            new_state = {
                'w': [
                    w + self.value_plus * x
                    for w, x in zip(state['w'], covariates)
                ]
            }
        else:
            assignment = 0
            new_state = {
                'w': [
                    w + self.value_minus * x
                    for w, x in zip(state['w'], covariates)
                ]
            }
        return assignment, new_state

    def backup_assign(self, state):
        return np.random.randint(0, 1, size=1).item()
