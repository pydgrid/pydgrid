.. pydss documentation master file, created by
   sphinx-quickstart on Wed Sep  6 19:53:31 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Grid formers
------------

Grid formers are considered as fix voltage sources in the power flow calculation.



.. code:: python
   
    "grid_formers":[
                     {"bus": "Bus_1",
                      "bus_nodes": [1, 2, 3], "deg": [0, -120, -240],
                      "kV": [0.23094, 0.23094, 0.23094]}
                   ]

where:

* ``"bus"``: name of the bus
* ``"bus_nodes"``: list of nodes where the grid former source is connected
* ``"kV"``: phase-neutral RMS voltages list (kV)   
* ``"deg"``: phase-neutral voltage angles list (deg)

