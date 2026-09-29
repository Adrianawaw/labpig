from abc import ABC, abstractmethod


class Interface(ABC):
    @abstractmethod
    def set_parameters(self, params, values):
        pass

    @abstractmethod
    def get_parameters(self, params):
        pass
