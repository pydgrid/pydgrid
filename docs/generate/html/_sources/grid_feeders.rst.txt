.. pydss documentation master file, created by
   sphinx-quickstart on Wed Sep  6 19:53:31 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Grid feeders
------------

Grid feeders are considered as fix power or current sources in the power flow calculation.



.. code:: python
   
   "grid_feeders":[{"bus": "Bus_0","bus_nodes": [1, 2, 3], "mode": "PQ"
	                "kVA": [11.547, 11.547, 11.547], "fp": [0.9,0.9,0.9], 
			        "kA": [20,10,5], "phi_deg":[0, 0, 0]}
				  ]

where:

* ``"bus"``: name of the bus
* ``"bus_nodes"``: list of nodes where the grid former source is connected
* ``"mode"``: available modes are:
	- ``"PQ"``: 
	- ``"IABC"``: 
* ``"kVA"``: phase-neutral RMS voltages list (kV)   
* ``"deg"``: phase-neutral voltage angles list (deg)

