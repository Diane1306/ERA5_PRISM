import numpy as np
import pygrib
import pandas as pd
import time
import pytz

var = ['lake_bottom_temperature', 'lake_ice_depth', 'lake_ice_temperature',
'lake_mix_layer_depth', 'lake_mix_layer_temperature', 'lake_shape_factor',
'lake_total_layer_temperature', 'leaf_area_index_high_vegetation', 'leaf_area_index_low_vegetation',
'potential_evaporation', 'runoff', 'skin_reservoir_content',
'skin_temperature', 'snow_albedo', 'snow_density', 'snow_depth_water_equivalent',
'snow_evaporation', 'snowfall', 'snowmelt',
'soil_temperature_level_1', 'soil_temperature_level_2', 'soil_temperature_level_3',
'soil_temperature_level_4', 'sub_surface_runoff', 'surface_latent_heat_flux',
'surface_net_solar_radiation', 'surface_net_thermal_radiation', 'surface_pressure',
'surface_runoff', 'surface_sensible_heat_flux', 'surface_solar_radiation_downwards',
'surface_thermal_radiation_downwards', 'temperature_of_snow_layer', 'total_evaporation',
'total_precipitation', 'volumetric_soil_water_layer_1', 'volumetric_soil_water_layer_2',
'volumetric_soil_water_layer_3', 'volumetric_soil_water_layer_4']

# East Lansing 42.7 -84.6


for vi in var:
    data = []
    for yl in range(40):
        grbs = pygrib.open(f'./data/ERA5-Land_9km_EastLansing/{vi}_{1981+yl}.grib') 
        n = grbs.messages
        units = grbs.message(1).units
        for i in range(1,n+1):
            data0 = grbs.message(i).data(lat1=42.6,lat2=42.7,lon1=-84.6,lon2=-84.5)[0].data[0,0]
            data.append(data0)
        grbs.close()
        
    if len(data) == 350639:
        dff = pd.date_range(start='1/1/1981 01:00', end='12/31/2020 23:00', freq='H').tz_localize(pytz.utc)
    elif len(data) == 350640:
        dff = pd.date_range(start='1/1/1981 00:00', end='12/31/2020 23:00', freq='H').tz_localize(pytz.utc)
    else:
        dff = pd.date_range(start='1/1/1981 01:00', end='12/1/2020 00:00', freq='H').tz_localize(pytz.utc)
    
    year = dff.strftime('%Y')
    mon = dff.strftime('%-m')
    day = dff.strftime('%-d')
    hour = dff.strftime('%-H')

    # 1981/1/1/01:00 2020/11/4/00:00 349896
    pd.DataFrame({'YEAR':year, 'MONTH':mon, 'DAY':day, 'HOUR':hour, f'{vi} ({units})':np.array(data)}).to_csv(f'./data/ERA5-Land_9km_EastLansing/Variables/{vi}.csv', index=False)