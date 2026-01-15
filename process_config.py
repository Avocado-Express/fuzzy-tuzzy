from config import TOMLConfig
from multiprocessing import cpu_count
from afl_option import SAND
from random import choice
from arguments import Options


class Core():
    '''Fuzzer options for a single core'''

    options: list[any]

    def __init__(self):
        self.options = []

    def add_option(self, option: any) -> None:
        self.options.append(option)


def process_config(config: TOMLConfig, options: Options) -> list[Core]:

    cores = cpu_count()
    if cores < 8:
        print("Why are trying to do this")
        exit(1)

    fuzzers = [Core() for _ in range(cores)]

    # Sanitisers
    if config.sanitisers:
        choice(fuzzers).add_option(SAND(binary_dir=options.binary_directory))
