from django.contrib.gis.utils import LayerMapping
from models import Tract, tract_mapping
import os

us_tract_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/US_tract_1990.shp'))
ak_tract_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/AK_tract_1990.shp'))
hi_tract_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/HI_tract_1990.shp'))

def run_us(verbose=True):
    lm = LayerMapping(Tract, us_tract_shp, tract_mapping, transform=True, encoding='iso-8859-1')
    lm.save(strict=True, verbose=verbose)

def run_ak(verbose=True):
    lm = LayerMapping(Tract, ak_tract_shp, tract_mapping, transform=True, encoding='iso-8859-1')
    lm.save(strict=True, verbose=verbose)

def run_hi(verbose=True):
    lm = LayerMapping(Tract, hi_tract_shp, tract_mapping, transform=True, encoding='iso-8859-1')
    lm.save(strict=True, verbose=verbose)
