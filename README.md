# CaddyGoAccessDataLoggerConverter
Caddy/GoAccess data logger &amp; converter (translates Caddy web server JSON logs to a format that GoAccess can ingest)

[Caddy](https://caddyserver.com] is a powerful, extensible platform to serve your sites, services, and apps, written in Go. Although most people use it as a web server or proxy. It provides a really simple, performant and flexible platform to host secure static web sites and web applications. 

[GoAccess](https://goaccess.io/) is a tool for convenient and quick analysis of access logs, it shares a philosophy (if not its development language) with Caddy in that it is self-contained and stand-alone with no dependencies (and can even generate self-contained access log file reporting in a single HTML file, that can then be auto-deployed on your web sit.

It is currently difficult to obtain the full benefit from GoAccess with Caddy log files the log files output by Caddy are not in a format that can be easily ingested by GoAccess (Note: common log formats are supported by both tools, but that limits the data that can be shared).
