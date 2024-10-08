import numpy as np
import pandas as pd
import rasterio

lat = np.array([49.9166666666664 - i * 0.0416666666667 for i in range(357)])
lon = np.array([-105.0416666666507 + i * 0.0416666666667 for i in range(722)])
Lon, Lat = np.meshgrid(lon, lat)

tmin81 = np.load('./prism/mw_tmin/1981_tmin.npz')['tmin']
t, y, x = tmin81.shape

dff = pd.date_range(start='1/1/1981', end='12/31/2018', freq='D')
year = np.array(dff.strftime('%Y')).astype(int)
year = np.delete(year, [1154, 2615, 4076, 5537, 6998, 8459, 9920, 11381, 12842])
mon = np.array(dff.strftime('%-m')).astype(int)
mon = np.delete(mon, [1154, 2615, 4076, 5537, 6998, 8459, 9920, 11381, 12842])
day = np.array(dff.strftime('%-d')).astype(int)
day = np.delete(day, [1154, 2615, 4076, 5537, 6998, 8459, 9920, 11381, 12842])

am = rasterio.open('PRISM_tmin_stable_4kmD2_19810101_bil.bil')
a = am.read()[0, :357, 479:1201]
mask = np.where(a>-1000, 1, 0)

for i in range(y):
    for j in range(x):
        if mask[i, j]:
            tminij = []
            tmaxij = []
            precij = []
            for yl in range(38):
                tmin = np.load(f'./prism/mw_tmin/{1981+yl}_tmin.npz')['tmin']
                tminij.extend(tmin[:, i, j])
                tmax = np.load(f'./prism/mw_tmax/{1981+yl}_tmax.npz')['tmax']
                tmaxij.extend(tmax[:, i, j])
                prec = np.load(f'./prism/mw_prec/{1981+yl}_prec.npz')['prec']
                precij.extend(prec[:, i, j])
            tminij = np.array(tminij)
            tminij = np.delete(tminij, [1154, 2615, 4076, 5537, 6998, 8459, 9920, 11381, 12842])
            tmaxij = np.array(tmaxij)
            tmaxij = np.delete(tmaxij, [1154, 2615, 4076, 5537, 6998, 8459, 9920, 11381, 12842])
            precij = np.array(precij)
            precij = np.delete(precij, [1154, 2615, 4076, 5537, 6998, 8459, 9920, 11381, 12842])

            tminij = tminij * (9.0/5.0) + 32.0
            tmaxij = tmaxij * (9.0/5.0) + 32.0
            
            f = open(f'./{Lat[i, j]:5.2f}_{Lon[i, j]:7.2f}_1981-2018.txt', "w")
            f.write('YEAR,MONTH,DAY,MAX,MIN,PREC\n')
            for k in range(len(year)):
                f.write(f'{year[k]},{mon[k]},{day[k]},{tmaxij[k]:.1f},{tminij[k]:.1f},{precij[k]:.2f}\n')
            f.close()
                
