from models import Tract
import os

DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data'))
AREA_FILENAME = 'tract_areas.dat'
ADOPTION_FILENAME = 'tract_adoption.dat'
STATE_ADOPTION_FILENAME = 'state_tract_adoption.dat'


def write_state_adoptions(tracts=Tract.objects.all(), path=DATA_PATH, filename=STATE_ADOPTION_FILENAME):
    with open(os.path.join(path, filename), 'w') as f:
        f.write('BLOCKGR GISJOIN Adopted Week\n')
        for tract in tracts:
            f.write('%s %s %d %d\n' % (tract.blockgr, tract.gisjoin, tract.state_ever_adopts(), tract.state_adoption_weeks()[0]))

def write_adoptions(tracts=Tract.objects.all(), path=DATA_PATH, filename=ADOPTION_FILENAME):
    with open(os.path.join(path, filename), 'w') as f:
        f.write('BLOCKGR Adopted Week\n')
        for tract in tracts:
            f.write('%s %d %d\n' % (tract.blockgr, tract.ever_adopts(), tract.adoption_weeks()[0]))

def write_area(tracts=Tract.objects.all(), path=DATA_PATH, filename=AREA_FILENAME):
    with open(os.path.join(path, filename), 'w') as f:
        f.write('GISJOIN AREA\n')
        for tract in tracts:
            f.write('%s %s\n' % (tract.gisjoin, tract.shape_area))

def set_pumas(tracts=Tract.cont_us.all()):
    errors = []
    for t in tracts:
        if t.set_puma(): # Will return None if no error
            errors.append(t)
    return errors

def set_exchanges(tracts=Tract.cont_us.all()):
    errors = []
    length = len(tracts)
    for i, t in enumerate(tracts):
        print '%s (%d/%d)' % (t, t+1, length)
        try:
            t.set_exchanges()
        except t.ExchangeNotFound():
            errors.append(t)
    return errors
