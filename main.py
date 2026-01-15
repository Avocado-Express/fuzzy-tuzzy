from pydantic_cli import run_and_exit
from config import TOMLConfig
from arguments import Options


if __name__ == "__main__":
    config = TOMLConfig()
    print("Loaded configuration:", config.model_dump())
    run_and_exit(Options, version="0.1.0")
