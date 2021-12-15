import os
def get_rest_api_server():
  return "http://" + '127.0.0.1' + ":3032/"

def is_prod():
    return os.environ.get('AWS_ACCESS_KEY_ID') or False