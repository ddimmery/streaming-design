from abc import abstractmethod, ABCMeta
from config import Config


class Processor(metaclass=ABCMeta):
    @abstractmethod
    def process(self, cov_dict):
        pass


class ConfigProcessor(Processor):
    def process(self, cov_dict):
        defs = Config().COVARIATE_MAP

        continuous_values = []
        c_defs = defs.get('continuous', {})
        for name, cfg in c_defs.items():
            continuous_values.append(
                float(cov_dict.get(name, cfg.get('missing', None)))
            )

        dummy_values = []
        d_defs = defs.get('dummy', {})
        for name, cfg in d_defs.items():
            ohe = [
                float(val == cov_dict[name])
                for val in cfg
            ]
            dummy_values += ohe[1:len(ohe)]

        avg_values = []
        a_defs = defs.get('avg')
        for name, cfg in a_defs.items():
            print(name, cfg)
            avg = 0.0
            num = 0
            for key in cfg:
                print(key)
                try:
                    avg += float(cov_dict[key])
                    num += 1
                except (KeyError, ValueError):
                    num += 1
            avg /= len(cfg)
            avg_values.append(avg)

        covs = [1.0] + continuous_values + dummy_values
        if any(cv is None for cv in covs):
            return([0] * len(covs))
        return covs


def processor_factory(processor_name):
    if processor_name.lower() == 'config':
        return ConfigProcessor
    else:
        raise ValueError("Unknown processor name.")
