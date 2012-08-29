#!/usr/bin/env python

from httplib import HTTPSConnection
from urllib import urlencode
from random import randint
from xml.etree.cElementTree import ElementTree

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Sploitego Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'

__all__ = [
    'NessusXmlRpcCmd',
    'NessusException',
    'NessusXmlRpcClient',
    'NessusManager',
    'FamilyManager',
    'PluginManager',
    'UserManager',
    'ServerPreferences',
    'PluginPreference',
    'PluginPreferences',
    'PluginItem',
    'IndividualPluginSelection',
    'FamilyItem',
    'FamilyPreferences',
    'Policy',
    'PolicyManager',
    'Detail',
    'Host',
    'Vulnerability',
    'ReportError',
    'ReportAttribute',
    'Report',
    'Scan',
    'ScanManager',
    'ReportManager'
]


def _empty(val):
    return val if val is not None else ''


def _dictify(e):
    d = {}
    for x in e:
        if x.tag in d:
            if not isinstance(d[x.tag], list):
                t = d[x.tag]
                d[x.tag] = [t]
            d[x.tag].append(x.text)
        else:
            d[x.tag] = x.text
    return d


class NessusXmlRpcCmd:
    Login = '/login'
    Logout = '/logout'

    UsersAdd = '/users/add'
    UsersDelete = '/users/delete'
    UsersEdit = '/users/edit'
    UsersChpasswd = '/users/chpasswd'
    UsersList = '/users/list'

    PluginsList = '/plugins/list'
    PluginsListFamily = '/plugins/list/family'
    PluginsDescription = '/plugins/description'
    PluginsPreferences = '/plugins/preferences'
    PluginsAttributesList = '/plugins/attributes/list'

    PreferencesList = '/preferences/list'
    PolicyList = '/policy/list'
    PolicyDelete = '/policy/delete'
    PolicyCopy = '/policy/copy'
    PolicyEdit = '/policy/edit'
    PolicyAdd = '/policy/add'
    PolicyDownload = '/policy/download/'
    FileUpload = '/file/upload'
    FilePolicyImport = '/file/policy/import'

    Feed = '/feed/'
    Timezones = '/timezones/'

    ScanNew = '/scan/new'
    ScanStop = '/scan/stop'
    ScanPause = '/scan/pause'
    ScanResume = '/scan/resume'
    ScanList = '/scan/list'

    ScanTemplateNew = '/scan/template/new'
    ScanTemplateEdit = '/scan/template/edit'
    ScanTemplateDelete = '/scan/template/delete'
    ScanTemplateLaunch = '/scan/template/launch'

    ReportList = '/report/list'
    ReportDelete = '/report/delete'
    ReportHosts = '/report/hosts'
    ReportPorts = '/report/ports'
    ReportDetails = '/report/details'
    ReportErrors = '/report/errors'
    Report2Vulnerabilities = '/report2/vulnerabilities'
    Report2HostsPlugin = '/report2/hosts/plugin'
    Report2Hosts = '/report2/hosts'
    ReportHasAuditTrail = '/report/hasAuditTrail'
    ReportCanDeleteItems = '/report/canDeleteItems'
    ReportHasKB = '/report/hasKB'
    Report2DetailsPlugin = '/report2/details/plugin'
    Report2DeleteItem = '/report2/deleteItem'
    ReportTags = '/report/tags'
    ReportAttributesList = '/report/attributes/list'
    FileReportDownload = '/file/report/download'
    FileReportImport = '/file/report/import'
    FileXsltList = '/file/xslt/list'
    FileXsltDownload = '/file/xslt/download/'
    ChapterList = '/chapter/list'


    ServerSecureSettingsList = '/server/securesettings/list'
    ServerPreferencesList = '/server/preferences/list'
    ServerPreferences = '/server/preferences'
    ServerSecureSettings = '/server/securesettings'


class NessusException(Exception):
    pass


class NessusSessionException(Exception):
    pass


class NessusXmlRpcClient(object):

    def __init__(self, username='', password='', host='localhost', port=8834, token=None):
        self.h = HTTPSConnection(host, port)
        self.token = token
        if token is None:
            try:
                self.token = 'token=%s' % self.post(
                    NessusXmlRpcCmd.Login, login=username, password=password
                ).find('contents/token').text
            except AttributeError:
                raise NessusSessionException('Failed to login.')
        else:
            self.timezones

    def post(self, cmd, **kwargs):
        kwargs.update({'seq':randint(0,65535)})
        headers={'Content-Type':'application/x-www-form-urlencoded'}
        if self.token is not None:
            headers['Cookie'] = self.token
        self.h.request(
            'POST',
            cmd,
            body=urlencode(kwargs),
            headers=headers
        )
        return self._getresponse()

    def save(self, cmd, f, **kwargs):
        kwargs.update({'seq':randint(0,65535)})
        headers={'Content-Type':'application/x-www-form-urlencoded'}
        if self.token is not None:
            headers['Cookie'] = self.token
        self.h.request(
            'POST',
            cmd,
            body=urlencode(kwargs),
            headers=headers
        )
        r = self.h.getresponse()
        if r.status == 200:
            if isinstance(f, basestring):
                f = file(f, mode='wb')
            f.write(r.read())
            return f.close()
        elif r.status == 403:
            self.token = None
            raise NessusSessionException('Session timed out.')
        raise NessusException(r.read())

    def get(self, cmd, **kwargs):
        kwargs.update({'seq':randint(0,9999)})
        headers = {}
        if self.token is not None:
            headers['Cookie'] = self.token
        self.h.request(
            'GET',
            '%s?%s' % (cmd, urlencode(kwargs)),
            headers=headers
        )
        return self._getresponse()

    def _getresponse(self):
        r = self.h.getresponse()
        if r.status == 200:
            et = ElementTree()
            et.parse(r)
            if et.find('status').text == 'OK':
                return et
            raise NessusException(et.find('contents').text)
        elif r.status == 403:
            self.token = None
            raise NessusSessionException('Session timed out.')
        raise NessusException(r.read())

    def logout(self):
        self.post(NessusXmlRpcCmd.Logout)

    @property
    def users(self):
        return UserManager(self)

    @property
    def policies(self):
        return PolicyManager(self)

    @property
    def plugins(self):
        return FamilyManager(self)

    @property
    def scanner(self):
        return ScanManager(self)

    @property
    def reports(self):
        return ReportManager(self)

    @property
    def feed(self):
        return _dictify(self.post(NessusXmlRpcCmd.Feed).find('contents'))

    @property
    def timezones(self):
        d = {}
        for t in self.post(NessusXmlRpcCmd.Timezones).findall('contents/timezones/timezone'):
            d[t.get('value')] = t.text
        return d


class NessusManager(object):

    def __init__(self, rpc):
        self.rpc = rpc


class FamilyManager(NessusManager):

    @property
    def families(self):
        fs = {}
        for f in self.rpc.post(NessusXmlRpcCmd.PluginsList).findall('contents/pluginFamilyList/family'):
            pm = PluginManager(self.rpc, f)
            fs[pm.family] = pm
        return fs


class PluginManager(object):

    def __init__(self, rpc, e):
        self.rpc = rpc
        self.family = e.find('familyName').text
        self.members = e.find('numFamilyMembers').text

    @property
    def plugins(self):
        return IndividualPluginSelection(
            self.family,
            self.rpc.post(
                NessusXmlRpcCmd.PluginsListFamily,
                family=self.family
            ).find('contents/pluginList')
        )

    def description(self, plugin):
        if plugin.filename:
            e = self.rpc.post(
                NessusXmlRpcCmd.PluginsDescription,
                fname=plugin.filename
            ).find('contents/pluginDescription')
            return {
                'id' : plugin.id,
                'name' : plugin.name,
                'family' : plugin.family,
                'attributes' : _dictify(e.find('pluginAttributes').getchildren())
            }
        return {
            'id' : plugin.id,
            'name' : plugin.name,
            'family' : plugin.family
        }


class UserManager(NessusManager):

    def add(self, username, password, admin=False):
        self.rpc.post(NessusXmlRpcCmd.UsersAdd, login=username, password=password, admin=int(admin))

    def delete(self, username):
        self.rpc.post(NessusXmlRpcCmd.UsersDelete, login=username)

    def edit(self, username, password, admin=False):
        self.rpc.post(NessusXmlRpcCmd.UsersEdit, login=username, password=password, admin=int(admin))

    def chpasswd(self, username, password):
        self.rpc.post(NessusXmlRpcCmd.UsersChpasswd, login=username, password=password)

    @property
    def list(self):
        users = {}
        for u in self.rpc.post(NessusXmlRpcCmd.UsersList).findall('contents/users/user'):
            users[u.find('name').text] = {
                'admin': True if u.find('admin') == 'TRUE' else False,
                'lastlogin' : u.find('lastlogin').text
            }
        return users


class ServerPreferences(dict):

    def __init__(self, e):
        super(ServerPreferences, self).__init__()
        self.update(
            dict(
                map(
                    lambda x: (
                        x.find('name').text,
                        _empty(x.find('value').text)
                        ),
                    e.findall('preference')
                )
            )
        )


class PluginPreference(object):

    def __init__(self, e):
        self.options = _empty(e.find('preferenceValues').text)
        self.options = [] if not self.options else self.options.split(';')
        self.name = e.find('pluginName').text
        self.id = e.find('pluginId').text
        self.param = e.find('fullName').text
        self.type = e.find('preferenceType').text
        sv = e.find('selectedValue')
        self._value = _empty(sv.text if sv is not None else '')

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        if self.options and val not in self.options and self.type != 'entry':
            raise ValueError('%s was not one of %s'% (repr(val), repr(self.options)))
        elif self.type == 'checkbox' and val not in ['yes', 'no']:
            raise ValueError("Value must be either 'yes' or 'no'")
        self._value = val

    def __str__(self):
        return self.value

    def __repr__(self):
        return '< PolicyPreference(%s) object at 0x%x >' % (repr(self.value), id(self))


class PluginPreferences(dict):

    def __init__(self, e):
        super(PluginPreferences, self).__init__()
        for p in e.findall('item'):
            pp = PluginPreference(p)
            self[pp.param] = pp


class PluginItem(object):

    def __init__(self, e):
        self.filename = ''
        if e.tag == 'PluginItem':
            self.name = e.find('PluginName').text
            self.family = e.find('Family').text
            self.status = e.find('Status').text
            self.id = e.find('PluginId').text
        else:
            self.name = e.find('pluginName').text
            self.family = e.find('pluginFamily').text
            self.status = 'enabled'
            self.id = e.find('pluginID').text
            self.filename = e.find('pluginFileName').text

    def __str__(self):
        return self.status

    def __repr__(self):
        return '< PluginItem(%s) object at 0x%x >' % (repr(self.status), id(self))


class IndividualPluginSelection(dict):

    def __init__(self, family, e=None):
        super(IndividualPluginSelection, self).__init__()
        if e is not None:
            remove = []
            if e.tag == 'IndividualPluginSelection':
                for p in e.findall('PluginItem'):
                    if p.find('Family').text == family:
                        pi = PluginItem(p)
                        self['plugin_selection.individual_plugin.%s' % pi.id] = pi
                        remove.append(p)
            else:
                for p in e.findall('plugin'):
                    if p.find('pluginFamily').text == family:
                        pi = PluginItem(p)
                        self['plugin_selection.individual_plugin.%s' % pi.id] = pi
                        remove.append(p)
            for r in remove:
                e.remove(r)


class FamilyItem(object):

    def __init__(self, e, ips):
        self.name = e.find('FamilyName').text
        self._status = e.find('Status').text
        if self._status == 'mixed':
            self._enabled = IndividualPluginSelection(self.name, ips)
        else:
            self._enabled = IndividualPluginSelection(self.name)

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if value in ['disabled', 'enabled']:
            self.plugins.clear()
        elif value != 'mixed':
            raise ValueError('Status must either be "disabled", "enabled", or "mixed".')
        self._status = value

    @property
    def plugins(self):
        return self._enabled

    @plugins.setter
    def plugins(self, value):
        self._enabled = value
        if value:
            self.status = 'mixed'
        else:
            self.status = 'enabled'

    def __str__(self):
        return self.status

    def __repr__(self):
        return '< FamilyItem(%s) object at 0x%x >' % (repr(self.status), id(self))


class FamilyPreferences(dict):

    def __init__(self, e):
        super(FamilyPreferences, self).__init__()
        ips = e.find('IndividualPluginSelection')
        for f in e.findall('FamilySelection/FamilyItem'):
            fi = FamilyItem(f, ips)
            self['plugin_selection.family.%s' % fi.name] = fi


class Policy(object):

    def __init__(self, e):
        self.name = e.find('policyName').text
        self._id = e.find('policyID').text
        self.shared = e.find('visibility').text == 'shared'
        self.comments = _empty(e.find('policyContents/policyComments').text)
        self.owner = e.find('policyOwner').text
        p = e.find('policyContents/Preferences')
        self.serverprefs = ServerPreferences(p.find('ServerPreferences'))
        self.pluginprefs = PluginPreferences(p.find('PluginsPreferences'))
        self.families = FamilyPreferences(e.find('policyContents'))

    @property
    def id(self):
        return self._id

    def todict(self):
        d = {
            'policy_name' : self.name,
            'policy_shared' : int(self.shared),
            'policy_comments' : self.comments,
            #'policy_owner' : self.owner,
        }
        if self.id is not None:
            d['policy_id'] = self.id
        d.update(self.serverprefs)
        d.update(self.pluginprefs)
        d.update(self.families)
        for f in self.families:
            if self.families[f].status == 'mixed':
                d.update(self.families[f].plugins)
        return d

    def __repr__(self):
        return '< Policy(%s) object at 0x%x >' % (repr(self.name), id(self))

    def __str__(self):
        return '%s (ID=%s)' % (self.name, self.id)


class PolicyManager(NessusManager):

    @property
    def list(self):
        return [Policy(p) for p in self.rpc.post(NessusXmlRpcCmd.PolicyList).findall('contents/policies/policy')]

    def update(self, policy):
        if isinstance(policy, Policy):
            self.rpc.post(NessusXmlRpcCmd.PolicyEdit, **policy.todict())
        raise ValueError('Expected Policy object not %s', repr(type(policy)))

    def copy(self, policy):
        if isinstance(policy, Policy):
            return Policy(self.rpc.post(NessusXmlRpcCmd.PolicyCopy, policy_id=policy.id).find('contents/policy'))
        raise ValueError('Expected Policy object not %s', repr(type(policy)))

    def delete(self, policy):
        if not isinstance(policy, Policy):
            raise ValueError('Expected Policy object not %s' % type(policy))
        self.rpc.post(NessusXmlRpcCmd.PolicyDelete, policy_id=policy.id)

    def download(self, policy, file):
        if not isinstance(policy, Policy):
            raise ValueError('Expected Policy object not %s' % type(policy))
        self.rpc.save(NessusXmlRpcCmd.PolicyDownload, file, policy_id=policy.id)

    def add(self, name, comments='', shared=False):
        return Policy(
            self.rpc.post(
                NessusXmlRpcCmd.PolicyAdd,
                policy_name=name,
                policy_comments=comments,
                policy_shared=int(shared)
            ).find('contents/policy')
        )


class Detail(object):

    def __init__(self, e):
        self.id = e.find('item_id').text
        self.port = e.find('port').text
        self.severity = e.find('severity').text
        self.pluginid = e.find('pluginID').text
        self.pluginname = e.find('pluginName').text
        self.output = _dictify(e.find('data'))

    def __repr__(self):
        return '< Detail(%s) at 0x%x >' % (self.id, id(self))


class Host(object):

    def __init__(self, rpc, pluginid, severity, uuid, e):
        self.rpc = rpc
        self.uuid = uuid
        self.name = e.find('hostname').text
        self.port = e.find('port').text
        self.protocol = e.find('protocol').text
        self.pluginid = pluginid
        self.severity = severity

    @property
    def details(self):
        return [
            Detail(d) for d in self.rpc.post(
                NessusXmlRpcCmd.Report2DetailsPlugin,
                severity=self.severity,
                hostname=self.name,
                plugin_id=self.pluginid,
                protocol=self.protocol,
                port=self.port,
                report=self.uuid
            ).findall('contents/portDetails/ReportItem')
        ]

    def __repr__(self):
        return '< Host(%s:%s/%s) at 0x%x >' % (self.name, self.port, self.protocol, id(self))


class Vulnerability(object):

    def __init__(self, rpc, uuid, e):
        self.rpc = rpc
        self.id = e.find('plugin_id').text
        self.name = e.find('plugin_name').text
        self.family = e.find('plugin_family').text
        self.count = int(e.find('count').text)
        self.severity = int(e.find('severity').text)
        self.uuid = uuid

    @property
    def hosts(self):
        return [
            Host(self.rpc, self.id, self.severity, self.uuid, h) for h in self.rpc.post(
                NessusXmlRpcCmd.Report2HostsPlugin, severity=self.severity, plugin_id=self.id, report=self.uuid
            ).findall('contents/hostList/host')
        ]

    def __repr__(self):
        return '< Vulnerability(%s) at 0x%x >' % (repr(self.name), id(self))


class ReportError(object):

    def __init__(self, e):
        self.title = e.find('title').text
        self.message = e.find('message').text
        self.severity = int(e.find('severity').text)


class ReportAttribute(object):

    def __init__(self, e):
        self.name = e.find('name').text
        self.readablename = e.find('readable_name').text
        self.control = _dictify(e.find('control'))
        self.operators = _dictify(e.find('operators'))['operator']

    def __repr__(self):
        return '< ReportAttribute(%s) at 0x%x >' % (self.name, id(self))


class Report(object):

    def __init__(self, rpc, uuid, name):
        self.rpc = rpc
        self.uuid = uuid
        self.name = name

    def _getreport(self):
        for s in self.rpc.post(NessusXmlRpcCmd.ReportList).findall('contents/reports/report'):
            if s.find('name').text == self.uuid:
                return s

    @property
    def vulnerabilities(self):
        d = {}
        for v in self.rpc.post(
            NessusXmlRpcCmd.Report2Vulnerabilities,
            report=self.uuid
        ).findall('contents/vulnList/vulnerability'):
            vuln = Vulnerability(self.rpc, self.uuid, v)
            d[vuln.id] = vuln
        return d

    @property
    def errors(self):
        return [
            ReportError(e)
            for e in self.rpc.post(NessusXmlRpcCmd.ReportErrors, report=self.uuid).findall('contents/errors/error')
        ]

    @property
    def status(self):
        return self._getreport().find('status').text

    @property
    def timestamp(self):
        return self._getreport().find('timestamp').text

    @property
    def isaudited(self):
        return self.rpc.post(
            NessusXmlRpcCmd.ReportHasAuditTrail,
            report=self.uuid
        ).find('contents/hasAuditTrail').text == 'TRUE'

    @property
    def haskb(self):
        return self.rpc.post(
            NessusXmlRpcCmd.ReportHasKB,
            report=self.uuid
        ).find('contents/hasKB').text == 'TRUE'

    @property
    def candelete(self):
        return self.rpc.post(
            NessusXmlRpcCmd.ReportCanDeleteItems, report=self.uuid
        )

    def delete(self):
        self.rpc.post(NessusXmlRpcCmd.ReportDelete, report=self.uuid)

    @property
    def attributes(self):
        return [
            ReportAttribute(r)
            for r in self.rpc.post(
                NessusXmlRpcCmd.ReportAttributesList,
                report=self.uuid
            ).findall('contents/reportAttributes/attribute')
        ]

    def __repr__(self):
        return '< Report(%s) at 0x%x >' % (repr(self.name), id(self))


class Scan(object):

    def __init__(self, rpc, e):
        self.rpc = rpc
        self.name = e.find('scan_name')
        if self.name is None:
            self.name = e.find('readableName').text
        else:
            self.name = self.name.text
        self.uuid = e.find('uuid').text
        self.owner = e.find('owner').text
        self.start = int(e.find('start_time').text)

    def _getscan(self):
        for s in self.rpc.post(NessusXmlRpcCmd.ScanList).findall('contents/scans/scanList/scan'):
            if s.find('readableName').text == self.name:
                return s

    @property
    def completed(self):
        return int(self._getscan().find('completion_current').text)

    @property
    def total(self):
        return int(self._getscan().find('completion_total').text)

    @property
    def status(self):
        s = self._getscan()
        if s is None:
            return self.report.status
        return s.find('status').text

    def pause(self):
        self.rpc.post(NessusXmlRpcCmd.ScanPause, scan_uuid=self.uuid)

    def stop(self):
        self.rpc.post(NessusXmlRpcCmd.ScanStop, scan_uuid=self.uuid)

    def resume(self):
        self.rpc.post(NessusXmlRpcCmd.ScanResume, scan_uuid=self.uuid)

    @property
    def report(self):
        return Report(
            self.rpc,
            self.uuid,
            self.name
        )

    def __repr__(self):
        return '< Scan(%s) at 0x%x >' % (self.uuid, id(self))


class ScanManager(NessusManager):

    def scan(self, name, targets, policy):
        if isinstance(targets, list):
            targets = '\n'.join(targets)
        return Scan(self.rpc, self.rpc.post(
            NessusXmlRpcCmd.ScanNew,
            target=targets,
            policy_id=policy.id,
            scan_name=name
        ).find('contents/scan'))

    @property
    def list(self):
        return [
            Scan(self.rpc, s) for s in self.rpc.post(NessusXmlRpcCmd.ScanList).findall('contents/scans/scanList/scan')
        ]


class ReportManager(NessusManager):

    @property
    def list(self):
        return [
            Report(self.rpc, r.find('name').text, r.find('readableName').text)
            for r in self.rpc.post(NessusXmlRpcCmd.ReportList).findall('contents/reports/report')
        ]