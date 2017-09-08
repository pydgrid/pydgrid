.. pydss documentation master file, created by
   sphinx-quickstart on Wed Sep  6 19:53:31 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Shunt elements
--------------

Impedances that can be connected beetwen phases, phases and neutral and phases and neutral and ground.



.. code:: python

   "shunts":[
             {"bus": "Bus_1" , "R": 0.001, "X": 0.0, "bus_nodes": [4,0]},
             {"bus": "Bus_2" , "R":  40.0, "X": 0.0, "bus_nodes": [4,0]}
            ]


where:

* ``"bus"``: name of the bus
* ``"bus_node"``: list of nodes where the shunt element is connected
* ``"R"``: shunt element resistance (Ω)
* ``"X"``: shunt element reactance (Ω)



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
