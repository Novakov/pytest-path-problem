from setuptools import setup

setup(
    name='test-entry-point',
    packages=[],
    entry_points={
        'console_scripts': [
            'do_test=do_test:do_run'
        ]
    }
)
