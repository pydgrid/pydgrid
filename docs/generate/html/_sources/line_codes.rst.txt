.. pydss documentation master file, created by
   sphinx-quickstart on Wed Sep  6 19:53:31 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Line codes
----------

Two types of lines models can be considered:

* Serie Impedance (only R and X)
* PI Section Line (R, X ans shunt C)

Line parammeters can be introduced as:


* Sequence coordinates
* Primitive matrices
* Unitary voltage drop for p.f.= 1.0 and p.f.= 0.8


Serie impedance sequence parameters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Sequence coordinates
''''''''''''''''''''

.. code:: python

    "line_codes":
        {"mv_al_50":  {"R1":0.8,    "X1":	0.148, "R0":0.8,   "X0":	0.148},
         "mv_al_95":  {"R1":0.403,  "X1":	0.129, "R0":0.403, "X0":	0.129},
         "mv_al_120": {"R1":0.321,  "X1":	0.123, "R0":0.321, "X0":	0.321},
         "mv_al_185": {"R1":0.209,  "X1":	0.113, "R0":0.209, "X0":	0.209},
         "mv_al_300": {"R1":0.128,  "X1":	0.105, "R0":0.128, "X0":	0.128}
        }


where:

* ``"R1"``: Positive sequence resistance (Ω/km)
* ``"X1"``: Positive sequence reactance (Ω/km)
* ``"R0"``: Zero sequence resistance (Ω/km)
* ``"X0"``: Zero sequence reactance (Ω/km)


Primitive matrices
''''''''''''''''''

.. code:: python

    "line_codes":
      {"UG1":
        {"R":[[ 0.211,  0.049,  0.049,  0.049],
              [ 0.049,  0.211,  0.049,  0.049],
              [ 0.049,  0.049,  0.211,  0.049],
              [ 0.049,  0.049,  0.049,  0.211]],
         "X":[[ 0.747,  0.673,  0.651,  0.673],
              [ 0.673,  0.747,  0.673,  0.651],
              [ 0.651,  0.673,  0.747,  0.673],
              [ 0.673,  0.651,  0.673,  0.747]]
        },
      "UG3":
        {"R":[[ 0.871,  0.049,  0.049,  0.049],
              [ 0.049,  0.871,  0.049,  0.049],
              [ 0.049,  0.049,  0.871,  0.049],
              [ 0.049,  0.049,  0.049,  0.871]],
         "X":[[ 0.797,  0.719,  0.697,  0.719],
              [ 0.719,  0.797,  0.719,  0.697],
              [ 0.697,  0.719,  0.797,  0.719],
              [ 0.719,  0.697,  0.719,  0.797]]
        }
      }


where:

* ``"R"``: Resistance primitive (Ω/km)
* ``"X"``: Reactance primitive (Ω/km)


Unitary voltage drop
''''''''''''''''''''

.. code:: python

    "line_codes":
        {
        "lv_cu_150":  {"u90_pf10":0.27,"u90_pf08":0.31, 'T_deg':90.0, 'alpha':0.004},
        "lv_cu_240":  {"u90_pf10":0.17,"u90_pf08":0.27, 'T_deg':90.0, 'alpha':0.004} 
        }

where:

* ``"u90_pf10"``: Unitary voltage drop with load cos(φ) = 1.0 at 90ºC (V/(km A))
* ``"u90_pf08"``: Unitary voltage drop with load cos(φ) = 0.8 at 90ºC (V/(km A))
* ``"T_deg"``: Current conductor temperature (ºC)
* ``"alpha"``: Temperature coefficient (1/ºC)



PI section sequence parameters
''''''''''''''''''''''''''''''

.. code:: python

    "line_codes":
        {
         "mv_cu_50_pi":  {"R1":0.387,  "X1":	0.152, "R0":0.387, "X0":	0.152, "C_1_muF":0.135, "C_0_muF":0.135},
         "mv_cu_95_pi":  {"R1":0.193,  "X1":	0.136, "R0":0.193, "X0":	0.136, "C_1_muF":0.175, "C_0_muF":0.175},
         "mv_cu_120_pi": {"R1":0.153,  "X1":	0.132, "R0":0.153, "X0":	0.132, "C_1_muF":0.186, "C_0_muF":0.186},
         "mv_cu_185_pi": {"R1":0.099,  "X1":	0.121, "R0":0.099, "X0":	0.121, "C_1_muF":0.226, "C_0_muF":0.226},
         "mv_cu_300_pi": {"R1":0.060,  "X1":	0.112, "R0":0.060, "X0":	0.112, "C_1_muF":0.275, "C_0_muF":0.275}
        }


where:

* ``"R1"``: Positive sequence resistance (Ω/km)
* ``"X1"``: Positive sequence reactance (Ω/km)
* ``"R0"``: Zero sequence resistance (Ω/km)
* ``"X0"``: Zero sequence reactance (Ω/km)
* ``"C_1_muF"``: Zero sequence resistance (µF/km)
* ``"C_0_muF"``: Zero sequence reactance  (µF/km)



Serie impedance primitives
''''''''''''''''''''''''''


PI section sequence parameters
''''''''''''''''''''''''''''''

.. code:: python

      "line_codes":
      {
       "K1":
          {"R":[[0.8667, 0.2955, 0.2907],
                [0.2955, 0.8837, 0.2992],
                [0.2907, 0.2992, 0.8741]],
           "X":[[2.0417,0.9502, 0.7290],
                [0.9502,1.9852, 0.8023],
                [0.7290,0.8023, 2.0172]],
           "B_mu":[[10.7409, -3.4777, -1.3322],
                   [-3.4777, 11.3208, -2.2140],
                   [ -1.3322, -2.2140, 10.2104]]}
      }


where:

* ``"R"``: Resistance primitive (Ω/km)
* ``"X"``: Reactance primitive (Ω/km)
* ``"B_mu"``: Zero sequence resistance (µ℧/km)
