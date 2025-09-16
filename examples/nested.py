from hyperdict import HyperDict

if __name__ == "__main__":
    # No name provided, create a new dict with random name
    ultra = HyperDict(name="my_name", recurse=True)
    # Connect `other` dict to `ultra` dict via `name`
    other = HyperDict(name=ultra.name)

    ultra["nested"] = {"deeper": {0: 1}}

    other["nested"]["deeper"][0] += 1

    print(ultra, " == " if other == ultra else " != ", other)
