"""Setup for mediasite XBlock."""

import os
from setuptools import setup


def package_data(pkg, root):
    """Generic function to find package_data for `pkg` under `root`."""
    data = []
    for dirname, _, files in os.walk(os.path.join(pkg, root)):
        for fname in files:
            data.append(os.path.relpath(os.path.join(dirname, fname), pkg))
    return {pkg: data}


setup(
    name='xblock-mediasite',
    version='0.1.9.7',
    description='''
    This XBlock gives the ability to access TU Delft Collegerama where a lot
    of recorded lectures, presentations and live events are stored.
    With this XBlock a teacher or course maker can select a part of a
    recording to use in an edX online course.
    Collegerama runs under mediasite software from sonicfoundry.
    ''',
    packages=[
        'mediasite', 'xblockmediasite'
    ],
    py_modules=['mediasite_settings'],
    install_requires=[
        'XBlock',
        'requests',
    ],
    entry_points={
        'xblock.v1': [
            'xblockmediasite = xblockmediasite:XBlockMediasite',
        ]
    },
    package_data=package_data("xblockmediasite", "static"),
)
