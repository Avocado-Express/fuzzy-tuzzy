import typer
from typing import Optional
from pathlib import Path
from config import TOMLConfig
from process_config import process_config
from arguments import Arguments


def main(binary_directory: Path,
         seeds: Path,
         output: Path,
         dictionary: Optional[Path] = None):

    arguments = Arguments(binary_directory=binary_directory,
                          seeds=seeds,
                          output=output,
                          dictionary=dictionary)

    fuzzers = process_config(TOMLConfig(), arguments)


if __name__ == "__main__":
    config = TOMLConfig()
    print("Loaded configuration:", config.model_dump())
    typer.run(main)
