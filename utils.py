from models import Tract
import os

DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data'))
AREA_FILENAME = 'tract_areas.dat'

def write_area(tracts=Tract.objects.all(), path=DATA_PATH, filename=AREA_FILENAME):
    with open(os.path.join(path, filename), 'w') as f:
        f.write('GISJOIN AREA\n')
        for tract in tracts:
            f.write('%s %s\n' % (tract.gisjoin, tract.shape_area))

