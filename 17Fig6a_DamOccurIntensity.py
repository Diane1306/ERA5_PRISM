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
NYmask = np.where(mdmask['NY'], 1, 0)
PAmask = np.where(mdmask['PA'], 1, 0)
WImask = np.where(mdmask['WI'], 1, 0)
MImask = np.where(mdmask['MI'], 1, 0)

mdmask_sub = [NWmask, SWmask, NCmask, Cmask, NYmask, PAmask, WImask, MImask]
region = ['Northern Great Plains', 'Southern Great Plains', 'Upper Midwest', 'Ohio Valley', 'NY', 'PA', 'WI', 'MI']

def trend(slope):
    if slope<0:
        return 'b', '-'
    else:
        return 'r', '+'

len_year = 43
DamDayStage = np.load(work_dir + f'var/Cherry_DamDayStage.npy')
DamDayStage_states = np.zeros((len_year, 9, len(mdmask_sub)))
for yl in range(len_year):
    for st in range(9):
        DamDayStage_states[yl, st, :] = np.array(
            [np.nanmean(np.where(mdmask_sub[ii], DamDayStage[yl, st, :, :], np.nan)) for ii in range(len(mdmask_sub))])
DamDayStage_states_mean = np.nanmean(DamDayStage_states, axis=0)

DamMeanStage = np.load(work_dir + f'var/Cherry_DamMeanStage.npy')
DamMeanStage_states = np.zeros((len_year, 9, len(mdmask_sub)))
for yl in range(len_year):
    for st in range(9):
        DamMeanStage_states[yl, st, :] = np.array(
            [np.nanmean(np.where(mdmask_sub[ii], DamMeanStage[yl, st, :, :], np.nan)) for ii in range(len(mdmask_sub))])
DamMeanStage_states_sum = np.nanmean(DamMeanStage_states, axis=0)

slope_occur = np.zeros((9, len(mdmask_sub))) * np.nan
slope_inten = np.zeros((9, len(mdmask_sub))) * np.nan
DamYearCount = np.zeros((9, len(mdmask_sub)))
year = np.linspace(1981, 2023, len_year)
for si in range(9):
    for ri in range(len(mdmask_sub)):
        flag1 = ~np.isnan(DamDayStage_states[:, si, ri])
        if len(year[flag1]):
            r = stats.theilslopes(DamDayStage_states[:, si, ri][flag1], year[flag1], alpha=0.95)
            slope_occur[si, ri] = r[0]
        DamYearCount[si, ri] = flag1.sum()
        flag2 = ~np.isnan(DamMeanStage_states[:, si, ri])
        if len(year[flag2]):
            r = stats.theilslopes(DamMeanStage_states[:, si, ri][flag2], year[flag2], alpha=0.95)
            slope_inten[si, ri] = r[0]

X = np.linspace(0, 8, 9)
fig, axs = plt.subplots(4, 2, sharex=True, sharey=True, figsize=(13, 9))
for i in range(len(mdmask_sub)):
    ax = plt.subplot(4, 2, i + 1)
    plt.xticks(X, ['0', '2', '3', '4', '5', '6', '7', '8', '9'], fontsize=15)
    ax.bar(X - .2, DamDayStage_states_mean[:, i], width=.4, facecolor='springgreen', label='Frequency')
    axx = ax.twinx()
    axx.bar(X + .2, DamMeanStage_states_sum[:, i], width=.4, facecolor='green', label='Severity')
    for si in range(9):
        ax.text(X[si] - .35, DamDayStage_states_mean[si, i] + 0.3, int(DamYearCount[si, i]), color='k', fontsize=10,
                fontweight='bold')
        if not np.isnan(slope_occur[si, i]):
            c, s = trend(slope_occur[si, i])
            ax.text(X[si] - .35, DamDayStage_states_mean[si, i], s, color=c, fontsize=15, fontweight='bold')
        if not np.isnan(slope_inten[si, i]):
            c, s = trend(slope_inten[si, i])
            axx.text(X[si] + .05, DamMeanStage_states_sum[si, i], s, color=c, fontsize=15, fontweight='bold')
    ax.set_ylim(0, 4)
    axx.set_ylim(0, 1)
    ax.set_xlim(-1, 9)
    axx.set_xlim(-1, 9)
    ax.text(.99, .9, f'{region[i]}', fontsize=16, fontweight='bold', horizontalalignment='right',
            transform=ax.transAxes)
    if not i % 2:
        axx.set_yticks([])
        ax.set_yticks([0, 1, 2, 3, 4])
        ax.set_yticklabels([0, 1, 2, 3, 4], fontsize=15, color='springgreen')
        ax.set_ylabel('Damage days', fontsize=15)
    else:
        # ax.set_yticks([])
        axx.set_yticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
        axx.set_yticklabels([0.0, 0.2, 0.4, 0.6, 0.8, 1.0], fontsize=15, color='green')
        axx.set_ylabel('Damage percent', fontsize=15)
    if i == 6:
        ax.legend(loc='upper left', fontsize=15, frameon=False)
        ax.set_xlabel('Phenological Stages', fontsize=15)
    if i == 7:
        axx.legend(loc='upper left', fontsize=15, frameon=False)
        ax.set_xlabel('Phenological Stages', fontsize=15)

plt.subplots_adjust(bottom=0.02, top=.98, left=0.02, right=.98,
                    wspace=0.005, hspace=0.12)
plt.savefig(work_dir + 'plot/6a_DamOccurIntensity.png', bbox_inches='tight')
plt.close()