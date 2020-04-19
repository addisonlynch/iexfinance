from setuptools import setup, find_packages
import codecs
import os
import re

here = os.path.abspath(os.path.dirname(__file__))


def find_version(*file_paths):
    """Read the version number from a source file.
    Why read it, and not import?
    see https://groups.google.com/d/topic/pypa-dev/0PkjVpcxTzQ/discussion
    """
    # Open in Latin-1 so that we avoid encoding errors.
    # Use codecs.open for Python 2 compatibility
    with codecs.open(os.path.join(here, *file_paths), "r", "latin1") as f:
        version_file = f.read()

    # The version line must have the form
    # __version__ = 'ver'
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


def parse_requirements(filename):

    with open(filename) as f:
        required = f.read().splitlines()
        return required


# Get the long description from the relevant file
with codecs.open("README.rst", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="iexfinance",
    version=find_version("iexfinance", "__init__.py"),
    description="Python module to get stock data from IEX Cloud and " "IEX API 1.0",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    # The project URL.
    url="https://github.com/addisonlynch/iexfinance",
    download_url="https://github.com/addisonlynch/iexfinance/releases",
    # Author details
    author="Addison Lynch",
    author_email="ahljunk@gmail.com",
    test_suite="pytest",
    # Choose your license
    license="Apache",
    classifiers=[
        # How mature is this project? Common values are
        # 3 - Alpha
        # 4 - Beta
        # 5 - Production/Stable
        "Development Status :: 4 - Beta",
        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Operating System :: OS Independent",
        # Pick your license as you wish (should match "license" above)
        "License :: OSI Approved :: Apache Software License",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
    # What does your project relate to?
    keywords="stocks market finance iex quotes shares currency",
    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages.
    packages=find_packages(exclude=["contrib", "docs", "tests*"]),
    # List run-time dependencies here. These will be installed by pip when your
    # project is installed.
    install_requires=parse_requirements("requirements.txt"),
    setup_requires=["pytest-runner"],
    tests_require=parse_requirements("requirements-dev.txt"),
    # If there are data files included in your packages that need to be
    # installed, specify them here. If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    package_data={"iexfinance": []},
)
