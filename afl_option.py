from pydantic import BaseModel
from pathlib import Path


class AFLOption(BaseModel):
    is_environment_variable: bool

    def get_cmdline_option(self) -> str:
        raise NotImplementedError


class SAND(AFLOption):
    is_environment_variable: bool = False

    binary_dir: Path

    # Fix me
    def get_cmdline_option(self) -> str:
        return ' '.join(["-w {}".format(path)
                         for path in self.sanitiser_paths])
