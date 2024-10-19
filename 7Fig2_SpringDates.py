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

var_mean = np.load(work_dir + 'var/var_yearly_Cherry.npy')
var_std = np.load(work_dir + 'var/var_std_Cherry.npy')
var_slope = np.load(work_dir + 'var/var_yearly_slope_Cherry.npy')
var_pvalue = np.load(work_dir + 'var/var_yearly_pvalue_Cherry.npy')

data = []
pvalue = []
data.append(var_mean[0, :, :])
data.append(var_std[0, :, :])
data.append(var_slope[0, :, :])
pvalue.append(var_pvalue[0, :, :])
data.append(var_mean[1, :, :])
data.append(var_std[1, :, :])
data.append(var_slope[1, :, :])
pvalue.append(var_pvalue[1, :, :])
data.append(var_mean[4, :, :])
data.append(var_std[4, :, :])
data.append(var_slope[4, :, :])
pvalue.append(var_pvalue[4, :, :])

extent = [-105, -75, 34, 49]
fig, axs = plt.subplots(3, 3, figsize=(15, 10))
ll = [60, 0, -.6, 0, 0, -.6, 0, 0, -.6]
lr = [160, 12, .6, 160, 12, .6, 30, 12, .6]
step = [20, 2, .2, 40, 2, .2, 6, 2, .2]
title = ['(a) side green mean', '(b) side green std', '(c) side green trend', '(d) full bloom mean',
         '(e) full bloom std', '(f) full bloom trend', '(g) spring duration mean', '(h) spring duration std',
         '(i) spring duration trend']
pc = []
for i in range(9):
    ax = plt.subplot(3, 3, i + 1, projection=ccrs.AlbersEqualArea(np.mean(extent[:2]), np.mean(extent[2:])))
    ax.set_extent(extent)
    ax.add_feature(cartopy.feature.BORDERS, lw=.1, linestyle=':')
    ax.add_feature(cartopy.feature.COASTLINE, lw=.1, linestyle=':')
    ax.add_feature(cartopy.feature.STATES.with_scale('10m'), lw=.5)
    ax.add_feature(cartopy.feature.LAKES, edgecolor='black', facecolor='white', lw=.3)

    levels = MaxNLocator(nbins=100).tick_values(ll[i], lr[i])
    if i % 3 - 2:
        cmap = plt.get_cmap('viridis')
    else:
        cmap = plt.get_cmap('bwr')
    norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)

    pc.append(plt.pcolormesh(Lon, Lat, data[i], cmap=cmap, norm=norm, transform=ccrs.PlateCarree()))
    if i % 3 == 2:
        plt.scatter(Lon, Lat, np.where(pvalue[int((i - 2) / 3)] < 0.05, 1, np.nan), 'grey', alpha=.1,
                    transform=ccrs.PlateCarree())
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
                    wspace=0.005, hspace=0.1)
i = 0
cb_ax = fig.add_axes([.005, 0.345, 0.01, 0.64])
cbar = fig.colorbar(pc[i], cax=cb_ax, ticks=np.arange(ll[i], lr[i] + step[i], step[i]), extend='max')
cb_ax.yaxis.set_ticks_position('left')
cb_ax.tick_params(labelsize=15)
cb_ax.tick_params(axis='y', which='minor', length=0)  # Remove minor ticks
i = 2
cb_ax = fig.add_axes([0.985, .02, 0.01, 0.96])
cbar = fig.colorbar(pc[i], cax=cb_ax, ticks=np.arange(ll[i], lr[i] + step[i], step[i]), extend='both')
cb_ax.tick_params(labelsize=15)
cb_ax.tick_params(axis='y', which='minor', length=0)  # Remove minor ticks
i = 6
cb_ax = fig.add_axes([0.005, .02, 0.01, 0.32])
cbar = fig.colorbar(pc[i], cax=cb_ax, ticks=np.arange(ll[i], lr[i] + step[i], step[i]), extend='max')
cb_ax.yaxis.set_ticks_position('left')
cb_ax.tick_params(labelsize=15)
cb_ax.tick_params(axis='y', which='minor', length=0)  # Remove minor ticks
i = 7
cb_ax = fig.add_axes([0.34, .005, 0.32, 0.01])
cbar = fig.colorbar(pc[i], cax=cb_ax, ticks=np.arange(ll[i], lr[i] + step[i], step[i]), extend='max',
                    orientation="horizontal")
cb_ax.tick_params(labelsize=15)
cb_ax.tick_params(axis='x', which='minor', length=0)  # Remove minor ticks

plt.savefig(work_dir + 'plot/2SpringDates.png', bbox_inches='tight')
plt.close()