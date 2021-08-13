import pandas as pd
import numpy as np
import rasterio

lat = np.array([49.9166666666664 - i * 0.0416666666667 for i in range(357)])
lon = np.array([-105.0416666666507 + i * 0.0416666666667 for i in range(722)])
Lon, Lat = np.meshgrid(lon, lat)

am = rasterio.open('PRISM_tmin_stable_4kmD2_19810101_bil.bil')
a = am.read()[0, :357, 479:1201]
mask = np.where(a>-1000, 1, 0)

tmin81 = np.load('./prism/mw_tmin/1981_tmin.npz')['tmin']
t, y, x = tmin81.shape

DamDateStage = np.zeros((40, 9, y, x)) * np.nan
TminDamStage = np.zeros((40, 9, y, x)) * np.nan
stage = [0., 2., 3., 4., 5., 6., 7., 8., 9.]
for i in range(y):
    for j in range(x):
        if mask[i, j]:
            df = pd.read_table(f'./GDD/output_Cherry/daily/{Lat[i, j]:.2f}_{Lon[i, j]:.2f}_daily.txt', delim_whitespace=True, 
                                   names=('YR','cd','TMAX','TMIN','rprecip','gdd','CDHTOT','STAGE','rgdd','FDIAMT','FDIAMS','DAM','YLD'))
            for yl in range(40):
                dfyl = df[yl*365:(yl+1)*365]
                grouped = dfyl.groupby(dfyl['STAGE'])
#                 if not (len(grouped) - 9):
                DamDay = grouped['DAM'].apply(lambda column: column.to_numpy().nonzero())
                for key, item in grouped:
                    damid = DamDay[key][0]
                    if len(damid):
                        index = stage.index(key)
                        DamDateStage[yl, index, i, j] = np.array([item['cd'].iloc[ii] for ii in damid]).mean()
                        TminDamStage[yl, index, i, j] = np.array([item['TMIN'].iloc[ii] for ii in damid]).mean()
            print(i, j)
np.save('./var/Cherry_DamDateStage', DamDateStage)
np.save('./var/Cherry_TminDamStage', TminDamStage)