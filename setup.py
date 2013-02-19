#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup, find_packages
except ImportError:
    import ez_setup
    ez_setup.use_setuptools()
    from setuptools import setup, find_packages
    
setup(
    name="pysrc-audit",
    version="0.1",
    url='https://github.com/sys-git/pysrc-audit',
    packages=find_packages(),
    package_dir={'pysrc-audit': 'Auditer'},
    include_package_data=True,
    author="Francis Horsman",
    author_email="francis.horsman@gmail.com",
    description="A simple pure python python-source-code line auditor.",
    license="GNU General Public License",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Communications',
    ]
)
