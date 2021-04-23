from .base import Processor

import numpy as np


class Continuous(Processor):
    def process(self, cov_dict):
        return float(
            cov_dict.get(self.var_name, self.cfg.get('missing', None))
        )

    def mock_value(self):
        return {self.var_name: np.random.uniform(low=0, high=1)}
