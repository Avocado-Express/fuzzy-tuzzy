from pydantic import BaseModel
from pathlib import Path
from typing import Optional

from enum import StrEnum

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


class Strategy(AFLOption):
    is_environment_variable: bool = False
    strategy_name: str

    def get_string(self) -> str:
        return f'-P {self.strategy_name}'


class ExploreStrategy(Strategy):
    strategy_name: str = 'explore'


class ExploitStrategy(Strategy):
    strategy_name: str = 'exploit'


class TypeName(StrEnum):
    ASCII = "ascii"
    BINARY = "binary"


class TypeOption(AFLOption):
    is_environment_variable: bool = False
    type_name: TypeName

    def get_string(self) -> str:
        return f'-t {self.type_name}'


class ScheduleName(StrEnum):
    EXPLORE = "explore"
    FAST = "fast"
    EXPLOIT = "exploit"
    SEEK = "seek"
    RARE = "rare"
    MMOPT = "mmopt"
    COE = "coe"
    LIN = "lin"
    QUAD = "quad"


class Schedule(AFLOption):
    is_environment_variable: bool = False
    schedule_name: ScheduleName

    def get_string(self) -> str:
        return f"-p {self.schedule_name}"

    def get_all_schedules() -> list['Schedule']:
        ret = []
        for s in ScheduleName:
            ret.append(Schedule(schedule_name=s))

        return ret