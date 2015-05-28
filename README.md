# PingPongPy
Simple TCP network latency test tool.

First start a server on one host, then start a client on another host which will measure the latency.  A ping packet is sent to the server and the server will respond with a pong packet. The next ping packet is sent only after the full pong packet is received. The roundtrip time is measured for each combination of ping request and pong response. Statistics (average, min, max, std.dev.) are printed for the roundtrip times when ready.


## Usage

### Server
Start a server:
```
# ./pingpong.py pong ALL 1234
```
This will bind the socket to all addresses and start listening on port 1234.

The server will serve one client at a time, while letting the others wait.


### Client
Start a client:
```
# ./pingpong.py ping server_hostname.example.com 1234 --ping-size 50000 --pong-size 1000 --seconds 10
```
This will start a client that connects to the specified server and port. The size of the ping payload is 50000 bytes and the size of the pong payload is 1000 bytes. It will stop sending ping requests after 10 seconds and will terminate after the pong response to the final ping request is fully received.


## Example output
```
# ./pingpong.py ping localhost 1234 --seconds 5 --ping-size 500000 --pong-size 100000
seq     roundtrip-time  elapsed-time
1       0.455527067184  0.45556306839
2       0.391165018082  0.846796035767
3       0.408379793167  1.25522899628
4       0.473116159439  1.7283911705
5       0.481930971146  2.21041607857
6       0.517910003662  2.72848510742
7       0.449773788452  3.17840099335
8       0.513982772827  3.69247198105
9       0.458905220032  4.1514852047
10      0.448948860168  4.60057902336
11      0.494635105133  5.09529209137
Connection closed.
Roundtrips: 11
Average: 0.463115887208
Min: 0.391165018082
Max: 0.517910003662
Stddev: 0.0377363014256
```
