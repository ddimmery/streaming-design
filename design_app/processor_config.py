from abc import abstractmethod, ABCMeta
from itertools import chain
from typing import Iterable

from config import Config
from .processor import processor_factory
from flask import current_app as app


class DummyDict(dict):
    def __getitem__(self, key):
        return dict.get(self, key, 0.0)


class ProcessCFG(metaclass=ABCMeta):
    @abstractmethod
    def process(self, cov_dict):
        pass

    @abstractmethod
    def covariate_length(self):
        pass
    
    @abstractmethod
    def mock_config(self):
        pass


class YamlCFG(ProcessCFG):
    def covariate_length(self):
        return len(self.process(DummyDict()))

    def mock_config(self):
        defs = Config().COVARIATE_MAP

        covariate_vector = []
        cov_dict = {}
        for proc_name in defs.keys():
            processor_cls = processor_factory(proc_name)
            p_defs = defs[proc_name]
            for var_name, cfg in p_defs.items():
                cov_dict.update(processor_cls(var_name, cfg).mock_value())

        return cov_dict
            

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
