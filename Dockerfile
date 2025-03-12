FROM nginx:alpine

RUN rm -rf /usr/share/nginx/html/*

COPY combined.m3u /usr/share/nginx/html/iptv.m3u

COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 33333
