import os
import shlex
import codecs
import shutil
import getpass
import platform
import subprocess
import multiprocessing
from sys import exit as sysexit

import memwiper

"""
coretest.py - An example of the memwiper functionality
Usage:
    python coretest.py

This script will generate 3 files:
    1) supersecretinfo.txt: contains the rot_13 encoding of your input string.
    2) core-pre.<pid>: contains the core file previous to the wipe
    3) core-pos.<pid>: contains the core file post wipe.

Requirements for the test:
    - You need a Linux host, Mac Os and windows host still pending!
    - You need to have the core files active in your system
"""


corefn = "core-{when}"
gdb_cmds = "gdb -q -ex 'set auto-solib-add 0' -ex 'attach {pid}' \
-ex 'gcore {filename}.{pid}' -ex detach -ex quit"
filter = "strings {filename} | grep <your secret string>"


def supersecretinfogenerator():
    """
    Generate a file with the rot_13(super secret string)
    """
    s = getpass.getpass("Write your secret string:")
    srot13 = codecs.encode(s, "rot_13")
    with open("supersecretinfo.txt", "w") as f:
        f.write(srot13)


def main():
    if platform.system().lower() != "linux":
        print("Sorry, currently this work only on linux.")
        sysexit(-1)
    sfromfile = None
    mypid = os.getpid()
    if shutil.which("gdb") is None:
        print("There is no gdb to use for this example! :()")
        sysexit(-1)
    # Generating the secret file:
    print("Generating the supersecretinfo.txt file:")
    p = multiprocessing.Process(target=supersecretinfogenerator)
    p.start()
    p.join()
    # Reading the contents of the file:
    with open("supersecretinfo.txt", "r") as f:
        sfromfile = f.read()
    if sfromfile is None:
        print("Well, did you write nothing? Or maybe cancel the input?")
        sysexit(-1)
    # Showing the secret:
    print("The super secret info is:", sfromfile)
    # "Decoding" the file:
    s1 = codecs.encode(sfromfile, "rot_13")
    # Generating pre-core
    print("Generating {f}.{pid}:".format(f=corefn.format(when="pre"), pid=mypid))
    cmd = gdb_cmds
    corename = corefn.format(when="pre")
    print(cmd.format(filename=corename, pid=mypid))
    subprocess.run(shlex.split(cmd.format(filename=corename, pid=mypid)))
    print("Now we're going to overwrite the memory,")
    memwiper.wipeit(s1)
    # Generating pos-core
    print("Generating {f}.{pid}:".format(f=corefn.format(when="pos"), pid=mypid))
    corename = corefn.format(when="pos")
    print(cmd.format(filename=corename, pid=mypid))
    subprocess.run(shlex.split(cmd.format(filename=corename, pid=mypid)))
    s1 = codecs.encode(sfromfile, "rot_13")
    print(
        """Well, all done now you can check the files using:

# strings core-pre.{pid} | grep '{ssi}'
# strings core-pos.{pid} | grep '{ssi}'

The core-pre.{pid} contains the secret, as object was active in memory.
The core-pos.{pid} don't contains the secret, because we wipeit() from memory.
""".format(
            pid=mypid, ssi=s1
        )
    )


if __name__ == "__main__":
    main()
