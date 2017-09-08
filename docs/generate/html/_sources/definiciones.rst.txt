Definiciones
============

Buses y nodos
-------------




Orden de los nodos
------------------


El orden de los nodos en los vectores ``V_node`` y ``I_node``  es el siguiente:

* nodos con fuentes de tensión
* nodos con cargas (corrientes conocidas)
* nodos de transición (corrientes nulas)

A su vez cada uno de estos bloques se ordenan según orden de aparición en el archivo ``.json``


Ejemplo
'''''''

.. image:: orden_nodos.png

V_known tiene los nodos con fuentes de tensión
V_unknown tiene los demás (nodos de corrientes conocidas, cargas y transición)

V_sorted está ordenada de manera tal que los nodos que pertenecen al mismo bus estén juntos y en orden.
A su vez el orden de los buses está según ``buses`` del ``.json``

