import numpy as np
import rasterio
from scipy import stats
import pandas as pd

lat = np.array([49.9166666666664 - i * 0.0416666666667 for i in range(357)])
lon = np.array([-105.0416666666507 + i * 0.0416666666667 for i in range(722)])
Lon, Lat = np.meshgrid(lon, lat)

am = rasterio.open('PRISM_tmin_stable_4kmD2_19810101_bil.bil')
a = am.read()[0, :357, 479:1201]
mask = np.where(a>-1000, 1, 0)

tmin81 = np.load('./prism/mw_tmin/1981_tmin.npz')['tmin']
t, y, x = tmin81.shape

tmax = np.zeros((40, y, x)) * np.nan
tmin = np.zeros((40, y, x)) * np.nan
for i in range(y):
    for j in range(x):
        if mask[i, j]:
            df = pd.read_table(f'./GDD/output_Cherry/daily/{Lat[i, j]:.2f}_{Lon[i, j]:.2f}_daily.txt', delim_whitespace=True, 
                                   names=('YR','cd','TMAX','TMIN','rprecip','gdd','CDHTOT','STAGE','rgdd','FDIAMT','FDIAMS','DAM','YLD'))
            for yl in range(40):
                dfyl = df[yl*365+59:(yl+1)*365+151]
                tmax[yl, i, j] = dfyl['TMAX'].mean()
                tmin[yl, i, j] = dfyl['TMIN'].mean()
                
np.save('./var/spring_tmax', tmax)
np.save('./var/spring_tmin', tmin)

slope = np.zeros((2, y, x)) * np.nan
pvalue = np.zeros((2, y, x)) * np.nan
std = np.zeros((2, y, x)) * np.nan
mean = np.zeros((2, y, x)) * np.nan
X = np.linspace(1, 40, 40)
data = [tmax, tmin]
for i in range(y):
    for j in range(x):
        if mask[i, j]:
            for vi in range(2):
                mean[vi, i, j] = np.nanmean(data[vi][:, i, j])
                std[vi, i, j] = np.nanstd(data[vi][:, i, j])
                
                r = stats.linregress(X, data[vi][:, i, j])
                slope[vi, i, j] = r.slope
                pvalue[vi, i, j] = r.pvalue
                
np.save('./var/spring_input_slope', slope)   
np.save('./var/spring_input_pvalue', pvalue)   
np.save('./var/spring_input_mean', mean)
np.save('./var/spring_input_std', std)   