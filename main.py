import typer
from typing import Optional
from pathlib import Path
from config import TOMLConfig
from process_config import process_config
from arguments import Arguments
from random import seed
from run_fuzzers import run_fuzzers


def main(binary_directory: Path,
         corpus: Path,
         output: Path,
         dictionary: Optional[Path] = None):

    arguments = Arguments(binary_directory=binary_directory,
                          corpus=corpus,
                          output=output,
                          dictionary=dictionary)

    fuzzers = process_config(TOMLConfig(), arguments)
    run_fuzzers(fuzzers, arguments)


if __name__ == "__main__":
    typer.run(main)
