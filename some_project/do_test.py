import os
import subprocess
import sys


def do_run():
    hw_tests_dir = os.path.join(os.path.dirname(__file__), 'hw_tests').replace('\\', '/')

    cmdline1 = [  # baseline
        sys.executable,
        '-m', 'pytest',
        '--argument', 'abc',
        hw_tests_dir,
        *sys.argv[1:]
    ]

    cmdline2 = [  # override testpaths
        sys.executable,
        '-m', 'pytest',
        '--argument', 'abc',
        f'--override-ini=testpaths={hw_tests_dir}',
        *sys.argv[1:]
    ]

    cmdline3 = [  # override root dir
        sys.executable,
        '-m', 'pytest',
        f'--rootdir={hw_tests_dir}',
        '--argument', 'abc',
        *sys.argv[1:]
    ]

    cmdline = cmdline1

    return subprocess.run(cmdline).returncode
