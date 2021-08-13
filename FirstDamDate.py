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

# si = np.zeros((40, y, x)) * np.nan
# for i in range(y):
#     for j in range(x):
#         if mask[i, j]:
#             dfy = pd.read_table(f'./GDD/output_Cherry/yearly/{Lat[i, j]:.2f}_{Lon[i, j]:.2f}_yearly.txt', delim_whitespace=True, 
#                                    names=('year','sidegreen','bloom','pdays','yield'))
#             si[:, i, j] = dfy['sidegreen']
# np.save('./var/Cherry_sidegreen', si)

FirstDamDate = np.zeros((40, y, x)) * np.nan
for i in range(y):
    for j in range(x):
        if mask[i, j]:
            df = pd.read_table(f'./GDD/output_Cherry/daily/{Lat[i, j]:.2f}_{Lon[i, j]:.2f}_daily.txt', delim_whitespace=True, 
                                   names=('YR','cd','TMAX','TMIN','rprecip','gdd','CDHTOT','STAGE','rgdd','FDIAMT','FDIAMS','DAM','YLD'))
            for yl in range(40):
                dfyl = df[yl*365:(yl+1)*365]
                DamDay = dfyl['DAM'].to_numpy().nonzero()
#                 if len(DamDay[0]):
#                     FirstDamDate[yl, i, j] = dfyl['cd'].iloc[DamDay[0][0]]
                if len(DamDay[0])>2: #select damage days more than 2 days
                    FirstDamDate[yl, i, j] = dfyl['cd'].iloc[DamDay[0][0]]  
np.save('./var/Cherry_FirstDamDate3days', FirstDamDate)
