#!/usr/bin/env python

from sploitego.webtools.geolocate import reversegeo
from sploitego.webtools.geolocate import geomac
from canari.maltego.entities import Location

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Sploitego Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'


def getlocbymac(mac):
    ll = geomac(mac)
    gcr = reversegeo(ll['latitude'], ll['longitude'])[0]
    l = Location('-, -')
    l.city = '-'
    l.country = '-'
    for i in gcr['address_components']:
        if 'locality' in i['types']:
            l.city = i['long_name']
        if 'administrative_area_level_1' in i['types']:
            l.area = i['long_name']
        if 'country' in i['types']:
            l.country = i['long_name']
    l.latitude = gcr['geometry']['location']['lat']
    l.longitude = gcr['geometry']['location']['lng']
    l.value = '%s, %s' % (l.city, l.country)
    return l