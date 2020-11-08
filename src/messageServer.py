from flask import Flask
from flask import jsonify
from flask import request

import json
import messageManager

app = Flask('Cloud Messaging Server')