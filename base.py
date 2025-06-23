from abc import ABC, abstractmethod

class OutputStrategy(ABC):
    @abstractmethod
    def write(self, data):
        pass
