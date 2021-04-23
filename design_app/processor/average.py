from .base import Processor

import numpy as np


class Average(Processor):
    def process(self, cov_dict):
        avg = 0.0
        num = 0
        for key in self.cfg:
            try:
                avg += float(cov_dict[key])
                num += 1
            except (KeyError, ValueError):
                num += 1
        avg /= len(self.cfg)
        return avg

    def mock_value(self):
        cov_dict = {
            key: np.random.uniform(low=0, high=1) for key in self.cfg
        }
        return cov_dict
