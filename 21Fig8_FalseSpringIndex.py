import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs
import cartopy
from matplotlib.ticker import MaxNLocator
from matplotlib.colors import BoundaryNorm
import matplotlib as mpl
mpl.rc("savefig", dpi=300)
import rasterio
from scipy.stats import skew

lat = np.array([49.9166666666664 - i * 0.0416666666667 for i in range(357)])
lon = np.array([-105.0416666666507 + i * 0.0416666666667 for i in range(722)])
Lon, Lat = np.meshgrid(lon, lat)

work_dir = '/home/mmfire/Diane/Ag_paper/'

# Set the path to the directory containing the downloaded shapefiles
cartopy.config['data_dir'] = '/home/mmfire/Diane/Ag_paper/shapefiles'  # Change to your directory

tmin81 = np.load(work_dir + f'prism/mw_tmin/1981_tmin.npz')['tmin']
t, y, x = tmin81.shape

am = rasterio.open(work_dir + 'prism/data/tmin/1981/PRISM_tmin_stable_4kmD2_19810101_bil/PRISM_tmin_stable_4kmD2_19810101_bil.bil')
a = am.read()[0, :357, 479:1201]
mask = np.where(a>-1000, 1, 0)

len_year = 43
fdd1 = np.load(work_dir + 'var/Cherry_FirstDamDate1day.npy')
sdd = np.load(work_dir + 'var/Cherry_sidegreen.npy')
sddn = np.load(work_dir + 'var/Cherry_sidegreen_norm.npy')
fsi = np.zeros((len_year, y, x))

ni = 1./3.
fsi = np.where(np.logical_and(sddn<ni, sdd<fdd1), 1, 0)
fsi1 = np.where(mask, fsi, np.nan)

fdd3 = np.load(work_dir + 'var/Cherry_FirstDamDate3days.npy')
fsi = np.where(np.logical_and(sddn<ni, sdd<fdd3), 1, 0)
fsi3 = np.where(mask, fsi, np.nan)

skewness = skew(sdd, axis=0)

extent = [-105, -75, 34, 49]
fsidata = [fsi1, fsi3]
title = ['(a) 1 damage days after side green date', '(b) 3 damage days after side green date', '(c) Skewness of Side Green Day']
yr = 16
fig, axes = plt.subplots(3, 1, figsize=(5, 10))
pc = []
for i in range(3):
    ax = plt.subplot(3, 1, i+1, projection=ccrs.AlbersEqualArea(np.mean(extent[:2]), np.mean(extent[2:])))
    ax.set_extent(extent)
    ax.add_feature(cartopy.feature.BORDERS, lw=.1, linestyle=':')
    ax.add_feature(cartopy.feature.COASTLINE, lw=.1, linestyle=':')
    ax.add_feature(cartopy.feature.STATES.with_scale('10m'), lw=.5)
    ax.add_feature(cartopy.feature.LAKES, edgecolor='black', facecolor='white', lw=.3)
    ax.gridlines(color="black", linestyle="dotted", lw=.1)

    if i < 2:
        levels = MaxNLocator(nbins=yr+1).tick_values(0, yr)
        cmap = plt.get_cmap('viridis')
        norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)
        pc.append(plt.pcolormesh(Lon, Lat, fsidata[i].sum(axis=0), cmap=cmap, norm=norm, transform=ccrs.PlateCarree()))
    else:
        levels = MaxNLocator(nbins=100).tick_values(-1, 1)
        cmap = plt.get_cmap('bwr')
        norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)
        pc.append(plt.pcolormesh(Lon, Lat, skewness, cmap=cmap, norm=norm, transform=ccrs.PlateCarree()))

    plt.title(f'{title[i]}', fontsize=16, fontweight='bold')

for ax in axes.flat:  # Loop through all axes objects
    ax.set_xticks([])  # Remove x-axis ticks
    ax.set_yticks([])
    # Hide the right and top spines
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(True)  # Ensure only the bottom spine is visible

plt.subplots_adjust(bottom=0.02, top=.98, left=0.02, right=.98, wspace=0.005, hspace=0.1)
i = 0
cb_ax = fig.add_axes([0.985, 0.345, 0.02, 0.64])
cbar = fig.colorbar(pc[i], cax=cb_ax, ticks=np.arange(0, yr+1, 2), extend='max')
cb_ax.tick_params(labelsize=15)
cb_ax.tick_params(axis='y', which='minor', length=0)  # Remove minor ticks
i = 2
cb_ax = fig.add_axes([0.985, .02, 0.02, 0.31])
cbar = fig.colorbar(pc[i], cax=cb_ax, ticks=np.arange(-1, 1.1, .2), extend='both')
cb_ax.tick_params(labelsize=15)
cb_ax.tick_params(axis='y', which='minor', length=0)  # Remove minor ticks

plt.savefig(work_dir + 'plot/8FalseSpringIndex.png', bbox_inches='tight')
plt.close()

