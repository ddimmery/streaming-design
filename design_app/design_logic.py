from abc import abstractmethod, ABCMeta
from typing import Iterable
import numpy as np
import pandas as pd


class Processor(metaclass=ABCMeta):
    @abstractmethod
    def process(self, cov_dict):
        pass


class BasicProcessor(Processor):
    def process(self, cov_dict):
        df = pd.DataFrame(cov_dict, index=[0])
        covariate_map = {
            'gender': ['Male', 'Female', 'Non-binary', 'Other'],
            'ideology': 'float',
        }

        cov_array = [1.0]
        for cov, values in covariate_map.items():
            if values == 'float':
                cov_array.append(float(df[cov].item()))
            elif isinstance(values, Iterable):
                ohe = [
                    float(val == df[cov].values.item()) 
                    for val in values
                ]
                cov_array += ohe[1:len(ohe)]
            else:
                raise ValueError("Unknown value in covariate_map")
        return cov_array


class Design(metaclass=ABCMeta):
    @abstractmethod
    def initial_state(self):
        pass

    @abstractmethod
    def assign(self, state, covariates):
        pass


class SimpleRandomizer(Design):
    def initial_state(self):
        return {}

    def assign(self, state, covariates):
        return np.random.randint(0, 1, size=1).item(), {}


class BWDRandomizer(Design):
    def __init__(self):
        self.D = 5
        self.q = 0.5
        self.value_plus = 1 - self.q
        self.value_minus = -self.q
        self.p_upper = 2 * self.q
    
    def initial_state(self):
        return {'w': [0] * self.D}

    def assign(self, state, xs):
        dot = sum(x * w for x, w in zip(xs, state['w']))
        if dot > 1.0 * self.q:
            p_i = 0.0
        elif dot < -self.q:
            p_i = self.p_upper
        else:
            p_i = self.q - dot

        if np.random.rand() < p_i:
            assignment = 1
            new_state = {'w': [w + self.value_plus * x for w, x in zip(state['w'], xs)]}
        else:
            assignment = 0
            new_state = {'w': [w + self.value_minus * x for w, x in zip(state['w'], xs)]}
        return assignment, new_state

    
class BasicSimple(BasicProcessor, SimpleRandomizer):
    pass


class BasicBWD(BasicProcessor, BWDRandomizer):
    pass