import requests
import json




class Navigator():

    def __init__(self):
        self.token = None
        self.servers = {}
        self.serviceCatalog = None
        self.fg_servers = None
        self.ng_servers = None


    @staticmethod
    def dump_json(dic):
        return json.dumps(dic, indent=4, separators=(',', ': '))


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

        if kwargs['version'] == 2:
            url = "https://%(region)s.servers.api.rackspacecloud.com/v2/%(account_id)s/servers/detail" % {
                'region': kwargs['region'].lower(),
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

        r = requests.get(url, headers={'X-Auth-Token': self.token['id']})

        if kwargs['version'] == 2:
            self.ng_servers = json.loads(r.text)['servers']
        elif kwargs['version'] == 1:
            self.fg_servers = json.loads(r.text)['servers']

        return {
            'status_code': r.status_code,
            'text': r.text,
        }

    def get_private_network_addresses():

        self.get_all_network_addresses()


    def get_all_network_addresses(self, **kwargs):

        server_addresses = {}

        for server in self.ng_servers:
            server_addresses[server['name']] = self.get_server_network_addresses(server)

        return server_addresses


    def get_server_network_addresses(self, server):
        return server['addresses']



if __name__ == '__main__':

    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), '../'))

    import settings.settings as settings

    nav = Navigator()
    nav.log_in(username=settings.ACCOUNTS['rax-ord-ng']['USERNAME'],
                     api_key=settings.ACCOUNTS['rax-ord-ng']['API_KEY'])
    nav.get_servers(version=2, region='DFW')

    print self.dump_json(nav.get_all_network_addresses())
