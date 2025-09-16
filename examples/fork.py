#
# Two processes incrementing a counter in parallel
#
# This only without shared_lock, using multiprocessing.RLock() internally.
# This is much faster than the spawn alterntive.
#
from hyperdict import HyperDict

import multiprocessing

count = 100000


def run(d: HyperDict, target: int) -> None:
    for _ in range(target):
        # Adding 1 to the counter is unfortunately not an atomic operation in Python,
        # but HyperDict's shared lock comes to our rescue: We can simply reuse it.
        with d.lock:
            # Under the lock, we can safely read, modify and
            # write back any values in the shared dict
            d["counter"] += 1
            print(f"{multiprocessing.current_process().name}: {d['counter']}")


if __name__ == "__main__":
    hyper = HyperDict(name="fork-demo", buffer_size=10_000)
    hyper["some-key"] = "some value"
    hyper["counter"] = 0

    name = hyper.name

    # print(hyper)

    p1 = multiprocessing.Process(target=run, name="Process 1", args=[hyper, count // 2])
    p2 = multiprocessing.Process(target=run, name="Process 2", args=[hyper, count // 2])

    # These processes should write more or less at the same time
    p1.start()
    p2.start()

    p1.join()
    p2.join()

    print("Counter: ", hyper["counter"], " == ", count)
