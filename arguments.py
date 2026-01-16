from pydantic import field_validator, BaseModel
from pathlib import Path
from typing import Optional

BINARY_NAMES = ['normal', 'san1', 'san2', 'san3']


class Arguments(BaseModel):
    binary_directory: Path
    corpus: Path
    output: Path
    dictionary: Optional[Path] = None

    @field_validator('binary_directory')
    def validate_binaries(cls, v: Path) -> Path:
        if not v.exists() or not v.is_dir():
            raise ValueError("binary_directory path must be valid directory")

        for name in BINARY_NAMES:
            binary_path = v / name
            if not binary_path.exists() or not binary_path.is_file():
                raise ValueError(f"Expected binary '{name}' not found in {v}")
        return v

    @field_validator('corpus', 'output')
    def validate_paths(cls, v: Path) -> Path:
        if not v.exists() or not v.is_dir():
            raise ValueError("Path must be an existing directory")
        return v

    @field_validator('dictionary')
    def validate_dictionary(cls, v: Optional[Path]) -> Optional[Path]:
        if v is not None and (not v.exists() or not v.is_file()):
            raise ValueError("Dictionary path must be an existing file")
        return v
