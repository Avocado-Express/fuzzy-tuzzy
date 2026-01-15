from pydantic import BaseModel, Field
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource
)
from typing import Tuple, Type, Optional

# https://medium.com/@wihlarkop/how-to-load-configuration-in-pydantic-3693d0ee81a3

Percentage = Field(None, ge=0, le=1)


class Instrumentation(BaseModel):
    laf: bool


class SecondaryOptions(BaseModel):
    MOpt_mutator: float = Percentage

    old_queue_cycle: float = Percentage
    disable_trimming: float = Percentage

    explore_strategy: float = Percentage
    exploit_strategy: float = Percentage

    ascii_type: float = Percentage
    binary_type: float = Percentage


class PowerSchedule(BaseModel):
    explore: Optional[float] = Percentage
    coe: Optional[float] = Percentage
    lin: Optional[float] = Percentage
    quad: Optional[float] = Percentage
    exploit: Optional[float] = Percentage
    rare: Optional[float] = Percentage


class TOMLConfig(BaseSettings):
    model_config = SettingsConfigDict(toml_file="config.toml")

    sanitisers: bool
    instrumentation: Instrumentation
    secondary_options: SecondaryOptions
    power_schedule: PowerSchedule

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (TomlConfigSettingsSource(settings_cls),)
