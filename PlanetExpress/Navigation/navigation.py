import requests
import json


class Navigator(object):
    """
    This is just a generic class that provides some functions to help you get authenticated, and work
    with the rackspace cloud.
    """

    def __init__(self, **kwargs):
        self.region = kwargs.get('region')
        self.token = None
        self.servers = {}
        self.serviceCatalog = None

        self.fg_servers = None
        self.ng_servers = None
        self.ng_servers_url = None

        self.images = None


    @staticmethod
    def dump_json(var):
        return json.dumps(var, indent=4, separators=(',', ': '), ensure_ascii=False)

    def get_request(self, url, **kwargs):
        """
        Just a GET request. Not a static method, because you need to be authenticated.

        :param url: A URL to request
        :param kwargs: Anything additional you want to pass to requests.
        :return: The request
        """
        return requests.get(url, headers={'X-Auth-Token': self.token['id']}, **kwargs)

    def post_request(self, url, **kwargs):
        """
        Just a POST request. Not a static method, because you need to be authenticated.

        :param url: A URL to request
        :param kwargs: Anything additional you want to pass to requests.
        :return: The request
        """
        return requests.post(url, headers={'X-Auth-Token': self.token['id']}, **kwargs)

    def log_in(self, username, api_key):
        """
        Log into the API, update __this__ with auth token

        :param username: Your username
        :param api_key: Your API key
        :return: Status code and response body
        """

        data = {
            "auth": {
                "RAX-KSKEY:apiKeyCredentials": {
                    "username": username,
                    "apiKey": api_key,
                }
            }
        }

        r = requests.post("https://identity.api.rackspacecloud.com/v2.0/tokens",
                          data=json.dumps(data),
                          headers={"content-Type": "application/json",})

        response = json.loads(r.text)

        self.token = response['access']['token']
        self.serviceCatalog = response['access']['serviceCatalog']

        self.ng_servers_url = "https://%(region)s.servers.api.rackspacecloud.com/v2/%(account_id)s" % {
            'region': self.region,
            'account_id': self.token['tenant']['id']
        }

        return {
            'status_code': r.status_code,
            'text': r.text,
        }

    def add_network_to_server(self, instance_id, network_id):
        """
        Attach network to a server

        :param instance_id: ID of server
        :param network_id: ID of network
        :return: Dict containing 'status_code' and 'text'
        """

        payload = {
            "virtual_interface":
            {
                "network_id": network_id
            }
        }
        headers = {
            'content-type': 'application/json'
        }

        r = self.post_request(
            self.ng_servers_url + "/servers/%(instance_id)s/os-virtual-interfacesv2" % instance_id,
            data=json.dumps(payload),
            headers=headers
        )

        return {
            'status_code': r.status_code,
            'text': r.text,
        }

    def parse_catalog(self):
        for endpoints in self.serviceCatalog:
            if endpoints['type'] == 'compute':
                endpoint_list = endpoints['endpoints']
                if float(endpoint_list[0]['versionId']) >= 2:
                    print "second gen:", self.dump_json(endpoint_list)
                else:
                    print "first gen:", self.dump_json(endpoint_list)

    def get_servers(self, **kwargs):

        if kwargs.get('version', 2) == 2:
            url = "https://%(region)s.servers.api.rackspacecloud.com/v2/%(account_id)s/servers/detail" % {
                'region': self.region.lower(),
                'account_id': self.token['tenant']['id'],
            }
        elif kwargs['version'] == 1:
            url = "https://servers.api.rackspacecloud.com/v1.0/%(account_id)s" % {
                'account_id': self.token['tenant']['id'],
            }
        else:
            return {
                'status_code': 0,
                'text': 'version %d not supported.' % kwargs['version']
            }

        r = self.get_request(url)

        if kwargs.get('version', 2) == 2:
            self.ng_servers = json.loads(r.text)['servers']
        elif kwargs['version'] == 1:
            self.fg_servers = json.loads(r.text)['servers']

        return {
            'status_code': r.status_code,
            'text': r.text,
        }

    def get_images(self, **kwargs):

        if kwargs.get('version', 2) == 2:
            url = "https://%(region)s.images.api.rackspacecloud.com/v2/%(account_id)s/images" % {
                'region': self.region.lower(),
                'account_id': self.token['tenant']['id'],
            }
        else:
            return {
                'status_code': 0,
                'text': 'version %d not supported.' % kwargs['version']
            }

        r = self.get_request(url)

        if kwargs.get('version', 2) == 2:
            self.images = json.loads(r.text)['images']

        return {
            'status_code': r.status_code,
            'text': r.text,
        }

    def get_image_by_id(self, id, **kwargs):

        for image in self.images:
            if image['id'] == id:
                return image

        return None

    def get_image_members(self, image_id, **kwargs):

        if kwargs.get('version', 2) == 2:
            url = "https://%(region)s.images.api.rackspacecloud.com/v2/%(account_id)s/images/%(image_id)s/members" % {
                'region': self.region.lower(),
                'account_id': self.token['tenant']['id'],
                'image_id': image_id,
            }
        else:
            return {
                'status_code': 0,
                'text': 'version %d not supported.' % kwargs['version']
            }

        r = self.get_request(url)

        return {
            'status_code': r.status_code,
            'text': r.text,
        }

    def get_private_network_addresses(self):

        self.get_all_network_addresses()

    def get_all_network_addresses(self, **kwargs):

        server_addresses = {}

        for server in self.ng_servers:
            server_addresses[server['name']] = self.get_server_network_addresses(server)

        return server_addresses

    def get_server_network_addresses(self, server):
        return server['addresses']

    def add_image_member(self, **kwargs):

        if kwargs.get('version', 2) == 2:
            url = "https://%(region)s.images.api.rackspacecloud.com/v2/%(account_id)s/images/%(image_id)s/members" % {
                'region': self.region.lower(),
                'account_id': self.token['tenant']['id'],
                'image_id': kwargs['image_id'],
            }
            payload = {
                'member': kwargs['tenant_id']
            }
        else:
            return {
                'status_code': 0,
                'text': 'version %d not supported.' % kwargs['version']
            }

        r = requests.post(url, data=json.dumps(payload), headers={'X-Auth-Token': self.token['id']})

        return {
            'status_code': r.status_code,
            'text': r.text,
        }
