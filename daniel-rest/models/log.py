from flask import Flask
from flask_restful import Resource, Api, reqparse


class Log(Resource):
  def get(self):

    data = {'user':'test'}  # convert dataframe to dict
    return {'data': data}, 200  # return data and 200 OK

  def post(self):
    parser = reqparse.RequestParser()  # initialize
    parser.add_argument('userId', required=True)  # add args
    parser.add_argument('name', required=True)
    parser.add_argument('city', required=True)
    args = parser.parse_args()  # parse arguments to dictionary


    return {'data': 'data.to_dict()'}, 200  # return data with 200 OK