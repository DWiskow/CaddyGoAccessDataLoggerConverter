FROM python:3-alpine


WORKDIR /logconverter
RUN mkdir -pv /logconverter/input-logs &&\ 
    mkdir -pv /logconverter/output-logs &&\ 
    chmod -R 777 /logconverter/output-logs  &&\
    apk add goaccess && \
    wget https://github.com/UbuntuEvangelist/GeoLiteCity.dat.gz/raw/master/GeoLiteCity.dat.gz &&\
    gunzip GeoLiteCity.dat.gz

COPY ["caddyLog.py", "entrypoint.sh", "LICENSE", "goaccess.conf", "./"]

VOLUME [ "/logconverter/input-logs", "/logconverter/output-logs" ]

ENTRYPOINT ./entrypoint.sh
