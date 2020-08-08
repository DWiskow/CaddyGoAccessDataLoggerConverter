# CaddyGoAccessDataLoggerConverter
#### Caddy/GoAccess data logger &amp; converter that translates Caddy web server JSON logs into a format that GoAccess can ingest and exploit in either batch or real-time.

[Caddy](https://caddyserver.com) is a powerful, extensible platform to serve your sites, services, and apps, written in Go. Although most people use it as a web server or proxy. It provides a really simple, performant and flexible platform to host secure static web sites and web applications. 

[GoAccess](https://goaccess.io/) is a tool for convenient and quick analysis of access logs, it shares a philosophy (if not its development language) with Caddy in that it is self-contained and stand-alone with no dependencies (and can even generate self-contained access log file reporting in a single HTML file, that can then be auto-deployed on your web site).

It is currently difficult to obtain the full benefit from GoAccess with Caddy log files as the log files output by Caddy are not in a format that can be easily ingested by GoAccess (Note: common log formats are supported by both tools, but that significantly limits the data that can be shared).

#### caddyLog.py
caddyLog.py solves this problem by providing a tool to convert Caddy JSON logs into a format that GoAccess can understand, and maxmises the data that is shared with GOACCESS in order to optimise the analysis.

caddyLog.py can use the log file(s) written by Caddy as its input in either batch or live mode. In live mode, it can monitor a 'live' Caddy log file for events being appended to it in pseudo real-time and reflect those changes immediately in a converted format log file for processing by GoAccess.

caddyLog.py can alternatively instantiate a TCP/IP network socket server, configured to receive Caddy log data in real-time, and stream Caddy log data to a GoAccess format log file as events happen. This enables the 'live' monitoring capabilities of GoAccess to function seamlessly with Caddy in real-time.

## Usage

Copy the caddyLog.py file to your computer and make it executable (chmode +x caddyLog.py). You can then run caddyLog .py as shown in the examples detailed below.

```
./caddyLog.py -n localhost:55555 -g access.goaccess.log -j access.json

                 set up a TCP/IP network socket server on IP address localhost:55555
                 and output any log data streamed to it by Caddy over the network to
                 a file named "access.goaccess.log" (containing Caddy log data converted
                 into a format compatible with goAccess - https://goaccess.io/) AND ALSO
                 to an output file named "access.json" (containing the complete Caddy log
                 data in JSON format)
                
                 optionally select only the -g [--outputGoAccessFilename] OR the -j
                 [--outputJSONfilename] to output a single file of the required
                 format
```


```
./caddyLog.py -i access.log -g access.goaccess.log

                 read in the data from the file "access.log" (in JSON format) and write
                 out a file named "access.goaccess.log" (containing the Caddy log data
                 converted into a format compatible with goAccess).
```

```
./caddyLog.py -i access.log -i 600 -g access.goaccess.log

                 read in the data from the file "access.log" (in JSON format) and write
                 out a file named "access.goaccess.log" (containing the Caddy log data
                 converted into a format compatible with goAccess), then repeatedly
                 sleep for 10 minutes (600 seconds) before checking to see if any
                 additional Caddy log data has been written to "access.log". If
                 additional data has been added to "access.log", then convert it and
                 append it to "access.goaccess.log" before again sleeping.

```

Executing caddyLog.py with the argument -h or --help will provide more instructions and detail on how to use caddyLog.py
