import requests
import json




class Navigator():

    def __init__(self, **kwargs):
        self.region = kwargs.get('region')
        self.token = None
        self.servers = {}
        self.serviceCatalog = None

        self.fg_servers = None
        self.ng_servers = None

        self.images = None


    @staticmethod
    def dump_json(var):
        return json.dumps(var, indent=4, separators=(',', ': '), ensure_ascii=False)


    def get_request(self, url):
        return requests.get(url, headers={'X-Auth-Token': self.token['id']})


    def log_in(self, username, api_key):

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
