import os
from setuptools import setup

install_requires = ["slumber", "simplejson"]
tests_require = []

base_dir = os.path.dirname(os.path.abspath(__file__))

setup(
    name = "hs_restclient",
    version = "0.1.0",
    description = "A client library for HydroShare's REST API",
#     long_description="\n\n".join([
#         open(os.path.join(base_dir, "README.rst"), "r").read(),
#         open(os.path.join(base_dir, "CHANGELOG.rst"), "r").read()
#     ]),
    url = "http://www.hydroshare.org/",
    author = "Brian Miles",
    author_email = "brian_miles@unc.edu",
    packages = ["hs_restclient"],
    zip_safe = False,
    install_requires = install_requires,
    tests_require = tests_require,
    test_suite = "tests.get_tests",
)