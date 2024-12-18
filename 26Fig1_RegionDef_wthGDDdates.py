import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs
from cartopy.feature import NaturalEarthFeature
import cartopy
from matplotlib.cm import get_cmap
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.ticker import MaxNLocator
from matplotlib.colors import BoundaryNorm
import matplotlib as mpl
mpl.rc("savefig", dpi=300)
# plt.rcParams["font.family"] = "Times New Roman"

lat = np.array([49.9166666666664 - i * 0.0416666666667 for i in range(357)])
lon = np.array([-105.0416666666507 + i * 0.0416666666667 for i in range(722)])
Lon, Lat = np.meshgrid(lon, lat)

work_dir = '/home/mmfire/Diane/Ag_paper/'

# Set the path to the directory containing the downloaded shapefiles
cartopy.config['data_dir'] = '/home/mmfire/Diane/Ag_paper/shapefiles'  # Change to your directory

GDD20flag = np.load(work_dir + 'var/GDD_StartDates.npy')
GDD20ann = np.nanmean(GDD20flag, axis=0)
GDD20ann = np.nan_to_num(GDD20ann, nan=np.nanmean(GDD20ann))  # Replace NaNs with mean (or other approach)

states = ['MI', 'ND', 'SD', 'NE', 'KS', 'OK', 'MN', 'IA', 'MO', 'WI', 'IL', 'IN', 'OH', 'KY', 'WV', 'PA', 'AR', 'TN', 'NY', 'MD', 'VA', 'NC', 'CO', 'NM', 'TX', 'WY', 'MT', 'DE', 'NJ']
mdmask = {states[ii]:np.load(work_dir + f'var/{states[ii]}_mask.npy') for ii in range(len(states))}
cherrymask = np.load(work_dir + 'var/Cherry_mask.npy')

NWmask = np.where(np.logical_or.reduce((mdmask['ND'], mdmask['SD'], mdmask['NE'], mdmask['WY'], mdmask['MT'])), 1, 0)
SWmask = np.where(np.logical_or.reduce((mdmask['KS'], mdmask['OK'], mdmask['AR'], mdmask['CO'], mdmask['NM'], mdmask['TX'])), 1, 0)
NCmask = np.where(np.logical_or.reduce((mdmask['MN'], mdmask['IA'], mdmask['WI'], mdmask['MI'])), 1, 0)
Cmask = np.where(np.logical_or.reduce((mdmask['MO'], mdmask['IL'], mdmask['IN'], mdmask['OH'], mdmask['KY'], mdmask['TN'], mdmask['WV'])), 1, 0)
NEmask = np.where(np.logical_or.reduce((mdmask['NY'], mdmask['PA'], mdmask['MD'], mdmask['DE'], mdmask['NJ'])), 1, 0)
SEmask = np.where(np.logical_or(mdmask['VA'], mdmask['NC']), 1, 0)

data = [np.where(NWmask, 1, np.nan), np.where(SWmask, 2, np.nan), np.where(NCmask, 3, np.nan), np.where(Cmask, 4, np.nan),
        np.where(NEmask, 5, np.nan), np.where(SEmask, 6, np.nan), np.where(cherrymask, 7, np.nan)]

fig = plt.figure(figsize=(8, 8))
# extent = [-105, -75, 34, 49]
extent = [-120, -70, 23.3, 50.5]
ax = plt.axes(projection=ccrs.AlbersEqualArea(np.mean(extent[:2]), np.mean(extent[2:])))
ax.set_extent(extent)
states = NaturalEarthFeature(category="cultural", scale="10m",
                             facecolor="none",
                             name="admin_1_states_provinces")
ax.add_feature(states, linewidth=.3, edgecolor="black")
ax.add_feature(cartopy.feature.BORDERS, lw=.3, linestyle=':')
ax.add_feature(cartopy.feature.COASTLINE, lw=.3, linestyle=':')
ax.add_feature(cartopy.feature.LAKES, edgecolor='black', facecolor='white', lw=.3)

cmap_name = '6color'
colors= ['darkturquoise','cornflowerblue', 'khaki', 'plum', 'peachpuff', 'lightcoral', 'r']
# colors = ['#edf8e9', '#c7e9c0', '#a1d99b', '#74c476', '#41ab5d', '#238b45', '#005a32']
cmap = LinearSegmentedColormap.from_list(cmap_name, colors, N=7)
levels = MaxNLocator(nbins=7).tick_values(1, 8)
norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)

for di in range(7):
    pc = plt.pcolormesh(Lon, Lat, data[di], cmap=cmap, norm=norm, transform=ccrs.PlateCarree())

CS = plt.contour(Lon, Lat, GDD20ann, levels=np.linspace(10, 90, 9), cmap=plt.get_cmap('cool_r'), transform=ccrs.PlateCarree(), linewidths=.4)
plt.clabel(CS, inline=True, fontsize=6, colors='k')


fig.subplots_adjust(bottom=0, top=0.95, left=0.05, right=0.9)
cb_ax = fig.add_axes([0.905, 0.2, 0.02, 0.55])
cbar = fig.colorbar(pc, cax=cb_ax, ticks=np.arange(1.5, 8))
region = ['Northern Great Plains', 'Southern Great Plains', 'Upper Midwest', 'Ohio Valley', 'NY-PA', 'VA-NC', 'Cherry Yield Counties']
cbar.ax.set_yticklabels(region, fontweight='bold')
plt.savefig(work_dir + 'plot/1Region_Definition.png', bbox_inches='tight')
plt.close()