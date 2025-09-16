#
# Simple counter example
#
# Two dicts `ultra` and `other` are linked together using shared memory.

import sys

sys.path.insert(0, "..")

from hyperdict import HyperDict

count = 100_000

if __name__ == "__main__":
    # No name provided to create a new dict with random name
    ultra = HyperDict(buffer_size=100_000)
    # Connect `other` dict to `ultra` dict via `name`
    other = HyperDict(name=ultra.name)

    for i in range(count // 2):
        ultra[i] = i

    for i in range(count // 2, count):
        other[i] = i

    print("Length: ", len(other), " == ", len(ultra), " == ", count)
