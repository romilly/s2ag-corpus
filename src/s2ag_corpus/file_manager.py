import os
from abc import ABC, abstractmethod

from s2ag_corpus.monitor import Monitor


class AbstractFileManager(ABC):
    @abstractmethod
    def create_path(self, base_path):
        pass

    @abstractmethod
    def write_content(self, file_path: str, content: bytes) -> None:
        pass

    @abstractmethod
    def exists(self, file_path) -> bool:
        pass


class FileManager(AbstractFileManager):
    def exists(self, file_path) -> bool:
        return os.path.exists(file_path)

    def __init__(self, monitor: Monitor):
        self.monitor = monitor

    def write_content(self, file_path: str, content: bytes) -> None:
        with open(file_path, "wb") as pf:
            pf.write(content)

    def create_path(self, base_path):
        if not os.path.exists(base_path):
            self.monitor.warn(f"directory {base_path} does not exist")
            try:
                os.makedirs(base_path)
            except Exception as e:
                self.monitor.error(f"could not create {base_path} - exception {e}")
                raise e

