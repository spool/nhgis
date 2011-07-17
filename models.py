from django.contrib.gis.db import models
from fips.fields import USStateFipsField, USStateFipsCode
from ipums.models import PUMA
from fips import CONTINENTAL_CHARS
from area_codes.models import Exchange
from nodes.models import NodeTimePoint, TIME_SERIES_START_DATE, TIME_SERIES_END_DATE
from stats_dataset import StataDataset

dataset = StataDataset('exchange_data.dta', path='nhgis/data')

class ContinentalUSTractManager(models.GeoManager):

    def get_query_set(self):
        continental_fips = [USStateFipsCode(x) for x in CONTINENTAL_CHARS] # Find a way around this...
        return super(ContinentalUSTractManager, self).get_query_set().filter(state__in=continental_fips)

class Tract(models.Model):

    nhgisst = models.CharField(max_length=3)
    state = USStateFipsField(blank=True, null=True)
    nhgiscty = models.CharField(max_length=4)
    gisjoin = models.CharField(max_length=16)
    gisjoin2 = models.CharField(max_length=15)
    shape_area = models.FloatField()
    shape_len = models.FloatField()
    geom = models.MultiPolygonField(srid=4326)
    blockgr = models.CharField(max_length=13, null=True)
    fixed_exchange = models.BooleanField(default=False)
    puma = models.ForeignKey('ipums.PUMA', null=True)
    fixed_puma = models.BooleanField(default=False)
    cont_us = ContinentalUSTractManager()
    objects = models.GeoManager()

    @property
    def data(self):
        return dataset[self.gisjoin]

    def state_adoption_dates(self):
        return NodeTimePoint.objects.filter(phone_numbers__area_code__exchange__state_tracts=self).order_by('date').values_list('date', flat=True).distinct()

    def state_ever_adopts(self):
        if self.state_adoption_dates(): return 1
        else: return 0

    def state_adoption_weeks(self):
        start = TIME_SERIES_START_DATE
        if self.state_ever_adopts(): l = self.state_adoption_dates()
        else: l = [TIME_SERIES_END_DATE]
        return [(date - start).days / 7 for date in l]

    def adoption_dates(self):
        return NodeTimePoint.objects.filter(phone_numbers__area_code__exchange__tracts=self).order_by('date').values_list('date', flat=True).distinct()

    def ever_adopts(self):
        if self.adoption_dates(): return 1
        else: return 0

    def adoption_weeks(self):
        start = NodeTimePoint.objects.order_by('date').values_list('date', flat=True)[0]
        if self.ever_adopts(): return [(start - date).days / 7 for date in self.adoption_dates()]
        else: return NodeTimePoint.objects.order_by('-date').values_list('date', flat=True)[:1]

    # TODO: Make set_block a pre_save signal
    # TODO: Fix last 2 digit formatting
    def set_blockgr(self):
        s = self.gisjoin
        if len(s) < 14:
            self.blockgr = s[1:3] + s[5:7] + s[8:12] + '.' + '00:'
            self.save()
        else:
            self.blockgr = s[1:3] + s[5:7] + s[8:12] + '.' + '%02d' % int(s[12:13]) + ':'
            self.save()

    def set_state(self):
        self.state = USStateFipsCode(self.nhgisst[:2])
        self.save()

    def set_puma(self):
        try:
            self.puma = PUMA.objects.get(geom__contains=self.geom)
        except PUMA.DoesNotExist:
            try:
                self.puma = PUMA.objects.get(geom__contains=self.geom.centroid)
                self.fixed_puma = True
            except:
                try:
                    pumas = PUMA.objects.filter(geom__overlaps=self.geom).distance(self.geom.centroid)
                    self.puma = pumas.order_by('distance')[0]
                    self.fixed_puma = True
                except:
                    print "Error with %s" % self
                    return (self, pumas)
        self.save()

    def set_state_exchanges(self):
        print self
        self.state_exchanges.clear()
        if Exchange.cont_us.filter(coordinates__within=self.geom):
            self.state_exchanges = Exchange.us.filter(coordinates__within=self.geom)
            self.save()
        elif Exchange.cont_us.filter(area_codes__state=self.state.code):
            print "Using state filter: %s" % self.state
            self.fixed_exchange = True
            self.state_exchanges.add(Exchange.cont_us.filter(area_codes__state=self.state.code).distance(self.geom.centroid).order_by('distance')[0])
            self.save()
        else:
            raise ExchangeNotFound(self)

    def set_exchanges(self):
        print self
        self.exchanges.clear()
        if Exchange.cont_us.filter(coordinates__within=self.geom):
            self.exchanges = Exchange.us.filter(coordinates__within=self.geom)
            self.save()
        elif Exchange.cont_us.filter(puma=self.puma):
            print "Using puma filter: %s" % self.puma
            self.fixed_exchange = True
            self.exchanges.add(Exchange.cont_us.filter(puma=self.puma).distance(self.geom.centroid).order_by('distance')[0])
            self.save()
        elif Exchange.cont_us.filter(area_codes__state=self.state.code):
            print "Using state filter: %s" % self.state
            self.fixed_exchange = True
            self.exchanges.add(Exchange.cont_us.filter(area_codes__state=self.state.code).distance(self.geom.centroid).order_by('distance')[0])
            self.save()
        else:
            raise ExchangeNotFound(self)

    def __unicode__(self):
        return 'Tract %s in %s centroid: %f %f' % (self.blockgr, self.state,
                self.geom.centroid.coords[1], self.geom.centroid.coords[0])

class ExchangeNotFound(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return 'Could not find an Exchange for %s' % repr(self.value)


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


