from setuptools import setup, find_packages


setup(
    name='pyfsa',
    author='Natalia Maximo',
    author_email='iam@natalia.dev',
    version='0.1',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=['click'],
    tests_require=['mypy', 'pytest-cov', 'pytest', 'flake8'],
    extras_require={
        'tests': ['mypy', 'pytest-cov', 'pytest', 'flake8'],
    },
    entry_points={
        'console_scripts': ['pyfsa = pyfsa.main:main']
    },
)
