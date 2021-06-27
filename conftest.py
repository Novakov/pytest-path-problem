# type: ignore
def pytest_addoption(parser):
    parser.addoption('--argument', action='store', required=True, help='Argument passed to tests')
