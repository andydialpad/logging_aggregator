import datetime
import uuid


class Log:

    filename = None
    data = None
    last_modified = None
    host = None
    Key = None

    def __init__(self,
                 host,
                 filename,
                 data,
                 last_modified=datetime.datetime.now().timestamp()):
        self.host = host
        self.filename = filename
        self.data = data
        self.last_modified = last_modified
        self.Key = uuid.uuid4()
