from django.contrib.gis.db import models
from django.contrib.localflavor.us.models import USStateField

class Tract(models.Model):

    nhgisst = models.CharField(max_length=3)
    state = USStateField(blank=True, null=True)
    nhgiscty = models.CharField(max_length=4)
    gisjoin = models.CharField(max_length=16)
    gisjoin2 = models.CharField(max_length=15)
    shape_area = models.FloatField()
    shape_len = models.FloatField()
    geom = models.MultiPolygonField(srid=4326)
    blockgr = models.CharField(max_length=13, null=True)
    fixed_exchange = models.BooleanField(default=False)
    objects = models.GeoManager()

    # TODO: Make set_block a pre_save signal
    def set_blockgr(self):
        s = self.gisjoin
        print s
        if len(s) < 14:
            return s[1:3] + s[5:7] + s[8:12] + '.' + '00'
        else:
            return s[1:3] + s[5:7] + s[8:12] + '.' + s[12:13]

# Auto-generated `LayerMapping` dictionary for Tract model
tract_mapping = {
    'nhgisst' : 'NHGISST',
    'nhgiscty' : 'NHGISCTY',
    'gisjoin' : 'GISJOIN',
    'gisjoin2' : 'GISJOIN2',
    'shape_area' : 'SHAPE_AREA',
    'shape_len' : 'SHAPE_LEN',
    'geom' : 'MULTIPOLYGON',
}


