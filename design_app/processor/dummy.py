from .base import Processor


class Dummy(Processor):
    def process(self, cov_dict):
        ohe = [
            float(val == cov_dict[self.var_name])
            for val in self.cfg['values']
        ]
        return ohe[1:len(ohe)]
