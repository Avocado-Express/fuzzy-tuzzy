from pydantic_cli import run_and_exit, Cmd
from config import TOMLConfig


class Options(Cmd):

    def run(self) -> None:
        print("Mock example running with ")


if __name__ == "__main__":
    config = TOMLConfig()
    print("Loaded configuration:", config.model_dump())
    run_and_exit(Options, version="0.1.0")
