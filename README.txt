=====================
 pyrancid-RESTClient
=====================

This is a client for rancid REST service.

This module allows your applcations to easily manipulate rancid configuration
via the rancid REST service.


Usage:

from pprint import pprint
from rancid import RESTClient

r = RESTClient(
    url='http://localhost:10680/',
    secret='password',
)

g = r.getGroup('mygroup')
pprint(g)
{u'adminmailrcpt': u'rancid-admin-mygroup',
 u'mailrcpt': u'rancid-mygroup',
 u'name': u'mygroup',
 u'storage_path': u'/opt/data/mygroup'}

n=r.getNode('testdevice', 'mygroup')
pprint(n)
{u'config_path': u'/opt/data/mygroup/configs/testdevice',
 u'group': u'mygroup',
 u'name': u'testdevice',
 u'status': u'up',
 u'vendor': u'cisco'}


BSD license, (C) 2012 Matej Vadnjal <matej@arnes.si>
