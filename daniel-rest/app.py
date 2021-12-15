from flask import Flask
from flask_restful import Api

from models.log import Log
from models.host import Host
from models.hosts import Hosts

app = Flask(__name__)
api = Api(app)

api.add_resource(Hosts,   '/hosts/')  # Lists all hosts
api.add_resource(Host,    '/hosts/<host>/')  # Lists all files for a given host
api.add_resource(Log,     '/hosts/<host>/logs')  # Lists all logs for a given host

if __name__ == '__main__':
  app.run(host='localhost', port='3032', debug=True)  # run our Flask app