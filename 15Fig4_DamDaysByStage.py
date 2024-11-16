import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs
import cartopy
from matplotlib.ticker import MaxNLocator
from matplotlib.colors import BoundaryNorm
import matplotlib as mpl
mpl.rc("savefig", dpi=300)
import rasterio

lat = np.array([49.9166666666664 - i * 0.0416666666667 for i in range(357)])
lon = np.array([-105.0416666666507 + i * 0.0416666666667 for i in range(722)])
Lon, Lat = np.meshgrid(lon, lat)

work_dir = '/home/mmfire/Diane/Ag_paper/'

am = rasterio.open(work_dir + 'prism/data/tmin/1981/PRISM_tmin_stable_4kmD2_19810101_bil/PRISM_tmin_stable_4kmD2_19810101_bil.bil')
a = am.read()[0, :357, 479:1201]
mask = np.where(a>-1000, 1, 0)

# Set the path to the directory containing the downloaded shapefiles
cartopy.config['data_dir'] = '/home/mmfire/Diane/Ag_paper/shapefiles'  # Change to your directory

DamDayStage = np.load(work_dir + 'var/Cherry_DamDayStage.npy')
data = np.nansum(DamDayStage, axis=0)
data = np.where(np.isnan(data), 0, data)
data = np.where(mask, data, np.nan)

extent = [-105, -75, 34, 49]
fig, axs = plt.subplots(3, 3, figsize=(15, 10))
ll = 0
lr = 60
step = 5
title = ['(a) stage 0', '(b) stage 2', '(c) stage 3', '(d) stage 4',
         '(e) stage 5', '(f) stage 6', '(g) stage 7', '(h) stage 8',
         '(i) stage 9']
for i in range(9):
    ax = plt.subplot(3, 3, i + 1, projection=ccrs.AlbersEqualArea(np.mean(extent[:2]), np.mean(extent[2:])))
    ax.set_extent(extent)
    ax.add_feature(cartopy.feature.BORDERS, lw=.1, linestyle=':')
    ax.add_feature(cartopy.feature.COASTLINE, lw=.1, linestyle=':')
    ax.add_feature(cartopy.feature.STATES.with_scale('10m'), lw=.5)
    ax.add_feature(cartopy.feature.LAKES, edgecolor='black', facecolor='white', lw=.3)

    levels = MaxNLocator(nbins=100).tick_values(ll, lr)
    cmap = plt.get_cmap('viridis_r')
    norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)

    pc = plt.pcolormesh(Lon, Lat, data[i, :, :], cmap=cmap, norm=norm, transform=ccrs.PlateCarree())
    ax.text(.01, 1.03, title[i], fontsize=16, fontweight='bold', horizontalalignment='left', transform=ax.transAxes)

for ax in axs.flat:  # Loop through all axes objects
    ax.set_xticks([])  # Remove x-axis ticks
    ax.set_yticks([])
    # Hide the right and top spines
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)  # Ensure only the bottom spine is visible

plt.subplots_adjust(bottom=0.02, top=.98, left=0.02, right=.98,
                    wspace=0.005, hspace=0.1)
cb_ax = fig.add_axes([0.985, .02, 0.01, 0.96])
cbar = fig.colorbar(pc, cax=cb_ax, ticks=np.arange(ll, lr + step, step), extend='max')
cb_ax.tick_params(labelsize=15)
cb_ax.tick_params(axis='y', which='minor', length=0)  # Remove minor ticks

plt.savefig(work_dir + 'plot/4DamDaysByStage.png', bbox_inches='tight')
plt.close()