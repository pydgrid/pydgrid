# coding: utf-8


'''
python setup.py sdist upload
'''

from setuptools import setup, find_packages

setup(
    name='pydgrid',
    version='0.2.1',
    author='Juan Manuel Mauricio',
    author_email='jmmauricio@us.es',
    description='Python Distribution System Simulator',
    long_description='Python Distribution System Simulator',
    url='https://github.com/pydgrid/pydgrid',
    license='MIT',
    install_requires=[
        # Deactivated to avoid problems with system packages.
        # Manual installation of PYPOWER, NumPy and SciPy required.
        # 'numpy>=1.6',
        # 'scipy>=0.9',
    ],
    #packages=find_packages(exclude=['screenshots']),
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        "License :: OSI Approved :: MIT License",
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Scientific/Engineering',
    ],
)



#import os
#import io
#import sys
#from setuptools import setup, find_packages
#from setuptools.command.test import test
#
#
## https://packaging.python.org/guides/single-sourcing-package-version/
#version = {}
#with open(os.path.join("pydgrid", "__init__.py")) as fp:
#    exec(fp.read(), version)
#
#
## https://docs.pytest.org/en/latest/goodpractices.html#manual-integration
#class PyTest(test):
#    user_options = [('pytest-args=', 'a', "Arguments to pass to pytest")]
#
#    def initialize_options(self):
#        test.initialize_options(self)
#        self.pytest_args = ''
#
#    def run_tests(self):
#        import shlex
#        import pytest
#
#        sys.exit(pytest.main(shlex.split(self.pytest_args)))
#
## http://blog.ionelmc.ro/2014/05/25/python-packaging/
#setup(
#    name="pydgrid",
#    version=version['__version__'],
#    description="Python Distribution System Simulator",
#    author="",
#    author_email="",
#    url="http://pydgrid.github.io/",
#    download_url="",
#    license="MIT",
#    keywords=[
#        "distribution system", "electric engineering"
#    ],
#    python_requires=">=3.5",
#    install_requires=[
#        "numpy",
#        "matplotlib",
#        "bokeh",
#        "scipy",
#        "pandas",
#        "numba>=0.25",
#    ],
#    tests_require=[
#        "coverage",
#        "pytest-cov",
#    ],
#    extras_require={
#        'dev': [
#            "pep8",
#            "mypy",
#            "sphinx",
#            "sphinx_rtd_theme",
#            "nbsphinx",
#            "ipython"
#        ]
#    },
#    packages=['pydgrid'],
#    classifiers=[
#        "Development Status :: 4 - Beta",
#        "Intended Audience :: Education",
#        "Intended Audience :: Science/Research",
#        "License :: OSI Approved :: MIT License",
#        "Operating System :: OS Independent",
#        "Programming Language :: Python",
#        "Programming Language :: Python :: 3",
#        "Programming Language :: Python :: 3.5",
#        "Programming Language :: Python :: 3.6",
#        "Programming Language :: Python :: Implementation :: CPython",
#        "Topic :: Scientific/Engineering",
#    ]
#)
