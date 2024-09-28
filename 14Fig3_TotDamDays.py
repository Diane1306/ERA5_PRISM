import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs
import cartopy
from matplotlib.ticker import MaxNLocator
from matplotlib.colors import BoundaryNorm
import matplotlib as mpl
mpl.rc("savefig", dpi=300)

lat = np.array([49.9166666666664 - i * 0.0416666666667 for i in range(357)])
lon = np.array([-105.0416666666507 + i * 0.0416666666667 for i in range(722)])
Lon, Lat = np.meshgrid(lon, lat)

work_dir = '/home/mmfire/Diane/Ag_paper/'

# Set the path to the directory containing the downloaded shapefiles
cartopy.config['data_dir'] = '/home/mmfire/Diane/Ag_paper/shapefiles'  # Change to your directory

DamDayann = np.load(work_dir + 'var/Cherry_DamDayann.npy')
DamDayann_slope = np.load(work_dir + 'var/Cherry_DamDayann_slope.npy')
var_mean = np.load(work_dir + 'var/var_yearly_Cherry.npy')
var_std = np.load(work_dir + 'var/var_std_Cherry.npy')
var_slope = np.load(work_dir + 'var/var_yearly_slope_Cherry.npy')

data = []
data.append(var_mean[3, :, :])
data.append(np.nanmean(DamDayann, axis=0))
data.append(var_std[3, :, :])
data.append(np.nanstd(DamDayann, axis=0))
data.append(var_slope[3, :, :])
data.append(DamDayann_slope)

extent = [-105, -75, 34, 49]
fig, axs = plt.subplots(3, 2, figsize=(10, 10))
ll = [0, 0, 0, 0, -.03, -.2]
lr = [1, 4, .5, 4, .03, .2]
step = [.2, 1, .1, 1, .01, .1]
title = ['(a) buds remaining fraction mean', '(b) damage days mean', '(c) buds remaining fraction std',
         '(d) damage days std',
         '(e) buds remaining fraction trend', '(f) damage days trend']
pc = []
for i in range(6):
    ax = plt.subplot(3, 2, i + 1, projection=ccrs.AlbersEqualArea(np.mean(extent[:2]), np.mean(extent[2:])))
    ax.set_extent(extent)
    ax.add_feature(cartopy.feature.BORDERS, lw=.1, linestyle=':')
    ax.add_feature(cartopy.feature.COASTLINE, lw=.1, linestyle=':')
    ax.add_feature(cartopy.feature.STATES.with_scale('10m'), lw=.5)
    ax.add_feature(cartopy.feature.LAKES, edgecolor='black', facecolor='white', lw=.3)

    levels = MaxNLocator(nbins=100).tick_values(ll[i], lr[i])
    if i < 4:
        cmap = plt.get_cmap('viridis')
    else:
        cmap = plt.get_cmap('bwr')
    norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)

    pc.append(plt.pcolormesh(Lon, Lat, data[i], cmap=cmap, norm=norm, transform=ccrs.PlateCarree()))

    ax.text(.01, 1.03, title[i], fontsize=16, fontweight='bold', horizontalalignment='left', transform=ax.transAxes)

for ax in axs.flat:  # Loop through all axes objects
    ax.set_xticks([])  # Remove x-axis ticks
    ax.set_yticks([])
    # Hide the right and top spines
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(True)  # Ensure only the bottom spine is visible

plt.subplots_adjust(bottom=0.02, top=.98, left=0.02, right=.98,
                    wspace=0.006, hspace=0.1)
i = 0
cb_ax = fig.add_axes([.005, 0.665, 0.01, 0.315])
cbar = fig.colorbar(pc[i], cax=cb_ax, ticks=np.arange(ll[i], lr[i] + step[i], step[i]))
cb_ax.yaxis.set_ticks_position('left')
cb_ax.tick_params(labelsize=12)
cb_ax.tick_params(axis='y', which='minor', length=0)  # Remove minor ticks
i = 1
cb_ax = fig.add_axes([0.985, 0.665, 0.01, 0.315])
cbar = fig.colorbar(pc[i], cax=cb_ax, ticks=np.arange(ll[i], lr[i] + step[i], step[i]), extend='max')
cb_ax.tick_params(labelsize=15)
cb_ax.tick_params(axis='y', which='minor', length=0)  # Remove minor ticks
i = 2
cb_ax = fig.add_axes([0.005, .345, 0.01, 0.315])
cbar = fig.colorbar(pc[i], cax=cb_ax, ticks=np.arange(ll[i], lr[i] + step[i], step[i]), extend='max')
cb_ax.yaxis.set_ticks_position('left')
cb_ax.tick_params(labelsize=15)
cb_ax.tick_params(axis='y', which='minor', length=0)  # Remove minor ticks
i = 3
cb_ax = fig.add_axes([0.985, .345, 0.01, 0.315])
cbar = fig.colorbar(pc[i], cax=cb_ax, ticks=np.arange(ll[i], lr[i] + step[i], step[i]), extend='max')
cb_ax.tick_params(labelsize=15)
cb_ax.tick_params(axis='y', which='minor', length=0)  # Remove minor ticks
i = 4
cb_ax = fig.add_axes([0.005, .02, 0.01, 0.315])
cbar = fig.colorbar(pc[i], cax=cb_ax, ticks=np.arange(ll[i], lr[i] + step[i], step[i]), extend='max')
cb_ax.yaxis.set_ticks_position('left')
cb_ax.tick_params(labelsize=15)
cb_ax.tick_params(axis='y', which='minor', length=0)  # Remove minor ticks
i = 5
cb_ax = fig.add_axes([0.985, .02, 0.01, 0.315])
cbar = fig.colorbar(pc[i], cax=cb_ax, ticks=np.arange(ll[i], lr[i] + step[i], step[i]), extend='max')
cb_ax.tick_params(labelsize=12)
cb_ax.tick_params(axis='y', which='minor', length=0)  # Remove minor ticks

plt.savefig(work_dir + 'plot/3TotDamDays.png', bbox_inches='tight')
plt.close()