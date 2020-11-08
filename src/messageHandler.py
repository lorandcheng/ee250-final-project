import json
import requests
import datetime

from pprint import pprint

class messageHandler:
    def __init__(self, name, serverAddress):
        """
        Summary: Class that manages the HTTP interactions with the messaging server

        Args:
            name (string): Name of node
            serverAddress (string): Target server to connect to in format ip_addr:port
        """
        self.name = name
        self.serverAddress = serverAddress


    def sendMessage(self, message):
        """
        Summary: Sends a POST message to the server

        Args:
            message (string): Content of the message
        """
        headers = {
            'Content-Type': 'application/json',
            'Authorization': None   # not using HTTP secure
        }

        payload = {
            'sender': self.name,
            'message': message,
            'timestamp': datetime.datetime()
        }

        response = requests.post("http://{}/send-message".format(self.address),
                                 headers=headers,
                                 data=json.dumps(payload))

        if response.status_code == 200:
            pprint(response.json())
            return 1
        else:
            return 0


    def getMessage(self):
        pass
    