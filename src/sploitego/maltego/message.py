#!/usr/bin/python

from cStringIO import StringIO
from copy import deepcopy
from numbers import Number
from sploitego.xmltools.oxml import *
from re import sub

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Sploitego Project'
__credits__ = ['Nadeem Douba']

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'

__all__ = [
    'Message',
    'MaltegoElement',
    'TransformAdapter',
    'MaltegoTransform',
    'BuiltInTransformSets',
    'TransformSet',
    'InputConstraint',
    'OutputEntity',
    'InputEntity',
    'PropertyType',
    'TransformProperty',
    'TransformPropertySetting',
    'CmdLineTransformProperty',
    'CmdLineTransformPropertySetting',
    'CmdParmTransformProperty',
    'CmdParmTransformPropertySetting',
    'CmdCwdTransformProperty',
    'CmdCwdTransformPropertySetting',
    'CmdDbgTransformProperty',
    'CmdDbgTransformPropertySetting',
    'TransformSettings',
    'MaltegoMessage',
    'MaltegoTransformExceptionMessage',
    'MaltegoException',
    'MaltegoTransformResponseMessage',
    'Label',
    'MatchingRule',
    'Field',
    'StringEntityField',
    'EnumEntityField',
    'IntegerEntityField',
    'BooleanEntityField',
    'FloatEntityField',
    'LongEntityField',
    'EntityFieldType',
    'EntityField',
    'UIMessageType',
    'UIMessage',
    'Entity',
    'Device',
    'BuiltWithTechnology',
    'Domain',
    'DNSName',
    'MXRecord',
    'NSRecord',
    'IPv4Address',
    'Netblock',
    'AS',
    'Website',
    'URL',
    'Phrase',
    'Document',
    'Person',
    'EmailAddress',
    'Twit',
    'Affiliation',
    'AffiliationBebo',
    'AffiliationFacebook',
    'AffiliationFlickr',
    'AffiliationLinkedin',
    'AffiliationMySpace',
    'AffiliationOrkut',
    'AffiliationSpock',
    'AffiliationTwitter',
    'AffiliationZoominfo',
    'AffiliationWikiEdit',
    'Location',
    'PhoneNumber',
    'Banner',
    'Port',
    'Service',
    'Vuln',
    'Webdir',
    'WebTitle',
    'HTML',
    'TABLE',
    'TR',
    'A',
    'IMG',
    'TD',
    'Table'
]


class Message(ElementTree):
    pass

class MaltegoElement(Element):
    pass

class TransformAdapter(object):
    Local ='com.paterva.maltego.transform.protocol.v2.LocalTransformAdapterV2'
    Remote ='com.paterva.maltego.transform.protocol.v2.RemoteTransformAdapterV2'


@XMLAttribute(name='abstract', type=XSAttributeType.Bool, default=False)
@XMLAttribute(name='author', default='')
@XMLAttribute(name='description', default='')
@XMLAttribute(name='displayName', propname='displayname')
@XMLAttribute(name='name')
@XMLAttribute(name='requireDisplayInfo', propname='requireinfo', type=XSAttributeType.Bool, default=False)
@XMLAttribute(name='template', type=XSAttributeType.Bool, default=False)
@XMLAttribute(name='visibility', default='public')
@XMLAttribute(name='helpURL', propname='helpurl')
@XMLAttribute(name='owner')
@XMLAttribute(name='version', default='1.0')
@XMLAttribute(name='locationRelevance', propname='locrel')
@XMLSubElement(name='TransformAdapter', propname='adapter', type=XSSubElementType.Enum, choices=[TransformAdapter.Local, TransformAdapter.Remote], default=TransformAdapter.Local)
@XMLSubElement(name='StealthLevel', propname='stealthlvl', type=XSSubElementType.Integer, default=0)
@XMLSubElement(name='defaultSets', propname='sets', type=XSSubElementType.List)
@XMLSubElement(name='Disclaimer', propname='disclaimer', type=XSSubElementType.CData)
@XMLSubElement(name='Help', propname='help', type=XSSubElementType.CData)
@XMLSubElement(name='OutputEntities', propname='output', type=XSSubElementType.List)
@XMLSubElement(name='InputConstraints', propname='input', type=XSSubElementType.List)
@XMLSubElement(name='Properties/Fields', propname='properties', type=XSSubElementType.List)
class MaltegoTransform(MaltegoElement):
    def __init__(self, name, displayname, **kwargs):
        super(MaltegoTransform, self).__init__(self.__class__.__name__)
        self.name = name
        self.displayname = displayname
        self.abstract = kwargs.get('abstract', self.abstract)
        self.author = kwargs.get('author', self.author)
        self.description = kwargs.get('description', self.description)
        self.requireinfo = kwargs.get('requireinfo', self.requireinfo)
        self.template = kwargs.get('template', self.template)
        self.visibility = kwargs.get('visibility', self.visibility)
        self.helpurl = kwargs.get('helpurl', self.helpurl)
        self.owner = kwargs.get('owner', self.owner)
        self.version = kwargs.get('version', self.version)
        self.locrel = kwargs.get('locrel', self.locrel)
        self.adapter = kwargs.get('adapter', self.adapter)
        self.stealthlvl = kwargs.get('stealthlvl', self.stealthlvl)
        self.disclaimer = kwargs.get('disclaimer')
        self.help = kwargs.get('help')
        self.appendelements(kwargs.get('sets'))
        self.appendelements(kwargs.get('input'))
        self.appendelements(kwargs.get('output'))
        self.appendelements(kwargs.get('properties'))

    def appendelement(self, other):
        if isinstance(other, TransformSet):
            self.sets += other
        elif isinstance(other, TransformProperty):
            self.properties += other
        elif isinstance(other, InputConstraint) or isinstance(other, InputEntity):
            self.input += other
        elif isinstance(other, OutputEntity):
            self.output += other

    def removeelement(self, other):
        if isinstance(other, TransformSet):
            self.sets -= other
        if isinstance(other, TransformProperty):
            self.properties -= other
        elif isinstance(other, InputConstraint) or isinstance(other, InputEntity):
            self.input -= other
        elif isinstance(other, OutputEntity):
            self.output -= other


class BuiltInTransformSets(object):
    ConvertToDomain = "Convert to Domain"
    DomainsUsingMXNS = "Domains using MX NS"
    FindOnWebpage = "Find on webpage"
    RelatedEmailAddresses = "Related Email addresses"
    DNSFromDomain = "DNS from Domain"
    EmailAddressesFromDomain = "Email addresses from Domain"
    IPOwnerDetail = "IP owner detail"
    ResolveToIP = "Resolve to IP"
    DNSFromIP = "DNS from IP"
    EmailAddressesFromPerson = "Email addresses from Person"
    InfoFromNS = "Info from NS"
    DomainFromDNS = "Domain From DNS"
    FilesAndDocumentsFromDomain = "Files and Documents from Domain"
    LinksInAndOutOfSite = "Links in and out of site"
    DomainOwnerDetail = "Domain owner detail"
    FilesAndDocumentsFromPhrase = "Files and Documents from Phrase"


@XMLAttribute(name='name')
class TransformSet(MaltegoElement):

    def __init__(self, name):
        super(MaltegoElement, self).__init__('Set')
        self.name = name


@XMLAttribute(name='max', type=XSAttributeType.Integer, default=1)
@XMLAttribute(name='min', type=XSAttributeType.Integer, default=1)
@XMLAttribute(name='type')
class InputConstraint(MaltegoElement):
    def __init__(self, type, **kwargs):
        super(InputConstraint, self).__init__('Entity')
        self.type = type
        self.min = kwargs.get('min', self.min)
        self.max = kwargs.get('max', self.max)


class OutputEntity(InputConstraint):
    pass


class InputEntity(InputConstraint):
    pass


class PropertyType(object):
    String = 'string'
    Boolean = 'boolean'
    Integer = 'int'


@XMLSubElement(name='DefaultValue', propname='defaultvalue')
@XMLSubElement(name='SampleValue', propname='samplevalue', default='')
@XMLAttribute(name='abstract', type=XSAttributeType.Bool, default=False)
@XMLAttribute(name='description', default='')
@XMLAttribute(name='displayName', propname='displayname')
@XMLAttribute(name='hidden', type=XSAttributeType.Bool, default=False)
@XMLAttribute(name='name')
@XMLAttribute(name='nullable', type=XSAttributeType.Bool, default=False)
@XMLAttribute(name='readonly', type=XSAttributeType.Bool, default=False)
@XMLAttribute(name='popup', type=XSAttributeType.Bool, default=False)
@XMLAttribute(name='type', default=PropertyType.String)
@XMLAttribute(name='visibility', default='public')
class TransformProperty(MaltegoElement):

    def __init__(self, name, default, displayname, description, **kwargs):
        super(TransformProperty, self).__init__("Property")
        self.name = name
        self.displayname = displayname
        self.defaultvalue = default
        self.description = description
        self.abstract = kwargs.get('abstract', self.abstract)
        self.samplevalue = kwargs.get('sample', self.samplevalue)
        self.hidden = kwargs.get('hidden', self.hidden)
        self.nullable = kwargs.get('nullable', self.nullable)
        self.popup = kwargs.get('popup', self.popup)
        self.readonly = kwargs.get('readonly', self.readonly)
        self.type = kwargs.get('type', self.type)
        self.visibility = kwargs.get('visibility', self.visibility)


@XMLAttribute(name='name')
@XMLAttribute(name='popup', type=XSAttributeType.Bool, default=False)
@XMLAttribute(name='type', default=PropertyType.String)
class TransformPropertySetting(MaltegoElement):

    def __init__(self, name, value, **kwargs):
        super(TransformPropertySetting, self).__init__("Property")
        self.name = name
        self.text = value
        self.popup = kwargs.get('popup', self.popup)
        self.type = kwargs.get('type', self.type)


def CmdLineTransformProperty(cmd=''):
    return TransformProperty(
        'transform.local.command',
        cmd,
        'Command line',
        'The command to execute for this transform'
    )


def CmdLineTransformPropertySetting(cmd=''):
    return TransformPropertySetting(
        'transform.local.command',
        cmd
    )


def CmdParmTransformProperty(params=''):
    return TransformProperty(
        'transform.local.parameters',
        params,
        'Command parameters',
        'The parameters to pass to the transform command'
    )


def CmdParmTransformPropertySetting(params=''):
    return TransformPropertySetting(
        'transform.local.parameters',
        params
    )


def CmdCwdTransformProperty(cwd=''):
    return TransformProperty(
        'transform.local.working-directory',
        cwd,
        'Working directory',
        'The working directory used when invoking the executable',
        sample_val='/'
    )


def CmdCwdTransformPropertySetting(cwd=''):
    return TransformPropertySetting(
        'transform.local.working-directory',
        cwd
    )


def CmdDbgTransformProperty(dbg=False):
    return TransformProperty(
        'transform.local.debug',
        str(dbg).lower(),
        'Show debug info',
        "When this is set, the transform's text output will be printed to the output window",
        sample_val=False,
        type=PropertyType.Boolean
    )


def CmdDbgTransformPropertySetting(dbg=False):
    return TransformPropertySetting(
        'transform.local.debug',
        str(dbg).lower(),
        type=PropertyType.Boolean
    )


@XMLAttribute(name='enabled', type=XSAttributeType.Bool, default=True)
@XMLAttribute(name='disclaimerAccepted', propname='accepted', type=XSAttributeType.Bool, default=False)
@XMLAttribute(name='showHelp', propname='show', type=XSAttributeType.Bool, default=True)
@XMLSubElement(name='Properties', propname='properties', type=XSSubElementType.List)
class TransformSettings(MaltegoElement):

    def __init__(self, **kwargs):
        super(TransformSettings, self).__init__(self.__class__.__name__)
        self.enabled = kwargs.get('enabled', self.enabled)
        self.accepted = kwargs.get('accepted', self.accepted)
        self.show = kwargs.get('show', self.show)
        self.appendelements(kwargs.get('properties'))

    def appendelement(self, other):
        if isinstance(other, TransformPropertySetting):
            self.properties += other

    def removeelement(self, other):
        if isinstance(other, TransformPropertySetting):
            self.properties -= other


class MaltegoMessage(MaltegoElement):

    def __init__(self, message):
        super(MaltegoMessage, self).__init__(self.__class__.__name__)
        self.append(message)


@XMLSubElement(name='Exceptions', propname='exceptions', type=XSSubElementType.List)
class MaltegoTransformExceptionMessage(MaltegoElement):

    def __init__(self, **kwargs):
        super(MaltegoTransformExceptionMessage, self).__init__(self.__class__.__name__)
        self.appendelements(kwargs.get('exceptions'))

    def appendelement(self, exception):
        if isinstance(exception, MaltegoException):
            self.exceptions += exception
        else:
            self.exceptions += MaltegoException(str(exception))


class MaltegoException(MaltegoElement, Exception):

    def __init__(self, message):
        super(MaltegoException, self).__init__('Exception')
        Exception.__init__(self, message)
        self.text = str(message)


@XMLSubElement(name='UIMessages', propname='uimessages', type=XSSubElementType.List)
@XMLSubElement(name='Entities', propname='entities', type=XSSubElementType.List)
class MaltegoTransformResponseMessage(MaltegoElement):

    def __init__(self, **kwargs):
        super(MaltegoTransformResponseMessage, self).__init__(self.__class__.__name__)
        self.appendelements(kwargs.get('entities'))
        self.appendelements(kwargs.get('uimessages'))

    def appendelement(self, other):
        if isinstance(other, Entity):
            self.entities += other
        elif isinstance(other, UIMessage):
            self.uimessages += other

    def removeelement(self, other):
        if isinstance(other, Entity):
            self.entities -= other
        elif isinstance(other, UIMessage):
            self.uimessages -= other


@XMLAttribute(name='Name', propname='name')
@XMLAttribute(name='Type', propname='type', default='text/text')
@XMLSubElement(name='CDATA', propname='cdata')
class Label(MaltegoElement):

    def __init__(self, name, value, **kwargs):
        super(Label, self).__init__(self.__class__.__name__)
        self.name = name
        self.type = kwargs.get('type', self.type)

        if self.type == 'text/html':
            self.cdata = value
        else:
            self.text = str(value)


class MatchingRule(object):
    Strict = "strict"
    Loose = "loose"


@XMLAttribute(name='Name', propname='name')
@XMLAttribute(name='DisplayName', propname='displayname')
@XMLAttribute(name='MatchingRule', propname='matchingrule', default=MatchingRule.Strict)
class Field(MaltegoElement):

    def __init__(self, name, value, **kwargs):
        super(Field, self).__init__(self.__class__.__name__)
        self.name = name
        self.matchingrule = kwargs.get('matchingrule', self.matchingrule)
        self.displayname = kwargs.get('displayname', name.title())
        self.text = str(value)


class StringEntityField(object):

    def __init__(self, name, displayname=None, decorator=None, matchingrule=MatchingRule.Strict):
        self.name = name
        self.displayname = name.title() if displayname is None else displayname
        self.decorator = decorator
        self.matchingrule = matchingrule

    def _find(self, obj):
        for f in obj.fields:
            if f.name == self.name:
                return f
        return None

    def __get__(self, obj, objtype):
        o = self._find(obj)
        return o.text if o is not None else None

    def __set__(self, obj, val):
        f = self._find(obj)
        if not isinstance(val, basestring) and val is not None:
            val = str(val)
        if f is None and val is not None:
            f = Field(self.name, val, displayname=self.displayname, matchingrule=self.matchingrule)
            obj += f
        elif f is not None and val is None:
            obj -= f
        else:
            f.text = val
        if self.decorator is not None:
            self.decorator(obj, val)


class EnumEntityField(StringEntityField):

    def __init__(self, name, displayname=None, choices=[], decorator=None):
        self.choices = [ str(c) for c in choices ]
        super(EnumEntityField, self).__init__(name, displayname, decorator)

    def __set__(self, obj, val):
        val = str(val)
        if val not in self.choices:
            raise ValueError('Expected one of %s (got %s instead)' % (self.choices, val))
        super(EnumEntityField, self).__set__(obj, val)


class IntegerEntityField(StringEntityField):

    def __get__(self, obj, objtype):
        return int(super(IntegerEntityField, self).__get__(obj, objtype))

    def __set__(self, obj, val):
        if not isinstance(val, Number):
            raise TypeError('Expected an instance of int (got %s instance instead)' % type(val).__name__)
        super(IntegerEntityField, self).__set__(obj, val)


class BooleanEntityField(StringEntityField):

    def __get__(self, obj, objtype):
        return super(BooleanEntityField, self).__get__(obj, objtype) == 'true'

    def __set__(self, obj, val):
        if not isinstance(val, bool):
            raise TypeError('Expected an instance of bool (got %s instance instead)' % type(val).__name__)
        super(BooleanEntityField, self).__set__(obj, str(val).lower())


class FloatEntityField(StringEntityField):

    def __get__(self, obj, objtype):
        return float(super(FloatEntityField, self).__get__(obj, objtype))

    def __set__(self, obj, val):
        if not isinstance(val, Number):
            raise TypeError('Expected an instance of float (got %s instance instead)' % type(val).__name__)
        super(FloatEntityField, self).__set__(obj, val)


class LongEntityField(StringEntityField):

    def __get__(self, obj, objtype):
        return long(super(LongEntityField, self).__get__(obj, objtype))

    def __set__(self, obj, val):
        if not isinstance(val, Number):
            raise TypeError('Expected an instance of float (got %s instance instead)' % type(val).__name__)
        super(LongEntityField, self).__set__(obj, val)


class EntityFieldType(object):
    String = StringEntityField
    Integer = IntegerEntityField
    Long = LongEntityField
    Float = FloatEntityField
    Bool = BooleanEntityField
    Enum = EnumEntityField


class EntityField(object):

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        if self.name is None:
            raise ValueError("Keyword argument 'name' is required.")
        self.property = kwargs.get('propname', sub('[^\w]+', '_', self.name))
        self.displayname = kwargs.get('displayname', self.name.title())
        self.type = kwargs.get('type', EntityFieldType.String)
        self.required = kwargs.get('required', False)
        self.choices = kwargs.get('choices')
        self.matchingrule = kwargs.get('matchingrule', MatchingRule.Strict)
        self.decorator = kwargs.get('decorator')

    def __call__(self, cls):
        if self.type is EntityFieldType.Enum:
            setattr(cls, self.property, self.type(self.name, self.displayname, self.choices, self.decorator))
        else:
            setattr(cls, self.property, self.type(self.name, self.displayname, self.decorator))
        return cls


class UIMessageType(object):
    Fatal = "FatalError"
    Partial = "PartialError"
    Inform = "Inform"
    Debug = "Debug"


@XMLAttribute(name='MessageType', propname='type', default=UIMessageType.Inform)
class UIMessage(MaltegoElement):

    def __init__(self, message, **kwargs):
        super(UIMessage, self).__init__(self.__class__.__name__)
        self.type = kwargs.get('type', self.type)
        self.text = str(message)


@XMLSubElement(name='Value', propname='value')
@XMLSubElement(name='Weight', propname='weight', type=XSSubElementType.Integer, default=1)
@XMLSubElement(name='IconURL', propname='iconurl')
@XMLSubElement(name='AdditionalFields', propname='fields', type=XSSubElementType.List)
@XMLSubElement(name='DisplayInformation', propname='labels', type=XSSubElementType.List)
@XMLSubElement(name='Value', propname='value')
@XMLAttribute(name='Type', propname='type')
class Entity(MaltegoElement):

    name = None

    def __init__(self, value, **kwargs):
        super(Entity, self).__init__("Entity")
        type = kwargs.get('type', None)
        if type is None:
            self.type = 'maltego.%s' % self.__class__.__name__ if self.name is None else self.name
        self.value = value
        self.weight = kwargs.get('weight', self.weight)
        self.iconurl = kwargs.get('iconurl', self.iconurl)
        self.appendelements(kwargs.get('fields'))
        self.appendelements(kwargs.get('labels'))

    def appendelement(self, other):
        if isinstance(other, Field):
            display_name = other.get('DisplayName')
            if display_name is None:
                name = other.get('Name')
                if name in self.fields.keys():
                    other.set('DisplayName', self.fields[name])
                else:
                    other.set('DisplayName', name.title())
            self.fields += other
        elif isinstance(other, Label):
            self.labels += other

    def removeelement(self, other):
        if isinstance(other, Field):
            self.fields -= other
        elif isinstance(other, Label):
            self.labels -= other


class Device(Entity):
    pass


class BuiltWithTechnology(Entity):
    pass


@EntityField(name='fqdn', displayname='Domain Name')
@EntityField(name='whois-info', propname='whoisinfo', displayname='WHOIS Info')
class Domain(Entity):
    pass


@EntityField(name='fqdn', displayname='DNS Name')
class DNSName(Entity):
    pass


@EntityField(name='fqdn', displayname='MX Record')
@EntityField(name='mxrecord.priority', propname='mxpriority', type=EntityFieldType.Integer)
class MXRecord(Entity):
    pass


@EntityField(name='fqdn', displayname='NS Record')
class NSRecord(Entity):
    pass


@EntityField(name='ipv4-address', propname='ipv4address', displayname='IP Address')
@EntityField(name='ipaddress.internal', propname='internal', displayname='Internal', type=EntityFieldType.Bool)
class IPv4Address(Entity):
    pass


@EntityField(name='ipv4-range', propname='ipv4range', displayname='IP Range')
class Netblock(Entity):
    pass


@EntityField(name='as.number', propname='number', displayname='AS Number', type=EntityFieldType.Integer)
class AS(Entity):
    pass


@EntityField(name='http', displayname='HTTP Ports')
@EntityField(name='https', displayname='HTTPS Ports')
@EntityField(name='servertype', displayname='Server Banner')
@EntityField(name='URLS', propname='urls', displayname='URLs')
class Website(Entity):
    pass


@EntityField(name='fqdn', displayname='Website')
@EntityField(name='website.ssl-enabled', propname='ssl', displayname='SSL Enabled', type=EntityFieldType.Bool)
@EntityField(name='ports', displayname='Ports')
class URL(Entity):
    pass


@EntityField(name='text', displayname='Text')
class Phrase(Entity):
    pass


@EntityField(name='title', displayname='Title')
@EntityField(name='document.meta-data', propname='metadata', displayname='Meta-Data')
@EntityField(name='url', displayname='URL')
class Document(Entity):
    pass


@EntityField(name='person.fullname', propname='fullname', displayname='Full Name')
@EntityField(name='person.firstnames', propname='firstnames', displayname='First Names')
@EntityField(name='person.lastname', propname='lastname', displayname='Surname')
class Person(Entity):
    pass


@EntityField(name='email', displayname='Email Address')
class EmailAddress(Entity):
    pass


@EntityField(name='twit.name', propname='name', displayname='Twit')
@EntityField(name='id', displayname='Twit ID')
@EntityField(name='author', displayname='Author')
@EntityField(name='author_uri', propname='authoruri', displayname='AUthor URI')
@EntityField(name='content', displayname='Content')
@EntityField(name='imglink', displayname='Image Link')
@EntityField(name='pubdate', displayname='Date published')
@EntityField(name='title', displayname='Title')
class Twit(Entity):
    pass


@EntityField(name='person.name', propname='name', displayname='Name')
@EntityField(name='affiliation.uid', propname='uid', displayname='UID')
@EntityField(name='affiliation.network', propname='network', displayname='Network')
@EntityField(name='affiliation.profile-url', propname='profileurl', displayname='Profile URL')
class Affiliation(Entity):
    pass


class AffiliationBebo(Affiliation):
    pass


class AffiliationFacebook(Affiliation):
    name = "maltego.affiliation.Facebook"


class AffiliationFlickr(Affiliation):
    name = "maltego.affiliation.Flickr"


class AffiliationLinkedin(Affiliation):
    pass


class AffiliationMySpace(Affiliation):
    pass


class AffiliationOrkut(Affiliation):
    pass


class AffiliationSpock(Affiliation):
    pass


@EntityField(name='twitter.number', propname='number', displayname='Twitter Number')
@EntityField(name='twitter.screen-name', propname='number', displayname='Screen Name')
@EntityField(name='twitter.friendcount', propname='number', displayname='Friend Count')
@EntityField(name='twitter.fullname', propname='fullname', displayname='Real Name')
class AffiliationTwitter(Affiliation):
    name = "maltego.affiliation.Twitter"


class AffiliationZoominfo(Affiliation):
    pass


class AffiliationWikiEdit(Affiliation):
    pass


@EntityField(name='location.name', propname='name', displayname='Name')
@EntityField(name='country', displayname='Country')
@EntityField(name='city', displayname='City')
@EntityField(name='location.area', propname='area', displayname='Area')
@EntityField(name='countrycode', displayname='Country Code')
@EntityField(name='longitude', displayname='Longitude')
@EntityField(name='latitude', displayname='Latitude')
class Location(Entity):
    pass


@EntityField(name='phonenumber', displayname='Phone Number')
@EntityField(name='phonenumber.countrycode', propname='countrycode', displayname='Country Code')
@EntityField(name='phonenumber.citycode', propname='citycode', displayname='City Code')
@EntityField(name='phonenumber.areacode', propname='areacode', displayname='Area Code')
@EntityField(name='phonenumber.lastnumbers', propname='lastnumbers', displayname='Last Digits')
class PhoneNumber(Entity):
    pass


class Banner(Entity):
    pass


class Port(Entity):
    pass


class Service(Entity):
    pass


class Vuln(Entity):
    pass


class Webdir(Entity):
    pass


@EntityField(name='title', displayname='Title')
class WebTitle(Entity):
    pass


class HTML(Element, object):

    def __init__(self, tag='html', attrib={}, **extra):
        attrib = attrib.copy()
        attrib.update(extra)
        super(HTML, self).__init__(tag, attrib)

    def __add__(self, other):
        newobj = deepcopy(self)
        newobj.append(other)
        return newobj

    def __iadd__(self, other):
        self.append(other)
        return self

    def __sub__(self, other):
        self.remove(other)
        newobj = deepcopy(self)
        self.append(other)
        return newobj

    def __isub__(self, other):
        self.remove(other)
        return self

    def __str__(self):
        sio = StringIO()
        ElementTree(self).write(sio)
        return sio.getvalue()


class TABLE(HTML):

    def __init__(self, title="GENERAL INFORMATION", colspan="2", **kwargs):
        super(TABLE, self).__init__(
            "table",
            attrib={
                'width' : '100%',
                'border' : '1',
                'rules' : 'cols',
                'frame' : 'box',
                'cellpadding' : '2'
            }
        )

        tr = TR()
        self.append(tr)
        tr.append(TD(title, colspan=colspan, css_class=TD.ONE))

        for i in kwargs:
            self.set(i, str(kwargs[i]))

class TR(HTML):

    def __init__(self):
        super(TR, self).__init__('tr')


class A(HTML):

    def __init__(self, label, href, **kwargs):
        attrib = { 'href' : href }
        attrib.update(kwargs)
        super(A, self).__init__(
            'a',
            attrib=attrib
        )
        self.text = label


class IMG(HTML):

    def __init__(self, src, **kwargs):
        attrib = { 'src' : src }
        attrib.update(kwargs)

        super(IMG, self).__init__(
            'img',
            attrib=attrib
        )

class TD(HTML):

    ONE = "one"
    TWO = "two"
    THREE = "three"
    VALUE = "value"

    def __init__(self, value, css_class=TWO, align="center", **kwargs):
        super(TD, self).__init__(
            'td',
            attrib={
                'class' : css_class,
                'align' : align,
            }
        )
        self.text = str(value)

        for i in kwargs:
            self.set(i, str(kwargs[i]))


class Table(object):

    def __init__(self, columns, title='GENERAL INFORMATION'):
        self._rows = []
        self._title = title
        self._rows.append([ TD(c, TD.THREE) for c in columns ])

    def addrow(self, columns):
        self._rows.append([ TD(c) for c in columns ])

    def __str__(self):
        self.table = TABLE(self._title, colspan=len(self._rows[0]))
        for r in self._rows:
            tr = TR()
            c = tr.getchildren()
            c += r
            self.table += tr
        return str(self.table)
