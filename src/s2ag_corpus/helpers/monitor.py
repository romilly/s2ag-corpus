from abc import ABC, abstractmethod


class Monitor(ABC):
    @abstractmethod
    def info(self, message: str) -> None:
        pass

    @abstractmethod
    def warn(self, message: str):
        pass

    @abstractmethod
    def debug(self, message):
        pass

    @abstractmethod
    def error(self, message):
        pass



