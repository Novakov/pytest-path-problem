Pytest wrapper
===

# Setup
1. Create venv (`py -3 -m venv ./.venv`)
2. Activate venv (`./.venv/scripts/activate` or `source ./.venv/bin/activate`)
3. Install requirements (`pip install -r ./some_project/requirements.txt`)
4. Install `do_test` wrapper: `cd some_project && python ./setup.py -q develop -U`

# Contents
Simplified version of issue we hit in real-life project. This repository contains two sets of tests built with pytest: 
unit tests and hardware tests (name not important, just the distinction into two sets). Unit tests are fast and easy to 
run, hardware tests are long and require some additional setup. Hardware tests require some additional command line 
arguments (`--argument <value>` in this sample). Arguments are defined in `conftest.py` in root of the repository, so 
pytest will not complain when running unit tests with unnecessary argument.

To simplify running hardware tests there is wrapper script (installed by running `setup.py`, defined in `do_test.py`) that
automatically deduces values for required arguments and runs hardware tests. 

# Problem
Problem is related to paths in pytest. It is intended for wrapper script to work when called from any directory without 
providing path to `hw_tests` directory, in essence calling `do_test --collect-only` translates to `pytest --argument <some value> <path>/hw_tests --collect-only`.
This works nicely and is super-useful in our workflow. 

Problem arises when someone is trying to run tests from single file by specifying its path: `do_test <path>/hw_tests/test_hw_1.py`.
In that cases translated command line is: `pytest --argument <some value> <path>/hw_tests <path>/hw_tests/test_hw_1.py`
which results in invoking tests from `test_hw_1.py` **twice**. Running the same test file twice is a result of two paths 
passed to pytest: one is path in `hw_tests` directory added in wrapper script, second one is path passed by user.

# Working
* Run all HW tests:
```
> do_test 
============================================================================================= test session starts ==============================================================================================
platform win32 -- Python 3.9.1, pytest-6.2.4, py-1.10.0, pluggy-0.13.1
rootdir: d:\coding\pytest-problem
collected 4 items

hw_tests\test_hw_1.py ..                                                                                                                                                                                  [ 50%]
hw_tests\test_hw_2.py ..                                                                                                                                                                                  [100%]

============================================================================================== 4 passed in 0.02s ===============================================================================================
```

* Collect only
```
> do_test --collect-only
============================================================================================= test session starts ==============================================================================================
platform win32 -- Python 3.9.1, pytest-6.2.4, py-1.10.0, pluggy-0.13.1
rootdir: d:\coding\pytest-problem
collected 4 items

<Package hw_tests>
  <Module test_hw_1.py>
    <Function test_hw_1_a>
    <Function test_hw_1_b>
  <Module test_hw_2.py>
    <Function test_hw_2_a>
    <Function test_hw_2_b>

========================================================================================== 4 tests collected in 0.01s ==========================================================================================
```

* Filter by `-k`
```
> do_test --collect-only -k "a"
============================================================================================= test session starts ==============================================================================================
platform win32 -- Python 3.9.1, pytest-6.2.4, py-1.10.0, pluggy-0.13.1
rootdir: d:\coding\pytest-problem
collected 4 items / 2 deselected / 2 selected

<Package hw_tests>
  <Module test_hw_1.py>
    <Function test_hw_1_a>
  <Module test_hw_2.py>
    <Function test_hw_2_a>

================================================================================= 2/4 tests collected (2 deselected) in 0.01s ==================================================================================
```

# Not working
* Run tests by pointing to file
```
> do_test .\hw_tests\test_hw_1.py --collect-only
============================================================================================= test session starts ==============================================================================================
platform win32 -- Python 3.9.1, pytest-6.2.4, py-1.10.0, pluggy-0.13.1
rootdir: d:\coding\pytest-problem
collected 6 items

<Package hw_tests> # Should not be listed
  <Module test_hw_1.py>
    <Function test_hw_1_a>
    <Function test_hw_1_b>
  <Module test_hw_2.py>
    <Function test_hw_2_a>
    <Function test_hw_2_b>
<Module hw_tests/test_hw_1.py> # Only this should be listed
  <Function test_hw_1_a>
  <Function test_hw_1_b>

========================================================================================== 6 tests collected in 0.02s ==========================================================================================
```

# Tried solutions
File `do_test.py` contains few `cmdlineN` variables which generates pytest invocations according to following modifications:

* Overriding `testpaths` by adding `--override-ini=testpaths=<path>/hw_tests` (`cmdline2`)
    * Works when running with `some_project` as working directory
    * When working directory is different (e.g. repository root) fails with unrecognized arguments `--argument`
* Overriding `rootdir` by adding `--rootdir=<path>/hw_tests` (`cmdline3`)
  * Run all (hw and unit tests) when `some_project` is working directory
  * When working directory is different (e.g. repository root) fails with unrecognized arguments `--argument`
