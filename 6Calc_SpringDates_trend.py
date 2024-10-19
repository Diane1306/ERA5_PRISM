import numpy as np
import pandas as pd
import rasterio
from scipy import stats
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
var_mean = [np.zeros((y, x)) * np.nan for i in range(5)]
var_std = [np.zeros((y, x)) * np.nan for i in range(5)]
slope = [np.zeros((y, x)) * np.nan for i in range(5)]
pvalue = [np.zeros((y, x)) * np.nan for i in range(5)]
X = np.linspace(1, len_year, len_year)
name = ['year','sidegreen','bloom','pdays','yield']

recordnum = 0
for i in range(y):
    for j in range(x):
        if mask[i, j]:
            df = pd.read_table(work_dir + f'GDD/GDD_output/yearly/{Lat[i, j]:.2f}_{Lon[i, j]:.2f}_yearly.txt', sep='\s+',
                                   names=('year','sidegreen','bloom','pdays','yield'))
            for ii in range(1,5):
                var_mean[ii-1][i,j] = df[name[ii]][:len_year].mean()

                var_detrend = df[name[ii]][:len_year] - var_mean[ii-1][i, j]
                var_std[ii-1][i,j] = np.sqrt(((var_detrend - var_detrend.mean())**2).sum() / len_year)

                r = stats.theilslopes(df[name[ii]][:len_year], X, alpha=0.95)
                slope[ii-1][i, j] = r[0]

                result = mk.original_test(df[name[ii]][:len_year])
                pvalue[ii-1][i, j] = result.p

            spring = df['bloom'][:len_year] - df['sidegreen'][:len_year]
            var_mean[-1][i,j] = spring.mean()
            var_detrend = spring - var_mean[-1][i, j]
            var_std[-1][i,j] = np.sqrt(((var_detrend - var_detrend.mean())**2).sum() / len_year)
            r = stats.theilslopes(spring, X, alpha=0.95)
            slope[-1][i, j] = r[0]

            result = mk.original_test(spring)
            pvalue[-1][i, j] = result.p
            recordnum = recordnum + 1
            print(recordnum)

np.save(work_dir + 'var/var_yearly_Cherry', np.array(var_mean))
np.save(work_dir + 'var/var_std_Cherry', np.array(var_std))
np.save(work_dir + 'var/var_yearly_slope_Cherry', np.array(slope))
np.save(work_dir + 'var/var_yearly_pvalue_Cherry', np.array(pvalue))