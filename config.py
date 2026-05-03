from pathlib import Path
from typing import Optional
from pydantic import BaseModel, Field
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
    TomlConfigSettingsSource,
)

# https://medium.com/@wihlarkop/how-to-load-configuration-in-pydantic-3693d0ee81a3

class Instrumentation(BaseModel):
    laf: bool
    cmplog: bool
    cmplog_options: Optional[list[str]] = None


class SecondaryOptions(BaseModel):
    MOpt_mutator: float | None = Field(None, ge=0, le=1)

    old_queue_cycle: float | None = Field(None, ge=0, le=1)
    disable_trimming: float | None = Field(None, ge=0, le=1)

    explore_strategy: float | None = Field(None, ge=0, le=1)
    exploit_strategy: float | None = Field(None, ge=0, le=1)

    ascii_type: float | None = Field(None, ge=0, le=1)
    binary_type: float | None = Field(None, ge=0, le=1)


class PowerSchedule(BaseModel):
    explore: float | None = Field(None, ge=0, le=1)
    fast: float | None = Field(None, ge=0, le=1)
    exploit: float | None = Field(None, ge=0, le=1)
    seek: float | None = Field(None, ge=0, le=1)
    rare: float | None = Field(None, ge=0, le=1)
    mmopt: float | None = Field(None, ge=0, le=1)
    coe: float | None = Field(None, ge=0, le=1)
    lin: float | None = Field(None, ge=0, le=1)
    quad: float | None = Field(None, ge=0, le=1)


class TOMLConfig(BaseSettings):
    sanitisers: bool
    instrumentation: Instrumentation
    secondary_options: SecondaryOptions
    power_schedule: PowerSchedule

    model_config = SettingsConfigDict()

    _toml_path: str = "config.toml"

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls,
        init_settings,
        env_settings,
        dotenv_settings,
        file_secret_settings,
    ):
        return (
            TomlConfigSettingsSource(settings_cls, cls._toml_path),
        )

    @classmethod
    def from_toml(cls, path: Path):
        cls._toml_path = path.absolute().as_posix()
        return cls()
