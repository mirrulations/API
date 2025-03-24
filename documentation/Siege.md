# Siege Installation and Usage Guide

Siege is a powerful HTTP load testing and benchmarking tool that can be used to test the performance of your web applications. This guide provides instructions on how to install Siege and explains the various command line options for running tests.

## Installing Siege

### On MacOS

To install Siege

```
 brew install siege  
```

```
siege [options] URL
```
### Common Parameters
-c: Sets the number of concurrent users. For example, -c 30 simulates 30 users hitting the server at the same time.

-t: Specifies the test duration. For example, -t 1M runs the test for 1 minute. The time can be specified in seconds (S), minutes (M), or hours (H).

-b: Runs the test in benchmark mode, where Siege sends requests as quickly as possible without waiting.

-r: Specifies the number of repetitions. Each simulated user will hit the server this many times.

### Example command 
siege -c 25 -t 1M http://127.0.0.1:3000/dummy


### Understanding Outputs 

- Transactions: Total number of server hits.

- Availability: Percentage of successfully handled requests.
Elapsed time: Total duration of the test.

- Data transferred: Total data amount transferred during the test.
Response time: Average time taken to handle a request.

- Transaction rate: Average number of transactions per second.
Throughput: Average number of bytes transferred per second.

- Concurrency: Average number of concurrent connections, closely related to the number of users.

- Successful transactions: Number of requests that were successfully served.

- Failed transactions: Number of requests that failed (useful for identifying errors under load).

- Longest transaction: Duration of the longest transaction.

- Shortest transaction: Duration of the shortest transaction.
