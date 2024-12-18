import matplotlib.pyplot as plt
import numpy as np
import cartopy
import matplotlib as mpl
mpl.rc("savefig", dpi=300)
import rasterio
from scipy import stats
import pymannkendall as mk

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
cherrymask = np.load(work_dir + 'var/Cherry_mask.npy')

NYmask = np.where(np.logical_or.reduce((mdmask['NY'], cherrymask)), 1, 0)
PAmask = np.where(np.logical_or.reduce((mdmask['PA'], cherrymask)), 1, 0)
WImask = np.where(np.logical_or.reduce((mdmask['WI'], cherrymask)), 1, 0)
MImask = np.where(np.logical_or.reduce((mdmask['MI'], cherrymask)), 1, 0)

mdmask_sub = [NYmask, PAmask, WImask, MImask]
region = ['NY', 'PA', 'WI', 'MI']

len_year = 40
DamDayann = np.load(work_dir + f'var/Cherry_DamDayann.npy')
DamDayann_states = np.zeros((len_year, len(mdmask_sub)))
for yl in range(len_year):
    DamDayann_states[yl, :] = np.array(
        [np.nanmean(np.where(mdmask_sub[ii], DamDayann[yl, :, :], np.nan)) for ii in range(len(mdmask_sub))])

X = np.linspace(1981, 2020, len_year)
slope = []
pvalue = []
for ri in range(len(mdmask_sub)):
    flag = ~np.isnan(DamDayann_states[:, ri])
    if len(X[flag]):
        r = stats.theilslopes(DamDayann_states[:, ri][flag], X[flag], alpha=0.95)
        slope.append(r[0])

        result = mk.original_test(DamDayann_states[:, ri][flag])
        pvalue.append(result.p)
yl =0
yr = 10
fig, axs = plt.subplots(2, 2, sharex=True, sharey=True, figsize=(12, 5))
for i in range(len(mdmask_sub)):
    ax = plt.subplot(2, 2, i + 1)
    plt.plot(X, DamDayann_states[:, i], 'bo-', ms=3)
    plt.ylim(0, 10)
    ax.text(.01, .9, f'mean = {np.nanmean(DamDayann_states[:, i]):.2f}', fontsize=15, transform=ax.transAxes)
    ax.text(.01, .8, f'std = {np.nanstd(DamDayann_states[:, i]):.2f}', fontsize=15, transform=ax.transAxes)
    ax.text(.01, .7, f'trend = {slope[i]:.2f} (p={pvalue[i]:.4f})', fontsize=15,transform=ax.transAxes)
    ax.text(.99, .9, f'{region[i]}', fontsize=16, fontweight='bold', horizontalalignment='right',
            transform=ax.transAxes)
    #     plt.grid()
    plt.vlines(np.arange(1981, 2021, 4), 0, 10, alpha=0.5, linestyles='dashed', colors='grey')
    plt.subplots_adjust(wspace=.06)
    if not i % 2:
        ax.set_yticks(np.arange(0, yr + 1, 3))
        ax.set_yticklabels(np.arange(0, yr + 1, 3), fontsize=14)
        ax.set_ylabel('Damage Days', fontsize=15)
    else:
        ax.set_yticks(np.arange(0, yr + 1, 3))

    if i < 2:
        plt.xticks(np.arange(1981, 2021, 4), [])
    else:
        plt.xticks(np.arange(1981, 2021, 1), ['81', '', '', '', '85', '', '', '', '89', '', '', '', '93', '', '', '',
                                              '97', '', '', '', '01', '', '', '', '05', '', '', '', '09', '', '', '',
                                              '13', '', '', '', '17', '', '', ''], fontsize=14)
        #         plt.xticks(np.arange(1981, 2021, 4), fontsize=14)
        plt.xlabel('Year', fontsize=15)
plt.subplots_adjust(bottom=0.02, top=.98, left=0.02, right=.98,
                    wspace=0.005, hspace=0.07)
plt.savefig(work_dir + 'plot/5DamDayByCherryYieldCountyTimeSeries.png', bbox_inches='tight')
plt.close()