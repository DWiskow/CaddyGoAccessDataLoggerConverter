# CaddyGoAccessDataLoggerConverter
Caddy/GoAccess data logger &amp; converter (translates Caddy web server JSON logs to a format that GoAccess can ingest)

Caddy is a 

[GoAccess](https://goaccess.io/) is a tool for convenient and quick analysis of access logs, it shares a philosophy (if not its development language) with Caddy in that it is self-contained and stand-alone with no dependencies (and can even generate self-contained access log file reporting in a single HTML file, that can then be auto-deployed on your web sit.

Currently, it is difficult to obtain the full benefit from goaccess with Caddy log files as there is not a log file format shared by both Caddy and goaccess that passes the full set of Caddy log file data that goaccess can use (rather than the somewhat limited common format).
