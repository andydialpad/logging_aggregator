import datetime
import json
import time
import os
from models.log import Log
from models.datastore import Datastore

# Henrik will parse the logs every n minutes. It will compare the last modified date to a date stored on disk, if newer, will do a scan/push and update date stored on disk

# to do this, we could use git, to keep track of changes, and help us find new lines, but that might not be in the spirit of the assignment.
# so instead, lets keep track of changes for each file by inserting a special character into the logfile, and reading back from the end of the file to that character


class App:
    LOG_DIR = '/var/log'
    #LOG_DIR = 'test/var_log'
    LAST_MODIFIED = 'last-modified'

    LOG_ACCESS_DELIMITER = u"\u200E"  #use LTR character as non-visible indicator that we're caught up

    def __init__(self):
        pass

    @staticmethod
    def write_metadata(metadata, filename):
        metadata_file = open(filename, 'w')
        json.dump(metadata, metadata_file)
        metadata_file.close()

    @staticmethod
    def get_metadata(filename):

        metadata_file = open(filename, "r")
        metadata = metadata_file.read()
        metadata = json.loads(metadata)
        metadata_file.close()
        return metadata or {}

    def process_file(self, file_metadata, filename):
        print(" Processing %s" % filename)
        new_log_lines = []
        file_path = self.LOG_DIR + "/" + filename
        for line in reversed(list(open(file_path))):
            if not self.LOG_ACCESS_DELIMITER in line:
                new_log_lines.append(
                    Log(filename=filename, data=line, host=os.uname()[1]))
            else:
                break
        if len(new_log_lines) > 0:
            Datastore().save_batch(reversed(new_log_lines)) #reverse this list so oldest entries get earliest timestamps
            with open(file_path, "a") as append_file:
                append_file.write(self.LOG_ACCESS_DELIMITER)

        # update the metadata to now, ie all log until now have been processed.
        current_time = int(datetime.datetime.now().timestamp())
        file_metadata[self.LAST_MODIFIED] = current_time

    def main(self):

        while True:
            print("*** Checking for log updates")
            self.check_and_process_logs()
            print("*** *** Sleeping")
            time.sleep(30)

    def check_and_process_logs(self):
        metadata_filename = 'data/metadata'
        files = [f for f in os.listdir(self.LOG_DIR)]
        metadata = self.get_metadata(metadata_filename)
        for f in files:
            if not os.access( self.LOG_DIR + "/" + f, os.W_OK):
                continue
            file_metadata = metadata.get(f)
            if not file_metadata:
                file_metadata = {self.LAST_MODIFIED: None}
                self.process_file(filename=f, file_metadata=file_metadata)
            elif os.path.getmtime(self.LOG_DIR + '/' +
                                  f) > file_metadata[self.LAST_MODIFIED]:
                self.process_file(filename=f, file_metadata=file_metadata)
            metadata[f] = file_metadata
        self.write_metadata(metadata, metadata_filename)


if __name__ == '__main__':
    App().main()
