from pydantic import BaseModel
from pathlib import Path
from typing import Optional


BINARY_NAMES = ['normal', 'san1', 'san2', 'san3']


class AFLOption(BaseModel):
    is_environment_variable: bool

    def get_string(self) -> str:
        raise NotImplementedError


class SAND(AFLOption):
    is_environment_variable: bool = False

    binary_dir: Path

    def get_string(self) -> str:
        return ' '.join(["-w {}".format(self.binary_dir / binary)
                         for binary in BINARY_NAMES])


class CMPLOG(AFLOption):
    is_environment_variable: bool = False

    cmplog_binary: Path
    cmplog_options: Optional[str] = None

    def get_string(self) -> str:
        if self.cmplog_options is None:
            return "-c {}".format(self.cmplog_binary)
        return "-c {} -l {}".format(self.cmplog_binary, self.cmplog_options)


class MOptMutator(AFLOption):
    is_environment_variable: bool = False

    def get_string(self) -> str:
        return '-L 0'


class OldQueueCycle(AFLOption):
    is_environment_variable: bool = False

    def get_string(self) -> str:
        return '-Z'


class DisableTrimming(AFLOption):
    is_environment_variable: bool = True

    def get_string(self) -> str:
        return 'AFL_DISABLE_TRIM=1'


class ExploreStrategy(AFLOption):
    is_environment_variable: bool = False

    def get_string(self) -> str:
        return '-P explore'


class ExploitStrategy(AFLOption):
    is_environment_variable: bool = False

    def get_string(self) -> str:
        return '-P exploit'


class AsciiType(AFLOption):
    is_environment_variable: bool = False

    def get_string(self) -> str:
        return '-a ascii'


class BinaryType(AFLOption):
    is_environment_variable: bool = False

    def get_string(self) -> str:
        return '-a binary'
