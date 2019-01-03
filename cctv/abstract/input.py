from abc import ABC, abstractmethod


class AbstractInput(ABC):
    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def cleanup(self):
        pass

    @abstractmethod
    def set_callback(self):
        pass
