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

DamDayann = np.zeros((38, y, x)) * np.nan
DamDayStage = np.zeros((38, 9, y, x)) * np.nan
DamMeanStage = np.zeros((38, 9, y, x)) * np.nan
TminStage = np.zeros((38, 9, y, x)) * np.nan
for i in range(y):
    for j in range(x):
        if mask[i, j]:
            df = pd.read_table(f'./GDD/output_Cherry/daily/{Lat[i, j]:.2f}_{Lon[i, j]:.2f}_daily.txt', delim_whitespace=True, 
                                   names=('YR','cd','TMAX','TMIN','rprecip','gdd','CDHTOT','STAGE','rgdd','FDIAMT','FDIAMS','DAM','YLD'))
            for yl in range(38):
                dfyl = df[yl*365:(yl+1)*365]
                grouped = dfyl.groupby(dfyl['STAGE'])
                if not (len(grouped) - 9):
                    DamDayann[yl, i, j] = np.where(dfyl['DAM'], 1, 0).sum()
                    DamDayStage[yl, :, i, j] = grouped['DAM'].apply(lambda column: (column != 0).sum())
                    DamMeanStage[yl, :, i, j] = grouped['DAM'].mean()
                    TminStage[yl, :, i, j] = grouped['TMIN'].mean()
                    
            print(i, j)
                    
np.save('./var/DamMeanStage', DamMeanStage)
np.save('./var/TminStage', TminStage)
np.save('./var/DamDayann', DamDayann)
np.save('./var/DamDayStage', DamDayStage)