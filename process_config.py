from config import TOMLConfig
from multiprocessing import cpu_count
from afl_option import SAND, AFLOption, CMPLOG
from random import choice
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
