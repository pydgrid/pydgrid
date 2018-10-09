# coding: utf-8


'''
python setup.py sdist upload
'''
import os
from setuptools import setup, find_packages


# https://packaging.python.org/guides/single-sourcing-package-version/
version = {}
with open(os.path.join("pydgrid", "__init__.py")) as fp:
    exec(fp.read(), version)



setup(
    name='pydgrid',
    version=version['__version__'],
    author='Juan Manuel Mauricio',
    author_email='jmmauricio@us.es',
    description='Python Distribution System Simulator',
    long_description='Python Distribution System Simulator',
    url='https://github.com/pydgrid/pydgrid',
    license='MIT',
    install_requires=[
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
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering',
    ],
)


