import numpy as np
import pandas as pd
import rasterio
import geopandas as gpd
from shapely.geometry import Point, Polygon
import pandas as pd

lat = np.array([49.9166666666664 - i * 0.0416666666667 for i in range(357)])
lon = np.array([-105.0416666666507 + i * 0.0416666666667 for i in range(722)])
Lon, Lat = np.meshgrid(lon, lat)

work_dir = '/home/mmfire/Diane/Ag_paper/'

tmin81 = np.load(work_dir + f'prism/mw_tmin/1981_tmin.npz')['tmin']
t, y, x = tmin81.shape

am = rasterio.open(work_dir + 'prism/data/tmin/1981/PRISM_tmin_stable_4kmD2_19810101_bil/PRISM_tmin_stable_4kmD2_19810101_bil.bil')
a = am.read()[0, :357, 479:1201]
mask = np.where(a>-1000, 1, 0)

usa = gpd.read_file(work_dir + 'states_21basic/states.shp')
co_poly = usa[usa.STATE_ABBR == 'CO'].geometry
nm_poly = usa[usa.STATE_ABBR == 'NM'].geometry
tx_poly = usa[usa.STATE_ABBR == 'TX'].geometry
wy_poly = usa[usa.STATE_ABBR == 'WY'].geometry
mt_poly = usa[usa.STATE_ABBR == 'MT'].geometry
de_poly = usa[usa.STATE_ABBR == 'DE'].geometry
nj_poly = usa[usa.STATE_ABBR == 'NJ'].geometry

poly = [co_poly, nm_poly, tx_poly, wy_poly, mt_poly, de_poly, nj_poly]
mdmask = [np.zeros((y, x)) for k in range(len(poly))]
for i in range(y):
    for j in range(x):
        if mask[i, j]:
            p = Point(Lon[i, j], Lat[i, j])
            for k in range(len(poly)):
                mdmask[k][i, j] = np.array(poly[k].contains(p))
states = ['CO', 'NM', 'TX', 'WY', 'MT', 'DE', 'NJ']
[np.save(work_dir + f'var_GDD20/{states[ii]}_mask', mdmask[ii]) for ii in range(len(poly))]