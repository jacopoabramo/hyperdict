from pathlib import Path
from setuptools import setup, Extension
import Cython.Build

# read the contents of your README file
this_directory = Path(__file__).parent
long_description = (this_directory / "readme.md").read_text()

version = "0.1.0"

ext = [
    Extension("hyperdict", ["src/hyperdict/_hyperdict.py", "src/hyperdict/_errors.py"],),
]

setup(
    name="hyperdict",
    version=version,
    description="Sychronized, streaming dictionary that uses shared memory as a backend",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={"hyperdict": "src"},
    packages=["hyperdict"],
    zip_safe=False,
    ext_modules=Cython.Build.cythonize(
        ext, compiler_directives={"language_level": "3"}
    ),
    python_requires=">=3.10",
)
