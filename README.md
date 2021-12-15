# Logging Aggregator

This is a simple logging aggregator. It collects logs from various systems, and aggregates them into a single service to read and search.

## Push vs Pull
A lot of thought went into the original design, whether this should be a collection of distinct systems that a user queried explicitely to get data (Pull). Or whether these systems periodically updated a central data store with their data, which a user could then query.

The benefits of Pull is that there is less infrastructure. Each system lives in isolation, and can be queried by the end-user. This has huge advantages in simplicity, as we don't need to collect and store the log data, and instead realy on just-in-time parsing of the log files.

The disadvantage of this is that searching becomes harder, also parsing data between different systems becomes slightly more difficult (although not too bad since it will have a common REST api).  Scaling could become an issue, as the end user will have to navigate between all N systems to get logs for all N systems.

The benefits of Push is that searching becomes trivial, as all the data is collected in a single place. It becomes easier to act on the common log data. Scaling is easier, as a new system just needs a push daemon to then join the rest of the systems. Searching across multiple systems is easier, and way less computationally expensive.

A disadvantage of Push is added complexity, along with more points of failure. If the message queue or datastore go down then the system will not work.


I have decided to implement a Push style system with the folowing design.

## Design

Each machine will have a push daemon that monitors the log files and periodically sends messages to the nosql datastore. To simplify things, this daemon will be called Henrik, as it is primarily responsible for passing data to other systems.

There will be a REST api service for retrieving the data that was passed to it by Henrik. This service will be called Daniel, and will be responsible for "shooting" the data to the end user.



## REST API

The REST api is described below:
  /hosts/  Lists all hosts
  /hosts/<host>/ Lists all files for a given host
  /hosts/<host>/files/ Lists all log file names for a given host
  /hosts/<host>/logs Lists all logs for a given host

Where /hosts/<hosts>/logs takes the following query parameters
?filter=<filter> for filtering the log line
?count=<count> to restrict the number of responses
?file=<file> to restrict the responses to a given log file


example requests and responses:
```
GET http://127.0.0.1:3032/hosts/
{
    "data": [
        {
            "host": "andynewman",
            "url": "http://127.0.0.1:3032/hosts/andynewman/"
        },
        {
            "host": "othersystem",
            "url": "http://127.0.0.1:3032/hosts/othersystem/"
        }
    ]
}
```

```
GET http://127.0.0.1:3032/hosts/andynewman/
{
    "data": [
        {
            "filename": "fsck_apfs_error.log",
            "host": "andynewman",
            "url": "http://127.0.0.1:3032/hosts/andynewman/logs?file=fsck_apfs_error.log"
        },
        {
            "filename": "syslog",
            "host": "andynewman",
            "url": "http://127.0.0.1:3032/hosts/andynewman/logs?file=syslog"
        },
        {
            "filename": "other_log",
            "host": "andynewman",
            "url": "http://127.0.0.1:3032/hosts/andynewman/logs?file=other_log"
        }
    ]
}
```

```
GET http://127.0.0.1:3032/hosts/andynewman/logs
{
  "data": [
        {
            "filename": "fsck_apfs_error.log",
            "last_modified": "1639596366.62149810791015625",
            "logline": "fsck_apfs completed at Tue Dec 14 07:59:50 2021",
            "host": "andynewman"
        },
        {
        "filename": "syslog",
        "last_modified": "1639508052.0629189014434814453125",
        "logline": "Line one",
        "host": "andynewman"
    }
]
}
```

```
http://127.0.0.1:3032/hosts/andynewman/logs?file=syslog&filter=three&count=2
{
    "data": [
        {
            "filename": "other_log",
            "last_modified": "1639525487.50638103485107421875",
            "logline": "three log lines",
            "host": "andynewman"
        },
        {
            "filename": "syslog",
            "last_modified": "1639508052.062982082366943359375",
            "logline": "line three",
            "host": "andynewman"
        }
    ]
}
```


## Bugs and Caveats
There is a bug that exists when initializing the system for the first time. The producer daemon scans all open files, and uploads them to the nosql datastore. Unfortunately, the daemon has no idea when this log data was added to the log files, so they are all uploaded with relative timestamps (earlier in the logfile is uploaded with an earlier timestamp).  one way to work around this is to scan each line, and see if there is a Date/Time format as part of that log line.

For subsequent log lines, they will have a timestamp that is within 30s of the time the line was added to the log file.

There could be an issue with processing too many log entities on a given host, if the amount of processing time exceeds 30s, then logs could show up out of order (this is a very unlikely edge case)



# Tests
There are unit tests for both of these components, but ideally, there would be system/integration tests to ensure a proper flow from start to finish, but I was unable to complete that in time.

# Running

On each  host, start up Daniel's app.py (using python3 after installing the requirements.txt with pip3).

On the REST api side, start up Henrik's app.py the same way.

It will need to connect to a dynamodb Table (one can be created with the create_table.py script). To do so, it will be necessary to set your AWS credentials (either by ENV vars, or an .aws config file)


# Authentication
Requests to the REST api need to be authenticated with a pre-determined bearer token.
ideally, this would be retrieved from an IDP system, or a better login/authentication system would be in place (no time right now to implement that)

The bearer token is the following:
'bearer SECRETCODE'
