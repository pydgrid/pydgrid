.. pydss documentation master file, created by
   sphinx-quickstart on Wed Sep  6 19:53:31 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Grid feeders
------------

Grid feeders are considered as fix power or current sources in the power flow calculation.



.. code:: python

       "grid_feeders":[{"bus": "Bus_2","bus_nodes": [1, 2, 3,4],
                        "kW": [0.5,0.5,0.5], "kvar": [0,0,0],
                        "kA": [0,0,0], "phi_deg":[30, 30, 30]}
                      ]

where:

* ``"bus"``: name of the bus
* ``"bus_nodes"``: list of nodes where the grid former source is connected
* ``"kW"``: active power for each phase
* ``"kvar"``: reactive power for each phase
* ``"kA"``: RMS value of the current in each phase
* ``"phi_deg"``: angle between voltages and currents


Voltage Source Converter (VSC)
''''''''''''''''''''''''''''''

.. code:: python

       "grid_feeders":[{"bus": "Bus_2","bus_nodes": [1, 2, 3],
                        "type":"vsc","control_mode":"pq_leon",
                        "kW": 500.0, "kvar": 200.0,
                        "L":400e-6, "R":0.01,"V_dc":800.0}
                      ]
