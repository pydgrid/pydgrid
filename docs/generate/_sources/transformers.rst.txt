.. pydss documentation master file, created by
   sphinx-quickstart on Wed Sep  6 19:53:31 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Transformers
------------

Transformers are modeled as [Dugan].




.. code:: python

	"transformers":[
                    {"bus_j": "Bus_0",  "bus_k": "Bus_1",  "S_n_kVA": 2500.0, "U_1_kV":20, "U_2_kV":0.69,
                     "R_cc_pu": 0.01, "X_cc_pu":0.04, "connection": "Dyg11_3w",   "conductors_1": 3, "conductors_2": 3},
			],

where:

* ``"bus_j"``: name of the j bus
* ``"bus_k"``: name of the k bus
* ``"pos_x"``: x position of the bus
* ``"pos_y"``: y position of the bus
* ``"S_n_kVA"``: based power in kVA
* ``"U_1_kV"``: primary side base RMS phase-phase voltage in kV
* ``"U_2_kV"``: secondary side base RMS phase-phase voltage in kV
* ``"connection"``: connection type (see available connections
* ``"conductors_1"``: primary side conductors
* ``"conductors_2"``: secondary side conductors
