from s2ag_corpus.helpers.monitor import Monitor


class MockMonitor(Monitor):
    def __init__(self):
        self.infos = []
        self.warnings = []
        self.debugs = []
        self.errors = []

    def info(self, message: str) -> None:
        self.infos.append(message)

    def warn(self, message: str):
        self.warnings.append(message)

    def debug(self, message):
        self.debugs.append(message)

    def error(self, message):
        self.errors.append(message)

