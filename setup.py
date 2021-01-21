# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

with open('VERSION', 'r') as f:
    version = f.read()


setup(
    name='pyfsa',
    author='Natalia Maximo',
    author_email='iam@natalia.dev',
    version=version,
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    python_requires='>=3.6',
    license='Apache Software License',
    install_requires=[
        'click',
        'pygraphviz',
    ],
    tests_require=['mypy', 'pytest-cov', 'pytest', 'flake8'],
    extras_require={
        'tests': ['mypy', 'pytest-cov', 'pytest', 'flake8'],
    },
    entry_points={
        'console_scripts': ['fsa = pyfsa.main:main']
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Utilities',
        'Typing :: Typed',
    ],
)
