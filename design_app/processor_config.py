from abc import abstractmethod, ABCMeta
from itertools import chain
from typing import Iterable

from config import Config
from .processor import processor_factory


class ProcessCFG(metaclass=ABCMeta):
    @abstractmethod
    def process(self, cov_dict):
        pass


class YamlCFG(ProcessCFG):
    def process(self, cov_dict):
        defs = Config().COVARIATE_MAP

        covariate_vector = []
        for proc_name in defs.keys():
            processor_cls = processor_factory(proc_name)
            p_defs = defs[proc_name]
            for var_name, cfg in p_defs.items():
                val = processor_cls(var_name, cfg).process(cov_dict)
                if not isinstance(val, Iterable):
                    val = [val]
                covariate_vector.append(val)

        covs = [1.0] + list(chain.from_iterable(covariate_vector))
        if any(cv is None for cv in covs):
            return([0] * len(covs))
        return covs


def process_cfg_factory(config_name):
    if config_name.lower() == 'yaml':
        return YamlCFG
    else:
        raise ValueError("Unknown configurator type.")
