# coding: utf-8


'''
python setup.py sdist upload
'''

from setuptools import setup, find_packages

setup(
    name='pydgrid',
    version='0.3.1',
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


