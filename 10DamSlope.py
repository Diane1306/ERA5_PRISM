import numpy as np
import rasterio
from scipy import stats

work_dir = '/home/mmfire/Diane/Ag_paper/'

tmin81 = np.load(work_dir + f'prism/mw_tmin/1981_tmin.npz')['tmin']
t, y, x = tmin81.shape

am = rasterio.open(work_dir + 'prism/data/tmin/1981/PRISM_tmin_stable_4kmD2_19810101_bil/PRISM_tmin_stable_4kmD2_19810101_bil.bil')
a = am.read()[0, :357, 479:1201]
mask = np.where(a>-1000, 1, 0)

lat = np.array([49.9166666666664 - i * 0.0416666666667 for i in range(357)])
lon = np.array([-105.0416666666507 + i * 0.0416666666667 for i in range(722)])
Lon, Lat = np.meshgrid(lon, lat)

DamDayann = np.load(work_dir + 'var/Cherry_DamDayann.npy')
DamDayStage = np.load(work_dir + 'var/Cherry_DamDayStage.npy')
DamMeanStage = np.load(work_dir + 'var/Cherry_DamMeanStage.npy')
TminStage = np.load(work_dir + 'var/Cherry_TminStage.npy')
DamDateStage = np.load(work_dir + 'var/Cherry_DamDateStage.npy')
TminDamStage = np.load(work_dir + 'var/Cherry_TminDamStage.npy')



DamDayann_slope = np.zeros((y, x)) * np.nan
stage_slope = np.zeros((5, 9, y, x)) * np.nan
stage_data = [DamDayStage, DamMeanStage, TminStage, DamDateStage, TminDamStage]

len_year = 43
X = np.linspace(1, len_year, len_year)
for i in range(y):
    for j in range(x):
        if mask[i, j]:
            r = stats.theilslopes(np.nan_to_num(DamDayann[:, i, j]), X, alpha=0.95)
            DamDayann_slope[i, j] = r[0]

            for di in range(5):
                for si in range(9):
                    if di < 3:
                        r = stats.theilslopes(np.nan_to_num(stage_data[di][:, si, i, j]), X, alpha=0.95)
                        stage_slope[di, si, i, j] = r[0]
                    else:
                        mm = ~np.isnan(stage_data[di][:, si, i, j])
                        if len(X[mm]) > 1:
                            r = stats.theilslopes(np.nan_to_num(stage_data[di][:, si, i, j][mm]), X[mm], alpha=0.95)
                            stage_slope[di, si, i, j] = r[0]

np.save(work_dir + 'var/Cherry_DamDayann_slope', DamDayann_slope)
np.save(work_dir + 'var/Cherry_stage_slope', stage_slope)
