import matplotlib.pyplot as plt
import numpy as np
import cartopy
import matplotlib as mpl
mpl.rc("savefig", dpi=300)
import rasterio
from scipy import stats

lat = np.array([49.9166666666664 - i * 0.0416666666667 for i in range(357)])
lon = np.array([-105.0416666666507 + i * 0.0416666666667 for i in range(722)])
Lon, Lat = np.meshgrid(lon, lat)

work_dir = '/home/mmfire/Diane/Ag_paper/'

am = rasterio.open(work_dir + 'prism/data/tmin/1981/PRISM_tmin_stable_4kmD2_19810101_bil/PRISM_tmin_stable_4kmD2_19810101_bil.bil')
a = am.read()[0, :357, 479:1201]
mask = np.where(a>-1000, 1, 0)

# Set the path to the directory containing the downloaded shapefiles
cartopy.config['data_dir'] = '/home/mmfire/Diane/Ag_paper/shapefiles'  # Change to your directory

states = ['MI', 'ND', 'SD', 'NE', 'KS', 'OK', 'MN', 'IA', 'MO', 'WI', 'IL', 'IN', 'OH', 'KY', 'WV', 'PA', 'AR', 'TN', 'NY', 'MD', 'VA', 'NC']
mdmask = {states[ii]:np.load(work_dir + f'var/{states[ii]}_mask.npy') for ii in range(22)}

NWmask = np.where(np.logical_or.reduce((mdmask['ND'], mdmask['SD'], mdmask['NE'])), 1, 0)
SWmask = np.where(np.logical_or.reduce((mdmask['KS'], mdmask['OK'], mdmask['AR'])), 1, 0)
NCmask = np.where(np.logical_or.reduce((mdmask['MN'], mdmask['IA'], mdmask['WI'], mdmask['MI'])), 1, 0)
Cmask = np.where(np.logical_or.reduce((mdmask['MO'], mdmask['IL'], mdmask['IN'], mdmask['OH'], mdmask['KY'], mdmask['TN'], mdmask['WV'])), 1, 0)
NEmask = np.where(np.logical_or.reduce((mdmask['NY'], mdmask['PA'], mdmask['MD'])), 1, 0)
SEmask = np.where(np.logical_or(mdmask['VA'], mdmask['NC']), 1, 0)
mdmask_sub = [NWmask, SWmask, NCmask, Cmask, NEmask, SEmask]
region = ['Northern Great Plains', 'Southern Great Plains', 'Upper Midwest', 'Ohio Valley', 'NY-PA', 'VA-NC']

def trend(slope):
    if slope<0:
        return 'b', '-'
    else:
        return 'r', '+'

len_year = 43
TminDamStage = np.load(work_dir + f'var/Cherry_TminDamStage.npy')
TminDamStage_states = np.zeros((len_year, 9, len(mdmask_sub)))
for yl in range(len_year):
    for st in range(9):
        TminDamStage_states[yl, st, :] = np.array(
            [np.nanmean(np.where(mdmask_sub[ii], TminDamStage[yl, st, :, :], np.nan)) for ii in range(len(mdmask_sub))])
TminDamStage_states_mean = np.nanmean(TminDamStage_states, axis=0)

DamDateStage = np.load(work_dir + f'var/Cherry_DamDateStage.npy')
DamDateStage_states = np.zeros((len_year, 9, len(mdmask_sub)))
for yl in range(len_year):
    for st in range(9):
        DamDateStage_states[yl, st, :] = np.array(
            [np.nanmean(np.where(mdmask_sub[ii], DamDateStage[yl, st, :, :], np.nan)) for ii in range(len(mdmask_sub))])
DamDateStage_states_sum = np.nanmean(DamDateStage_states, axis=0)

slope_tmin = np.zeros((9, len(mdmask_sub))) * np.nan
slope_date = np.zeros((9, len(mdmask_sub))) * np.nan
DamYearCount = np.zeros((9, len(mdmask_sub))) * np.nan
year = np.linspace(1981, 2023, len_year)
for si in range(9):
    for ri in range(len(mdmask_sub)):
        flag1 = ~np.isnan(TminDamStage_states[:, si, ri])
        if len(year[flag1]):
            r = stats.theilslopes(TminDamStage_states[:, si, ri][flag1], year[flag1], alpha=0.95)
            slope_tmin[si, ri] = r[0]
        DamYearCount[si, ri] = flag1.sum()
        flag2 = ~np.isnan(DamDateStage_states[:, si, ri])
        if len(year[flag2]):
            r = stats.theilslopes(DamDateStage_states[:, si, ri][flag2], year[flag2], alpha=0.95)
            slope_date[si, ri] = r[0]

X = np.linspace(0, 8, 9)
plt.subplots(3, 2, sharex=True, sharey=True, figsize=(12, 7))
for i in range(len(mdmask_sub)):
    ax = plt.subplot(3, 2, i + 1)
    plt.xticks(X, ['0', '2', '3', '4', '5', '6', '7', '8', '9'], fontsize=15)
    axx = ax.twinx()
    ax.plot(X[1:], TminDamStage_states_mean[:, i][1:], 'o-', color='orange', label='Dam Tmin')
    axx.bar(X, DamDateStage_states_sum[:, i], width=.4, facecolor='green', label='Dam Date')
    ax.set_ylim(-15, 0)
    axx.set_ylim(0, 240)
    ax.set_xlim(-1, 9)
    axx.set_xlim(-1, 9)
    if not i % 2:
        axx.set_yticks([])
        ax.set_yticks(np.arange(-15, 1, 3))
        ax.set_yticklabels(np.arange(-15, 1, 3), fontsize=15, color='orange')
        ax.set_ylabel('Temperature (\u2103)', fontsize=15)
    else:
        # ax.set_yticks([])
        axx.set_yticks(np.arange(0, 250, 40))
        axx.set_yticklabels(np.arange(0, 250, 40), fontsize=15, color='green')
        axx.set_ylabel('Julian Date', fontsize=15)

    for si in range(9):
        axx.text(X[si] - .15, DamDateStage_states_sum[si, i] + 20, int(DamYearCount[si, i]), color='k', fontsize=10,
                 fontweight='bold')
        if (not np.isnan(slope_tmin[si, i])) and si > 0:
            c, s = trend(slope_tmin[si, i])
            ax.text(X[si] - .15, TminDamStage_states_mean[si, i], s, color=c, fontsize=15, fontweight='bold')
        if not np.isnan(slope_date[si, i]):
            c, s = trend(slope_date[si, i])
            axx.text(X[si] - .15, DamDateStage_states_sum[si, i], s, color=c, fontsize=15, fontweight='bold')

    ax.text(.99, .9, f'{region[i]}', fontsize=16, fontweight='bold', horizontalalignment='right',
            transform=ax.transAxes)
    if i == 4:
        ax.legend(loc='upper left', fontsize=15, frameon=False)
        ax.set_xlabel('Phenological Stages', fontsize=15)
    if i == 5:
        axx.legend(loc='upper left', fontsize=15, frameon=False)
        ax.set_xlabel('Phenological Stages', fontsize=15)

plt.subplots_adjust(bottom=0.02, top=.98, left=0.02, right=.98,
                    wspace=0.005, hspace=0.12)
plt.savefig(work_dir + 'plot/6b_DamDateTmin_original.png', bbox_inches='tight')
plt.close()