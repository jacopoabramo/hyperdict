from hyperdict import HyperDict

if __name__ == "__main__":
    hyper = HyperDict(name="my_name", recurse=True)
    other = HyperDict(name=hyper.name)

    hyper["nested"] = {"deeper": {0: 1}}

    other["nested"]["deeper"][0] += 1

    print(hyper, " == " if other == hyper else " != ", other)
