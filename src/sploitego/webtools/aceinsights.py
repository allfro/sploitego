#!/usr/bin/env python

from json import JSONDecoder, JSONEncoder
from httplib import HTTPConnection
from time import sleep


__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Sploitego Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'

__all__ = [
    'MinerError',
    'Miner',
    'AceInsightMiner'
]


class MinerError(Exception):
    pass


class Miner(object):
    GeoLocation = 1
    GlobalRanking = 2
    AlexaMetrics = 3
    TwitterTrend = 4
    Unknown = 5
    WebsenseCategory = 6
    SecurityCategory = 7
    CurrentThreatLevel = 8


class AceInsightMiner(object):

    _headers = {'Content-Type' : 'application/json; charset=utf-8'}

    def __init__(self, url):
        self.conn = HTTPConnection('aceinsight.websense.com')
        self._jd = JSONDecoder()
        self._je = JSONEncoder()
        self._lid = self._guid(url)

    def _status(self, miner, attempt):
        self.conn.request(
            'POST',
            '/AceDataService.svc/GetMinerStatus',
            headers=self._headers,
            body=self._je.encode({
                'lookupId' : self._lid,
                'minerId' : miner,
                'attempts' : attempt
            })
        )
        r = self.conn.getresponse()
        return r.status == 200 and r.read() == '{"d":"Complete"}'

    def _guid(self, url):
        self.conn.request(
            'POST',
            '/AceDataService.svc/GetGuid',
            headers=self._headers,
            body=self._je.encode({
                'currentUrl' : url,
                'userIp' : '',
                'userName' : 'guest'
            })
        )
        r = self.conn.getresponse()
        if r.status == 200:
            data = self._jd.decode(r.read())
            if isinstance(data['d'], dict) and 'LookupId' in data['d']:
                return data['d']['LookupId']
        return None

    def getdata(self, miner):
        data = {}
        if self._lid is not None:
            for attempt in xrange(0, 10):
                if self._status(miner, attempt):
                    self.conn.request(
                        'POST',
                        '/AceDataService.svc/GetCategoryData',
                        headers=self._headers,
                        body=self._je.encode({
                            'lookupId' : self._lid,
                            'minerId' : miner
                        })
                    )
                    r = self.conn.getresponse()
                    if r.status == 200:
                        data = self._jd.decode(self._jd.decode(r.read())['d'])
                    break
                sleep(0.5)
        return data

