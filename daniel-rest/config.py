import socket



def get_rest_api_server():
  print(socket.gethostname())
  return "http://" + socket.gethostname() + ":3032/"