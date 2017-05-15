# coding: UTF-8
# Copyright © 2017 Alex Forster. All rights reserved.
# This software is licensed under the 3-Clause ("New") BSD license.
# See the LICENSE file for details.

from setuptools import setup


setup(
    name='nrdpy',
    version='0.9.0',
    description='A library for submitting passive checks to Nagios NRDP endpoints',
    author='Alex Forster',
    author_email='alex@alexforster.com',
    maintainer='Alex Forster',
    maintainer_email='alex@alexforster.com',
    url='https://github.com/AlexForster/nrdpy',
    license='3-Clause ("New") BSD license',
    packages=['nrdpy'],
    package_dir={'nrdpy': './nrdpy'},
    package_data={'nrdpy': [
        'README*',
        'LICENSE',
    ]},
    install_requires=[
        'requests<3.0.0'
    ]
)
