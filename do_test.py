import os
import subprocess
import sys


def do_run():
    hw_tests_dir = os.path.join(os.path.dirname(__file__), 'hw_tests')
    cmdline = [
        sys.executable,
        '-m', 'pytest',
        '--argument', 'abc',
        hw_tests_dir,
        *sys.argv[1:]
    ]

    return subprocess.run(cmdline).returncode
