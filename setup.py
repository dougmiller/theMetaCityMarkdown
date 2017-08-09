#! /usr/bin/env python

from setuptools import setup

setup(
    name='tmcmarkdown',
    packages=['tmcmarkdown', 'tmcmarkdown.extensions', 'tmcmarkdown.tests'],
    version='1.0.2',
    maintainer="Doug Miller",
    maintainer_email="dougmiller@themetacity.com",
    url="themetacity.com",
    py_modules=[
        'gifv',
    ],
    license='LICENCE.md',
    description='A collection of markdown extensions used on theMetaCity.com',
    long_description=open('./README.txt', 'r').read(),
    install_requires=['markdown']
)
