#!/usr/bin/env python

from canari.maltego.message import Entity, EntityField, EntityFieldType, MatchingRule
from sploitego.resource import (unavailableport, closedport, timedoutport, openport, high, medium, low, info, critical,
                                systems)


__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Sploitego Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'

__all__ = [
    'SploitegoEntity',
    'PortStatus',
    'Port',
    'NmapReport',
    'Service',
    'OS',
    'SiteCategory'
]


class SploitegoEntity(Entity):

    namespace = 'sploitego'


class PortStatus(object):
    Open = 'Open'
    Closed = 'Closed'
    Unavailable = 'Service Unavailable'
    TimedOut = 'TimedOut'
    Filtered = 'Filtered'

    @staticmethod
    def icon(obj, val):
        values = val.split('|')
        if PortStatus.Open in values:
            obj.iconurl = openport
        elif PortStatus.Closed in values:
            obj.iconurl = closedport
        elif PortStatus.Unavailable in values:
            obj.iconurl = unavailableport
        elif PortStatus.TimedOut in values or PortStatus.Filtered in values:
            obj.iconurl = timedoutport


class VulnerabilitySeverity(object):
    Critical = 4
    High = 3
    Medium = 2
    Low = 1
    Info = 0

    @staticmethod
    def icon(obj, val):
        val = int(val)
        if val == VulnerabilitySeverity.Critical:
            obj.iconurl = critical
        elif val == VulnerabilitySeverity.High:
            obj.iconurl = high
        elif val == VulnerabilitySeverity.Medium:
            obj.iconurl = medium
        elif val == VulnerabilitySeverity.Low:
            obj.iconurl = low
        else:
            obj.iconurl = info


class OsName(object):

    @staticmethod
    def icon(obj, val):
        for s in systems:
            if s in val.lower():
                obj.iconurl = systems[s]
                return


@EntityField(name='ip.source', propname='source', displayname='Source IP')
@EntityField(name='ip.destination', propname='destination', displayname='Destination IP')
@EntityField(name='protocol')
@EntityField(name='port.response', propname='response', displayname='Port Response')
@EntityField(name='port.status', propname='status', displayname='Port Status', decorator=PortStatus.icon)
class Port(SploitegoEntity):
    pass


@EntityField(name='report.file', propname='file', displayname='Report File')
@EntityField(name='scan.command', propname='command', displayname='Command')
class NmapReport(SploitegoEntity):
    pass


@EntityField(name='ip.destination', propname='destination', displayname='Destination IP')
@EntityField(name='protocol')
@EntityField(name='port', matchingrule=MatchingRule.Loose)
class Service(SploitegoEntity):
    pass


@EntityField(name='os.name', propname='name', displayname='Operating System', decorator=OsName.icon)
class OS(SploitegoEntity):
    pass


class SiteCategory(SploitegoEntity):
    pass


@EntityField(name='snmp.community', propname='community', displayname='SNMP Community')
@EntityField(name='snmp.version', propname='version', displayname='SNMP Version',
    type=EntityFieldType.Enum, choices=['1', '2c', '2', '3', 'v1', 'v2c', 'v3'])
@EntityField(name='snmp.agent', propname='agent', displayname='SNMP Agent')
@EntityField(name='ip.port', propname='port', displayname='Port', type=EntityFieldType.Integer)
@EntityField(name='protocol')
class SNMPCommunity(SploitegoEntity):
    pass


@EntityField(name='nessusreport.uuid', propname='uuid', displayname='Report UUID')
#@EntityField(name='nessusreport.errors', propname='errors', displayname='Errors')
class NessusReport(SploitegoEntity):
    pass


@EntityField(name='nessusplugin.id', propname='pluginid', displayname='Plugin ID')
@EntityField(name='nessusplugin.family', propname='family', displayname='Plugin Family')
@EntityField(name='nessusplugin.severity', propname='severity',
    displayname='Severity', decorator=VulnerabilitySeverity.icon)
@EntityField(name='nessusplugin.count', propname='count', displayname='Count')
@EntityField(name='nessusreport.uuid', propname='uuid', displayname='Report UUID')
class NessusVulnerability(SploitegoEntity):
    pass