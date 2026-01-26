from process_config import Core
from arguments import Arguments
import libtmux


def run_fuzzers(fuzzers: list[Core], arguments: Arguments) -> None:


    server = libtmux.Server()


    session = server.new_session(session_name='fuzzing', kill_session=True)

    is_main = True
    for i, fuzzer in enumerate(fuzzers):
        cmds = ''
        env = ''
        dictionary = f"-x {arguments.dictionary}" if arguments.dictionary else ''
        fuzzer_name = ''

        for option in fuzzer.options:
            if option.is_environment_variable:
                env += option.get_string() + ' '
            else:
                cmds += option.get_string() + ' '

        if is_main:
            fuzzer_name = '-M main'
            env += 'AFL_FINAL_SYNC=1 '
            is_main = False
            window_name = 'Main'
            window = session.windows[0]
        else:
            env += 'AFL_IMPORT_FIRST=1 '
            fuzzer_name = '-S secondary-{}'.format(i)
            window_name = 'Secondary-{}'.format(i)
            window = session.new_window(attach=False,
                                        start_directory=arguments.output)

        window.rename_window(window_name)

        full_command = f"{env}afl-fuzz {fuzzer_name} -i {arguments.corpus} -o {arguments.output} {dictionary} {cmds} -- {arguments.binary_directory / 'normal'}"
        print(f"Running fuzzer with command: {full_command}")

        # full_command = f'clear;echo "{full_command}"'
        window.active_pane.send_keys(full_command)

    monitor_window = session.new_window(attach=False,
                                        window_name='Monitor')
    monitor_command = f'watch -n 300 afl-whatsup -s {arguments.output}'
    monitor_window.active_pane.send_keys(monitor_command)
