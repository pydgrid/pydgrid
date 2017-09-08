.. pydss documentation master file, created by
   sphinx-quickstart on Wed Sep  6 19:53:31 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Loads
-----

Loads.

.. code:: python

   "loads":[
            {"bus": "Bus_2" , "kVA": 50.0, "pf": 0.85,"type":"1P+N","bus_nodes": [1,4]},
            {"bus": "Bus_2" , "kVA": 30.0, "pf": 0.85,"type":"1P+N","bus_nodes": [2,4]},
            {"bus": "Bus_2" , "kVA": 20.0, "pf": 0.85,"type":"1P+N","bus_nodes": [3,4]}
           ],

where:

* ``"bus"``: name of the bus
* ``"bus_nodes"``: list of nodes where the load is connected
* ``"type"``: available types are:
	- ``"1P+N"``: single phase load connected between one phase and other or neutral 
	- ``"IABC"``: 
* ``"kVA"``: aparent power (kW)   
* ``"pf"``: load power factor 



