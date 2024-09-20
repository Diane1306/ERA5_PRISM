import numpy as np
import pandas as pd
import os

import rasterio

lat = np.array([49.9166666666664 - i * 0.0416666666667 for i in range(357)])
lon = np.array([-105.0416666666507 + i * 0.0416666666667 for i in range(722)])
Lon, Lat = np.meshgrid(lon, lat)

c_path = os.getcwd()

work_dir = '/home/mmfire/Diane/Ag_paper/'

tmin81 = np.load(work_dir + f'prism/mw_tmin/1981_tmin.npz')['tmin']
t, y, x = tmin81.shape

am = rasterio.open(work_dir + 'prism/data/tmin/1981/PRISM_tmin_stable_4kmD2_19810101_bil/PRISM_tmin_stable_4kmD2_19810101_bil.bil')
a = am.read()[0, :357, 479:1201]
mask = np.where(a>-1000, 1, 0)

input_file_name = []
for i in range(y):
    for j in range(x):
        if mask[i, j]:
            input_file_name.append(f'{Lat[i, j]:.2f}_{Lon[i, j]:.2f}_1981-2023.txt')

f = open(work_dir + 'GDD/input_list.txt', 'w')
for fi in input_file_name:
    f.write(f'{fi}\n')
f.close()

output_daily_file_name = []
output_yearly_file_name = []
for i in range(y):
    for j in range(x):
        if mask[i, j]:
            output_daily_file_name.append(f'{Lat[i, j]:.2f}_{Lon[i, j]:.2f}_daily.txt')
            output_yearly_file_name.append(f'{Lat[i, j]:.2f}_{Lon[i, j]:.2f}_yearly.txt')

f = open(work_dir + 'GDD/output_daily_list.txt', 'w')
for fi in output_daily_file_name:
    f.write(f'{fi}\n')
f.close()

f = open(work_dir + 'GDD/output_yearly_list.txt', 'w')
for fi in output_yearly_file_name:
    f.write(f'{fi}\n')
f.close()