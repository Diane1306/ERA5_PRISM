import numpy as np
import rasterio
from scipy import stats

DamDayann = np.load('./var/DamDayann.npy')
DamDayStage = np.load('./var/DamDayStage.npy')
DamMeanStage = np.load('./var/DamMeanStage.npy')
TminStage = np.load('./var/TminStage.npy')
DamDateStage = np.load('./var/DamDateStage.npy')
TminDamStage = np.load('./var/TminDamStage.npy')

lat = np.array([49.9166666666664 - i * 0.0416666666667 for i in range(357)])
lon = np.array([-105.0416666666507 + i * 0.0416666666667 for i in range(722)])
Lon, Lat = np.meshgrid(lon, lat)

am = rasterio.open('PRISM_tmin_stable_4kmD2_19810101_bil.bil')
a = am.read()[0, :357, 479:1201]
mask = np.where(a>-1000, 1, 0)

tmin81 = np.load('./prism/mw_tmin/1981_tmin.npz')['tmin']
t, y, x = tmin81.shape
y, x

DamDayann_slope = np.zeros((y, x)) * np.nan
DamDayann_pvalue = np.zeros((y, x)) * np.nan
DamDayann_slope_rmd = np.zeros((y, x)) * np.nan
DamDayann_pvalue_rmd = np.zeros((y, x)) * np.nan
stage_slope = np.zeros((5, 9, y, x)) * np.nan
stage_pvalue = np.zeros((5, 9, y, x)) * np.nan
stage_data = [DamDayStage, DamMeanStage, TminStage, DamDateStage, TminDamStage]

X = np.linspace(1, 38, 38)
for i in range(y):
    for j in range(x):
        if mask[i, j]:
            r = stats.linregress(X, DamDayann[:, i, j])
            DamDayann_slope[i, j] = r.slope
            DamDayann_pvalue[i, j] = r.pvalue
            
            r = stats.linregress(X[np.r_[0:30,32:38]], DamDayann[:, i, j][np.r_[0:30,32:38]])
            DamDayann_slope_rmd[i, j] = r.slope
            DamDayann_pvalue_rmd[i, j] = r.pvalue
            for di in range(5):
                for si in range(9):
                    r = stats.linregress(X, stage_data[di][:, si, i, j])
                    stage_slope[di, si, i, j] = r.slope
                    stage_pvalue[di, si, i, j] = r.pvalue
                    
np.save('./var/DamDayann_slope', DamDayann_slope)
np.save('./var/DamDayann_pvalue', DamDayann_pvalue)
np.save('./var/DamDayann_slope_rmd', DamDayann_slope_rmd)
np.save('./var/DamDayann_pvalue_rmd', DamDayann_pvalue_rmd)
np.save('./var/stage_slope', stage_slope)
np.save('./var/stage_pvalue', stage_pvalue)
