from s2ag_corpus.file_manager import AbstractFileManager


class MockFileManager(AbstractFileManager):
    def __init__(self):
        self.files = {}

    def create_path(self, base_path):
        pass

    def write_content(self, file_path: str, content: bytes) -> None:
        self.files[file_path] = content

    def exists(self, file_path) -> bool:
        return file_path in self.files

