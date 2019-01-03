from abc import ABC, abstractmethod


class AbstractOutput(ABC):
    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def terminate(self):
        pass
