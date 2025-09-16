#
# Simple counter example
#
# Two dicts `hyper` and `other` are linked together using shared memory.

import sys

sys.path.insert(0, "..")

from hyperdict import HyperDict

count = 100_000

if __name__ == "__main__":
    # No name provided to create a new dict with random name
    hyper = HyperDict(buffer_size=100_000)
    # Connect `other` dict to `hyper` dict via `name`
    other = HyperDict(name=hyper.name)

    for i in range(count // 2):
        hyper[i] = i

    for i in range(count // 2, count):
        other[i] = i

    print("Length: ", len(other), " == ", len(hyper), " == ", count)
