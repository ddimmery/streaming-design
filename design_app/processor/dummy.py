from .base import Processor

import numpy as np


class Dummy(Processor):
    def process(self, cov_dict):
        ohe = [
            float(val == cov_dict.get(self.var_name, None))
            for val in self.cfg['values']
        ]
        return ohe[1:len(ohe)]

    def mock_value(self):
        val = np.random.choice(self.cfg['values'])
        return {self.var_name: val}
