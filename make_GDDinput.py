import numpy as np
import pandas as pd
import os
# import rasterio

lat = np.array([49.9166666666664 - i * 0.0416666666667 for i in range(357)])
lon = np.array([-105.0416666666507 + i * 0.0416666666667 for i in range(722)])
Lon, Lat = np.meshgrid(lon, lat)

c_path = os.getcwd()

if 'diane_wt' in c_path:
    box_path = '/Users/diane_wt/Library/CloudStorage/Box-Box'
elif 'admin-dianew68' in c_path:
    box_path = 'C:/Users/admin-dianew68/Box'

work_dir = box_path + '/Diane/WORK/work_AJ/'

tmin81 = np.load(work_dir + f'prism/mw_tmin/1981_tmin.npz')['tmin']
t, y, x = tmin81.shape

dff = pd.date_range(start='1/1/1981', end='12/31/2023', freq='D')
year = np.array(dff.strftime('%Y')).astype(int)
year = np.delete(year, [1154, 2615, 4076, 5537, 6998, 8459, 9920, 11381, 12842, 14303])
mon = np.array(dff.strftime('%-m')).astype(int)
mon = np.delete(mon, [1154, 2615, 4076, 5537, 6998, 8459, 9920, 11381, 12842, 14303])
day = np.array(dff.strftime('%-d')).astype(int)
day = np.delete(day, [1154, 2615, 4076, 5537, 6998, 8459, 9920, 11381, 12842, 14303])

# am = rasterio.open('PRISM_tmin_stable_4kmD2_19810101_bil.bil')
# a = am.read()[0, :357, 479:1201]
# mask = np.where(a>-1000, 1, 0)

for yl in range(43):
    tmin = np.load(work_dir + f'prism/mw_tmin/{1981+yl}_tmin.npz')['tmin']
    tmax = np.load(work_dir + f'prism/mw_tmax/{1981+yl}_tmax.npz')['tmax']
    prec = np.load(work_dir + f'prism/mw_prec/{1981+yl}_prec.npz')['prec']
    for i in range(y):
        for j in range(x):
            tminij = []
            tmaxij = []
            precij = []

            if (1981+yl) % 4:
                tminij.extend(tmin[:, i, j])
                tmaxij.extend(tmax[:, i, j])
                precij.extend(prec[:, i, j])
            else:
                tminij.extend(tmin[:59, i, j])
                tminij.extend(tmin[60:, i, j])
                tmaxij.extend(tmax[:59, i, j])
                tmaxij.extend(tmax[60:, i, j])
                precij.extend(prec[:59, i, j])
                precij.extend(prec[60:, i, j])

            tminij = np.array(tminij)
            tmaxij = np.array(tmaxij)
            precij = np.array(precij)
            
            tminij = tminij * (9.0/5.0) + 32.0
            tmaxij = tmaxij * (9.0/5.0) + 32.0
            

            f = open(work_dir + f'prism/GDD_input/{Lat[i, j]:.2f}_{Lon[i, j]:.2f}_1981-2023.txt', 'a')
            if yl == 0:
                f.write('YEAR,MONTH,DAY,MAX,MIN,PREC\n')
                
            for k in range(365):
                f.write(f'{year[yl*365+k]},{mon[yl*365+k]},{day[yl*365+k]},{tmaxij[k]:.1f},{tminij[k]:.1f},{precij[k]:.2f}\n')
            f.close()