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

stage = [0., 2., 3., 4., 5., 6., 7., 8., 9.]
DamDayann = np.zeros((40, y, x)) * np.nan
DamDayStage = np.zeros((40, 9, y, x)) * np.nan
DamMeanStage = np.zeros((40, 9, y, x)) * np.nan
TminStage = np.zeros((40, 9, y, x)) * np.nan
for i in range(y):
    for j in range(x):
        if mask[i, j]:
            df = pd.read_table(f'./GDD/output_Cherry/daily/{Lat[i, j]:.2f}_{Lon[i, j]:.2f}_daily.txt', delim_whitespace=True, 
                                   names=('YR','cd','TMAX','TMIN','rprecip','gdd','CDHTOT','STAGE','rgdd','FDIAMT','FDIAMS','DAM','YLD'))
            for yl in range(40):
                dfyl = df[yl*365:(yl+1)*365]
                DamDayann[yl, i, j] = np.where(dfyl['DAM'], 1, 0).sum()
                grouped = dfyl.groupby(dfyl['STAGE'])
#                 if not (len(grouped) - 9):
                DamDay = grouped['DAM'].apply(lambda column: column.to_numpy().nonzero()) #return indices those are nonzeros in each group
                for key, item in grouped:
                    index = stage.index(key) #get which stage
                    TminStage[yl, index, i, j] = item['TMIN'].mean()
                    damid = DamDay[key][0] #get the indices at each stage
                    if len(damid):
                        DamValue = np.array([item['DAM'].iloc[ii] for ii in damid])
                        DamDayStage[yl, index, i, j] = DamValue.shape[0]
                        DamMeanStage[yl, index, i, j] = DamValue.mean()                    
            print(i, j)
                    
np.save('./var/Cherry_DamMeanStage', DamMeanStage)
np.save('./var/Cherry_TminStage', TminStage)
np.save('./var/Cherry_DamDayann', DamDayann)
np.save('./var/Cherry_DamDayStage', DamDayStage)