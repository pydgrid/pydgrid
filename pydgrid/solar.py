#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 10:55:17 2017

@author: jmmauricio
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import numba
import random
import os




#crst_wb = '/home/jmmauricio/Desktop/CREST_Integrated_PV_electricity_demand_model_1.0B1.xlsm'
#df_ClearnessIndexTPM = pd.read_excel(crst_wb,sheetname='ClearnessIndexTPM', skiprows=8, parse_cols='B:CY')



class pv_gen(object):
    
    def __init__(self):
               
        self.Latitude =  37.3828300  # B10 # Sevilla
        self.Longitude = -5.9731700 # B11  # Sevilla
        self.Day_summer_starts = 87 # B14
        self.Day_summer_ends = 304 # B15

        self.Local_standard_time_meridian = 0.0 # B17
        self.Azimuth_of_panel = 0.0  # B24
        self.Ground_reflectance = 0.2 # B42

        self.Slope_of_panel = 30.0
        self.Panel_area = 10.0
        self.System_efficiency = 0.1

        df_ClearnessIndexTPM = pd.read_csv(os.path.join(os.path.dirname(__file__), "ClearnessIndexTPM.csv"))
        self.df_ClearnessIndexTPM = df_ClearnessIndexTPM.set_index('Unnamed: 0')
        self.dKArray = np.array(self.df_ClearnessIndexTPM) 



    
    
    def radiation_on_panel_eval(self,Day_of_the_year,Local_time_hours,Local_time_minutes):

        Panel_area = self.Panel_area
        System_efficiency  = self.System_efficiency

        
        Latitude = self.Latitude  # B10
        Longitude = self.Longitude # B11
    #    Day_of_the_year = 172 # B12
    #    Local_time_hours = date.hour      # B13
    #    Local_time_minutes = date.minute       # D13
        Day_summer_starts = self.Day_summer_starts # B14
        Day_summer_ends = self.Day_summer_ends # B15
        Slope_of_panel = self.Slope_of_panel # B23
        Local_standard_time_meridian = self.Local_standard_time_meridian # B17
        Azimuth_of_panel = self.Azimuth_of_panel  # B24
        Ground_reflectance = self.Ground_reflectance # B42
    
         
        
        Slope_of_panel_rad = np.deg2rad(Slope_of_panel) # D23
        Azimuth_of_panel_rad = np.deg2rad(Azimuth_of_panel) # D24
        B = (360*(Day_of_the_year-81)/364) #[1] eq. 7.13, p403.
        B_rad = np.deg2rad(B)
        
        Eq_of_time = (9.87*np.sin(2*B_rad))-(7.53*np.cos(B_rad))-(1.5*np.sin(B_rad)) #[1] eq. 7.12, p403. and [5]
        
        Time_correction_factor = (4*(Longitude-Local_standard_time_meridian))+Eq_of_time # B20 [2]
        
        if (Day_of_the_year>=Day_summer_starts) and (Day_of_the_year<Day_summer_ends):
            Local_standard_time_hours = Local_time_hours-1 # B16
        else:
            Local_standard_time_hours = Local_time_hours # B16
        
        
        Hours_before_solar_noon = 12-(Local_standard_time_hours+(Local_time_minutes/60.0)+(Time_correction_factor/60)) # See [1] eq. 7.14, p404 and [2] B21
        
        Extraterrestrial_radiation = 1367*(1+(0.034*np.cos(2*np.pi*Day_of_the_year/365.25))) # [3] eq. 2.35, p42.  B26
        
        Optical_depth_k = 0.174+(0.035*np.sin(np.deg2rad(360*(Day_of_the_year-100)/365))) # B27
        
        
        Hour_angle_H = 15*Hours_before_solar_noon
        Hour_angle_H_rad = np.deg2rad(Hour_angle_H) # D29
        Declination_delta = 23.45*np.sin(np.deg2rad(360*(284+Day_of_the_year)/365.25))
        Declination_delta_rad = np.deg2rad(Declination_delta) # D30
        Solar_altitude_angle_beta = np.rad2deg(np.arcsin((np.cos(np.deg2rad(Latitude))*np.cos(Declination_delta_rad)*np.cos(np.deg2rad(Hour_angle_H)))+
                                                         (np.sin(np.deg2rad(Latitude))*np.sin(Declination_delta_rad))))  # B31
        Solar_altitude_angle_beta_rad = np.deg2rad(Solar_altitude_angle_beta)         # D31                                    
        Azimuth_of_sun_theta = np.rad2deg(np.arcsin(np.cos(Declination_delta_rad)*np.sin(Hour_angle_H_rad)/np.cos(Solar_altitude_angle_beta_rad)))  # B32
        
        aux_123 = np.tan(Declination_delta_rad)/np.tan(np.deg2rad(Latitude))
        if np.cos(Hour_angle_H_rad)>=np.tan(Declination_delta_rad)/np.tan(np.deg2rad(Latitude)):
            Azimuth_angle_test = 0 # B33
        else:
            Azimuth_angle_test = 1 # B33
        
        
        
        # jmmauricio: possible error here, when panel slope is larger than 0º
        if (Azimuth_angle_test==0): 
           if (Azimuth_of_sun_theta>90):
              Adjusted_azimuth_of_sun_theta = Azimuth_of_sun_theta-90
           else: 
               if (Azimuth_of_sun_theta<-90): 
                  Adjusted_azimuth_of_sun_theta =  Azimuth_of_sun_theta+90
               else: 
                   Adjusted_azimuth_of_sun_theta=Azimuth_of_sun_theta
        else:
            if Azimuth_of_sun_theta>0 and Azimuth_of_sun_theta<90:
                Adjusted_azimuth_of_sun_theta=180-Azimuth_of_sun_theta
            else: 
                if (Azimuth_of_sun_theta>-90 and Azimuth_of_sun_theta<0):
                    Adjusted_azimuth_of_sun_theta=-180-Azimuth_of_sun_theta
                else: 
                   Adjusted_azimuth_of_sun_theta =  Azimuth_of_sun_theta #D34
                    
        
        Adjusted_azimuth_of_sun_theta_rad = np.deg2rad(Adjusted_azimuth_of_sun_theta)
        # =DEGREES(ACOS((COS(D31)*COS(D34-D24)*SIN(D23))+(SIN(D31)*COS(D23))))
        Solar_incicident_angle_on_panel = np.rad2deg(np.arccos((np.cos(Solar_altitude_angle_beta_rad)*np.cos(Adjusted_azimuth_of_sun_theta_rad-Azimuth_of_panel_rad)*np.sin(Slope_of_panel_rad)) +
                                                                (np.sin(Solar_altitude_angle_beta_rad)*np.cos(Slope_of_panel_rad))))  # B36
        Solar_incicident_angle_on_panel_rad =   np.deg2rad(Solar_incicident_angle_on_panel)        # D36                                             
        if Solar_altitude_angle_beta_rad>0.0:
            Clear_sky_beam_radiation_at_surface_horizontal = Extraterrestrial_radiation*np.exp((0-Optical_depth_k)/np.sin(Solar_altitude_angle_beta_rad))
        else:
            Clear_sky_beam_radiation_at_surface_horizontal = 0.0 # B38
            
        
        if np.abs(Solar_incicident_angle_on_panel)>90:
            Direct_beam_radiation_on_panel  = 0.0
        else:
            Direct_beam_radiation_on_panel  =  Clear_sky_beam_radiation_at_surface_horizontal*np.cos(Solar_incicident_angle_on_panel_rad) # B39
        
        Sky_diffuse_factor = 0.095+(0.04*np.sin(np.deg2rad(360*(Day_of_the_year-100)/365)))
        
        
        # B41
        Diffuse_radiation_on_panel = Sky_diffuse_factor*Clear_sky_beam_radiation_at_surface_horizontal*((1+np.cos(Slope_of_panel_rad))/2)
        
        Reflected_radiation_on_panel = Ground_reflectance*Clear_sky_beam_radiation_at_surface_horizontal*(np.sin(Solar_altitude_angle_beta_rad)+Sky_diffuse_factor)*((1-np.cos(Slope_of_panel_rad))/2)
        
        Total_radiation_on_panel = Direct_beam_radiation_on_panel + Diffuse_radiation_on_panel+ Reflected_radiation_on_panel
        #
        
        Power = Panel_area*System_efficiency*Total_radiation_on_panel
        
        #Electricity generated on the day
        #
        self.Extraterrestrial_radiation = Extraterrestrial_radiation
        self.Optical_depth_k = Optical_depth_k
        self.Hour_angle_H = Hour_angle_H
        self.Solar_incicident_angle_on_panel = Solar_incicident_angle_on_panel
        self.Diffuse_radiation_on_panel = Diffuse_radiation_on_panel
        self.Power = Power      
        self.Azimuth_of_sun_theta = Azimuth_of_sun_theta  
        self.Reflected_radiation_on_panel = Reflected_radiation_on_panel
        self.Total_radiation_on_panel = Total_radiation_on_panel
        self.Direct_beam_radiation_on_panel = Direct_beam_radiation_on_panel
        return Total_radiation_on_panel



    def radiations(self,date_range):
        '''
        date_range = pd.date_range(start='2017-03-01',end='2017-03-02', freq='min')
        pv_powers(date_range)
        '''
        N = len(date_range,) 
        self.N = N
        radiations_on_panel = np.zeros((N-1,))
        for it in range(N-1):
            Total_radiation_on_panel = self.radiation_on_panel_eval(date_range[it].dayofyear,date_range[it].hour,date_range[it].minute)
            radiations_on_panel[it] = Total_radiation_on_panel
            
        self.clearness()    
        self.radiation_on_panel_clear_sky =  radiations_on_panel
        self.radiation_on_panel = self.clearness_values * self.radiation_on_panel_clear_sky
        
        return self.radiation_on_panel
    
    def radiations_clear(self,date_range):
        '''
        date_range = pd.date_range(start='2017-03-01',end='2017-03-02', freq='min')
        pv_powers(date_range)
        '''
        N = len(date_range,) 
        self.N = N
        radiations_on_panel = np.zeros((N-1,))
        for it in range(N-1):
            Total_radiation_on_panel = self.radiation_on_panel_eval(date_range[it].dayofyear,date_range[it].hour,date_range[it].minute)
            radiations_on_panel[it] = Total_radiation_on_panel
            
        self.radiation_on_panel_clear_sky =  radiations_on_panel
        
        return self.radiation_on_panel_clear_sky
    
    
    def clearness(self):
    
        N = self.N-1
        PV_Model_K = np.zeros((N,))
        vSimulationArray = np.zeros((N,))
        PV_Model_K[0] = 1.0
        
        iCurrentStateBin = 100
        fRand = random.random()
        
        
        for iTimeStep in range(N):
            
            # Get a random number
            fRand = random.random()
            
            # Reset the cumulative probability count
            fCumulativeP = 0.0
            
            # Cycle through the probabilities for this state
            for i in range(101):
                
                # Add this probability
                fCumulativeP = fCumulativeP + self.dKArray[iCurrentStateBin, i]
                
                # See if this is a state transition
                if fRand <= fCumulativeP:
                    
                    #Transition to another or same state
                    iCurrentStateBin = i
                    break
            
            # Work out the k value for this step
            if iCurrentStateBin == 100:
                dk = 1        
            else:
                dk = (iCurrentStateBin / 100) - 0.01
                
            # Store the k value
            vSimulationArray[iTimeStep] = dk
                
        self.clearness_values = vSimulationArray
        return vSimulationArray





high_energy_power = []


def multi_run(radiations_on_panel):
    high_energy_net_radiation = []
    
    for it in range(100):
        clearness_indexes = clearness()
        net_radiation = radiations_on_panel*clearness_indexes
        
        Panel_area = 10.0
        System_efficiency = 0.1
        
        Powers = net_radiation*Panel_area*System_efficiency
        Energy = np.sum(Powers)/60/1000
        high_energy_net_radiation += [net_radiation]
        
        if Energy>7.9:
            
            print(it)
            
    return np.array(high_energy_net_radiation)

def multi_run_clouds():
    clearness_list = []
    for it in range(100000):
        clearness_indexes = clearness()
        clearness_list += [clearness_indexes]        
    return np.array(clearness_list)

        

@numba.jit(nopython=True,cache=True)
def fast_pv_powers():
    N = 1440
    radiations_on_panel = np.zeros((N-1,))
    Panel_area = 10.0
    System_efficiency = 0.1

    for it in range(N-1):
        mins = it % 60
        hours = (it-mins)/60
        Total_radiation_on_panel = pv_power(hours,mins)
        radiations_on_panel[it] = Total_radiation_on_panel
    
    Powers = net_radiation*Panel_area*System_efficiency
    Energy = np.sum(Powers)/60/1000
    return radiations_on_panel

if __name__ == "__main__":
    
    
    pv = pv_gen()
    q = pv.radiation_on_panel_eval(1,10,00)
    print(q)
    drange = pd.date_range(start='2017-07-01',end='2017-07-02', freq='min')
    radiations_on_panel = pv.radiations(drange)
    
#    
#    radiations_on_panel = pv_powers(drange)
#    
#    clearness_indexes = clearness()
   
    #high_energy_net_radiation = multi_run(radiations_on_panel)
#    
#    clearness = multi_run_clouds()
#    np.savez_compressed('clearness_outputs_2', clearness.T, delimiter=',')
#    
#    #
    import matplotlib.pyplot as plt
#    
    fig, ax = plt.subplots()
    ax.plot(drange[1:],pv.radiation_on_panel_clear_sky)
    ax.plot(drange[1:],pv.radiation_on_panel)
#    ax.plot(drange[1:],radiations_on_panel*clearness_indexes)
#    fig.autofmt_xdate()
#    ax.grid(True)
    #plt.plot(net_radiation)
    
    #print('Energy: {:2.2f} kWh'.format(Energy))