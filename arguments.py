from pydantic import field_validator, BaseModel
from pathlib import Path
from typing import Optional

BINARY_NAMES = ['normal', 'san1', 'san2', 'san3']


class Arguments(BaseModel):
    binary_directory: Path
    corpus: Path
    output: Path
    config: Path
    dictionary: Optional[Path] = None

    @field_validator('binary_directory')
    def validate_binaries(cls, v: Path) -> Path:
        for name in BINARY_NAMES:
            binary_path = v / name
            if not binary_path.exists() or not binary_path.is_file():
                raise ValueError(f"Expected binary '{name}' not found in {v}")
        return v