#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  9 23:22:02 2017

@author: jmmauricio
"""

from pydgrid import solar

def test_sevilla():

    pv = solar.pv_gen()
    pv.Latitude =  37.3828300  # B10 # Sevilla
    pv.Longitude = -5.9731700 # B11  # Sevilla
    pv.Day_summer_starts = 87 # B14
    pv.Day_summer_ends = 304 # B15
 
    pv.Local_standard_time_meridian = 0.0 # B17
    pv.Azimuth_of_panel = 0.0  # B24
    pv.Ground_reflectance = 0.2 # B42
        
    pv.Slope_of_panel = 0.0
    pv.Panel_area = 10.0
    pv.System_efficiency = 0.1
    q = pv.radiation_on_panel_eval(180,10,0)
    
    q_crest = 806.94

    assert abs(q_crest-q)<1.0


def test_passau():

    pv = solar.pv_gen()
    pv.Latitude =  48.566667  # B10 # Passau
    pv.Longitude = -13.466667 # B11  # Passau
    pv.Day_summer_starts = 87 # B14
    pv.Day_summer_ends = 304 # B15

    pv.Local_standard_time_meridian = 0.0 # B17
    pv.Azimuth_of_panel = 0.0  # B24
    pv.Ground_reflectance = 0.2 # B42

    pv.Slope_of_panel = 30.0
    pv.Panel_area = 10.0
    pv.System_efficiency = 0.1
    q = pv.radiation_on_panel_eval(1,14,0)
    
    q_crest = 678.4781


    assert abs(q_crest-q)<1.0


  
if __name__ == "__main__":
    test_sevilla()
    test_passau()
    
     