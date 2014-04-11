import requests
import json


class Navigator():
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
        return {
            'status_code': r.status_code,
            'text': r.text,
        }


