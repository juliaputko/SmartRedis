# BSD 2-Clause License
#
# Copyright (c) 2021-2023, Hewlett Packard Enterprise
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import pytest
from os import path as osp
from os import getcwd
from glob import glob
from subprocess import Popen, PIPE, TimeoutExpired
import time

RANKS = 1
TEST_PATH = osp.dirname(osp.abspath(__file__))

def get_test_names():
    """Obtain test names by globbing for client_test
    Add tests manually if necessary
    """
    glob_path_1 = osp.join(TEST_PATH, "*/*/example*")
    glob_path_2 = osp.join(TEST_PATH, "*/*/smartredis*")
    test_names = glob(glob_path_1) + glob(glob_path_2)
    test_names = list(filter(lambda test: test.find('example_utils') == -1, test_names))
    test_names = list(filter(lambda test: test.find('.py') == -1, test_names))
    test_names = [(pytest.param(test,
                                id=osp.basename(test))) for test in test_names]
    return test_names

@pytest.mark.parametrize("test", get_test_names())
def test_example(test, build, sr_fortran, link):
    if (sr_fortran == "ON" or ".F90" not in test):
        # Build the path to the test executable from the source file name
        # . keep only the last three parts of the path: (parallel/serial, language, basename)
        test = "/".join(test.split("/")[-3:])
        test_subdir = "/".join(test.split("/")[0:2])
        # . drop the file extension
        test = ".".join(test.split(".")[:-1])
        # . prepend the path to the built test executable
        test = f"{getcwd()}/build/{build}/examples/{link}/{test}"
        cmd = ["mpirun", "-n", "2"] if "parallel" in test else []
        cmd += [test]
        print(f"Running test: {osp.basename(test)}")
        print(f"Test command {' '.join(cmd)}")
        execute_cmd(cmd, test_subdir)
        time.sleep(1)
    else:
        print (f"Skipping Fortran test {test}")

def execute_cmd(cmd_list, test_subdir):
    """Execute a command """

    # spawning the subprocess and connecting to its output
    run_path = TEST_PATH + "/" + test_subdir
    print(f"Test path: {run_path}")
    proc = Popen(
        cmd_list, stderr=PIPE, stdout=PIPE, stdin=PIPE, cwd=run_path)
    try:
        out, err = proc.communicate(timeout=120)
        if out:
            print("OUTPUT:", out.decode("utf-8"))
        if err:
            print("ERROR:", err.decode("utf-8"))
        assert(proc.returncode == 0)
    except UnicodeDecodeError:
        output, errs = proc.communicate()
        print("ERROR:", errs.decode("utf-8"))
        assert(False)
    except TimeoutExpired:
        proc.kill()
        output, errs = proc.communicate()
        print("TIMEOUT: test timed out after test timeout limit of 120 seconds")
        print("OUTPUT:", output.decode("utf-8"))
        print("ERROR:", errs.decode("utf-8"))
        assert(False)
    except Exception:
        proc.kill()
        output, errs = proc.communicate()
        print("OUTPUT:", output.decode("utf-8"))
        print("ERROR:", errs.decode("utf-8"))
        assert(False)
