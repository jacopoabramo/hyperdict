import unittest
import subprocess
import sys

sys.path.insert(0, "..")
from hyperdict import HyperDict


class UltraDictTests(unittest.TestCase):
    def setUp(self):
        pass

    def exec(self, filepath):
        ret = subprocess.run(
            [sys.executable, filepath], stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        # print(ret.stdout.decode())
        ret.stdout = ret.stdout.replace(b"\r\n", b"\n")
        self.assertEqual(
            ret.returncode,
            0,
            f"Running '{filepath}' returned exit code '{ret.returncode}' but expected exit code is '0'",
        )
        return ret

    def exec_show_output(self, ret):
        return f"\n\n{ret}\n\nOutput:\n{ret.stdout.decode()}\n"

    def assertReturnCode(self, ret, target=0):
        return self.assertEqual(ret.returncode, target, self.exec_show_output(ret))

    def test_count(self):
        ultra = HyperDict()
        other = HyperDict(name=ultra.name)

        count = 100
        for i in range(count // 2):
            ultra[i] = i

        for i in range(count // 2, count):
            other[i] = i

        self.assertEqual(len(ultra), len(other))

    def test_huge_value(self):
        ultra = HyperDict()

        # One megabyte string
        self.assertEqual(ultra.full_dump_counter, 0)

        length = 1_000_000

        ultra["huge"] = " " * length

        self.assertEqual(ultra.full_dump_counter, 1)
        self.assertEqual(len(ultra.data["huge"]), length)

        other = HyperDict(name=ultra.name)

        self.assertEqual(len(other.data["huge"]), length)

    def test_parameter_passing(self):
        ultra = HyperDict(
            shared_lock=True, buffer_size=4096 * 8, full_dump_size=4096 * 8
        )
        # Connect `other` dict to `ultra` dict via `name`
        other = HyperDict(name=ultra.name)

        self.assertIsInstance(ultra.lock, ultra.SharedLock)
        self.assertIsInstance(other.lock, other.SharedLock)

        self.assertEqual(ultra.buffer_size, other.buffer_size)

    def test_iter(self):
        ultra = HyperDict()
        # Connect `other` dict to `ultra` dict via `name`
        other = HyperDict(name=ultra.name)

        ultra[1] = 1
        ultra[2] = 2

        counter = 0
        for i in other.items():
            counter += 1

        self.assertEqual(counter, 2)

        self.assertEqual(ultra.items(), other.items())

    def test_delete(self):
        import random
        import string

        letters = string.ascii_lowercase
        rand_str = "".join(random.choice(letters) for i in range(1000))
        my_dict = HyperDict(buffer_size=10_000_000)
        for i in range(100_000):
            my_dict[i] = rand_str
        for i in list(my_dict.keys()):
            del my_dict[i]
        self.assertEqual(len(my_dict), 0)

    def test_already_exists(self):
        name = "ultra_test"
        # Ensure we have a clean state before the test
        HyperDict.unlink_by_name(name, ignore_errors=True)
        HyperDict.unlink_by_name(name + "_memory", ignore_errors=True)
        # Create should be possible now
        _ = HyperDict(name=name, create=True)
        with self.assertRaises(HyperDict.Exceptions.AlreadyExists):
            _ = HyperDict(name=name, create=True)

    def test_not_already_exists(self):
        name = "ultra_test"
        # Ensure we have a clean state before the test
        HyperDict.unlink_by_name(name, ignore_errors=True)
        HyperDict.unlink_by_name(name + "_memory", ignore_errors=True)

        with self.assertRaises(HyperDict.Exceptions.CannotAttachSharedMemory):
            _ = HyperDict(name=name, create=False)

    def test_lock_blocking(self):
        pass

    def test_full_dump(self):
        # TODO
        pass

    # Turns out MacOS can only do 24 characters in total
    # def test_longest_name(self):
    #    for i in range(5, 50):
    #        print('Loop ', i)
    #        ultra = HyperDict(name='x' * i)

    @unittest.skipUnless(sys.platform.startswith("linux"), "requires Linux")
    def test_cleanup(self):
        # TODO
        import psutil

        p = psutil.Process()
        file_count = len(p.open_files())
        self.assertEqual(
            file_count, 0, "file handle count before before tests should be 0"
        )
        ultra = HyperDict(nested={1: 1})
        file_count = len(p.open_files())
        self.assertEqual(
            file_count, 4, "file handle count with one simple HyperDict should be 4"
        )
        del ultra
        file_count = len(p.open_files())
        self.assertEqual(
            file_count,
            0,
            "file handle count after deleting the HyperDict should be 0 again",
        )
        ultra = HyperDict(nested={1: 1}, recurse=True)
        file_count = len(p.open_files())
        self.assertEqual(file_count, 12, "nested file handle count should be 12")
        del ultra
        file_count = len(p.open_files())
        self.assertEqual(
            file_count,
            0,
            "nested file handle count after deleting HyperDict should be 0 again",
        )

    def test_example_simple(self):
        filename = "examples/simple.py"
        ret = self.exec(filename)
        self.assertReturnCode(ret)
        self.assertEqual(
            ret.stdout.splitlines()[-1],
            b"Length:  100000  ==  100000  ==  100000",
            self.exec_show_output(ret),
        )

    def test_example_parallel(self):
        filename = "examples/parallel.py"
        ret = self.exec(filename)
        self.assertReturnCode(ret)
        self.assertEqual(
            ret.stdout.splitlines()[-1],
            b"Counter:  100000  ==  100000",
            self.exec_show_output(ret),
        )

    def test_example_nested(self):
        filename = "examples/nested.py"
        ret = self.exec(filename)
        self.assertReturnCode(ret)
        self.assertEqual(
            ret.stdout.splitlines()[-1],
            b"{'nested': {'deeper': {0: 2}}}  ==  {'nested': {'deeper': {0: 2}}}",
            self.exec_show_output(ret),
        )

    def test_example_recover_from_stale_lock(self):
        filename = "examples/recover_from_stale_lock.py"
        ret = self.exec(filename)
        self.assertReturnCode(ret)
        self.assertEqual(
            ret.stdout.splitlines()[-1],
            b"Counter: 100 == 100",
            self.exec_show_output(ret),
        )


if __name__ == "__main__":
    if len(sys.argv) > 1:
        for i in range(0, len(sys.argv)):
            if sys.argv[i].startswith("-"):
                continue
            if "." not in sys.argv[i]:
                sys.argv[i] = f"UltraDictTests.{sys.argv[i]}"
    unittest.main()
