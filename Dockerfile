FROM nginx:alpine

RUN rm -rf /usr/share/nginx/html/*

COPY combined.m3u /usr/share/nginx/html/iptv.m3u

EXPOSE 33333
