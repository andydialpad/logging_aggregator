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

Each machine will have a push daemon that monitors the log files and periodically sends messages to the activeMQ message queue. For simplicity sake, this daemon will be called Henrick, as it is primarily responsible for passing data to other systems.

There will be a message queue, as mentioned above, it should guantee log message delivery to the consumer service.

There will be a message consumer service who's purpose is to take the messages off the queue, and insert them into a datastore. Since this system is only required to collect messages passed to it from Henrick, and shoot them into the datastore, we will call this service Daniel.


In order to expose this data to the end user and various other integrations, we will need to pull the data from the datastore. This will be exposed via a REST api, which checks authorization of incoming requests before allowing access.  Because this service basically determines who can look at the data in the datastore, and serves up the data, we will call this service Roberto


