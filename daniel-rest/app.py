from flask import Flask
from flask_restful import Api

from models.log import Log

app = Flask(__name__)
api = Api(app)

api.add_resource(Log, '/logs')  # add endpoints

if __name__ == '__main__':
  app.run()  # run our Flask app¡