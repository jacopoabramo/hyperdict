# In this example two processes will write to an HyperDict
# with maximum speed.

import sys

sys.path.insert(0, "..")
sys.path.insert(0, "../..")

import multiprocessing
from hyperdict import HyperDict
import random
import string

name = "ultra6"


def P1():
    hyper = HyperDict(name=name)

    while True:
        hyper["P1"] = random.random()


def P2():
    hyper = HyperDict(name=name)

    while True:
        chars = "".join([random.choice(string.ascii_lowercase) for i in range(8)])
        hyper["P2"] = chars


if __name__ == "__main__":
    # Make sure the HyperDict with name='ultra6' does not exist,
    # it could be left over from a previous crash

    HyperDict.unlink_by_name(name, ignore_errors=True)

    hyper = HyperDict(
        {"P1": float(0), "P2": ""}, name=name, buffer_size=100, shared_lock=True
    )

    p1 = multiprocessing.Process(target=P1)
    p1.start()

    p2 = multiprocessing.Process(target=P2)
    p2.start()

    while True:
        print(hyper)

    p1.join()
    p2.join()
