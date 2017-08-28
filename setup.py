#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [
    'Click>=6.0',
    'SQLAlchemy',
    'enum34'
]

setup_requirements = [
    'pytest-runner',
]

test_requirements = [
    'pytest',
]

setup(
    name='hydrogen',
    version='0.1.0',
    description="command line utility",
    author="Nicolás Mendoza",
    author_email='nicolas.mendoza@yandex.com',
    url='https://github.com/niccolasmendoza/hydrogen',
    packages=[
        'hydrogen/',
        'hydrogen/core',
        'hydrogen/core/db',
        'hydrogen/core/galaxy',
        'hydrogen/core/geometry',
        'hydrogen/core/wheater',
        'hydrogen/core/wheater/job',
        'hydrogen/core/wheater/statistics',

    ],
    entry_points={
        'console_scripts': [
            'hydrogen=hydrogen.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='hydrogen',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
