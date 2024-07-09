import os
from dataclasses import dataclass, field
from typing import Optional, Union

import psycopg2.extensions

from s2ag_corpus.helpers.file_manager import AbstractFileManager
from s2ag_corpus.helpers.logging_monitor import LoggingMonitor
from s2ag_corpus.helpers.monitor import Monitor
from s2ag_corpus.api import AbstractAPI
from test.test.s2ag_corpus.helpers.mock_monitor import MockMonitor


@dataclass
class SyncConfig:
    base_dir: Optional[str]  = field(default=None)
    connection: Optional[psycopg2.extensions.connection] = field(default=None)
    monitor: Optional[Union[MockMonitor|LoggingMonitor]] = field(default=None)
    api: Optional[AbstractAPI] = field(default=None)
    filemanager: Optional[AbstractFileManager] = field(default=None)

    @property
    def datasets_dir(self):
        return os.path.join(self.base_dir, 'datasets')

    @property
    def diffs_dir(self):
        return os.path.join(self.base_dir, 'diffs')