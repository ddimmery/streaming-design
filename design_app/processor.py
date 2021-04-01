from abc import abstractmethod, ABCMeta
from typing import Iterable
from config import Config


class Processor(metaclass=ABCMeta):
    @abstractmethod
    def process(self, cov_dict):
        pass


class ConfigProcessor(Processor):
    def process(self, cov_dict):
        covariate_map = Config().COVARIATE_MAP

        cov_array = [1.0]
        for cov, values in covariate_map.items():
            if values == 'float':
                cov_array.append(float(cov_dict[cov]))
            elif isinstance(values, Iterable):
                ohe = [
                    float(val == cov_dict[cov])
                    for val in values
                ]
                cov_array += ohe[1:len(ohe)]
            else:
                raise ValueError("Unknown value in covariate_map")
        return cov_array


def processor_factory(processor_name):
    if processor_name.lower() == 'config':
        return ConfigProcessor
    else:
        raise ValueError("Unknown processor name.")
