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

# Set the path to the directory containing the downloaded shapefiles
cartopy.config['data_dir'] = '/home/mmfire/Diane/Ag_paper/shapefiles'  # Change to your directory

tmin81 = np.load(work_dir + f'prism/mw_tmin/1981_tmin.npz')['tmin']
t, y, x = tmin81.shape

am = rasterio.open(work_dir + 'prism/data/tmin/1981/PRISM_tmin_stable_4kmD2_19810101_bil/PRISM_tmin_stable_4kmD2_19810101_bil.bil')
a = am.read()[0, :357, 479:1201]
mask = np.where(a>-1000, 1, 0)

len_year = 43
fdd = np.load(work_dir + 'var/Cherry_FirstDamDate1day.npy')
sdd = np.load(work_dir + 'var/Cherry_sidegreen.npy')
sddn = np.load(work_dir + 'var/Cherry_sidegreen_norm.npy')
fsi = np.zeros((len_year, y, x))

ni = 1./3.
fsi = np.where(np.logical_and(sddn<ni, sdd<fdd), 1, 0)
fsi1 = np.where(mask, fsi, np.nan)
# fsi = np.where(sddn<ni, 1, 0)
# fsi = np.where(fdd>sdd, 1, 0)

fdd = np.load('./var/Cherry_FirstDamDate3days.npy')
fsi = np.where(np.logical_and(sddn<ni, sdd<fdd), 1, 0)
fsi3 = np.where(mask, fsi, np.nan)