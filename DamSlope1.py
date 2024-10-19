import numpy as np
import rasterio
from scipy import stats

DamDayann = np.load('./var/Cherry_DamDayann.npy')
DamDayStage = np.load('./var/Cherry_DamDayStage.npy')
DamMeanStage = np.load('./var/Cherry_DamMeanStage.npy')
TminStage = np.load('./var/Cherry_TminStage.npy')
DamDateStage = np.load('./var/Cherry_DamDateStage.npy')
TminDamStage = np.load('./var/Cherry_TminDamStage.npy')

lat = np.array([49.9166666666664 - i * 0.0416666666667 for i in range(357)])
lon = np.array([-105.0416666666507 + i * 0.0416666666667 for i in range(722)])
Lon, Lat = np.meshgrid(lon, lat)

am = rasterio.open('PRISM_tmin_stable_4kmD2_19810101_bil.bil')
a = am.read()[0, :357, 479:1201]
mask = np.where(a>-1000, 1, 0)

tmin81 = np.load('./prism/mw_tmin/1981_tmin.npz')['tmin']
t, y, x = tmin81.shape

DamDayann_slope = np.zeros((y, x)) * np.nan
DamDayann_pvalue = np.zeros((y, x)) * np.nan
# stage_data = [DamDateStage, TminDamStage]
stage_slope = np.zeros((5, 9, y, x)) * np.nan
stage_pvalue = np.zeros((5, 9, y, x)) * np.nan
stage_data = [DamDayStage, DamMeanStage, TminStage, DamDateStage, TminDamStage]

X = np.linspace(1, 40, 40)
for i in range(y):
    for j in range(x):
        if mask[i, j]:
            r = stats.linregress(X, np.nan_to_num(DamDayann[:, i, j]))
            DamDayann_slope[i, j] = r.slope
            DamDayann_pvalue[i, j] = r.pvalue
            
            for di in range(5):
                for si in range(9):
                    if di<3:
                        r = stats.linregress(X, np.nan_to_num(stage_data[di][:, si, i, j]))
                        stage_slope[di, si, i, j] = r.slope
                        stage_pvalue[di, si, i, j] = r.pvalue
                    else:
                        mm = ~np.isnan(stage_data[di][:, si, i, j])
                        if len(X[mm])>1:
                            r = stats.linregress(X[mm], np.nan_to_num(stage_data[di][:, si, i, j][mm]))
                            stage_slope[di, si, i, j] = r.slope
                            stage_pvalue[di, si, i, j] = r.pvalue
                    
np.save('./var/Cherry_DamDayann_slope', DamDayann_slope)
np.save('./var/Cherry_DamDayann_pvalue', DamDayann_pvalue)
np.save('./var/Cherry_stage_slope', stage_slope)
np.save('./var/Cherry_stage_pvalue', stage_pvalue)
