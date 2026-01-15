from pydantic import field_validator
from pathlib import Path
from pydantic_cli import Cmd
from typing import Optional
from config import TOMLConfig
from process_config import process_config

binary_names = ['normal', 'san1', 'san2', 'san3']


class Options(Cmd):
    binary_directory: Path
    seeds: Path
    output: Path
    dictionary: Optional[Path] = None

    def run(self) -> None:
        process_config(TOMLConfig(), self)
        print("Mock example running with ")

    @field_validator('binary_directory')
    def validate_binaries(cls, v: Path) -> Path:
        if not v.exists() or not v.is_dir():
            raise ValueError("binary_directory path must be an existing directory")

        for name in binary_names:
            binary_path = v / name
            if not binary_path.exists() or not binary_path.is_file():
                raise ValueError(f"Expected binary '{name}' not found in {v}")
        return v

    @field_validator('seeds', 'output')
    def validate_paths(cls, v: Path) -> Path:
        if not v.exists() or not v.is_dir():
            raise ValueError("Path must be an existing directory")
        return v

    @field_validator('dictionary')
    def validate_dictionary(cls, v: Optional[Path]) -> Optional[Path]:
        if v is not None and (not v.exists() or not v.is_file()):
            raise ValueError("Dictionary path must be an existing file")
        return v
