import datetime
import uuid


class Log:

    filename = None
    data = None
    last_modified = None
    Key = None

    def __init__(self,
                 filename,
                 data,
                 last_modified=datetime.datetime.now().timestamp()):
        self.filename = filename
        self.data = data
        self.last_modified = last_modified
        self.Key = uuid.uuid4()
