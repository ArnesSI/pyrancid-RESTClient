# REST client for rancid web service

import httplib, urllib
import json

class RESTClient:
    def __init__(self, **kwargs):
        if 'url' in kwargs:
            self.prefix = kwargs['url']
        else:
            self.prefix = 'http://localhost:10680'
        if 'secret' in kwargs:
            self.secret = kwargs['secret']
        else:
            self.secret = None
        if 'debug' in kwargs:
            self.debug = bool(kwargs['debug'])
        else:
            self.debug = False
            
        self._init()
        
    def setSecret(self, new_secret):
        self.secret = new_secret
    
    def getAllGroups(self):
        method = 'GET'
        uri = '/rancid/group/'

        response = self._run(uri=uri, method=method)
        if self.debug and 'message' in response:
            print response['message']
        groups = response['data']
        return groups

    def getGroup(self, name):
        name = str(name)
        method = 'GET'
        uri = '/rancid/group/%s/' % name
        
        response = self._run(uri=uri, method=method)
        if self.debug and 'message' in response:
            print response['message']
        group = response['data']
        return group

    def addGroup(self, name):
        name = str(name)
        method = 'POST'
        uri = '/rancid/group/'
        
        post = { 'name': name }
        
        response = self._run(uri=uri, method=method, post=post)
        if self.debug and 'message' in response:
            print response['message']
        group = response['data']
        return group
        
    def delGroup(self, name):
        name = str(name)
        method = 'DELETE'
        uri = '/rancid/group/%s/' % name
        
        response = self._run(uri=uri, method=method)
        if self.debug and 'message' in response:
            print response['message']
        return True
        
    def getAllNodes(self, group_name=None):
        method = 'GET'
        if group_name:
            group_name = str(group_name)
            uri = '/rancid/group/%s/node/' % group_name
        else:
            uri = '/rancid/node/'
        
        response = self._run(uri=uri, method=method)
        if self.debug and 'message' in response:
            print response['message']
        nodes = response['data']
        return nodes
        
    def getNode(self, name, group_name=None):
        name = str(name)
        method = 'GET'
        if group_name:
            group_name = str(group_name)
            uri = '/rancid/group/%s/node/%s/' % (group_name, name)
        else:
            uri = '/rancid/node/%s/' % name
        
        response = self._run(uri=uri, method=method)
        if self.debug and 'message' in response:
            print response['message']
        node = response['data']
        return node
    
    def addNode(self, group_name, **kwargs):
        group_name = str(group_name)
        method = 'POST'
        uri = '/rancid/group/%s/node/' % group_name
        
        if 'name' not in kwargs:
            raise RancidRestRequestError('Name parameter is mandatory')
        post = kwargs
        
        response = self._run(uri=uri, method=method, post=post)
        if self.debug and 'message' in response:
            print response['message']
        node = response['data']
        return node
        
    def modifyNode(self, name, **kwargs):
        name = str(name)
        method = 'POST'
        uri = '/rancid/node/%s/' % name
        
        post = kwargs
        
        response = self._run(uri=uri, method=method, post=post)
        if self.debug and 'message' in response:
            print response['message']
        node = response['data']
        return node
        
    def delNode(self, group_name, name):
        group_name = str(group_name)
        name = str(name)
        method = 'DELETE'
        uri = '/rancid/group/%s/node/%s/' % (group_name, name)
        
        response = self._run(uri=uri, method=method)
        if self.debug and 'message' in response:
            print response['message']
        return True
        
    def getNodeConfig(self, name):
        name = str(name)
        method = 'GET'
        uri = '/rancid/node/%s/config/' % name
        
        response = self._run(uri=uri, method=method)
        if self.debug and 'message' in response:
            print response['message']
        config = response['data']
        return config
        
    def addNodeConfig(self, name, **kwargs):
        name = str(name)
        method = 'POST'
        uri = '/rancid/node/%s/config/' % name
        
        post = kwargs
        
        response = self._run(uri=uri, method=method, post=post)
        if self.debug and 'message' in response:
            print response['message']
        # return diff (if any)
        if 'data' in response:
            return response['data']
        else:
            return ''
            
    def saveNodeConfig(self, name):
        name = str(name)
        method = 'GET'
        uri = '/rancid/node/%s/config/save/' % name
        
        # this can take some time - increase timeout
        timeout_orig = self.conn.timeout
        self.conn.timeout = 120
        
        try:
            response = self._run(uri=uri, method=method)
        finally:
            self.conn.timeout = timeout_orig
        
        if self.debug and 'message' in response:
            print response['message']
        # return diff (if any)
        if 'data' in response:
            return response['data']
        else:
            return ''
        
    def exportCloginrc(self):
        method = 'GET'
        uri = '/rancid/cloginrc/export/'
        
        response = self._run(uri=uri, method=method)
        if self.debug and 'message' in response:
            print response['message']
        return True

        
    def _init(self):
        tmp_prefix = self.prefix.split('://', 1)
        if tmp_prefix.count == 1:
            # just host was given
            proto = 'http'
            host = self.prefix
        else:
            proto = tmp_prefix[0]
            host = tmp_prefix[1]
        if proto == 'http':
            self.conn = httplib.HTTPConnection(host, timeout=10)
        elif proto == 'https':
            self.conn = httplib.HTTPSConnection(host, timeout=10)
        else:
            raise RancidRestRequestError('Unsupported protocol (%s)' % proto)
        if self.debug:
            self.conn.set_debuglevel(4)
    
    def _buildHeaders(self):
        headers = dict()
        if self.secret:
            headers['Auth-Secret'] = self.secret
        return headers
            
    def _run(self, **kwargs):
        if 'method' in kwargs:
            method = kwargs['method']
        else:
            method = 'GET'
        if 'uri' in kwargs:
            uri = kwargs['uri']
        else:
            raise RancidRestRequestError('uri argument not given')
        if 'post' in kwargs:
            post = kwargs['post']
            post = urllib.urlencode(post)
        else:
            post = None
        
        if not self.conn:
            self._init()
        headers = self._buildHeaders()
        
        if method == 'GET':
            self.conn.request('GET', uri, '', headers)
        elif method == 'POST':
            self.conn.request('POST', uri, post, headers)
        elif method == 'DELETE':
            self.conn.request('DELETE', uri, '', headers)
        else:
            raise RancidRestRequestError('Method (%s) not supported' % method)
        
        response = self.conn.getresponse()
        if response.status != 200:
            raise RancidRestHttpError(response.status, response.reason)
        content = response.read()
        if (self.debug): print content
        result = json.loads(content)
        if result['success'] != True:
            raise RancidRestResponseError(result['errcode'], result['message'])
        return result
 
class RancidRestError(Exception):
    def __init__(self, code, message=None):
        self.code = code
        self.message = message
 
class RancidRestHttpError(RancidRestError):
    """ Server returned non-OK HTTP status code """
    def __str__(self):
        if self.message:
            return 'Got non-OK HTTP response (%s) %s' % (self.code, self.message)
        else:
            return 'Got non-OK HTTP response (%s)' % (self.code)

class RancidRestRequestError(RancidRestError):
    """ Something was wrong while constructing request """
    def __init__(self, message):
        self.message = message
    def __str__():
        return self.message

class RancidRestResponseError(RancidRestError):
    """ Success flag in response was false """
    def __str__(self):
        if self.message:
            return 'Request was not successful (%s) %s' % (self.code, self.message)
        else:
            return 'Request was not successful (%s)' % (self.code)
