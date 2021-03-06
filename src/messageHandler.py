# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# 
# Author: Lorand Cheng https://github.com/lorandcheng
# Date: Nov 15, 2020
# Project: USC EE250 Final Project, Morse Code Translator and Messenger
# 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
import json
import requests

from datetime import datetime
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
            'timestamp': datetime.now()
        }

        response = requests.post("http://{}/send-message".format(self.serverAddress),
                                 headers=headers,
                                 data=json.dumps(payload, indent=4, sort_keys=True, default=str))

        if response.status_code == 200:
            pprint(response.json())
            return 1
        else:
            return 0

    def getMessages(self,lastRead):
        """
        Summary: Sends a GET message to the server
        """

        params = {
            'sender': self.name,
            'lastRead': lastRead
        }

        return requests.get("http://{}/get-messages".format(self.serverAddress), params=params)

    def getMessageHistory(self):
        """
        Summary: Sends a GET message to the server
        """

        params = {
            'sender': self.name
        }

        return requests.get("http://{}/history".format(self.serverAddress), params=params)
