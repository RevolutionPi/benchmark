# SPDX-FileCopyrightText: 2023 KUNBUS GmbH
#
# SPDX-License-Identifier: MIT

# -*- coding: utf-8 -*-
"""Setup-script for revpi-stress-tester."""
__author__ = "Nicolai"
__copyright__ = "Copyright (C) 2023 KUNBUS GmbH"
__license__ = "MIT"

from setuptools import find_packages, setup

from revpi_stress_tester.__about__ import __version__

with open("README.md") as fh:
    # Load long description from readme file
    long_description = fh.read()

setup(
    name="revpi_stress_tester",
    version=__version__,
    packages=find_packages(),
    include_package_data=True,
    python_requires=">= 3.6",
    install_requires=["psutil"],
    entry_points={
        "console_scripts": [
            "revpi-stress-tester = revpi_stress_tester.cli:main",
        ]
    },
    platforms=["revolution pi"],
    url="https://github.com/RevolutionPi/benchmark",
    license="MIT",
    author="Nicolai Buchwitz",
    author_email="n.buchwitz@kunbus.com",
    description="RevPi Stress Tests for laboratory benchmarking",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=["revpi", "revolution pi", "plc", "automation"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
