# CaddyGoAccessDataLoggerConverter
#### Caddy/GoAccess data logger &amp; converter that translates Caddy web server JSON logs into a format that GoAccess can ingest and exploit in either batch or real-time modes.

[Caddy](https://caddyserver.com) is a powerful, extensible platform to serve your sites, services, and apps, written in Go. Although most people use it as a web server or proxy. It provides a really simple, performant and flexible platform to host secure static web sites and/or web applications. 

[GoAccess](https://goaccess.io/) is a tool for convenient and quick analysis of access logs, it shares a philosophy (if not its development language) with Caddy in that it is self-contained and stand-alone with no dependencies (and can even generate self-contained access log file reporting in a single HTML file, that can then be auto-deployed on your web site).

It is currently difficult to obtain the full benefit from GoAccess with Caddy log files as the log files output by Caddy are not in a format that can be easily ingested by GoAccess (Note: common log formats are supported by both tools, but that significantly limits the analysis and reporting).

#### caddyLog.py
caddyLog.py solves this problem by providing a tool to convert Caddy JSON logs into a format that GoAccess can understand, and maxmises the data that is shared with GOACCESS in order to optimise the analysis.

caddyLog.py can use the log file(s) written by Caddy as its input in either batch or live mode. In live mode, it can monitor a 'live' Caddy log file for events being appended to it in pseudo real-time and reflect those changes immediately in a converted format log file that is streamed to GoAccess for processing.

caddyLog.py can alternatively instantiate its own TCP/IP network socket server, configured to receive Caddy log data in real-time, and stream Caddy log data to a GoAccess format log file as events happen. This enables the 'live' monitoring capabilities of GoAccess to function seamlessly with Caddy in real-time.

## Usage

Copy the caddyLog.py file to your computer and make it executable (**chmod +x caddyLog.py**). You can then run caddyLog .py as shown in one of the examples detailed below.

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
./caddyLog.py -i access.log -t 600 -g access.goaccess.log

                 read in the data from the file "access.log" (in JSON format) and write
                 out a file named "access.goaccess.log" (containing the Caddy log data
                 converted into a format compatible with goAccess), then repeatedly
                 sleep for 10 minutes (600 seconds) before checking to see if any
                 additional Caddy log data has been written to "access.log". If
                 additional data has been added to "access.log", then convert it and
                 append it to "access.goaccess.log" before again sleeping.

```

Executing caddyLog.py with the argument -h or --help will provide more instructions and detail on how to use caddyLog.py

Example output format

```
2020-08-03 19:17:37 example.com 192.168.1.1 GET / HTTP/1.1 200 458 0.005674565 unkown "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
2020-08-03 18:35:53 example.com 192.168.100.3 GET /wp-login.php HTTP/1.1 404 0 0.000298749 http://example.com/wp-login.php "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/62.0"
2020-08-03 19:04:35 example.com 192.168.200.56 GET /admin/ HTTP/1.1 404 0 0.000482654 http://example.com/admin/ "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/62.0"
```

