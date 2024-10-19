import pandas as pd
import numpy as np
import rasterio

work_dir = '/home/mmfire/Diane/Ag_paper/'

tmin81 = np.load(work_dir + f'prism/mw_tmin/1981_tmin.npz')['tmin']
t, y, x = tmin81.shape

am = rasterio.open(work_dir + 'prism/data/tmin/1981/PRISM_tmin_stable_4kmD2_19810101_bil/PRISM_tmin_stable_4kmD2_19810101_bil.bil')
a = am.read()[0, :357, 479:1201]
mask = np.where(a>-1000, 1, 0)

lat = np.array([49.9166666666664 - i * 0.0416666666667 for i in range(357)])
lon = np.array([-105.0416666666507 + i * 0.0416666666667 for i in range(722)])
Lon, Lat = np.meshgrid(lon, lat)

len_year = 40
si = np.zeros((len_year, y, x)) * np.nan
for i in range(y):
    for j in range(x):
        if mask[i, j]:
            dfy = pd.read_table(work_dir + f'GDD/GDD_output/yearly/{Lat[i, j]:.2f}_{Lon[i, j]:.2f}_yearly.txt', sep='\s+',
                                   names=('year','sidegreen','bloom','pdays','yield'))
            sddate = dfy['sidegreen'][:len_year]
            si[:, i, j] = (sddate - min(sddate))/ (max(sddate) - min(sddate))
np.save(work_dir + 'var/Cherry_sidegreen_norm', si)

FirstDamDate = np.zeros((len_year, y, x)) * np.nan
for i in range(y):
    for j in range(x):
        if mask[i, j]:
            df = pd.read_table(work_dir + f'GDD/GDD_output/daily/{Lat[i, j]:.2f}_{Lon[i, j]:.2f}_daily.txt', sep='\s+',
                                   names=('YR','cd','TMAX','TMIN','rprecip','gdd','CDHTOT','STAGE','rgdd','FDIAMT','FDIAMS','DAM','YLD'))
            for yl in range(len_year):
                dfyl = df[yl*365:(yl+1)*365]
                DamDay = dfyl['DAM'].to_numpy().nonzero()
                if len(DamDay[0]):
                    FirstDamDate[yl, i, j] = dfyl['cd'].iloc[DamDay[0][0]]
                # if len(DamDay[0])>2: #select damage days more than 2 days
                #     FirstDamDate[yl, i, j] = dfyl['cd'].iloc[DamDay[0][0]]
np.save(work_dir + 'var/Cherry_FirstDamDate1day', FirstDamDate)
