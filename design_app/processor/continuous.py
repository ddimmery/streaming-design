from .base import Processor


class Continuous(Processor):
    def process(self, cov_dict):
        return float(
            cov_dict.get(self.var_name, self.cfg.get('missing', None))
        )
