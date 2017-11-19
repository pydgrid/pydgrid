User guide
==========

The simplest use can be understood with an example. Suppose we want to calculate the power flow of the following system:

.. image:: ./png/trafo_line_load.png
   :width: 600 px

The following steps should be considered:

1. Import modules
2. Define or load grid parameters
3. Generate a grid instance
4. Read grid parameters
5. Run power flow
6. Post process results
7. Plot results

Import modules
--------------

First of all, we have to import the relevant modules and classes:

.. code-block:: python

    import numpy as np

    from pydgrid import grid



Define or write grid parameters
-------------------------------

The network can be introduced in two ways:

* Python dictionary
* json file with the same structure as in the case of the previous python dictionary


For the proposed system example the following elemnts from pydgrid should be considered:

.. image:: ./png/trafo_line_load_pydgrid.png
   :width: 600 px


.. code-block:: python

    data = {     
            "buses":[
                     {"bus": "B1",  "pos_x":   0, "pos_y":   0, "units": "m", "U_kV":20.0},
                     {"bus": "B2",  "pos_x":  10, "pos_y":   0, "units": "m", "U_kV":0.4},
                     {"bus": "B3",  "pos_x": 100, "pos_y":  0, "units": "m", "U_kV":0.4}
                    ],
            "grid_formers":[
                            {"bus": "B1",
                            "bus_nodes": [1, 2, 3], "deg": [0, -120, -240],
                            "kV": [11.547, 11.547, 11.547]}
                           ],
            "transformers":[
                            {"bus_j": "B1",  "bus_k": "B2",  "S_n_kVA": 2500.0, "U_j_kV":20, "U_k_kV":0.42,
                             "R_cc_pu": 0.01, "X_cc_pu":0.04, "connection": "Dyn11",   "conductors_j": 3, "conductors_k": 4},
                           ],
            "lines":[
                     {"bus_j": "B2",  "bus_k": "B3",  "code": "UG1", "m": 100.0},
                    ],
            "loads":[
                     {"bus": "B3" , "kVA": 300.0, "pf": 0.85,"type":"3P+N"}
                    ],
            "shunts":[
              {"bus": "B2" , "R": 0.001, "X": 0.0, "bus_nodes": [4,0]}
                     ]

           }

Generate a grid instance
------------------------

.. code-block:: python

    grid_1 = grid()

Read grid parameters
--------------------

.. code-block:: python

    grid_1 = grid(data)



Execute power flow
------------------

.. code-block:: python

    grid_1.pf()


Post process results
--------------------

.. code-block:: python

    grid_1.get_v()
    grid_1.get_i()


Plot results
------------

.. code-block:: python

    from bokeh.io import output_notebook, show
    from bokeh.plotting import figure
    from bokeh.models import ColumnDataSource, HoverTool
    from bokeh.io import push_notebook
    from bokeh.resources import INLINE
    output_notebook(INLINE)

    p = figure(width=600, height=400,
               title='3 bus 4 wire system with transformer')

    # trafos:
    source = ColumnDataSource(grid_1.transformer_data)
    trafo = p.multi_line(source=source, xs='x_s', ys='y_s', color="green", alpha=0.5, line_width=5)

    # lines:
    source = ColumnDataSource(grid_1.line_data)
    lin = p.multi_line(source=source, xs='x_s', ys='y_s', color="red", alpha=0.5, line_width=5)

    # buses:
    source = ColumnDataSource(grid_1.bus_data)
    cr = p.circle(source=source, x='x', y='y', size=15, color="navy", alpha=0.5)

    p.add_tools(HoverTool(renderers=[trafo], tooltips=grid_1.transformer_tooltip))
    p.add_tools(HoverTool(renderers=[lin], tooltips=grid_1.line_tooltip))
    p.add_tools(HoverTool(renderers=[cr], tooltips=grid_1.bus_tooltip))
    show(p)


.. image:: ./png/bokeh_plot.png
   :width: 600 px
