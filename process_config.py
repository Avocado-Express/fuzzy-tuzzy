from config import TOMLConfig
from multiprocessing import cpu_count
from afl_option import (
    SAND,
    AFLOption,
    CMPLOG,
    MOptMutator,
    OldQueueCycle,
    DisableTrimming,
    ExploreStrategy,
    ExploitStrategy,
    AsciiType,
    BinaryType
)
from random import choice, sample
from pathlib import Path
from typing import Optional
from arguments import Arguments
from pydantic import BaseModel


class Core(BaseModel):
    '''Fuzzer options for a single core'''

    options: list[AFLOption] = []
    binary: Optional[Path] = None

    # def add_option(self, option: any) -> None:
    #     self.options.append(option)


def process_config(config: TOMLConfig, arguments: Arguments) -> list[Core]:

    def add_to_random_core(option: AFLOption) -> None:
        choice(fuzzers).options.append(option)

    def random_fuzzers_by_percent(percent: float) -> list[Core]:
        # Get a random sample of fuzzers based on percentage
        n_cores = round(percent * cores)
        return sample(fuzzers, k=n_cores)

    cores = cpu_count()
    if cores < 8:
        print("Why are trying to do this")
        exit(1)

    fuzzers = [Core() for _ in range(cores)]

    # Sanitisers
    if config.sanitisers:
        add_to_random_core(SAND(binary_dir=arguments.binary_directory))

    # Instrumentation
    if config.instrumentation.laf:
        laf_binary_path = arguments.binary_directory / 'laf'
        # Check file exists
        if not (laf_binary_path).exists():
            raise FileNotFoundError(
                f"LAF binary not found at {laf_binary_path}"
            )
        choice([f for f in fuzzers if
                f.binary is None]).binary = laf_binary_path

    if config.instrumentation.cmplog:
        cmplog_binary_path = arguments.binary_directory / 'cmplog'
        # Check file exists
        if not (cmplog_binary_path).exists():
            raise FileNotFoundError(
                f"Cmplog binary not found at {cmplog_binary_path}"
            )

        # If no options, just add one CMPLOG without options
        if config.instrumentation.cmplog_options is None:
            add_to_random_core(CMPLOG(
                cmplog_binary=cmplog_binary_path))
        else:
            for option in config.instrumentation.cmplog_options:
                add_to_random_core(
                    CMPLOG(
                        cmplog_binary=cmplog_binary_path,
                        cmplog_options=option
                    )
                )

    secondary_options = config.secondary_options
    for i in random_fuzzers_by_percent(secondary_options.MOpt_mutator):
        i.options.append(MOptMutator())

    for i in random_fuzzers_by_percent(secondary_options.old_queue_cycle):
        i.options.append(OldQueueCycle())

    for i in random_fuzzers_by_percent(secondary_options.disable_trimming):
        i.options.append(DisableTrimming())

    for i in random_fuzzers_by_percent(secondary_options.explore_strategy):
        i.options.append(ExploreStrategy())

    no_strategy_fuzzers = [f for f in fuzzers if
                           not any(isinstance(opt, ExploreStrategy)
                                   or isinstance(opt, ExploitStrategy)
                                   for opt in f.options)]

    exploit_cores = round(secondary_options.exploit_strategy * cores)
    for i in sample(no_strategy_fuzzers, k=exploit_cores):
        i.options.append(ExploitStrategy())

    for i in random_fuzzers_by_percent(secondary_options.ascii_type):
        i.options.append(AsciiType())

    no_type_fuzzers = [f for f in fuzzers if
                       not any(isinstance(opt, AsciiType)
                               or isinstance(opt, BinaryType)
                               for opt in f.options)]

    binary_type_cores = round(secondary_options.binary_type * cores)
    for i in sample(no_type_fuzzers, k=binary_type_cores):
        i.options.append(BinaryType())

    return fuzzers
