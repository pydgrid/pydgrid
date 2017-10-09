.. pydss documentation master file, created by
   sphinx-quickstart on Wed Sep  6 19:53:31 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Buses
-----

Buses are composed by nodes. 

.. image:: ./png/buses_nodes.png
   :width: 600 px
 

 

.. code-block::
	"buses":[
			{"bus": "Bus_0",  "pos_x": 0, "pos_y":   0, "units": "m", "U_kV":20.0},
			{"bus": "Bus_1",  "pos_x": 0, "pos_y":  10, "units": "m", "U_kV":0.4},
			{"bus": "Bus_2",  "pos_x": 0, "pos_y": 200, "units": "m", "U_kV":0.4}
			],

where:

* ``"bus"``: name of the bus
* ``"pos_x"``: x position of the bus  
* ``"pos_y"``: y position of the bus  
* ``"units"``: units for positions (only m is available)
* ``"U_kV"``: RMS phase-phase base voltage (kV)


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
