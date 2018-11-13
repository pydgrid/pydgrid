Getting started
===============

Requirements
------------

pydgrid requires the following Python packages:

* NumPy, for basic numerical routines
* numba, for accelerating the code
* json, for reading network data
* matplotlib, for results plotting
* bokeh, for results visualization
* pytest, for running the tests from the package

pydgrid is usually tested on Linux and Windows on Python
3.5 and 3.6 against latest NumPy.

Installation
------------

The easiest and fastest way to get the package up and running is to install anaconda with Python 3.5 or earlier.


Then you can `install pydgrid from PyPI`_
using pip::

  $ pip install pydgrid

  
.. _`install pydgrid from PyPI`: https://pypi.python.org/pypi/pydgrid/


.. warning::

    It is recommended that you **never ever use sudo** with distutils, pip,
    setuptools and friends in Linux because you might seriously break your
    system [1_][2_][3_][4_]. Options are `per user directories`_, `virtualenv`_
    or `local installations`_.

.. _1: http://wiki.python.org/moin/CheeseShopTutorial#Distutils_Installation
.. _2: http://stackoverflow.com/questions/4314376/how-can-i-install-a-python-egg-file/4314446#comment4690673_4314446
.. _3: http://workaround.org/easy-install-debian
.. _4: http://matplotlib.1069221.n5.nabble.com/Why-is-pip-not-mentioned-in-the-Installation-Documentation-tp39779p39812.html

.. _`per user directories`: http://stackoverflow.com/a/7143496/554319
.. _`virtualenv`: http://pypi.python.org/pypi/virtualenv
.. _`local installations`: http://stackoverflow.com/a/4325047/554319

