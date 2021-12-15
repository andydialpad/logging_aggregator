def create_item(filename=None,
                hostname=None,
                last_modified=None,
                logging_data=None):
    data = {}
    if hostname:
        data['host'] = {"S": hostname}

    if filename:
        data['filename'] = {"S": filename}

    if last_modified:
        data['last_modified'] = {"N": last_modified}

    if logging_data:
        data['logline'] = {"S": logging_data}

    return data
