import numpy as np
from zipfile import ZipFile
import os
import rasterio
from os.path import isfile, join


work_dir = '/home/mmfire/Diane/Ag_paper'

for yl in range(43):
    DIR = work_dir + f'prism/data/tmax/{1981+yl}/'
    fna = [name for name in os.listdir(DIR) if isfile(join(DIR, name)) and '.zip' in name]
    fna.sort()
    fno = len(fna)
    for i in range(fno):
        z = ZipFile(DIR+fna[i])
        z.extractall(DIR+fna[i][:-4])
    print(f'{1981 + yl} tmax finished')

for yl in range(43):
    tmax = []
    folder = work_dir + f'prism/data/tmax/{1981+yl}/'
    subfolders = [ f.path for f in os.scandir(folder) if f.is_dir() ]
    subfolders.sort()
    for i in range(len(subfolders)):
        with rasterio.open(subfolders[i]+'/'+subfolders[i][-36:]+'.bil') as bil:
            a = bil.read()[0, :357, 479:1201]
            tmax.append(a)
    tmax = np.array(tmax)
    np.savez_compressed(work_dir + f'prism/mw_tmax/{1981+yl}_tmax', tmax=tmax)



for yl in range(43):
    DIR = work_dir + f'prism/data/tmin/{1981+yl}/'
    fna = [name for name in os.listdir(DIR) if isfile(join(DIR, name)) and '.zip' in name]
    fna.sort()
    fno = len(fna)
    for i in range(fno):
        z = ZipFile(DIR+fna[i])
        z.extractall(DIR+fna[i][:-4])  # unzip zipped files
    print(f'{1981+yl} tmin finished')

for yl in range(43):
    tmin = []
    folder = work_dir + f'prism/data/tmin/{1981+yl}/'
    subfolders = [ f.path for f in os.scandir(folder) if f.is_dir() ]
    subfolders.sort()
    for i in range(len(subfolders)):
        with rasterio.open(subfolders[i]+'/'+subfolders[i][-36:]+'.bil') as bil:
            a = bil.read()[0, :357, 479:1201]
            tmin.append(a)
    tmin = np.array(tmin)
    np.savez_compressed(work_dir + f'prism/mw_tmin/{1981+yl}_tmin', tmin=tmin)

for yl in range(43):
    DIR = work_dir + f'prism/data/prec/{1981+yl}/'
    fna = [name for name in os.listdir(DIR) if isfile(join(DIR, name)) and '.zip' in name]
    fna.sort()
    fno = len(fna)
    for i in range(fno):
        z = ZipFile(DIR+fna[i])
        z.extractall(DIR+fna[i][:-4])  # unzip zipped files
    print(f'{1981+yl} ppt finished')

for yl in range(43):
    prec = []
    folder = work_dir + f'prism/data/prec/{1981+yl}/'
    subfolders = [ f.path for f in os.scandir(folder) if f.is_dir() ]
    subfolders.sort()
    for i in range(len(subfolders)):
        with rasterio.open(subfolders[i]+'/'+subfolders[i][-36:]+'.bil') as bil:
            a = bil.read()[0, :357, 479:1201]
            prec.append(a)
    prec = np.array(prec)
    np.savez_compressed(work_dir + f'prism/mw_prec/{1981+yl}_prec', prec=prec)