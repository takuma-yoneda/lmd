#!/usr/bin/env python3
import os
from os.path import join as pjoin
import sys
import argparse
import pathlib

import tel
from tel import __version__
from tel.config import DockerContainerConfig, SlurmConfig
from tel.helpers import find_project_root
from tel.machine import SSHMachine, DockerMachine, SlurmMachine

from tel.cli.commands.run import CLIRunCommand
from simple_slurm_command import SlurmCommand

_supported_commands = {
    'run': CLIRunCommand
    # 'create': CLICreateCommand,
    # 'info': CLIInfoCommand,
    # 'build': CLIBuildCommand,
    # 'run': CLIRunCommand,
    # 'clean': CLICleanCommand,
    # 'push': CLIPushCommand,
    # 'decorate': CLIDecorateCommand,
    # 'machine': CLIMachineCommand,
    # 'endpoint': CLIEndpointCommand,
}

def run():
    """
    - Read config file
    - Collect local project repo info (root directory, etc)
    - parse args and pass them to a proper subcommand
    """

    print(f"tel - Remote code execution for ML researchers - v{tel.__version__}")
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        'command',
        choices=_supported_commands.keys()
    )
    # print help (if needed)
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help']:
        parser.print_help()
        return
    # ---
    # parse `command`
    parsed, remaining = parser.parse_known_args()
    print(f'main.py -- parsed: {parsed}\tremaining:{remaining}')
    # get command
    command = _supported_commands[parsed.command]
    # let the command parse its arguments
    cmd_parser = command.get_parser(remaining)
    parsed = cmd_parser.parse_args(remaining)
    # sanitize workdir

    # TODO: find a correct project directory
    parsed.workdir = find_project_root()
    current_dir = pathlib.Path(os.getcwd()).resolve()
    relative_workdir = current_dir.relative_to(parsed.workdir)
    print('Project root directory:', parsed.workdir)
    print('relative working dir:', relative_workdir)  # cwd.relative_to(project_root)
    parsed.name = parsed.workdir.stem

    # Read from tel config file and reflect it
    # TODO: clean this up
    from tel.helpers import parse_config
    config = parse_config(parsed.workdir)

    command.execute(config, parsed, relative_workdir=relative_workdir)

if __name__ == '__main__':
    run()
