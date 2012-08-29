#!/usr/bin/env python

from json.decoder import JSONDecoder
from httplib import HTTPSConnection
from urllib import urlencode, urlopen
from random import randint
from sys import platform


__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Sploitego Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'

__all__ = [
    'GeoLocateError',
    'geolocate'
]


class GeoLocateError(Exception):
    pass


def _fullmac(mac):
    b = mac.split(':')
    return '-'.join(['%02X' % int(B, 16) for B in b])


def geolocate():
    networks = []
    if platform == 'darwin':
        from Foundation import NSBundle, objc
        b = NSBundle.bundleWithPath_(objc.pathForFramework('/System/Library/Frameworks/CoreWLAN.framework'))
        if b is None:
            raise SystemError('Unable to load wireless bundle. Maybe its not supported?')
        b.load()
        cwi = b.classNamed_('CWInterface')
        if cwi is None:
            raise SystemError('Unable to load CWInterface.')
        iface = cwi.interface()
        if iface is None or not iface:
            raise SystemError('Unable to load wireless interface.')
        networks = map(
            lambda x: {'ssid':x.ssid(),'mac':x.bssid(),'ss':x.rssi()},
            iface.scanForNetworksWithParameters_error_(None, None)
        )
#        iface.release()
#        b.unload()
    else:
        raise NotImplementedError('This module is still under development.')

    return _geolocate(networks)


def geomac(bssid):
    return _geolocate([{'ss': randint(-100, -70), 'mac': bssid, 'ssid': 'test'}])


def _geolocate(networks):
    if networks:
        p = '/maps/api/browserlocation/json?browser=sploitego&sensor=true'
        for n in networks:
            p += '&%s' % urlencode({'wifi':'mac:%s|ssid:%s|ss:%s' % (_fullmac(n['mac']), n['ssid'], n['ss'])})

        print p
        c = HTTPSConnection('maps.googleapis.com')
        c.request('GET', p)
        r = c.getresponse()

        if r.status == 200 and r.getheader('Content-Type').startswith('application/json'):
            j = JSONDecoder()
            d = j.decode(r.read())
            if d['status'] == 'OK':
                l = d['location']
                return {'latitude':l['lat'],'longitude':l['lng'],'accuracy':d['accuracy']}

    raise GeoLocateError('Unable to geolocate.')


def reversegeo(lat, lng):
    r = urlopen('https://maps.googleapis.com/maps/api/geocode/json?latlng=%f,%f&sensor=true' % (lat, lng))
    if r.code == 200 and r.headers['Content-Type'].startswith('application/json'):
        r = JSONDecoder().decode(r.read())
        if r['status'] == 'OK':
            return r['results']
        else:
            raise GeoLocateError('Unable to reverse geo code lat long: %s.' % r['status'])
    raise GeoLocateError('Unable to reverse geo code lat long.')