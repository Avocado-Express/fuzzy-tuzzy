from pydantic import BaseModel
from pathlib import Path
from typing import Optional


binary_names = ['normal', 'san1', 'san2', 'san3']


class AFLOption(BaseModel):
    is_environment_variable: bool

    def get_cmdline_option(self) -> str:
        raise NotImplementedError


class SAND(AFLOption):
    is_environment_variable: bool = False

    binary_dir: Path

    def get_cmdline_option(self) -> str:
        return ' '.join(["-w {}".format(self.binary_dir / binary)
                         for binary in binary_names])


class CMPLOG(AFLOption):
    is_environment_variable: bool = False

    cmplog_binary: Path
    cmplog_options: Optional[str] = None

    def get_cmdline_option(self) -> str:
        if self.cmplog_options is None:
            return "-c {}".format(self.cmplog_binary)
        return "-c {} -l {}".format(self.cmplog_binary, self.cmplog_options)
