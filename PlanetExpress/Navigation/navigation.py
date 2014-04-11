import requests


class Navigator():
    def log_in(self, username, api_key):
        requests.post("https://identity.api.rackspacecloud.com/v2.0/tokens", data={
                "username": username,
                "apiKey": api_key,
            })
