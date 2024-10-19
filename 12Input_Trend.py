import numpy as np
import rasterio
from scipy import stats
import pandas as pd
import pymannkendall as mk

lat = np.array([49.9166666666664 - i * 0.0416666666667 for i in range(357)])
lon = np.array([-105.0416666666507 + i * 0.0416666666667 for i in range(722)])
Lon, Lat = np.meshgrid(lon, lat)

work_dir = '/home/mmfire/Diane/Ag_paper/'

tmin81 = np.load(work_dir + f'prism/mw_tmin/1981_tmin.npz')['tmin']
t, y, x = tmin81.shape

am = rasterio.open(work_dir + 'prism/data/tmin/1981/PRISM_tmin_stable_4kmD2_19810101_bil/PRISM_tmin_stable_4kmD2_19810101_bil.bil')
a = am.read()[0, :357, 479:1201]
mask = np.where(a>-1000, 1, 0)

len_year = 40
tmax = np.zeros((len_year, y, x)) * np.nan
tmin = np.zeros((len_year, y, x)) * np.nan
for i in range(y):
    for j in range(x):
        if mask[i, j]:
            df = pd.read_table(work_dir + f'GDD/GDD_output/daily/{Lat[i, j]:.2f}_{Lon[i, j]:.2f}_daily.txt',
                               sep='\s+',
                               names=('YR', 'cd', 'TMAX', 'TMIN', 'rprecip', 'gdd', 'CDHTOT', 'STAGE', 'rgdd', 'FDIAMT',
                                      'FDIAMS', 'DAM', 'YLD'))
            for yl in range(len_year):
                dfyl = df[yl * 365 + 59:(yl + 1) * 365 + 151]
                tmax[yl, i, j] = dfyl['TMAX'].mean()
                tmin[yl, i, j] = dfyl['TMIN'].mean()
np.save(work_dir + 'var/spring_tmax', tmax)
np.save(work_dir + 'var/spring_tmin', tmin)

slope = np.zeros((2, y, x)) * np.nan
pvalue = np.zeros((2, y, x)) * np.nan
std = np.zeros((2, y, x)) * np.nan
mean = np.zeros((2, y, x)) * np.nan
X = np.linspace(1, len_year, len_year)
data = [tmax, tmin]
for i in range(y):
    for j in range(x):
        if mask[i, j]:
            for vi in range(2):
                mean[vi, i, j] = np.nanmean(data[vi][:, i, j])
                std[vi, i, j] = np.nanstd(data[vi][:, i, j])

                r = stats.theilslopes(data[vi][:, i, j], X, alpha=0.95)
                slope[vi, i, j] = r[0]
                result = mk.original_test(data[vi][:, i, j])
                pvalue[vi, i, j] = result.p

np.save(work_dir + 'var/spring_input_slope', slope)
np.save(work_dir + 'var/spring_input_mean', mean)
np.save(work_dir + 'var/spring_input_std', std)
np.save(work_dir + 'var/spring_input_pvalue', pvalue)