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

var_mean = np.load(work_dir + 'var/spring_input_mean.npy')
var_std = np.load(work_dir + 'var/spring_input_std.npy')
var_slope = np.load(work_dir + 'var/spring_input_slope.npy')
var_std_slope = np.load(work_dir + 'var/spring_input_Tstd_slope.npy')
var_pvalue = np.load(work_dir + 'var/spring_input_pvalue.npy')
var_std_pvalue = np.load(work_dir + 'var/spring_input_Tstd_pvalue.npy')

data = []
[data.append(var_mean[i, :, :]) for i in range(2)]
[data.append(var_slope[i, :, :]) for i in range(2)]
[data.append(var_std[i, :, :]) for i in range(2)]
[data.append(var_std_slope[i, :, :]) for i in range(2)]
pvalue = []
[pvalue.append(var_pvalue[i, :, :]) for i in range(2)]
[pvalue.append(var_std_pvalue[i, :, :]) for i in range(2)]


extent = [-105, -75, 34, 49]
fig, axs = plt.subplots(4, 2, figsize=(10, 13))
ll = [5, -5, -.06, -.06, 0, 0, -.03, -.03]
lr = [25, 15, .06, .06, 1.4, 1.4, .03, .03]
step = [5, 5, .03, .03, .2, .2, .01, .01]
title = ['(a) Tmax mean', '(b) Tmin mean', '(c) Tmax trend', '(d) Tmin trend',
         '(e) Tmax std', '(f) Tmin std', '(g) Tmax std trend', '(h) Tmin std trend']
pc = []
pi = 0
for i in range(8):
    ax = plt.subplot(4, 2, i + 1, projection=ccrs.AlbersEqualArea(np.mean(extent[:2]), np.mean(extent[2:])))
    ax.set_extent(extent)
    ax.add_feature(cartopy.feature.BORDERS, lw=.1, linestyle=':')
    ax.add_feature(cartopy.feature.COASTLINE, lw=.1, linestyle=':')
    ax.add_feature(cartopy.feature.STATES.with_scale('10m'), lw=.5)
    ax.add_feature(cartopy.feature.LAKES, edgecolor='black', facecolor='white', lw=.3)

    levels = MaxNLocator(nbins=100).tick_values(ll[i], lr[i])
    if i in [0, 1, 4, 5]:
        cmap = plt.get_cmap('nipy_spectral')
    else:
        cmap = plt.get_cmap('bwr')
    norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)

    if i in [2, 3, 6, 7]:
        pc.append(plt.pcolormesh(Lon, Lat, data[i], cmap=cmap, norm=norm, transform=ccrs.PlateCarree()))

        plt.scatter(Lon, Lat, np.where(pvalue[pi] < 0.05, 1, np.nan), 'grey', alpha=.07,
                    transform=ccrs.PlateCarree())
        pi = pi + 1
    else:
        pc.append(plt.pcolormesh(Lon, Lat, data[i], cmap=cmap, norm=norm, transform=ccrs.PlateCarree(), alpha=0.7))

    ax.text(.01, 1.03, title[i], fontsize=16, fontweight='bold', horizontalalignment='left', transform=ax.transAxes)
plt.subplots_adjust(bottom=0.02, top=.98, left=0.02, right=.98,
                    wspace=0.006, hspace=0.1)
for ax in axs.flat:  # Loop through all axes objects
    ax.set_xticks([])  # Remove x-axis ticks
    ax.set_yticks([])
    # Hide the right and top spines
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)  # Ensure only the bottom spine is visible

barheight = 0.23
i = 0
cb_ax = fig.add_axes([.005, 0.755, 0.01, barheight])
cbar = fig.colorbar(pc[i], cax=cb_ax, ticks=np.arange(ll[i], lr[i] + step[i], step[i]), extend='both')
cb_ax.yaxis.set_ticks_position('left')
cb_ax.tick_params(labelsize=15)
cb_ax.tick_params(axis='y', which='minor', length=0)  # Remove minor ticks
i = 1
cb_ax = fig.add_axes([0.985, 0.755, 0.01, barheight])
cbar = fig.colorbar(pc[i], cax=cb_ax, ticks=np.arange(ll[i], lr[i] + step[i], step[i]), extend='both')
cb_ax.tick_params(labelsize=15)
cb_ax.tick_params(axis='y', which='minor', length=0)  # Remove minor ticks
i = 2
cb_ax = fig.add_axes([0.005, .51, 0.01, barheight])
cbar = fig.colorbar(pc[i], cax=cb_ax, ticks=np.arange(ll[i], lr[i] + step[i], step[i]), extend='both')
cb_ax.yaxis.set_ticks_position('left')
cb_ax.tick_params(labelsize=15)
cb_ax.tick_params(axis='y', which='minor', length=0)  # Remove minor ticks
i = 3
cb_ax = fig.add_axes([0.985, .51, 0.01, barheight])
cbar = fig.colorbar(pc[i], cax=cb_ax, ticks=np.arange(ll[i], lr[i] + step[i], step[i]), extend='both')
cb_ax.tick_params(labelsize=15)
cb_ax.tick_params(axis='y', which='minor', length=0)  # Remove minor ticks
i = 4
cb_ax = fig.add_axes([0.005, .265, 0.01, barheight])
cbar = fig.colorbar(pc[i], cax=cb_ax, ticks=np.arange(ll[i], lr[i] + step[i], step[i]), extend='max')
cb_ax.yaxis.set_ticks_position('left')
cb_ax.tick_params(labelsize=15)
cb_ax.tick_params(axis='y', which='minor', length=0)  # Remove minor ticks
i = 5
cb_ax = fig.add_axes([0.985, .265, 0.01, barheight])
cbar = fig.colorbar(pc[i], cax=cb_ax, ticks=np.arange(ll[i], lr[i] + step[i], step[i]), extend='max')
cb_ax.tick_params(labelsize=15)
cb_ax.tick_params(axis='y', which='minor', length=0)  # Remove minor ticks
i = 6
cb_ax = fig.add_axes([0.005, .02, 0.01, barheight])
cbar = fig.colorbar(pc[i], cax=cb_ax, ticks=np.arange(ll[i], lr[i] + step[i], step[i]), extend='both')
cb_ax.yaxis.set_ticks_position('left')
cb_ax.tick_params(labelsize=15)
cb_ax.tick_params(axis='y', which='minor', length=0)  # Remove minor ticks
i = 7
cb_ax = fig.add_axes([0.985, .02, 0.01, barheight])
cbar = fig.colorbar(pc[i], cax=cb_ax, ticks=np.arange(ll[i], lr[i] + step[i], step[i]), extend='both')
cb_ax.tick_params(labelsize=15)
cb_ax.tick_params(axis='y', which='minor', length=0)  # Remove minor ticks

plt.savefig(work_dir + 'plot/7InputTrend_wth_std_trend.png', bbox_inches='tight')
plt.close()