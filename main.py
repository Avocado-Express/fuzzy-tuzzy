import click
from typing import Optional
from pathlib import Path
from config import TOMLConfig
from process_config import process_config
from arguments import Arguments
from random import seed
from run_fuzzers import run_fuzzers


@click.command()
@click.option('--binary-directory', '-b', type=click.Path(exists=True, file_okay=False, dir_okay=True), required=True, help='Path to the directory containing the binaries')
@click.option('--corpus', '-c', type=click.Path(exists=True, file_okay=False, dir_okay=True), required=True, help='Path to the corpus file')
@click.option('--output', '-o', type=click.Path(exists=True, file_okay=False, dir_okay=True), required=True, help='Path to the fuzzing directory')
@click.option('--config', '-f', type=click.Path(exists=True, file_okay=True, dir_okay=False), default=Path('./config.toml'), help='Path to the config file')
@click.option('--dictionary', '-d', type=click.Path(exists=True, file_okay=True, dir_okay=False), help='Path to the dictionary file')
def main(binary_directory: Path,
         corpus: Path,
         output: Path,
         config: Path,
         dictionary: Optional[Path] = None):

    arguments = Arguments(binary_directory=binary_directory,
                          corpus=corpus,
                          output=output,
                          config=config,
                          dictionary=dictionary)
    
    toml = TOMLConfig.from_toml(arguments.config)
    fuzzers = process_config(toml, arguments)
    print(fuzzers)
    #run_fuzzers(fuzzers, arguments)


if __name__ == "__main__":
    main()
